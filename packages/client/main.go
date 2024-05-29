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
    DocumentId      string
    DocumentContent string
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

    mux.HandleFunc("GET /documents/query", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("GET /documents/query")
        template, err := template.ParseFiles("./public/query.html")
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        template.Execute(w, struct {}{})
    })

    mux.HandleFunc("POST /documents/query/submit", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("POST /documents/query/submit")

        err := r.ParseForm()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
        queryStr := r.Form.Get("query")

        id, err := uuid.NewRandom()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        fmt.Printf("REQ-> Query:%s %s\n", id, queryStr)
        res, err := client.Query(context.Background(), &pb.QueryRequest{
            RequestId:      id.String(),
            Query:         queryStr,
        })
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        fmt.Printf("RES<- Query:%s %d\n", id, res.ResponseCode)
        if res.ResponseCode != 0 {
            http.Error(w, "Failed to insert document", http.StatusInternalServerError)
            return
        }

        template, err := template.ParseFiles("./public/query-submit.html")
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        for _, documentScore := range res.DocumentScores {
            fmt.Printf("DocumentId: %s, Score: %f\n", documentScore.DocumentId, documentScore.Score)
        }

        result := struct {
            DocumentScores []*pb.DocumentScore
        }{
            DocumentScores: res.DocumentScores,
        }
        template.Execute(w, result)
    })


    mux.HandleFunc("GET /documents/{id}", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("GET /documents/{id}")
        template, err := template.ParseFiles("./public/document.html")
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        documentId := r.PathValue("id")
        if documentId == "" {
            http.Error(w, "Document ID is required", http.StatusBadRequest)
            return
        }

        requestId, err := uuid.NewRandom()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        fmt.Printf("REQ-> GetDocument:%s %s\n", requestId, documentId)
        res, err := client.GetDocument(context.Background(), &pb.GetDocumentRequest{
            RequestId:  requestId.String(),
            DocumentId: documentId,
        })

        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        fmt.Printf("RES<- GetDocument:%s %s\n", requestId, res.ResponseCode)
        content, err := base64.StdEncoding.DecodeString(res.ContentsBase64)
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        template.Execute(w, struct {
            Document Document
        }{
            Document: Document{
                DocumentId:      documentId,
                DocumentContent: string(content),
            },
        })
    })

    mux.HandleFunc("GET /documents", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("GET /documents")
        template, err := template.ParseFiles("./public/documents.html")
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        id, err := uuid.NewRandom()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        // TODO: Fetch documents from GRPC service
        res, err := client.ListDocuments(context.Background(), &pb.ListDocumentsRequest{
            RequestId: id.String(),
            Limit:     20,
            Offset:    0,
        })

        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        template.Execute(w, struct {
            Documents []*pb.DocumentMetadata
        }{
            Documents: res.Documents,
        })
    })

    mux.HandleFunc("GET /documents/insert", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("GET /documents/insert")
        template, err := template.ParseFiles("./public/documents-insert.html")
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        template.Execute(w, nil)
    })

    mux.HandleFunc("POST /documents/insert/submit", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("POST /documents/insert/submit")
        err := r.ParseForm()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        document := Document{
            DocumentId:      r.Form.Get("title"),
            DocumentContent: r.Form.Get("content"),
        }
        documents = append(documents, document)

        id, err := uuid.NewRandom()
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        res, err := client.InsertDocument(context.Background(), &pb.InsertDocumentRequest{
            RequestId:      id.String(),
            DocumentId:     document.DocumentId,
            ContentsBase64: base64.StdEncoding.EncodeToString([]byte(document.DocumentContent)),
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

    mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
        fmt.Println("GET /")
        http.Redirect(w, r, "/documents", http.StatusSeeOther)
    })

    fmt.Println("Listening on http://localhost:8080")
    err = http.ListenAndServe("localhost:8080", mux)
    if err != nil {
        log.Fatal(err)
    }
}
