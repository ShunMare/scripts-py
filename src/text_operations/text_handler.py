import os
from typing import List, Optional, Any, Tuple
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class TextHandler:
    @staticmethod
    def split_string(text: Optional[str], separator: str = ",") -> List[str]:
        """
        指定された区切り文字で文字列を分割し、結果を配列として返します。
        Noneが入力された場合は空のリストを返します。

        :param text: 分割する文字列（Noneの場合あり）
        :param separator: 区切り文字（デフォルトはカンマ）
        :return: 分割された文字列のリスト
        """
        if text is None:
            logger.warning("None was input. Returning an empty list.")
            return []

        result = [item.strip() for item in text.split(separator)]
        logger.info(f"Split string '{text}' by '{separator}': {result}")
        return result

    @staticmethod
    def extract_substring(text: str, start: int = 0, length: int = 100) -> str:
        """
        指定された開始位置から指定された文字数分の部分文字列を返します。

        :param text: 元の文字列
        :param start: 開始位置（0から始まる）
        :param length: 抽出する文字数
        :return: 抽出された部分文字列
        """
        if start < 0:
            logger.warning("Start position is negative. Treating as 0.")
            start = 0

        end = start + length
        result = text[start:end]

        logger.info(f"Extracted {length} characters from position {start}: '{result}'")
        return result

    @staticmethod
    def count_occurrences(content: str, search_string: str) -> int:
        """
        指定された文字列の出現回数を数える

        :param content: 検索対象の文字列
        :param search_string: 検索する文字列
        :return: 出現回数
        """
        return content.count(search_string)

    @staticmethod
    def generate_display_value(
        value: Any, max_length: int = 100, placeholder: str = "..."
    ) -> str:
        """
        任意の型の値に対して、表示用の文字列を生成します。

        :param value: 表示用に変換する値（任意の型）
        :param max_length: 生成する文字列の最大長（デフォルト: 100）
        :param placeholder: 切り詰めた場合に末尾に付加する文字列（デフォルト: "..."）
        :return: 表示用の文字列
        """
        try:
            if value is None:
                return "None"
            if isinstance(value, str):
                if len(value) > max_length:
                    return value[: max_length - len(placeholder)] + placeholder
                return value
            if isinstance(value, (list, dict)):
                str_value = str(value)
                if len(str_value) > max_length:
                    return str_value[: max_length - len(placeholder)] + placeholder
                return str_value
            str_value = str(value)
            if len(str_value) > max_length:
                return str_value[: max_length - len(placeholder)] + placeholder
            return str_value

        except Exception as e:
            logger.error(f"Error occurred while converting value to string: {e}")
            return f"<Error: {type(value).__name__}>"

    @staticmethod
    def split_at_character(
        text: str, max_length: int, split_char: str = "_"
    ) -> Tuple[str, str]:
        """
        Split a string at a specified character, respecting the maximum length.

        This function attempts to split the input text at the specified character,
        ensuring that the first part does not exceed the specified maximum length.
        If the split character is not found within the maximum length, it splits at the
        maximum length.

        :param text: The text to split.
        :param max_length: The maximum length of the first part.
        :param split_char: The character at which to split the string (default is "_").
        :return: A tuple containing the first part and the remaining text.
        """
        if len(text) <= max_length:
            return text, ""

        split_index = text.rfind(split_char, 0, max_length)
        if split_index == -1:
            split_index = max_length

        return text[:split_index], text[split_index:]

    @staticmethod
    def format_text_with_keyword_split(
        text: str,
        keyword: str = "",
        split_char: str = "_",
        max_line_length: int = 25,
        max_lines: int = 3,
    ) -> str:
        """
        Process a title by splitting it into multiple lines based on a keyword and length constraints.

        :param text: The input text to process.
        :param keyword: The keyword to split the text on (default is "").
        :param max_line_length: The maximum length of each line (default is 25).
        :param max_lines: The maximum number of lines to produce (default is 3).
        :return: The processed text as a string with line breaks.
        """

        if keyword in text:
            first_part, second_part = text.split(keyword, 1)
            first_part = first_part.strip()
            lines = []
            while first_part and len(lines) < max_lines - 1:
                line, first_part = TextHandler.split_at_character(
                    first_part, max_line_length, split_char
                )
                lines.append(line)
            if first_part:
                lines[-1] += first_part
            lines.append(keyword)
            result = "\n".join(lines)
        else:
            lines = []
            remaining_text = text
            while remaining_text and len(lines) < max_lines:
                line, remaining_text = TextHandler.split_at_character(
                    remaining_text, max_line_length, split_char
                )
                lines.append(line)
            if remaining_text:
                lines[-1] += remaining_text
            result = "\n".join(lines)
        return result


class TextPathHandler:
    """
    TextPathHandler クラスは、テキストベースのパス操作を担当します。
    複数のパス要素を結合し、パスの区切り文字を正規化します。
    """

    @staticmethod
    def join_path(*path_elements: str) -> str:
        """
        複数のパス要素を結合してフルパスを生成します。
        :param path_elements: 結合するパス要素（可変長引数）
        :return: 結合された正規化されたパス
        """
        joined_path = os.path.join(*path_elements)
        normalized_path = os.path.normpath(joined_path)
        logger.info(f"Joined path: {normalized_path}")
        return normalized_path

    @staticmethod
    def join_and_normalize_path(path_elements: List[str]) -> str:
        """
        パス要素のリストを受け取り、結合して正規化されたパスを返します。
        :param path_elements: 結合するパス要素のリスト
        :return: 結合された正規化されたパス
        """
        if not path_elements:
            logger.warning("Empty list of path elements provided")
            return ""

        joined_path = os.path.join(*path_elements)
        normalized_path = os.path.normpath(joined_path)
        logger.info(f"Joined and normalized path: {normalized_path}")
        return normalized_path

    @staticmethod
    def normalize_separator(path: str) -> str:
        """
        パスの区切り文字をOSに応じて正規化します。
        :param path: 正規化するパス
        :return: 区切り文字が正規化されたパス
        """
        normalized_path = os.path.normpath(path)
        logger.info(f"Normalized path separators: {normalized_path}")
        return normalized_path
