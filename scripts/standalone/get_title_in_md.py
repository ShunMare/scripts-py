from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    file_reader,
    file_path_handler,
    folder_path_handler,
    folder_lister,
    text_finder,
)

TARGET_TEXT = "title:"
REPLACE_TARGET_TEXT = "【" + CREATE_BLOG_MD_PNG_TAG_NAME + "】"
REPLACEMENT_TEXT = ""
SPLIT_TEXT = " - "

MY_SCRIPTS_EXCEL_INDEX_ROW = 1
MY_SCRIPTS_EXCEL_START_ROW = 2
MY_SCRIPTS_TARGET_FOLDER_PATH = "C:\\Users\\okubo\\OneDrive\\ドキュメント\\001_repositories\\nexunity\\src\\content\\posts"
MY_SCRIPTS_TARGET_MD_FILE_NAME = "index.md*"


def get_title_in_md(columns):
    for row, folder_name in excel_manager.cell_handler.iterate_column_values(
        column=columns["folder_name"],
        start_row=MY_SCRIPTS_EXCEL_START_ROW,
    ):
        if folder_name is None:
            continue

        folder_path = folder_path_handler.join_path(
            MY_SCRIPTS_TARGET_FOLDER_PATH, folder_name
        )
        index_files = file_path_handler.find_files_with_wildcard(
            folder_path, MY_SCRIPTS_TARGET_MD_FILE_NAME
        )

        if index_files:
            file_full_path = index_files[0]
            lines = file_reader.read_file_line_list(file_full_path)
            text = text_finder.find_line_starting_with(lines, TARGET_TEXT)
            excel_manager.cell_handler.update_cell(row, columns["title_full"], text)


SEARCH_STRINGS = ["folder_name", "title_full"]


def main():
    if not excel_manager.set_info(
        STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_FULL_PATH,
        STANDALONE_GET_TITLE_IN_MD_EXCEL_SHEET_NAME,
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=1,
        search_strings=SEARCH_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    folder_list = list(
        folder_lister.list_folders_with_prefix(
            folder_path=MY_SCRIPTS_TARGET_FOLDER_PATH, folder_prefix=""
        )
    )

    excel_manager.cell_handler.insert_array_column_wise(
        start_row=MY_SCRIPTS_EXCEL_START_ROW,
        start_column=columns["folder_name"],
        data=folder_list,
    )
    get_title_in_md(columns)
    excel_manager.file_handler.save()


if __name__ == "__main__":
    main()
