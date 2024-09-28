from typing import List
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class TextSplitter:
    @staticmethod
    def split_string_to_lines(content: str) -> List[str]:
        """
        与えられた文字列を行ごとのリストに分割します。

        :param content: 分割する文字列
        :return: 行のリスト
        """
        logger.info("Splitting string into lines")
        try:
            lines = content.splitlines()
            logger.info(f"Successfully split string into {len(lines)} lines")
            return lines
        except Exception as e:
            logger.error(f"Error occurred while splitting string: {e}")
            return []