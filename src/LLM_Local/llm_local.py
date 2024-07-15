from llama_cpp import Llama
import sys
sys.path.insert(0, "/home/aisummer/ssemenov_workspace/nlp-service")
from src.LLM_Local.utils import LLM_Hardw_Conf
from src.LLM_Local.utils import LLM_Hyper_Conf



class LLM_model:
    """
    Класс для инициализации модели и обращения к ней
    """


    def __init__(self, conf_Hard: LLM_Hardw_Conf, conf_Hyper: LLM_Hyper_Conf) -> None:

        """
        Инициализация модели.
        
        Параметры:
        -conf_Hard: Конфиг с аппаратными параметрами работы LLM; \n
        -conf_Hyper: Конфиг с гиперпараметрами модели.
        """

        self.conf_Hard = conf_Hard
        self.conf_Hyper = conf_Hyper

        self.model = Llama(
            model_path=self.conf_Hard.model_path,
            n_gpu_layers=self.conf_Hard.n_gpu_layers, 
            seed=self.conf_Hard.seed,
            n_ctx=self.conf_Hard.n_ctx
        )



    def generate(self, system_prompt:str, assistant_prompt: str, user_prompt:str ) -> str:

        """
        Метод для создания чата с моделью и генерации ответа на вопрос

        Параметры:
        -system_prompt:str: System промпт для LLM; \n
        -assistant_prompt:str: Assistant промпт для LLM; \n
        -user_prompt:str: User промпт для LLM.

        Примеры промптов 
        -"role": "system", "content": "Ты вопросно-ответная система. Отвечай на русском языке."; \n
        -"role": "assistant","content": "Это твоя база знаний. Используй её при ответе: Вектор – это направленный отрезок прямой, т. е. отрезок, имеющий определенную длину и определенное направление.";\n
        -"role": "user", "content": "Что такое вектор?".

        Контент ответа:
        - output['choices'][0]["message"]['content']
        """
        

        output = self.model.create_chat_completion(


            messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": assistant_prompt},
            {"role": "user","content": user_prompt}
            ]
        )



        return output



if __name__=="__main__":

    conf1 = LLM_Hardw_Conf()
    conf2 = LLM_Hyper_Conf()

    model = LLM_model(conf1, conf2)
    system_prompt = "Ты вопросно-ответная система. Отвечай на русском языке."
    assistant_prompt = "Это твоя база знаний. Используй её при ответе: Вектор – это направленный отрезок прямой, т. е. отрезок, имеющий определенную длину и определенное направление."
    user_prompt = 'Что такое вектор?'

    output = model.generate(system_prompt, assistant_prompt, user_prompt)
    print(output['choices'][0]["message"]['content'])