import re
import logging
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)


class TextAppender:

    @staticmethod
    def add_spaces_to_matching_lines(content: str) -> Optional[str]:
        """
        特定のパターンに一致する行に空白を追加する

        :param content: 処理対象の文字列
        :return: 処理後の文字列、変更がない場合はNone
        """
        lines = content.splitlines(True)
        new_lines, modified = TextAppender._add_spaces_to_pattern_lines(lines)
        return "".join(new_lines) if modified else None

    @staticmethod
    def _add_spaces_to_pattern_lines(lines: List[str]) -> Tuple[List[str], bool]:
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
