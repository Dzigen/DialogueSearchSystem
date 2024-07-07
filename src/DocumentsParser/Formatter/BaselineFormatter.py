import pymupdf4llm
from tqdm import tqdm
import os
import re
from dataclasses import asdict
import json

from src.DocumentsParser.Formatter.utils import FormatterConfig
from src.DocumentsParser.utils import INFO_FILE
from src.logger import Logger

class BaselineFormatter:
    def __init__(self, config: FormatterConfig, log) -> None:
        self.log = log
        self.log.info("Initiating BaselineFormatter-class")
        self.config = config
        self.filename_regex = re.compile(self.config.filename_regex)

    @Logger.cls_se_log('''Сохранение конфигурации гиперпараметров,
                       используемой для форматирования документов''')
    def save_operation_log(self):
        log_data = {
            'formatter': self.__class__.__dict__['__module__'],
            'config': asdict(self.config)}
        with open(f"{self.config.save_dir}/{INFO_FILE}", 'w', encoding='utf-8') as fd:
            fd.write(json.dumps(log_data, indent=1))

    @Logger.cls_se_log('''Создание директории для сохранения 
                       отформатированных документов''')
    def create_save_dir(self):
        if not os.path.exists(self.config.save_dir):
            os.mkdir(self.config.save_dir)
            return True
        else:
            self.log.warning(f"Директория '{self.config.save_dir}' уже существует")
            return False

    @Logger.cls_se_log('''Выполнение форматирования набора документов''')
    def formate(self):  
        if not self.create_save_dir():
            return 

        files = sorted(os.listdir(self.config.load_dir))
        docs = list(filter(lambda file: self.filename_regex.search(file) is not None, files))

        for doc_name in tqdm(docs):
            md_name = doc_name.rsplit('.', maxsplit=1)[0] + '.md'
            md_text = pymupdf4llm.to_markdown(f"{self.config.load_dir}/{doc_name}")
            with open(f"{self.config.save_dir}/{md_name}", "w") as fd:
                fd.write(md_text)

        self.save_operation_log()
