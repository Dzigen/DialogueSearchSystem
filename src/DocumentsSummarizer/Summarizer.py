from src.DocumentsSummarizer.utils import SummarizerConfig
from src.LLM_build.utils import llmConfig
from src.utils import DialogueState
from src.logger import Logger
from ollama import Client

class SummarizerModule:
    def __init__(self) -> None:
        #self.log = log
        #self.log.info("Initiating Summarizer-class")
        #self.config = config
        self.client = Client(host='http://172.20.6.160:11434')

    #@Logger.cls_se_log('''Генерация ответа на основании концентрированного набора релевантных документов''')
    def create_answer(self, state: DialogueState, config:llmConfig, user_promt:str, assist_promt:str) -> None:
        
        response = self.client.chat(

            model='llama3', 
            messages=[
            {"role": "system", "content": "Ты вопросно-ответная система. Все ответы генерируешь на русском языке. Отвечай коротко по вопросам."},
            {"role": "assistant", "content": assist_promt},
            {"role": "user", "content": user_promt + '\n'}],
            stream=config.stream,
            temperature=config.temperature,
            max_tokens=config.max_tokens)

        answer = response['message']['content']
        state.answer = answer