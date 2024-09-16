import pyperclip
import pandas as pd

from src.text_operations.text_replacer import TextReplacer
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)
text_replacer = TextReplacer()


class PromptGenerator:
    def __init__(self, wait_time_after_prompt_short, wait_time_after_prompt_long):
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        logger.info("PromptGenerator initialized")

    def create_initial_prompt(self, theme, heading, evidence, initial_prompt):
        initial_prompt = self.replace_marker(initial_prompt, theme, heading)
        if pd.notna(evidence):
            evidence_text = f"参照内容：\n{evidence}"
        initial_prompt += evidence_text
        pyperclip.copy(initial_prompt)
        logger.info("Initial prompt created and copied to clipboard")
        return initial_prompt

    def create_additional_prompt(self, evidence):
        """追加の証拠を元にコンテンツを生成する"""
        additional_prompt = (
            f"下記の内容を上記に加えて。省略せずに全部書いて。\n{evidence}"
        )
        pyperclip.copy(additional_prompt)
        logger.info("Additional prompt created and copied to clipboard")
        return additional_prompt

    def replace_marker(self, prompt, theme, heading):
        """プロンプトの中のマーカーを置換する"""
        if prompt is None:
            prompt = ""
        prompt = text_replacer.replace(
            text=prompt, target_text="{theme}", replacement_text=theme
        )
        prompt = text_replacer.replace(
            text=prompt, target_text="{heading}", replacement_text=heading
        )
        return prompt
