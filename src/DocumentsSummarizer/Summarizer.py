from src.DocumentsSummarizer.utils import SummarizerConfig
from src.utils import DialogueState
from src.logger import Logger
import requests
import json


class SummarizerModule:
    '''
    sytem_prompt = Ты вопросно-ответная система. Все ответы генерируешь на русском языке. Отвечай коротко по вопросам.
    user_prompt = Ты вопросно-ответная система. Все ответы генерируешь на русском языке. Отвечай коротко по вопросам.
    assistant_prompt = Твоя база знаний, все ответы генерируются на основе текста ниже: \
                4.1.2 Вагон должен соответствовать климатическому исполнению УХЛ1 по ГОСТ 15150 с  \
                обеспе-чением работоспособного состояния в диапазоне рабочих температур от минус 60 °С до плюс 50 °С. 4.1.3 \
                Габарит вагона должен соответствовать требованиям ГОСТ 9238. 4.1.4 Вагон должен иметь кузов, включающий в себя \
                раму с установленными на ней отдельными емкостями (бункерами) для размещения грузов, а также иные устройства, \
                предусмотренные конструк-торской документацией, и должен быть оборудован: а) тележками по ГОСТ 9246 или иному стандарту, \
                    распространяющемуся на тележки грузовых вагонов железных дорог; 6) автосцепными устройствами по ГОСТ 33434 или иному стандарту, \
                распространяющемуся на автосцепные устройства грузовых вагонов, с контуром зацепления автосцепки по ГОСТ 21447, \
                с обо-рудованием автосцепок нижним ограничителем вертикальных перемещений и расцепным приводом с \
                блокировочной цепью и поглощающими аппаратами по ГОСТ 32913; в) автоматическим пневматическим тормозом по ГОСТ 34434; \
                г) стояночным тормозом по ГОСТ 32880. 
    '''


    def __init__(self, config: SummarizerConfig, log) -> None:
        self.log = log
        self.log.info("Initiating Summarizer-class")
        self.config = config
        
    def prepare_assistant_content(self, state):
        text_chunks = [doc.page_content for doc in state.base_relevant_docs]
        assist_content = '\n\n'.join([self.config.assist_prompt] + text_chunks)
        return assist_content

    #@Logger.cls_se_log('''Генерация ответа на основании концентрированного набора релевантных документов''')
    def create_answer(self, state: DialogueState) -> None:

        assist_content = self.prepare_assistant_content(state)

        url = 'http://llama_host:11434/api/chat'
        data = {
            "model": "llama3",
            "messages": [
                {
                    "role": "system",
                    "content": self.config.system_prompt
                    "content": "Ты вопросно-ответная система. Все ответы генерируй на том языке на котором задан вопрос. Отвечай коротко по вопросам."
                },
                {
                    "role": "assistant",
                    "content": assist_content
                },
                {
                    "role": "user",
                    "content": state.query
                }
            ],
            "stream": self.config.stream,
            "options": {
                "num_keep": self.config.num_keep,
                "seed": self.config.seed,
                "num_predict": self.config.num_predict,
                "top_k": self.config.top_k,
                "top_p": self.config.top_p,
                "tfs_z": self.config.tfs_z,
                "typical_p": self.config.typical_p,
                "repeat_last_n": self.config.repeat_last_n,
                "temperature": self.config.temperature,
                "repeat_penalty": self.config.repeat_penalty,
                "presence_penalty": self.config.presence_penalty,
                "frequency_penalty": self.config.frequency_penalty,
                "mirostat": self.config.mirostat,
                "mirostat_tau": self.config.mirostat_tau,
                "mirostat_eta": self.config.mirostat_eta,
                "penalize_newline": self.config.penalize_newline,
                #"stop": self.config.stop,
                "numa": self.config.numa,
                "num_ctx": self.config.num_ctx,
                "num_batch": self.config.num_batch,
                "num_gpu": self.config.num_gpu,
                "main_gpu": self.config.main_gpu,
                "low_vram": self.config.low_vram,
                "f16_kv": self.config.f16_kv,
                "vocab_only": self.config.vocab_only,
                "use_mmap": self.config.use_mmap,
                "use_mlock": self.config.use_mlock,
                "num_thread": self.config.num_thread
            }
        }

        response = requests.post(url, json=data, stream=True)
        result = ''
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    string_response = chunk.decode('utf-8')
                    json_data = json.loads(string_response)

                    # Извлечение значения content из JSON-данных
                    if 'message' in json_data and 'content' in json_data['message']:
                        content = json_data['message']['content']
                        result += json_data['message']['content']
                        #print(content, end='')
                    else:
                        print("Content field not found in JSON response.")
            print('\n')

        else:
            print("Failed to get a successful response. Status code:", response.status_code)

        state.answer = result
