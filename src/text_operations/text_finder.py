import logging
from typing import Optional, List
import re

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
        logger.debug(f"'{start_string}' で始まる行を検索します")
        for line in lines:
            if line.startswith(start_string):
                content = line.split(start_string)[1].strip()
                logger.debug(f"'{start_string}' で始まる行を見つけました: {content}")
                return content
        logger.debug(f"'{start_string}' で始まる行が見つかりませんでした")
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
        logger.debug(f"'{substring}' は '{text}' 内に {count} 回出現しました")
        return count

    @staticmethod
    def extract_pattern(text: str, pattern: str) -> Optional[str]:
        """
        指定されたパターンに一致する部分を文字列から抽出します。

        :param text: 解析対象の文字列
        :param pattern: 抽出に使用する正規表現パターン
        :return: 抽出された文字列。抽出できない場合はNone
        """
        logger.debug(f"テキストからパターンを抽出します: {text}")
        logger.debug(f"使用するパターン: {pattern}")

        match = re.search(pattern, text)

        if match:
            extracted = match.group(1)
            logger.debug(f"パターンに一致する文字列を抽出しました: {extracted}")
            return extracted
        else:
            logger.debug("パターンに一致する文字列の抽出に失敗しました")
            return None

    @staticmethod
    def extract_segments(text: str, segment_pattern: str = r"/([^/]+)") -> List[str]:
        """
        指定されたパターンに一致するセグメントをすべて抽出します。

        :param text: 解析対象の文字列
        :param segment_pattern: セグメントを抽出するための正規表現パターン
        :return: 抽出されたセグメントのリスト
        """
        logger.debug(f"テキストからセグメントを抽出します: {text}")
        logger.debug(f"使用するセグメントパターン: {segment_pattern}")

        matches = re.findall(segment_pattern, text)

        logger.debug(f"抽出されたセグメント: {matches}")
        return matches
