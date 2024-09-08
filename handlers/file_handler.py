import sys
import os
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

class FileHandler:
    """
    ファイルの読み書きと削除を管理するクラス
    """
    def __init__(self):
        self.text_extensions = [".txt", ".md", ".mdx", ".py", ".js", ".html", ".css", ".json", ".xml", ".csv"]

    def is_text_file(self, file_path: str) -> bool:
        """
        指定されたファイルがテキストファイルかどうかを判定する

        :param file_path: 判定するファイルのパス
        :return: テキストファイルの場合True、それ以外はFalse
        """
        return os.path.splitext(file_path)[1].lower() in self.text_extensions

    def read_file(self, file_path: str) -> Optional[str]:
        """
        ファイルを読み込み、内容を返す
        非テキストファイルの場合はNoneを返す
        複数のエンコーディングで試行する

        :param file_path: 読み込むファイルのパス
        :return: ファイルの内容、またはNone
        """
        if not self.is_text_file(file_path):
            print(f"Skipping non-text file: {file_path}")
            return None

        encodings = ["utf-8", "cp932"]
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        return None

    def write_file(self, file_path: str, content: str) -> None:
        """
        指定されたパスにファイルを書き込む

        :param file_path: 書き込むファイルのパス
        :param content: 書き込む内容
        """
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def delete_file(self, file_path: str) -> bool:
        """
        指定されたパスのファイルを削除する

        :param file_path: 削除するファイルのパス
        :return: 削除に成功した場合True、それ以外はFalse
        """
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                return True
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
                return False
        return False

    def get_file_content(self, file_path: str) -> Optional[str]:
        """
        指定されたパスのファイルを開いて中身を取得する

        :param file_path: 読み込むファイルのパス
        :return: ファイルの内容、またはNone（ファイルが存在しない場合や読み込みエラーの場合）
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None

        try:
            return self.read_file(file_path)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
