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

    def create_initial_prompt(self, theme, heading, evidence, initial_prompt):
        initial_prompt = initial_prompt.replace('{theme}', theme)
        initial_prompt = initial_prompt.replace('{heading}', heading)
        if pd.notna(evidence):
            evidence_text = f"参照内容：\n{evidence}"
        initial_prompt += evidence_text
        pyperclip.copy(initial_prompt)
        logging.info('Initial prompt created and copied to clipboard')
        return initial_prompt

    def generate_additional_prompt(self, evidence):
        """追加の証拠を元にコンテンツを生成する"""
        additional_prompt = (
            f"下記の内容を上記に加えて。省略せずに全部書いて。\n{evidence}"
        )
        pyperclip.copy(additional_prompt)
        logging.info('Additional prompt created and copied to clipboard')
        print(f"Additional prompt created")
        return additional_prompt

