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


def get_title_in_md(columns):
    for row, folder_name in excel_manager.cell_handler.iterate_column_values(
        column=columns["folder_name"],
        start_row=STANDALONE_GET_TITLE_IN_MD_EXCEL_START_ROW,
    ):
        if folder_name is None:
            continue

        folder_path = folder_path_handler.join_path(
            STANDALONE_GET_TITLE_IN_MD_TARGET_DIR_FULL_PATH, folder_name
        )
        index_files = file_path_handler.find_files_with_wildcard(
            folder_path, STANDALONE_GET_TITLE_IN_MD_TARGET_FILE_NAME
        )

        if index_files:
            file_full_path = index_files[0]
            lines = file_reader.read_file_line_list(file_full_path)
            text = text_finder.find_line_starting_with(
                lines, STANDALONE_GET_TITLE_IN_MD_TARGET_TEXT
            )
            excel_manager.cell_handler.update_cell(row, columns["title_full"], text)


def main():
    if not excel_manager.set_info(
        STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_FULL_PATH,
        STANDALONE_GET_TITLE_IN_MD_EXCEL_SHEET_NAME,
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=STANDALONE_GET_TITLE_IN_MD_EXCEL_INDEX_ROW,
        search_strings=STANDALONE_GET_TITLE_IN_MD_EXCEL_INDEX_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    folder_list = list(
        folder_lister.list_folders_with_prefix(
            folder_path=STANDALONE_GET_TITLE_IN_MD_TARGET_DIR_FULL_PATH,
            folder_prefix="",
        )
    )

    excel_manager.cell_handler.insert_array_column_wise(
        start_row=STANDALONE_GET_TITLE_IN_MD_EXCEL_START_ROW,
        start_column=columns["folder_name"],
        data=folder_list,
    )
    get_title_in_md(columns)
    excel_manager.file_handler.save()


if __name__ == "__main__":
    main()
