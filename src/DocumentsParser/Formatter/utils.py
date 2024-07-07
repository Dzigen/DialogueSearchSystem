from dataclasses import dataclass


@dataclass
class FormatterConfig:
    load_dir: str
    save_dir: str
    filename_regex: str = '.pdf$'
