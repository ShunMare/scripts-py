import os
import logging


class BingContentGenerator:
    def __init__(
        self,
        edge_handler,
        keyboard_handler,
        bing_handler,
        prompt_generator,
        wait_time_after_reload,
        wait_time_after_prompt_short,
        wait_time_after_prompt_long,
    ):
        self.edge_handler = edge_handler
        self.keyboard_handler = keyboard_handler
        self.bing_handler = bing_handler
        self.prompt_generator = prompt_generator
        self.wait_time_after_reload = wait_time_after_reload
        self.wait_time_after_prompt_short = wait_time_after_prompt_short
        self.wait_time_after_prompt_long = wait_time_after_prompt_long
        logging.info("ContentGenerator initialized")

    def get_md(self, theme, heading, evidences):
        """mdコンテンツを生成して取得する"""
        logging.info(f"Started generating Markdown content for theme")
        for i, evidence in enumerate(evidences):
            if i == 0:
                # 1回目のプロンプト処理
                logging.debug(f"Generating initial prompt with theme")
                prompt = self.prompt_generator.create_initial_prompt(
                    theme, heading, evidence
                )
            else:
                # 2回目以降のプロンプト処理
                logging.debug(f"Generating additional prompt for evidence")
                prompt = self.prompt_generator.generate_additional_prompt(evidence)
            logging.info(f"Sending prompt {i+1}")
            self.bing_handler.send_prompt(prompt)
            logging.info(f"Prompt {i+1} sent successfully")
        logging.info("All prompts sent. Waiting for generated content.")
        content = self.bing_handler.get_generated_content()
        logging.info(
            f"Markdown content generation completed. Content length: {len(content)} characters"
        )
        return content

    def get_title(self, theme):
        """タイトルコンテンツを生成して取得する"""
        title_prompt = os.getenv("TITLE_PROMPT").format(theme)
        title = self.bing_handler.get_content(title_prompt, repeat_count=0)
        logging.info("Title content generated")
        return title

    def get_permalink(self):
        """パーマリンクコンテンツを生成して取得する"""
        permalink = self.bing_handler.get_content(
            os.getenv("PERMALINK_PROMPT"), repeat_count=0
        )
        logging.info("Permalink content generated")
        return permalink

    def get_description(self):
        """短いメタディスクリプションコンテンツを生成して取得する"""
        description = self.bing_handler.get_content(
            os.getenv("SHORT_DESCRIPTION_PROMPT"), repeat_count=0
        )
        logging.info("Short description content generated")
        return description

    def get_keywords(self):
        """メタキーワードコンテンツを生成して取得する"""
        keywords = self.bing_handler.get_content(
            os.getenv("KEYWORDS_PROMPT"), repeat_count=0
        )
        logging.info("Keywords content generated")
        return keywords

    def get_evidence(self, theme, direction, isFirst):
        """エビデンスコンテンツを生成して取得する"""
        if "{theme}" in direction:
            evidence_prompt = direction.replace("{theme}", theme)
        else:
            evidence_prompt = direction
        evidence = self.bing_handler.get_content(evidence_prompt, isFirst)

        logging.info("Evidence content generated")
        return evidence

    def send_evidence(self, theme, direction, isFirst):
        """エビデンスコンテンツを生成して送信する"""
        if "{theme}" in direction:
            evidence_prompt = direction.replace("{theme}", theme)
        else:
            evidence_prompt = direction
        evidence = self.bing_handler.send_prompt(evidence_prompt, isFirst)

        logging.info("Evidence content generated")
        return evidence
