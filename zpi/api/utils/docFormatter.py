from docx import Document
import os


class DocFormatter:
    def __init__(self, file_path):
        print(self.file_path)
        self.file = Document(file_path)
        print(self.file)
