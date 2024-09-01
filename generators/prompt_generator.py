import pyperclip
import pandas as pd
import logging

class PromptGenerator:
    def __init__(self, keyboard_handler, chatgpt_handler, wait_time_after_prompt_short, wait_time_after_prompt_long):
        self.keyboard_handler = keyboard_handler
        self.chatgpt_handler = chatgpt_handler
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        logging.info('PromptGenerator initialized')

    def create_initial_prompt(self, theme, heading, evidence):
        initial_prompt = f"{theme}について書きたい。これまでの内容は入れないで、また一から書いて"
        if heading:
            initial_prompt += f"、見出しは{heading}です"
        initial_prompt += "。以下の指示に従って作成してください：\n"
        initial_prompt += "• できるだけわかりやすく、長く、ブログ形式で書いてください。\n"
        initial_prompt += "• 下記の内容以外から情報を出さないでください（ハルシネーション防止のため）。\n"
        initial_prompt += "• 見出しの番号は除いてください。\n\n"
        initial_prompt += "• タイトルは記載しないで、見出しはh2（##）、h3（###）、h4（####）で構成してください。\n\n"
        initial_prompt += "• 下記の内容を参照してください。\n"
        if pd.notna(evidence):
            initial_prompt += "参照内容：\n" + str(evidence)
        else:
            initial_prompt += "参照内容：\n"
        pyperclip.copy(initial_prompt)
        logging.info('Initial prompt created and copied to clipboard')
        print(f"Initial prompt created: {initial_prompt}")
        return initial_prompt  # Return the prompt if needed

    def generate_additional_prompt(self, evidence):
        """追加の証拠を元にコンテンツを生成する"""
        additional_prompt = (
            f"下記の内容を上記に加えて。省略せずに全部書いて。\n{evidence}"
        )
        pyperclip.copy(additional_prompt)
        logging.info('Additional prompt created and copied to clipboard')
        print(f"Additional prompt created: {additional_prompt}")
        return additional_prompt  # Return the prompt if needed

