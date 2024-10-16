import pyperclip
import pandas as pd

from src.text_operations.text_replacer import TextReplacer
from src.log_operations.log_handlers import CustomLogger

logger = CustomLogger(__name__)
text_replacer = TextReplacer()


class PromptGenerator:
    def __init__(self, wait_time_after_prompt_short, wait_time_after_prompt_long):
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        logger.debug("PromptGenerator initialized")

    def create_initial_prompt(self, theme, heading, evidence, initial_prompt):
        initial_prompt = self.replace_marker(initial_prompt, theme, heading)
        if pd.notna(evidence):
            evidence_text = f"参照内容：\n{evidence}"
        initial_prompt += evidence_text
        pyperclip.copy(initial_prompt)
        logger.debug("Initial prompt created and copied to clipboard")
        return initial_prompt

    def create_additional_prompt(self, evidence):
        """追加の証拠を元にコンテンツを生成する"""
        additional_prompt = (
            f"下記の内容を参考にして、もれなく文章をまとめて。他の内容は参照しないで。リストは極力使わずに、リストで書くのではなく見出しにして。\n{evidence}"
        )
        pyperclip.copy(additional_prompt)
        logger.debug("Additional prompt created and copied to clipboard")
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
