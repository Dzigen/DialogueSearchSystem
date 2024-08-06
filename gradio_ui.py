#from src.utils import DialogueSearchConfig
#from src.dialogue_loop import DialogueSearch
from src.utils.dialogue_configs import DialogueState, DialogueStatus

import gradio as gr
import random
import pandas as pd
import time
from typing import List, Tuple

# Полезные ссылки:
# https://www.gradio.app/guides/theming-guide
# https://www.gradio.app/guides/creating-a-chatbot-fast#add-streaming-to-your-chatbot
# https://www.gradio.app/guides/creating-a-chatbot-fast

#
UI_TITLE = "Поисковая система"

BOT_AVATAR, USER_AVATAR = [
    '/home/dzigen/Desktop/nlp_service/data/ui_images/bot_avatar.jpg',
    '/home/dzigen/Desktop/nlp_service/data/ui_images/user_avatar.png']
DOCS_INFO_PATH = '/nlp_service/data/infsec_gosts/docs/v1/info.csv'
GRADIO_PORT = 9090

#dialogue_config = DialogueSearchConfig.load()
#dialogue_system = DialogueSearch(dialogue_config)

DIALOGUE_STATE = None

#docs_df = pd.read_csv(DOCS_INFO_PATH, sep=';')

""" #
def question_handler(message, history):
    state = DialogueState(query=message)
    
    if dialogue_system.summarizer.llm.conf_Hyper.stream:
        answer = ''
        chunk = ''
        for answer_part in dialogue_system.start(state):
            if 'content' in answer_part['choices'][0]['delta']:
                chunk += answer_part['choices'][0]['delta']['content']
                if len(chunk) > 5:
                    answer += chunk
                    chunk = ''
                    yield answer
        answer += chunk
        yield answer        
    else:
        answer = dialogue_system.start(state)['choices'][0]['message']['content']
    state.answer = answer

    doc_links = list(set([docs_df[docs_df['filename'] == item.metadata['doc_id']].iloc[0]['url'] for item in state.base_relevant_docs]))
    source_docs_str = f"Source documents: [{', '.join([f'[{i}]({link})' for i, link in enumerate(doc_links)])}]" if len(doc_links) else "" 
    system_answer = f"{state.answer}\n\n{source_docs_str}"

    yield system_answer """

#

with gr.Blocks(title=UI_TITLE) as demo:
    with gr.Tab("Search system"):
        with gr.Row(equal_height=True):
            clearsearchtab_btn = gr.Button("Clear search result", scale=0)
            question_txtfield = gr.Textbox(scale=3,placeholder="insert your question...", show_label=False)
            search_btn = gr.Button("Search",scale=0)

        with gr.Accordion("Dialogue window", open=False):
            with gr.Column():
                chat_window = gr.Chatbot(bubble_full_width=False, avatar_images=[USER_AVATAR, BOT_AVATAR])
                with gr.Row():
                    chat_txtfield = gr.Textbox(scale=3, show_label=False, placeholder="insert your clarifying answer...")
                    chat_clarify_btn = gr.Button("Clarify",scale=0)
                chat_stop_btn = gr.Button("End dialogue & get system answer")

        with gr.Accordion("System answer", open=False):
            answer_txtfield = gr.TextArea(value="Hello World", container=False)
            vote_btn = gr.Radio(['like', 'dislike'], show_label=False, container=False)

        with gr.Column(variant='compact', visible=False) as relevant_docslist:
            gr.Markdown("### List of relevant document")
            with gr.Group():
                docs_btns = [gr.Button(f"Button {i}") for i in range(3)]

            with gr.Group():
                with gr.Row():
                    page_left_btn = gr.Button(f"<", scale=1)
                    pages_btns = [gr.Button(f"Button {i}", scale=0) for i in range(1)] 
                    page_right_btn = gr.Button(f">", scale=1)

    with gr.Tab("Description") as description_tab:
        desc_txtfield = gr.TextArea("Dialogue system description")

    with gr.Tab("Settings") as settings_tab:
        search_format_btn = gr.Radio(["single-turn", "multi-turn"], label = "Формат взаимодействия с пользователем")

    with gr.Tab("Authors") as authors_tab:
        authors_txtfield = gr.TextArea("menshikov.mikhail.2001@gmail.com")

    #

    def search_handler(question: str, history: List[Tuple[str, str]]):
        global DIALOGUE_STATE
        DIALOGUE_STATE = DialogueState(query=question)

        searcher_obj = DIALOGUE_SEARCHER.start(DIALOGUE_STATE)

        for info in searcher_obj:
            
            #
            if DIALOGUE_STATE.status == DialogueStatus.dialogue_continue_ask:
                pass
            
            #
            elif DIALOGUE_STATE.status == DialogueStatus.clarifying_awaiting:
                pass

            #
            elif DIALOGUE_STATE.status == DialogueStatus.documents_summarization:
                break
                
            #
            else:
                history.append([])
                yield 


        # generating text answer
        #

        return [[question, 'hi i am bot']]

    def clarify_handler(clarify_answer: str, chat_history: List[Tuple[str, str]]):
        return "", chat_history + [[clarify_answer, None]]

    def end_dialogue_handler(chat_history: List[Tuple[str, str]]):
        return chat_history + [[None, "Stop clarifying"]]

    def output_answer_handler():
        test_answer = 'Каждый охотник желает знать: где сидит фазан'
        for i in range(len(test_answer)):
            yield test_answer[:i]

    def output_doclist_handler():
        return [gr.Column(visible=True)] + [gr.Button(f"Button {i}") for i in range(3)]

    def answer_vote_handler(vote: str):
        print(f"vote {vote} recieved")

    def clear_search_handler():
        return "", None, "", gr.Column(visible=False)

    #

    search_btn.click(search_handler, [question_txtfield, chat_window], [chat_window], 
                     queue=False).then(output_doclist_handler, None, [relevant_docslist] + docs_btns).then(output_answer_handler, None, [answer_txtfield])
    
    clearsearchtab_btn.click(clear_search_handler, None, [question_txtfield, chat_window, answer_txtfield, relevant_docslist], queue=False)
    
    chat_clarify_btn.click(clarify_handler, [chat_txtfield, chat_window], [chat_txtfield, chat_window])
    
    chat_stop_btn.click(end_dialogue_handler, [chat_window], [chat_window])
    
    vote_btn.change(answer_vote_handler, vote_btn, None)

demo.queue()
demo.launch()
