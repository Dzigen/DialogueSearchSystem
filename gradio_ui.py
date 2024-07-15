import gradio as gr
import time

from src.utils import DialogueSearchConfig
from src.dialogue_loop import DialogueSearch

# Полезные ссылки:
# https://www.gradio.app/guides/theming-guide
# https://www.gradio.app/guides/creating-a-chatbot-fast#add-streaming-to-your-chatbot
# https://www.gradio.app/guides/creating-a-chatbot-fast

#
UI_TITLE = "Yes Man"
UI_DESCRIPTION = "Ask Yes Man any question"
UI_ARTICLE = ''
QUESTION_EXAMPLES = ["Hello", "Am I cool?", "Are tomatoes vegetables?"]
UNDO_BTN_NAME = 'Delete Previous'
CLEAR_BTN_NAME = 'Clear'
QUESTION_FIELD_PLACEHOLDER = "Ask me a yes or no question"

dialogue_config = DialogueSearchConfig.load()
dialogue_system = DialogueSearch(dialogue_config)

#
def question_handler(message, history):
    final_state = dialogue_system.start(query=message)

    system_answer = f"{final_state.answer}\n\nSource documents: {
        ','.join([f"[{i}]({item.metadata['doc_id']})" 
        for i, item in enumerate(final_state.base_relevant_docs)])}"

    return system_answer

#
demo = gr.ChatInterface(
    question_handler,
    chatbot=gr.Chatbot(height=300),
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