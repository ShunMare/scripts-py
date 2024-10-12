from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    file_handler,
    file_reader,
    file_path_handler,
    text_handler,
    text_finder,
    text_replacer,
)


def get_title_in_md(columns):
    for row, folder_name in excel_manager.cell_handler.iterate_column_values(
        column=columns["folder_name"],
        start_row=CREATE_BLOG_MD_EXCEL_START_ROW,
    ):
        if folder_name is None:
            continue

        path_elements = [
            CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH,
            folder_name,
            CREATE_BLOG_MD_TARGET_MDX_FILE_NAME,
        ]
        file_full_path = file_path_handler.join_and_normalize_path(path_elements)

        if file_handler.exists(file_full_path):
            lines = file_reader.read_file_line_list(file_full_path)
            text = text_finder.find_line_starting_with(
                lines, CREATE_BLOG_MD_GET_TITLE_IN_MD_TARGET_TEXT
            )
            text = text_replacer.replace(
                text,
                CREATE_BLOG_MD_GET_TITLE_IN_MD_REPLACE_TARGET_TEXT,
                CREATE_BLOG_MD_GET_TITLE_IN_MD_REPLACEMENT_TEXT,
            )
            excel_manager.cell_handler.update_cell(row, columns["title_full"], text)


def separate_title_in_md(columns):
    for row, title_full in excel_manager.cell_handler.iterate_column_values(
        column=columns["title_full"],
        start_row=CREATE_BLOG_MD_EXCEL_START_ROW,
    ):
        texts = text_handler.split_string(
            title_full, CREATE_BLOG_MD_GET_TITLE_IN_MD_SPLIT_TEXT
        )
        if len(texts) >= 2:
            excel_manager.cell_handler.update_cell(row, columns["title"], texts[0])
            excel_manager.cell_handler.update_cell(row, columns["subtitle"], texts[1])
        elif len(texts) == 1:
            excel_manager.cell_handler.update_cell(row, columns["title"], texts[0])
            excel_manager.cell_handler.update_cell(row, columns["subtitle"], "")


def main():
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

    get_title_in_md(columns)
    separate_title_in_md(columns)
    excel_manager.file_handler.save()


if __name__ == "__main__":
    main()
