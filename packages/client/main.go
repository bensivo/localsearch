package main

import (
	"html/template"
	"log"
	"net/http"
)

type Document struct {
	Title   string
	Content string
}

func main() {
	documents := []Document{}

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

		// TODO: Submit document using GRPC service

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

	err := http.ListenAndServe("localhost:8080", mux)
	if err != nil {
		log.Fatal(err)
	}
}
