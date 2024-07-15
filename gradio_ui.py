from src.utils import DialogueSearchConfig
from src.dialogue_loop import DialogueSearch

import gradio as gr
import pandas as pd

# Полезные ссылки:
# https://www.gradio.app/guides/theming-guide
# https://www.gradio.app/guides/creating-a-chatbot-fast#add-streaming-to-your-chatbot
# https://www.gradio.app/guides/creating-a-chatbot-fast

#
UI_TITLE = "Цифровой ассистент"
UI_DESCRIPTION = "Ассистен может ответить на ваши вопросы по теме 'Информационной безопасности'."
UI_ARTICLE = ''
QUESTION_EXAMPLES = [
    "Что такое алгоритм шифрования?", # doc3
    "Какое определение термина 'атака'?", # doc20
    "Что такое синхропосылка?", # doc38
    "Какую информацию о СОПС должен указывать изготовитель?" # doc68
    ]
UNDO_BTN_NAME = 'Удалить предыдущий вопрос/ответ'
CLEAR_BTN_NAME = 'Отчистить весь чат'
QUESTION_FIELD_PLACEHOLDER = "Какой у вас вопрос?"
BOT_AVATAR, USER_AVATAR = [
    '/home/aisummer/mikhail_workspace/nlp_service/data/ui_images/bot_avatar.jpg',
    '/home/aisummer/mikhail_workspace/nlp_service/data/ui_images/user_avatar.png']
DOCS_INFO_PATH = '/home/aisummer/mikhail_workspace/nlp_service/data/infsec_gosts/docs/v1/info.csv'

dialogue_config = DialogueSearchConfig.load()
dialogue_system = DialogueSearch(dialogue_config)

docs_df = pd.read_csv(DOCS_INFO_PATH, sep=';')

#
def question_handler(message, history):
    final_state = dialogue_system.start(query=message)

    doc_links = [ docs_df[docs_df['filename'] == item.metadata['doc_id']].iloc[0]['url'] for item in final_state.base_relevant_docs]

    system_answer = f'''{final_state.answer}\n\nSource documents: [{
        ', '.join([f"[{i}]({link})" for i, link in enumerate(doc_links)])}]'''

    return system_answer

#
demo = gr.ChatInterface(
    question_handler,
    chatbot=gr.Chatbot(
        height=500, 
        show_copy_button=True,
        avatar_images=[USER_AVATAR, BOT_AVATAR]),
    textbox=gr.Textbox(placeholder=QUESTION_FIELD_PLACEHOLDER, container=False, scale=7),
    title=UI_TITLE,
    description=UI_DESCRIPTION,
    theme=gr.themes.Default(),
    examples=QUESTION_EXAMPLES,
    cache_examples=True,
    retry_btn=None,
    undo_btn=UNDO_BTN_NAME,
    clear_btn=CLEAR_BTN_NAME,
)

demo.launch()