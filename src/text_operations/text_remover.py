from typing import Optional
import re
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class TextRemover:
    @staticmethod
    def remove_content_after(
        content: Optional[str], search_string: Optional[str]
    ) -> Optional[str]:
        """
        指定された文字列以降の内容をすべて削除する

        :param content: 処理対象の文字列（Noneの場合もあり）
        :param search_string: 削除開始位置を示す文字列
        :return: 処理後の文字列、contentがNoneの場合はNone
        """
        if content is None or search_string is None:
            logger.warning("Content is None in remove_content_after method")
            return content

        index = content.find(search_string)
        if index != -1:
            return content[:index]
        return content

    @staticmethod
    def remove_pattern(content: Optional[str], pattern: str) -> Optional[str]:
        """
        指定されたパターンに一致する文字列を削除する

        :param content: 処理対象の文字列（Noneの場合もあり）
        :param pattern: 削除するパターンを示す正規表現
        :return: 処理後の文字列、contentがNoneの場合はNone
        """
        if content is None:
            logger.warning("Content is None in remove_pattern method")
            return None

        try:
            return re.sub(pattern, "", content)
        except re.error as e:
            logger.error(f"Invalid regular expression pattern: {pattern}. Error: {e}")
            return content

    @staticmethod
    def remove_outer_tags(text):
        pattern_start = r"^\s*<(\w+)(?:\s+[^>]*)?\s*>"
        text = re.sub(pattern_start, "", text, count=1)
        pattern_end = r"</(\w+)>\s*$"
        text = re.sub(pattern_end, "", text, count=1)

        return text.strip()
