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
        excel_manager.current_sheet,
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
            excel_manager.update_cell(row, columns["title_full"], text)


def main():
    excel_manager.set_file_path(STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_FULL_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(STANDALONE_GET_TITLE_IN_MD_EXCEL_SHEET_NAME)
    search_strings = ["folder_name", "title_full"]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=MY_SCRIPTS_EXCEL_INDEX_ROW,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if value_validator.has_any_invalid_value_in_array(list(columns.values())):
        return

    folder_list = list(
        folder_lister.list_folders_with_prefix(
            folder_path=MY_SCRIPTS_TARGET_FOLDER_PATH, folder_prefix=""
        )
    )

    excel_manager.cell_handler.insert_array_column_wise(
        worksheet=excel_manager.current_sheet,
        start_row=MY_SCRIPTS_EXCEL_START_ROW,
        start_column=columns["folder_name"],
        data=folder_list,
    )
    get_title_in_md(columns)
    excel_manager.save_workbook()


if __name__ == "__main__":
    main()
