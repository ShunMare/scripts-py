import re
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class TextRemover:
    @staticmethod
    def remove_content_after(content: str, search_string: str) -> str:
        """
        指定された文字列以降の内容をすべて削除する

        :param content: 処理対象の文字列
        :param search_string: 削除開始位置を示す文字列
        :return: 処理後の文字列
        """
        index = content.find(search_string)
        if index != -1:
            return content[:index]
        return content

    @staticmethod
    def remove_pattern(content: str, pattern: str) -> str:
        """
        指定されたパターンに一致する文字列を削除する

        :param content: 処理対象の文字列
        :param pattern: 削除するパターンを示す正規表現
        :return: 処理後の文字列
        """
        return re.sub(pattern, '', content)
