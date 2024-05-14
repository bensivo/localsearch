package main

import (
	"context"
	"encoding/base64"
	"fmt"
	"html/template"
	pb "localsearch-grpc/pkg/grpc"
	"log"
	"net/http"

	"github.com/google/uuid"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type Document struct {
	Title   string
	Content string
}

func main() {
	documents := []Document{}

	conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	client := pb.NewLocalsearchClient(conn)

	mux := http.NewServeMux()

	mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		http.Redirect(w, r, "/documents", http.StatusSeeOther)
	})

	mux.HandleFunc("GET /documents", func(w http.ResponseWriter, r *http.Request) {
		template, err := template.ParseFiles("./public/documents.html")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		// TODO: Fetch documents from GRPC service

		template.Execute(w, struct {
			Documents []Document
		}{
			Documents: documents,
		})
	})

	mux.HandleFunc("GET /documents/insert", func(w http.ResponseWriter, r *http.Request) {
		template, err := template.ParseFiles("./public/documents-insert.html")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		template.Execute(w, nil)
	})

	mux.HandleFunc("POST /documents/insert/submit", func(w http.ResponseWriter, r *http.Request) {
		err := r.ParseForm()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		document := Document{
			Title:   r.Form.Get("title"),
			Content: r.Form.Get("content"),
		}
		documents = append(documents, document)

		id, err := uuid.NewRandom()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		res, err := client.InsertDocument(context.Background(), &pb.InsertDocumentRequest{
			RequestId:      id.String(),
			DocumentId:     document.Title,
			ContentsBase64: base64.StdEncoding.EncodeToString([]byte(document.Content)),
		})

		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		if res.ResponseCode != 0 {
			http.Error(w, "Failed to insert document", http.StatusInternalServerError)
			return
		}

		template, err := template.ParseFiles("./public/documents-insert-submit.html")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		result := struct {
			Result string
		}{
			Result: "success",
		}
		template.Execute(w, result)
	})

	fmt.Println("Listening on http://localhost:8080")
	err = http.ListenAndServe("localhost:8080", mux)
	if err != nil {
		log.Fatal(err)
	}
}
