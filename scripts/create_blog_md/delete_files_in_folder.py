from initialize import *
from scripts.load_env import *
from scripts.initialize import (
    file_handler,
    file_path_handler,
    folder_processor,
)


def main():
    folder_processor.folder_path = CREATE_BLOG_MD_TARGET_FOLDER_PATH
    folder_processor.folder_prefix = "test-1"
    delete_file_names = ["aa copy 1.txt", "aa copy 2.txt", "aa copy 3.txt"]

    def delete_files_in_folder(folder_path: str) -> bool:
        """
        対象のフォルダ内の複数ファイルを削除する関数
        :param folder_path: 処理対象のフォルダのパス
        :return: 成功したらTrue、失敗したらFalse
        """
        all_success = True

        for delete_file_name in delete_file_names:
            target_file = file_path_handler.join_path(folder_path, delete_file_name)
            if file_path_handler.exists(target_file):
                if not file_handler.delete_file(target_file):
                    all_success = False
            else:
                all_success = False
        return all_success

    folder_processor.process_all_matching_folders(delete_files_in_folder)


if __name__ == "__main__":
    main()
