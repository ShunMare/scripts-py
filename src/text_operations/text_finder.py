import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class TextFinder:
    """インデックスファイルを解析し、特定の文字列から始まる行の内容を抽出するクラス"""

    @staticmethod
    def find_line_starting_with(lines: List[str], start_string: str) -> Optional[str]:
        """
        指定された文字列で始まる行を探し、その内容を返します。

        :param lines: 検索対象の行のリスト
        :param start_string: 検索する行の開始文字列
        :return: 見つかった行の内容（開始文字列を除く）。見つからない場合はNone
        """
        logger.info(f"'{start_string}' で始まる行を検索します")
        for line in lines:
            if line.startswith(start_string):
                content = line.split(start_string)[1].strip()
                logger.info(f"'{start_string}' で始まる行を見つけました: {content}")
                return content
        logger.warning(f"'{start_string}' で始まる行が見つかりませんでした")
        return None

    @staticmethod
    def find_and_extract_after(content: str, search_string: str) -> Optional[str]:
        """
        指定された文字列以降の内容を検索して抽出する

        :param content: 処理対象の文字列
        :param search_string: 検索する文字列
        :return: 検索文字列以降の内容、見つからない場合はNone
        """
        index = content.find(search_string)
        return content[index:] if index != -1 else None

    @staticmethod
    def count_occurrences(text: str, substring: str) -> int:
        """
        指定された文字列内に、部分文字列が何回出現するかを数えます。

        :param text: 検索対象の文字列
        :param substring: 数える部分文字列
        :return: 部分文字列の出現回数
        """
        count = text.count(substring)
        logger.info(f"'{substring}' は '{text}' 内に {count} 回出現しました")
        return count