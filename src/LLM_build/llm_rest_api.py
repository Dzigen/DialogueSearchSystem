from src.LLM_build.utils import llmConfig
import requests
import json


def llm_question(config: llmConfig) -> None:

    url = 'http://localhost:11434/api/chat'
    data = {
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": "Ты вопросно-ответная система. Все ответы генерируешь на русском языке. Отвечай коротко по вопросам."
            },
            {
                "role": "assistant",
                "content": "Твоя база знаний, все ответы генерируются на основе текста ниже: \
            4.1.2 Вагон должен соответствовать климатическому исполнению УХЛ1 по ГОСТ 15150 с  \
            обеспе-чением работоспособного состояния в диапазоне рабочих температур от минус 60 °С до плюс 50 °С. 4.1.3 \
            Габарит вагона должен соответствовать требованиям ГОСТ 9238. 4.1.4 Вагон должен иметь кузов, включающий в себя \
            раму с установленными на ней отдельными емкостями (бункерами) для размещения грузов, а также иные устройства, \
            предусмотренные конструк-торской документацией, и должен быть оборудован: а) тележками по ГОСТ 9246 или иному стандарту, \
                распространяющемуся на тележки грузовых вагонов железных дорог; 6) автосцепными устройствами по ГОСТ 33434 или иному стандарту, \
            распространяющемуся на автосцепные устройства грузовых вагонов, с контуром зацепления автосцепки по ГОСТ 21447, \
            с обо-рудованием автосцепок нижним ограничителем вертикальных перемещений и расцепным приводом с \
            блокировочной цепью и поглощающими аппаратами по ГОСТ 32913; в) автоматическим пневматическим тормозом по ГОСТ 34434; \
            г) стояночным тормозом по ГОСТ 32880. "
            },
            {
                "role": "user",
                "content": 'Требованиями какого госта должен соответствовать габарит вагона?'
            }
        ],
        "stream": config.stream,
        "options": {
            "num_keep": config.num_keep,
            "seed": config.seed,
            "num_predict": config.num_predict,
            "top_k": config.top_k,
            "top_p": config.top_p,
            "tfs_z": config.tfs_z,
            "typical_p": config.typical_p,
            "repeat_last_n": config.repeat_last_n,
            "temperature": config.temperature,
            "repeat_penalty": config.repeat_penalty,
            "presence_penalty": config.presence_penalty,
            "frequency_penalty": config.frequency_penalty,
            "mirostat": config.mirostat,
            "mirostat_tau": config.mirostat_tau,
            "mirostat_eta": config.mirostat_eta,
            "penalize_newline": config.penalize_newline,
            #"stop": config.stop,
            "numa": config.numa,
            "num_ctx": config.num_ctx,
            "num_batch": config.num_batch,
            "num_gpu": config.num_gpu,
            "main_gpu": config.main_gpu,
            "low_vram": config.low_vram,
            "f16_kv": config.f16_kv,
            "vocab_only": config.vocab_only,
            "use_mmap": config.use_mmap,
            "use_mlock": config.use_mlock,
            "num_thread": config.num_thread
        }
    }

    response = requests.post(url, json=data, stream=True)

    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                string_response = chunk.decode('utf-8')
                json_data = json.loads(string_response)

                # Извлечение значения content из JSON-данных
                if 'message' in json_data and 'content' in json_data['message']:
                    content = json_data['message']['content']
                    print(content, end='')
                else:
                    print("Content field not found in JSON response.")
        print('\n')

    else:
        print("Failed to get a successful response. Status code:", response.status_code)


if __name__ == '__main__':
    config = llmConfig()
    llm_question(config)