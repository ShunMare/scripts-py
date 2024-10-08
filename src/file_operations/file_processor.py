import os
from typing import Callable, List, Dict, Optional
from src.log_operations.log_handlers import setup_logger
import time

logger = setup_logger(__name__)


class FileHandler:
    """
    FileHandler クラスは、ファイル操作（読み込み、書き込み、削除）を担当します。
    このクラスは、ファイルシステムの操作に関する共通の機能を提供し、
    他のクラスやメソッドから再利用可能な形にしています。
    """

    @staticmethod
    def write_file(file_path: str, content: str):
        """
        指定されたファイルに内容を書き込みます。
        :param file_path: 書き込むファイルのパス
        :param content: 書き込む内容
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        指定されたファイルを削除します。
        :param file_path: 削除するファイルのパス
        :return: 削除が成功した場合は True、失敗した場合は False を返す
        """
        try:
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error occurred while deleting file {file_path}: {e}")
            return False

    @staticmethod
    def exists(file_path: str) -> bool:
        """
        指定されたファイルが存在するかどうかを確認します。
        :param file_path: 存在確認するファイルのパス
        :return: 存在する場合は True、存在しない場合は False
        """
        result = os.path.exists(file_path)
        if not result:
            logger.info(f"File not found: {file_path}")
        return result

    def wait_for_file(
        file_path: str, timeout: int = 60, check_interval: float = 1.0
    ) -> bool:
        """
        指定されたファイルが存在するまで一定時間待機します。

        :param file_path: 存在確認するファイルのパス
        :param timeout: 最大待機時間（秒）
        :param check_interval: チェック間隔（秒）
        :return: タイムアウト前にファイルが見つかった場合はTrue、そうでない場合はFalse
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                logger.info(f"File found: {file_path}")
                return True
            time.sleep(check_interval)

        logger.warning(f"File not found within {timeout} seconds: {file_path}")
        return False

    @staticmethod
    def check_file_with_interval(
        file_path: str, interval: int, max_attempts: int = 5
    ) -> bool:
        """
        指定された間隔でファイルの存在を確認し、指定された回数だけ繰り返します。

        :param file_path: 存在確認するファイルのパス
        :param interval: 確認間隔（秒）
        :param max_attempts: 最大試行回数
        :return: ファイルが見つかった場合はTrue、そうでない場合はFalse
        """
        for attempt in range(max_attempts):
            logger.info(
                f"Attempt {attempt + 1}/{max_attempts}: Waiting {interval} seconds before checking for file: {file_path}"
            )
            time.sleep(interval)

            if os.path.exists(file_path):
                logger.info(f"File found after {attempt + 1} attempts: {file_path}")
                return True

            logger.info(f"File not found on attempt {attempt + 1}: {file_path}")

        logger.warning(f"File not found after {max_attempts} attempts: {file_path}")
        return False

    @staticmethod
    def create_empty_files(folder_path: str, file_names: list):
        """
        指定されたフォルダに空のファイルを作成する
        :param folder_path: ファイルを作成するフォルダのパス
        :param file_names: 作成するファイル名のリスト
        """
        if not os.path.exists(folder_path):
            logger.info(f"Creating folder as it doesn't exist: {folder_path}")
            os.makedirs(folder_path)

        for file_name in file_names:
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, "w") as f:
                    pass
                logger.info(f"Created empty file: {file_path}")
            except Exception as e:
                logger.error(f"Failed to create file {file_path}: {e}")

    @staticmethod
    def read_file(file_path: str, encoding: str = "utf-8") -> str:
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()


class FileReader:
    @staticmethod
    def read_file(file_path: str, encoding: str = "utf-8") -> str:
        """
        指定されたファイルを読み込み、内容を文字列として返します。
        :param file_path: 読み込むファイルのパス
        :return: ファイルの内容を文字列として返す
        """
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()

    @staticmethod
    def read_file_line_list(
        file_path: str, encoding: str = "utf-8"
    ) -> Optional[List[str]]:
        """
        指定されたファイルを読み込み、行のリストとして返します。

        :param file_path: 読み込むファイルのパス
        :param encoding: ファイルのエンコーディング（デフォルトはUTF-8）
        :return: ファイルの内容（行のリスト）。エラーの場合はNone
        """
        logger.info(f"Reading file '{file_path}'")
        try:
            with open(file_path, "r", encoding=encoding) as file:
                lines = file.readlines()
            logger.info(f"Successfully read file '{file_path}'")
            return lines
        except FileNotFoundError:
            logger.error(f"File '{file_path}' not found")
        except IOError as e:
            logger.error(f"Error occurred while reading file '{file_path}': {e}")
        except UnicodeDecodeError:
            logger.error(
                f"Failed to decode file '{file_path}'. Please check the encoding"
            )
        return None


class FileValidator:
    """
    FileValidator クラスは、ファイルの処理可否を判断するメソッドや、
    フォルダ内に特定のファイルが存在するかを確認する機能を提供します。
    """

    @staticmethod
    def is_processable_file(file_name: str, file_path: str = None) -> bool:
        """Determines if a file should be processed based on its MIME type."""
        if file_name.startswith("."):
            return False

        allowed_extensions = [
            ".txt",
            ".md",
            ".markdown",
            ".json",
            ".xml",
            ".js",
            ".html",
            ".mdx",
        ]

        excluded_extensions = [
            ".pyc",
            ".exe",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".svg",
            ".ico",
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".zip",
            ".rar",
            ".7z",
            ".tar",
            ".gz",
            # Add more binary or irrelevant file extensions as needed
        ]

        _, ext = os.path.splitext(file_name.lower())
        if ext in excluded_extensions:
            return False
        if ext in allowed_extensions:
            return True
        return False

    @staticmethod
    def has_required_files(folder_path: str, required_files: List[str]) -> bool:
        """
        指定されたフォルダに必要なファイルがすべて存在するかどうかを確認します。
        :param folder_path: フォルダのパス
        :param required_files: 必要なファイル名のリスト
        :return: すべてのファイルが存在すれば True、それ以外は False を返す
        """
        return all(
            os.path.exists(os.path.join(folder_path, file)) for file in required_files
        )


class FolderFilter:
    """
    FolderFilter クラスは、特定のフォルダプレフィックスに基づいて、
    サブフォルダをフィルタリングする機能を提供します。
    """

    def __init__(self, root_folder: str, folder_prefix: str):
        self.root_folder = root_folder
        self.folder_prefix = folder_prefix

    def get_matching_subfolders(self) -> List[str]:
        """
        プレフィックスに一致するサブフォルダを再帰的に取得します。
        :return: プレフィックスに一致するサブフォルダのリスト
        """
        matching_folders = []
        for root, dirs, _ in os.walk(self.root_folder):
            for dir in dirs:
                if dir.startswith(self.folder_prefix):
                    matching_folders.append(os.path.join(root, dir))
        return matching_folders


class FileProcessor:
    """
    FileProcessor クラスは、ファイルの処理（読み込み、書き込み、更新など）を行い、
    処理結果を集計します。フォルダ内の複数のファイルに対して処理を実行することができます。
    """

    def __init__(self, file_handler: FileHandler, file_validator: FileValidator):
        self.file_handler = file_handler
        self.file_validator = file_validator

    def process_file(
        self, file_path: str, process_function: Callable[[str], str]
    ) -> bool:
        """
        指定されたファイルを読み込み、指定された関数で処理し、変更があれば書き込みます。
        :param file_path: ファイルのパス
        :param process_function: ファイル内容を処理する関数
        :return: ファイルが更新された場合は True、そうでなければ False を返す
        """
        try:
            # Check if the file is processable
            file_name = os.path.basename(file_path)
            if not self.file_validator.is_processable_file(file_name, file_path):
                logger.info(f"Skipped non-processable file: {file_path}")
                return False
            content = self.file_handler.read_file(file_path)
            processed_content = process_function(content)
            if processed_content != content:
                self.file_handler.write_file(file_path, processed_content)
                logger.info(f"File updated: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error occurred while processing file {file_path}: {e}")
            return False

    def process_files_in_folder(
        self,
        root: str,
        files: List[str],
        required_files: List[str],
        process_function: Callable[[str], str],
    ) -> Dict[str, int]:
        """
        指定されたフォルダ内のファイルを処理するロジック。
        必要なファイルがすべて存在するフォルダに対して、ファイルの処理を実行します。
        :param root: フォルダのパス
        :param files: フォルダ内のファイルリスト
        :param required_files: 必要なファイルリスト
        :param process_function: ファイルを処理するための関数
        :return: 処理結果を示すディクショナリ
        """
        processed_files = 0
        updated_files = 0
        error_files = 0

        if self.file_validator.has_required_files(root, required_files):
            for file in files:
                if self.file_validator.is_processable_file(
                    file, os.path.join(root, file)
                ):
                    file_path = os.path.join(root, file)
                    success = self.process_file(file_path, process_function)
                    if success:
                        updated_files += 1
                    processed_files += 1
                else:
                    logger.info(f"Skipped file (not processable): {file}")
        else:
            logger.warning(
                f"Skipped folder (missing required files): {os.path.basename(root)}"
            )

        return {
            "processed_files": processed_files,
            "updated_files": updated_files,
            "error_files": error_files,
        }

    def process_all_matching_files(
        self,
        folder_path: str,
        folder_prefix: str,
        process_function: Callable[[str], str],
        required_files: List[str],
    ) -> Dict[str, int]:
        """
        指定されたフォルダパスの中で、フォルダ名が指定されたプレフィックスで始まる
        すべてのフォルダ内のファイルを処理します。
        :param folder_path: 親フォルダのパス
        :param folder_prefix: 処理対象フォルダのプレフィックス
        :param process_function: ファイルを処理するための関数
        :param required_files: 必要なファイルリスト
        :return: 処理結果を示すディクショナリ
        """
        logger.info(f"Starting search in folder: {folder_path}")
        logger.info(f"Folder prefix: {folder_prefix}")
        logger.info(f"Required files: {', '.join(required_files)}")

        total_processed_files = 0
        total_updated_files = 0
        total_error_files = 0

        for root, dirs, files in os.walk(folder_path, topdown=False):
            folder_name = os.path.basename(root)
            if folder_name.startswith(folder_prefix):
                results = self.process_files_in_folder(
                    root, files, required_files, process_function
                )
                total_processed_files += results["processed_files"]
                total_updated_files += results["updated_files"]
                total_error_files += results["error_files"]
            else:
                logger.info(f"Skipped folder (prefix doesn't match): {folder_name}")

        if total_processed_files == 0:
            logger.warning(
                f"Warning: No processable files found in folders starting with '{folder_prefix}'."
            )

        return {
            "processed_files": total_processed_files,
            "updated_files": total_updated_files,
            "error_files": total_error_files,
        }


class FilePathHandler:
    """
    FilePathHandler クラスは、ファイルパスの結合に関する処理を担当します。
    """

    @staticmethod
    def join_path(folder_path: str, file_name: str) -> str:
        """
        フォルダパスとファイル名を結合してフルパスを生成します。
        :param folder_path: フォルダのパス
        :param file_name: ファイル名
        :return: フルパス
        """
        return os.path.join(folder_path, file_name)

    @staticmethod
    def join_and_normalize_path(path_elements: List[str]) -> str:
        """
        パス要素のリストを受け取り、結合して正規化されたパスを返します。
        :param path_elements: 結合するパス要素のリスト
        :return: 結合された正規化されたパス
        """
        if not path_elements:
            logger.warning("空のパス要素リストが提供されました")
            return ""

        joined_path = os.path.join(*path_elements)
        normalized_path = os.path.normpath(joined_path)
        logger.info(f"パスを結合し正規化しました: {normalized_path}")
        return normalized_path


class FileWriter:
    def __init__(self):
        self.file_handler = FileHandler()

    def replace_file_content(self, file_path: str, new_content: str) -> bool:
        """
        指定されたファイルの内容を完全に新しい内容で置き換えます。

        :param file_path: 処理対象のファイルパス
        :param new_content: ファイルに書き込む新しい内容
        :return: ファイルの更新が成功した場合はTrue、失敗した場合はFalse
        """
        logger.info(f"Replacing content of file '{file_path}'")
        try:
            self.file_handler.write_file(file_path, new_content)
            logger.info(f"Successfully replaced content of file '{file_path}'")
            return True
        except Exception as e:
            logger.error(
                f"Error occurred while replacing content of file '{file_path}': {e}"
            )
            return False
