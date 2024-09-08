import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import re
from typing import Optional

class TextProcessor:
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
    def process_content_with_search(content: str, search_string: str) -> Optional[str]:
        """
        指定された文字列以降の内容を返す

        :param content: 処理対象の文字列
        :param search_string: 検索する文字列
        :return: 検索文字列以降の内容、見つからない場合はNone
        """
        index = content.find(search_string)
        return content[index:] if index != -1 else None

    @staticmethod
    def process_content_with_replacement(content: str, start_word: str, end_word: str, target_text: str, replacement_text: str) -> Optional[str]:
        """
        指定された開始語と終了語の間にある対象テキストを置換する

        :param content: 処理対象の文字列
        :param start_word: 開始語
        :param end_word: 終了語
        :param target_text: 置換対象のテキスト
        :param replacement_text: 置換後のテキスト
        :return: 置換後の文字列、変更がない場合はNone
        """
        pattern = re.compile(f"{re.escape(start_word)}(.*?){re.escape(end_word)}", re.DOTALL)
        new_content = pattern.sub(lambda m: f"{start_word}{m.group(1).replace(target_text, replacement_text)}{end_word}", content)
        return new_content if new_content != content else None

    @staticmethod
    def process_content_for_pattern(content: str) -> Optional[str]:
        """
        特定のパターンに一致する行に空白を追加する

        :param content: 処理対象の文字列
        :return: 処理後の文字列、変更がない場合はNone
        """
        lines = content.splitlines(True)
        new_lines, modified = TextProcessor._add_spaces_to_pattern(lines)
        return "".join(new_lines) if modified else None

    @staticmethod
    def _add_spaces_to_pattern(lines: list[str]) -> tuple[list[str], bool]:
        """
        '- `...`' パターンに一致する行の末尾に空白を追加する

        :param lines: 処理対象の行のリスト
        :return: 処理後の行のリストと変更があったかどうかのフラグ
        """
        pattern = re.compile(r"^- `[^`]+`(.*)$")
        modified = False
        for i, line in enumerate(lines):
            match = pattern.match(line.rstrip())
            if match and not line.rstrip().endswith("  "):
                lines[i] = f"{line.rstrip()}  \n"
                modified = True
        return lines, modified

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
