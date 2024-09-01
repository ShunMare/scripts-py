import os
import time
import pyperclip
import logging


class ContentGenerator:
    def __init__(
        self,
        edge_handler,
        keyboard_handler,
        chatgpt_handler,
        prompt_generator,
        wait_time_after_reload,
        wait_time_after_prompt_short,
        wait_time_after_prompt_long,
    ):
        self.edge_handler = edge_handler
        self.keyboard_handler = keyboard_handler
        self.chatgpt_handler = chatgpt_handler
        self.prompt_generator = prompt_generator
        self.wait_time_after_reload = wait_time_after_reload
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        logging.info("ContentGenerator initialized")

    def get_generated_content(self):
        """生成されたコンテンツをコピーして返す"""
        self.edge_handler.activate_edge()
        self.keyboard_handler.reload_page(self.wait_time_after_reload)
        self.chatgpt_handler.move_to_copy_button()
        self.chatgpt_handler.press_hotkey(["space"])
        generated_content = pyperclip.paste()
        logging.info("Generated content copied from clipboard")
        return generated_content

    def send_prompt_and_generate_content(self, prompt, repeat_count):
        """プロンプトを送信し、生成ボタンを押す処理を行う"""
        self.edge_handler.activate_edge()
        self.keyboard_handler.reload_page(self.wait_time_after_reload)
        pyperclip.copy(prompt)
        self.chatgpt_handler.paste_and_send_message()
        logging.info("Prompt sent and message generation initiated")
        time.sleep(self.wait_time_after_prompt_long)

        for _ in range(repeat_count):
            self.edge_handler.activate_edge()
            self.keyboard_handler.reload_page(self.wait_time_after_reload)
            self.chatgpt_handler.move_to_generate_button()
            self.chatgpt_handler.press_hotkey(["space"])
            logging.info("Generation button pressed")
            time.sleep(self.wait_time_after_prompt_short)

    def get_content(self, prompt, repeat_count):
        """プロンプトを送信し、生成されたコンテンツを返す"""
        self.send_prompt_and_generate_content(prompt, repeat_count)
        content = self.get_generated_content()
        logging.info("Content retrieved")
        return content

    def get_md(self, theme, heading, evidences):
        """mdコンテンツを生成して取得する"""
        for i, evidence in enumerate(evidences):
            if i == 0:
                # 1回目のプロンプト処理
                prompt = self.prompt_generator.create_initial_prompt(
                    theme, heading, evidence
                )
            else:
                # 2回目以降のプロンプト処理
                prompt = self.prompt_generator.generate_additional_prompt(evidence)
            self.send_prompt_and_generate_content(prompt, repeat_count=2)

        content = self.get_generated_content()
        logging.info("Markdown content generated")
        return content

    def get_title(self, theme):
        """タイトルコンテンツを生成して取得する"""
        title_prompt = os.getenv("TITLE_PROMPT").format(theme)
        title = self.get_content(title_prompt, repeat_count=0)
        logging.info("Title content generated")
        return title

    def get_permalink(self):
        """パーマリンクコンテンツを生成して取得する"""
        permalink = self.get_content(os.getenv("PERMALINK_PROMPT"), repeat_count=0)
        logging.info("Permalink content generated")
        return permalink

    def get_description(self):
        """短いメタディスクリプションコンテンツを生成して取得する"""
        description = self.get_content(
            os.getenv("SHORT_DESCRIPTION_PROMPT"), repeat_count=0
        )
        logging.info("Short description content generated")
        return description

    def get_keywords(self):
        """メタキーワードコンテンツを生成して取得する"""
        keywords = self.get_content(os.getenv("KEYWORDS_PROMPT"), repeat_count=0)
        logging.info("Keywords content generated")
        return keywords
