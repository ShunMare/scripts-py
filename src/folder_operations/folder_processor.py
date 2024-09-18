import os
import shutil
from typing import List, Callable

from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)

class FolderChecker:
    """フォルダの存在確認や必要なフォルダのチェックを行うクラス"""

    @staticmethod
    def check_required_folders(folder_path: str, required_folders: List[str]) -> bool:
        """
        指定されたフォルダ内に必要なフォルダがすべて存在するかを確認します。
        :param folder_path: チェックするフォルダのパス
        :param required_folders: 必要なフォルダのリスト
        :return: すべての必要なフォルダが存在すれば True、そうでなければ False
        """
        result = all(
            os.path.exists(os.path.join(folder_path, folder))
            for folder in required_folders
        )
        if result:
            logger.info(f"All required folders exist in: {folder_path}")
        else:
            logger.warning(f"Some required folders are missing in: {folder_path}")
        return result

    @staticmethod
    def check_folder_exists(folder_path: str) -> bool:
        """
        指定されたフォルダが存在するかを確認します。
        :param folder_path: フォルダのパス
        :return: フォルダが存在すれば True、存在しなければ False
        """
        result = os.path.exists(folder_path)
        if result:
            logger.info(f"Folder exists: {folder_path}")
        else:
            logger.warning(f"Folder does not exist: {folder_path}")
        return result


class FolderMover:
    """フォルダの移動操作を行うクラス"""

    @staticmethod
    def move_folder(source_folder: str, destination_base: str) -> bool:
        """
        フォルダを指定された場所に移動します。
        :param source_folder: 移動元のフォルダのパス
        :param destination_base: 移動先のベースパス
        :return: 移動が成功した場合は True、それ以外は False を返す
        """
        folder_name = os.path.basename(source_folder)
        destination_path = os.path.join(destination_base, folder_name)
        try:
            shutil.move(source_folder, destination_path)
            logger.info(f"Folder moved: {folder_name}")
            return True
        except Exception as e:
            logger.error(f"Error occurred while moving folder {folder_name}: {e}")
            return False


class FolderLister:
    """フォルダの一覧を取得するクラス"""

    @staticmethod
    def list_folders_with_prefix(folder_path: str, folder_prefix: str) -> List[str]:
        """
        指定されたプレフィックスで始まるフォルダの一覧を取得します。
        :param folder_path: 検索するフォルダのパス
        :param folder_prefix: フォルダ名のプレフィックス
        :return: マッチするフォルダ名のリスト
        """
        matching_folders = []
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path) and item.startswith(folder_prefix):
                    matching_folders.append(item)
            logger.info(f"Found {len(matching_folders)} folders matching prefix '{folder_prefix}'")
        except OSError as e:
            logger.error(f"Error occurred while listing folders: {e}")
        return matching_folders

    @staticmethod
    def list_folders_with_prefix_full_path(
        folder_path: str, folder_prefix: str
    ) -> List[str]:
        """
        指定されたプレフィックスで始まるフォルダの一覧をフルパスで取得します。
        :param folder_path: 検索するフォルダのパス
        :param folder_prefix: フォルダ名のプレフィックス
        :return: マッチするフォルダのフルパスのリスト
        """
        matching_folders = []
        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path) and item.startswith(folder_prefix):
                    matching_folders.append(item_path)
            logger.info(f"Found {len(matching_folders)} folders matching prefix '{folder_prefix}' (full path)")
        except OSError as e:
            logger.error(f"Error occurred while listing folders (full path): {e}")
        return matching_folders


class FolderCreator:
    """フォルダを作成するクラス"""

    @staticmethod
    def create_folders(base_folder_path: str, folder_names: List[str]):
        """
        指定されたベースフォルダ内に複数のフォルダを作成します。
        :param base_folder_path: ベースフォルダのパス
        :param folder_names: 作成するフォルダ名のリスト
        """
        if not os.path.exists(base_folder_path):
            logger.info(f"Creating base folder as it doesn't exist: {base_folder_path}")
            os.makedirs(base_folder_path)

        for folder_name in folder_names:
            folder_path = os.path.join(base_folder_path, folder_name)
            try:
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    logger.info(f"Created empty folder: {folder_path}")
                else:
                    logger.info(f"Folder already exists: {folder_path}")
            except OSError as e:
                logger.error(f"Error occurred while creating folder {folder_path}: {e}")

class FolderProcessor:
    """特定のプレフィックスを持つフォルダに対して処理を行うクラス"""

    def __init__(self, folder_path: str, folder_prefix: str):
        """
        :param folder_path: 処理を開始するフォルダのパス
        :param folder_prefix: 処理対象のフォルダプレフィックス
        """
        self.folder_path = folder_path
        self.folder_prefix = folder_prefix
        self.processed_folders = 0

    def process_all_matching_folders(self, process_function: Callable[[str], bool]):
        """
        指定されたプレフィックスにマッチするすべてのフォルダに対して処理を実行します。
        :param process_function: 各フォルダに対して実行する処理関数
        """
        for root, _, _ in os.walk(self.folder_path, topdown=False):
            folder_name = os.path.basename(root)
            if folder_name.startswith(self.folder_prefix):
                process_function(root)
                self.processed_folders += 1
                logger.info(f"Processed folder: {root}")
            else:
                logger.info(f"Skipped folder (prefix doesn't match): {folder_name}")

        if self.processed_folders == 0:
            logger.warning(f"Warning: No folders starting with '{self.folder_prefix}' were found.")

class FolderRemover:
    """フォルダを削除するクラス"""

    @staticmethod
    def remove_folder(folder_path: str) -> bool:
        """
        指定されたフォルダを削除します。
        :param folder_path: 削除するフォルダのパス
        :return: 削除が成功した場合は True、それ以外は False を返す
        """
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"Folder removed: {folder_path}")
                return True
            else:
                logger.warning(f"Folder does not exist, cannot remove: {folder_path}")
                return False
        except Exception as e:
            logger.error(f"Error occurred while removing folder {folder_path}: {e}")
            return False

    @staticmethod
    def remove_folders_with_prefix(base_folder: str, folder_prefix: str) -> int:
        """
        指定されたベースフォルダ内の、特定のプレフィックスを持つフォルダを全て削除します。
        :param base_folder: ベースフォルダのパス
        :param folder_prefix: 削除対象のフォルダプレフィックス
        :return: 削除されたフォルダの数
        """
        removed_count = 0
        try:
            for item in os.listdir(base_folder):
                item_path = os.path.join(base_folder, item)
                if os.path.isdir(item_path) and item.startswith(folder_prefix):
                    if FolderRemover.remove_folder(item_path):
                        removed_count += 1
            logger.info(f"Removed {removed_count} folders with prefix '{folder_prefix}' from {base_folder}")
        except OSError as e:
            logger.error(f"Error occurred while removing folders with prefix '{folder_prefix}': {e}")
        return removed_count