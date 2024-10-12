from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    excel_manager,
    value_validator,
    folder_checker,
    folder_path_handler,
    folder_processor,
    file_validator,
    folder_mover,
)


def move_folder():
    required_files = [
        CREATE_BLOG_MD_TARGET_MDX_FILE_NAME,
        CREATE_BLOG_MD_TARGET_PNG_FILE_NAME,
    ]
    folder_processor.folder_path = CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH
    folder_processor.folder_prefix = CREATE_BLOG_MD_TARGET_TAG_NAME

    def move_folder_if_files_exist(folder_path: str) -> bool:
        """
        フォルダ内に必要なファイルがすべて存在する場合にフォルダを移動する
        :param folder_path: 処理対象のフォルダのパス
        :return: 成功したらTrue、失敗したらFalse
        """
        if file_validator.has_required_files(folder_path, required_files):
            folder_mover.move_folder(
                folder_path, CREATE_BLOG_MD_MOVE_TO_DESTINATION_FOLDER_FULL_PATH
            )

    folder_processor.process_all_matching_folders(move_folder_if_files_exist)


def check_folders():
    if not excel_manager.set_info(
        CREATE_BLOG_MD_EXCEL_FILE_FULL_PATH, CREATE_BLOG_MD_EXCEL_SHEET_NAME
    ):
        return
    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=CREATE_BLOG_MD_EXCEL_INDEX_ROW,
        search_strings=CREATE_BLOG_MD_EXCEL_INDEX_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    for row, folder_name in excel_manager.cell_handler.iterate_column_values(
        column=columns["folder_name"],
        start_row=CREATE_BLOG_MD_EXCEL_START_ROW,
    ):
        if folder_name:
            folder_path = folder_path_handler.join_path(
                CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH, folder_name
            )
            result = folder_checker.check_folder_exists(folder_path)
            if result == False:
                excel_manager.cell_handler.update_cell(row, columns["exist"], result)
            else:
                excel_manager.cell_handler.update_cell(row, columns["exist"], "")
        excel_manager.file_handler.save()


def main():
    move_folder()
    check_folders()


if __name__ == "__main__":
    main()
