
# Полезные материалы
# https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/
# https://api.python.langchain.com/en/v0.0.339/schema/langchain.schema.document.Document.html
# https://python.langchain.com/v0.2/docs/how_to/semantic-chunker/

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from tqdm import tqdm
import re
import os
import json
from dataclasses import asdict
import pandas as pd

from src.DocumentsParser.Splitter.utils import SplitterConfig
from src.DocumentsParser.utils import TABLE_DIR_INFO_FILE, MDS_DIR_INFO_FILE, DOCS_DIR_INFO_FILE
from src.logger import Logger

class BaselineSplitter:
    def __init__(self, config: SplitterConfig, log) -> None:
        self.log = log
        self.log.info("Initiating BaselineSplitter-class")
        self.config = config 
        self.filename_regex = re.compile(config.filename_regex)

        self.splitters = []
        for i, splitter_name in enumerate(self.config.modification.sequence):
            params = self.config.modification.params[i]
            if splitter_name == 'markdown':
                self.splitters.append(MarkdownHeaderTextSplitter(**params))
            elif splitter_name == 'recursive':
                self.splitters.append(RecursiveCharacterTextSplitter(**params))
            elif splitter_name == 'semantic':
                self.embeddings == HuggingFaceEmbeddings(**params)
                self.splitters.append(SemanticChunker(self.embeddings))
            else:
                raise KeyError

    @Logger.cls_se_log('''Сохранение конфигурации гиперпараметров,
                       используемой для разбиения документов на чанки''')
    def save_operation_log(self):
        log_data = {
            'splitter': self.__class__.__dict__['__module__'],
            'config': asdict(self.config)}
        with open(f"{self.config.save_dir}/{TABLE_DIR_INFO_FILE}", 'w', encoding='utf-8') as fd:
            fd.write(json.dumps(log_data, indent=1))

    @Logger.cls_se_log('''Создание директории для сохранения 
                       разбитых на чанки документов''')
    def create_save_dir(self):
        if not os.path.exists(self.config.save_dir):
            os.mkdir(self.config.save_dir)
            return True
        else:
            self.log.warning(f"Директория '{self.config.save_dir}' уже существует")
            return False

    @Logger.cls_se_log('''Получение идентификаторов документов''')
    def get_docs_id(self, mds_filenames):
        return [md.replace('.md', '.pdf') for md in mds_filenames]
        

    @Logger.cls_se_log('''Выполнение разбиения набора документов на чанки''')
    def split(self):
        if not self.create_save_dir():
            return

        files = sorted(os.listdir(self.config.load_dir))
        
        mds = list(filter(lambda file: self.filename_regex.search(file) is not None, files))
        docs_ids = self.get_docs_id(mds)

        chunked_mds = []
        for doc_id, md_name in tqdm(zip(docs_ids, mds)):
            with open(f"{self.config.load_dir}/{md_name}") as fd:
                md_text = fd.read()

            splits = self.splitters[0].split_text(md_text)
            if len(self.splitters) > 1:
                splits = self.splitters[1].split_documents(splits)

            for chunk in splits:
                chunk.metadata['doc_id'] = doc_id

            chunked_mds += splits

        df = pd.DataFrame(chunked_mds)
        df.to_csv(f"{self.config.save_dir}/{self.config.table_name}", index=False, sep=';')
        self.save_operation_log()