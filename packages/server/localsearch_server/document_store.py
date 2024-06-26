from abc import ABC, abstractmethod
import os

class DocumentStore(ABC):
    """
    DocumentStore is an interface for saving raw document contents in persistant storage.

    Could be implemented with a filesystem, a database, a cloud object storage provider.
    """
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def insert_document(self, document_id, contents):
        pass

    @abstractmethod
    def get_document(self, document_id):
        pass

    @abstractmethod
    def list_documents(self):
        pass

class InMemoryDocumentStore(DocumentStore):
    """
    Implementation of DocumentStore using a simple in-memory dict
    """
    def __init__(self):
        self.documents = {}

    def init(self):
        pass

    def insert_document(self, document_id, contents):
        self.documents[document_id] = contents

    def get_document(self, document_id):
        if document_id not in self.documents:
            return None
        return self.documents[document_id]

    def list_documents(self):
        return list(self.documents.keys())

# class FileDocumentStore(DocumentStore):
#     """
#     Implementation of DocumentStore using a folder in the local filesystem.
    
#     Each document is saved in a file, using the filename {document_id}.txt. 
#     """
#     def __init__(self, base_dir):
#         self.base_dir = base_dir

#     def init(self):
#         if not os.path.exists(self.base_dir):
#             os.makedirs(self.base_dir)

#     def insert_document(self, document_id, contents):
#         with open(f'{self.base_dir}/{document_id}.txt', 'w') as file:
#             file.write(contents)

#     def get_document(self, document_id):
#         with open(f'{self.base_dir}/{document_id}.txt', 'r') as file:
#             contents = file.read()

#         return contents

#     def list_documents(self):
#         filenames = os.listdir(self.base_dir)
#         return [f.replace('.txt', '') for f in filenames if f.endswith('.txt')]

