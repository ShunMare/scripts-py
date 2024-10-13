import re
from typing import Optional
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class TextReplacer:
    """
    テキスト置換を行うためのクラス。
    様々な置換方法を提供し、ログ出力機能を持つ。
    すべてのメソッドはstaticmethodとして実装されている。
    """

    @staticmethod
    def replace_content(content: str, target_text: str, replacement_text: str) -> str:
        """
        ファイル全体に対して置換を行う。

        :param content: 置換を行う元のテキスト
        :param target_text: 置換対象のテキスト
        :param replacement_text: 置換後のテキスト
        :return: 置換後のテキスト
        """
        target_pattern = re.compile(re.escape(target_text))
        result = target_pattern.sub(replacement_text, content)
        logger.debug(
            f"Replaced '{target_text}' with '{replacement_text}' in the entire content"
        )
        return result

    @staticmethod
    def replace_content_regex(
        content: str, pattern: str, replacement: str, flags: int = re.DOTALL
    ) -> str:
        """
        正規表現を使用してコンテンツ内のテキストを置換します。

        :param content: 置換を行う元のテキスト
        :param pattern: 置換対象の正規表現パターン
        :param replacement: 置換後のテキスト
        :param flags: 正規表現フラグ（デフォルトは0）
        :return: 置換後のテキスト
        """
        compiled_pattern = re.compile(pattern, flags)
        result = compiled_pattern.sub(replacement, content)
        logger.debug(f"Replaced pattern '{pattern}' with '{replacement}' using regex")
        return result

    @staticmethod
    def replace_between(
        content: str,
        target_text: str,
        replacement_text: str,
        start_marker: Optional[str] = None,
        end_marker: Optional[str] = None,
        use_markers: bool = True,
    ) -> str:
        """
        指定されたマーカー間のテキストに対して置換を行う。

        :param content: 置換を行う元のテキスト
        :param target_text: 置換対象のテキスト
        :param replacement_text: 置換後のテキスト
        :param start_marker: 開始マーカー
        :param end_marker: 終了マーカー
        :param use_markers: マーカーを使用するかどうか
        :return: 置換後のテキスト
        """
        if not use_markers or not start_marker or not end_marker:
            logger.debug(
                "Markers not provided or not used. Replacing in the entire content."
            )
            return TextReplacer.replace_content(content, target_text, replacement_text)

        start_index = content.find(start_marker)
        if start_index == -1:
            logger.debug("Start marker not found. Replacing in the entire content.")
            return TextReplacer.replace_content(content, target_text, replacement_text)

        end_index = content.find(end_marker, start_index + len(start_marker))
        if end_index == -1:
            logger.debug(
                "End marker not found. Replacing from start marker to the end."
            )
            end_index = len(content)

        before_section = content[: start_index + len(start_marker)]
        target_section = content[start_index + len(start_marker) : end_index]
        after_section = content[end_index:]

        target_pattern = re.compile(re.escape(target_text))
        replaced_section = target_pattern.sub(replacement_text, target_section)
        logger.debug(
            f"Replaced '{target_text}' with '{replacement_text}' between markers"
        )

        return before_section + replaced_section + after_section

    @staticmethod
    def replace_with_exclusion(
        content: str, target_text: str, replacement_text: str, exclusion_pattern: str
    ) -> str:
        """
        指定された文字列を置換するが、除外パターンにマッチする部分は置換しない。

        :param content: 置換を行う元のテキスト
        :param target_text: 置換対象のテキスト
        :param replacement_text: 置換後のテキスト
        :param exclusion_pattern: 除外するパターン（正規表現）
        :return: 置換後のテキスト
        """
        target_pattern = re.compile(re.escape(target_text))
        exclusion_re = re.compile(exclusion_pattern)

        def replace_func(match):
            if exclusion_re.search(match.group(0)):
                return match.group(0)
            return replacement_text

        result = target_pattern.sub(replace_func, content)
        logger.debug(
            f"Replaced '{target_text}' with '{replacement_text}', excluding pattern: {exclusion_pattern}"
        )
        return result

    @staticmethod
    def replace_from_marker(
        content: str, target_text: str, replacement_text: str, marker: str = "---"
    ) -> str:
        """
        2番目のマーカー以降のテキストに対して置換を行う。

        :param content: 置換対象の文字列
        :param target_text: 置換対象のテキスト
        :param replacement_text: 置換後のテキスト
        :param marker: 位置を特定するためのマーカー文字列
        :return: 置換後の文字列
        """
        marker_pattern = re.compile(re.escape(marker))
        matches = list(marker_pattern.finditer(content))
        if len(matches) < 2:
            logger.debug("Second marker not found. No replacement performed.")
            return content
        position = matches[1].end()
        before = content[:position]
        after = content[position:]
        target_pattern = re.compile(re.escape(target_text))
        replaced_after = target_pattern.sub(replacement_text, after)
        logger.debug(
            f"Replaced '{target_text}' with '{replacement_text}' after the second '{marker}'"
        )
        return before + replaced_after

    @staticmethod
    def replace(
        text: Optional[str], target_text: Optional[str], replacement_text: Optional[str]
    ) -> Optional[str]:
        """
        指定されたテキストに対して単純な置換を行い、結果を返す。
        replacement_text が None の場合、空文字列で置換する。

        :param text: 置換を行う元のテキスト
        :param target_text: 置換対象のテキスト
        :param replacement_text: 置換後のテキスト（None の場合は空文字列として扱う）
        :return: 置換後のテキスト
        :raises ValueError: text または target_text が不適切な場合
        """
        if text is None:
            text = ""

        if target_text is None:
            text = ""

        if replacement_text is None:
            logger.debug("Replacement text is None. Using empty string for replacement.")
            replacement_text = ""

        pattern = re.compile(re.escape(target_text))
        result = pattern.sub(replacement_text, text)

        if result != text:
            logger.debug(
                f"Replaced '{target_text}' with '{replacement_text}' in the provided text"
            )
        else:
            logger.debug(f"No replacements made. '{target_text}' not found in the text.")

        return result

    @staticmethod
    def replace_text_between_markers(
        content: str,
        start_word: str,
        end_word: str,
        target_text: str,
        replacement_text: str,
    ) -> Optional[str]:
        """
        指定された開始語と終了語の間にある対象テキストを置換する

        :param content: 処理対象の文字列
        :param start_word: 開始語
        :param end_word: 終了語
        :param target_text: 置換対象のテキスト
        :param replacement_text: 置換後のテキスト
        :return: 置換後の文字列、変更がない場合はNone
        """
        pattern = re.compile(
            f"{re.escape(start_word)}(.*?){re.escape(end_word)}", re.DOTALL
        )
        new_content = pattern.sub(
            lambda m: f"{start_word}{m.group(1).replace(target_text, replacement_text)}{end_word}",
            content,
        )
        return new_content if new_content != content else None

    @staticmethod
    def replace_from_end(text, target, replacement):
        """
        文字列の後ろから対象の文字列を探して置換する

        :param text: 操作対象の文字列
        :param target: 置換対象の文字列
        :param replacement: 置換後の文字列
        :return: 置換後の文字列
        """
        logger.debug(
            f"replace_from_end called with text type: {type(text)}, length: {len(str(text))}"
        )
        logger.debug(f"Target: {target}, Replacement: {replacement}")

        if not isinstance(text, str):
            logger.debug(
                f"Input is not a string, converting from {type(text)} to string"
            )
            text = str(text)

        reversed_text = text[::-1]
        reversed_target = target[::-1]
        reversed_replacement = replacement[::-1]

        logger.debug(f"Reversed text (first 50 chars): {reversed_text[:50]}...")

        replaced_text = re.sub(
            re.escape(reversed_target), reversed_replacement, reversed_text, count=1
        )

        if replaced_text == reversed_text:
            logger.debug("No replacement made")
        else:
            logger.debug("Replacement successful")

        result = replaced_text[::-1]
        logger.debug(f"Final result (first 50 chars): {result[:50]}...")

        return result
