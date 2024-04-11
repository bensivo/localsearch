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
    def save(self, document_id, contents):
        pass

    @abstractmethod
    def get(self, document_id, contents):
        pass

class FileDocumentStore(DocumentStore):
    """
    Implementation of DocumentStore using a folder in the local filesystem.
    
    Each document is saved in a file, using the filename {document_id}.txt. 
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def init(self):
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def save(self, document_id, contents):
        with open(f'{self.base_dir}/{document_id}.txt', 'w') as file:
            file.write(contents)

    def get(self, document_id):
        with open(f'{self.base_dir}/{document_id}.txt', 'r') as file:
            contents = file.read()

        return contents
