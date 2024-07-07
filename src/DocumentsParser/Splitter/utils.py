
from dataclasses import dataclass
from typing import List

HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
]

@dataclass
class SplitterConfig:
    load_dir: str
    save_dir: str
    modification: dict
    table_name: str = 'chunked_docs.csv'
    filename_regex: str = '.md$'
    logfile_name: str = 'operation_info.json'

# Есть 4 возможные конфигурации разбиения текста на чанки:
# 1. markdown + recursive
# 2. markdown + semantic
# 3. recursive
# 4. semantic

@dataclass
class BaselineConfig:
    sequence: List[str] # markdown , recursive , semantic
    params: List[dict] # markdown : [headers_to_split_on, strip_headers], recursive : [chunk_size, chunk_overlap], semantic : [model_name, encode_kwargs, model_kwargs]