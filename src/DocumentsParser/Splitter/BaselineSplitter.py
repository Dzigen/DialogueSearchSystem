
# Полезные материалы
# https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/
# https://api.python.langchain.com/en/v0.0.339/schema/langchain.schema.document.Document.html
# https://python.langchain.com/v0.2/docs/how_to/semantic-chunker/

from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm
import re
import os
import pandas as pd

# TODO
class BaselineSplitter:
    def __init__(self, load_dir: str, save_dir: str, filename_regex: str = ".md$",
                 chunk_size: int = 250, chunk_overlap: int = 30) -> None:
        self.load_dir = load_dir
        self.save_dir = save_dir
        self.filename_regex = re.compile(filename_regex)
        self.chunk_overlap = chunk_overlap
        self.chunk_size = chunk_size
        self.table_name = 'chunked_docs.csv'

    def split(self):
        files = sorted(os.listdir(self.load_dir))
        mds = list(filter(lambda file: re.search(file, self.filename_regex) is not None, files))

        # MD splits
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=HEADERS_TO_SPLIT_ON, strip_headers=False
        )

        # Char-level splits
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        chunked_mds = []
        for md_name in tqdm(mds):
            with open(f"{self.load_dir}/{md_name}") as fd:
                md_text = fd.read()

            md_header_splits = markdown_splitter.split_text(md_text)
            splits = text_splitter.split_documents(md_header_splits)
            chunked_mds += splits

        df = pd.DataFrame(chunked_mds)
        df.to_csv(f"{self.save_dir}/{self.table_name}", index=False, sep=';')