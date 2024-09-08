import os
import logging


class ChatGPTContentGenerator:
    def __init__(
        self,
        edge_handler,
        keyboard_handler,
        chatgpt_handler,
        prompt_generator,
        text_processor,
        wait_time_after_reload,
        wait_time_after_prompt_short,
        wait_time_after_prompt_long,
    ):
        self.edge_handler = edge_handler
        self.keyboard_handler = keyboard_handler
        self.chatgpt_handler = chatgpt_handler
        self.prompt_generator = prompt_generator
        self.text_processor = text_processor
        self.wait_time_after_reload = wait_time_after_reload
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        logging.info("ContentGenerator initialized")

    def get_md(self, theme, heading, evidences, initial_prompt):
        """mdコンテンツを生成して取得する"""
        for i, evidence in enumerate(evidences):
            evidence = self.text_processor.remove_content_after(
                evidence, "ソース: Copilot との会話"
            )
            evidence = self.text_processor.remove_pattern(
                evidence, r"\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]+:\s*\[[^\]]+\]\([^\)]+\)"
            )
            if i == 0:
                # 1回目のプロンプト処理
                prompt = self.prompt_generator.create_initial_prompt(
                    theme, heading, evidence, initial_prompt
                )
            else:
                # 2回目以降のプロンプト処理
                prompt = self.prompt_generator.generate_additional_prompt(evidence)
            self.chatgpt_handler.send_prompt_and_generate_content(
                prompt, repeat_count=2
            )

        content = self.chatgpt_handler.get_generated_content()
        logging.info("Markdown content generated")
        return content

    def get_title(self, theme):
        """タイトルコンテンツを生成して取得する"""
        title_prompt = os.getenv("TITLE_PROMPT").format(theme)
        title = self.chatgpt_handler.get_content(title_prompt, repeat_count=0)
        logging.info("Title content generated")
        return title

    def get_permalink(self):
        """パーマリンクコンテンツを生成して取得する"""
        permalink = self.chatgpt_handler.get_content(
            os.getenv("PERMALINK_PROMPT"), repeat_count=0
        )
        logging.info("Permalink content generated")
        return permalink

    def get_description(self):
        """短いメタディスクリプションコンテンツを生成して取得する"""
        description = self.chatgpt_handler.get_content(
            os.getenv("SHORT_DESCRIPTION_PROMPT"), repeat_count=0
        )
        logging.info("Short description content generated")
        return description

    def get_keywords(self):
        """メタキーワードコンテンツを生成して取得する"""
        keywords = self.chatgpt_handler.get_content(
            os.getenv("KEYWORDS_PROMPT"), repeat_count=0
        )
        logging.info("Keywords content generated")
        return keywords
