from dataclasses import dataclass


@dataclass
class LLM_Hardw_Conf:

    model_path:str = '/home/aisummer/ssemenov_workspace/nlp-service/model_llm/blobs/sha256-6a0746a1ec1aef3e7ec53868f220ff6e389f6f8ef87a01d77c96807de94ca2aa'                      # Путь до модели
    n_gpu_layers:int = -1               # Количество слоев, которые нужно выгрузить в графический процессор (-ngl). Если -1, все слои будут выгружены.
    seed:int = 42                       # 
    n_ctx:int = 512                     # Токены отведённые на контекст
    n_batch:int = 512                   # Максимальный размер пакета для обработки промпта
    n_threads:int = None                # Количество потоков, используемых для генерации
    use_mmap: bool = True               # Использовать mmap при возможности.
    use_mlock: bool = True              # Cохранить модель в оперативной памяти


@dataclass
class LLM_Hyper_Conf:
    
    temperature: float = 0.8,           # Параметр, управляющий разнообразием генерируемого текста. Более высокая температура приводит к более случайному выбору токенов.
    top_k: int = 40                     # Параметр, используемый для ограничения выбора токенов только на основе топ-K наиболее вероятных токенов.
    top_p: float = 0.95                 # Параметр, используемый для ограничения выбора токенов только на основе токенов с накопленной вероятностью до достижения заданного порога.
    min_p: float = 0.05,                # определяет минимальную вероятность для выбора следующего слова в генерации текста. Чем выше значение, тем более вероятные слова будут выбираться моделью
    typical_p: float = 1,               # Указывает типичную вероятность для выбора следующего слова. Значение 1 означает, что модель будет выбирать слова на основе вероятностей, предсказанных ей
    stream: bool = False,                # Модель будет генерировать текст постепенно, в реальном времени (МОДЕЛЬ БУДЕТ ВОЗВРАЩАТЬ ГЕНЕРАТОР)
    max_tokens=100,                      # Максимальное количество токенов (слов или символов), которые модель может сгенерировать за один вызов.  
    
