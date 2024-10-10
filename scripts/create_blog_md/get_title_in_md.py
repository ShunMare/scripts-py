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

TARGET_TEXT = "title:"
REPLACE_TARGET_TEXT = "【" + CREATE_BLOG_MD_PNG_TAG_NAME + "】"
REPLACEMENT_TEXT = ""
SPLIT_TEXT = " - "


def get_title_in_md(columns):
    for row, folder_name in excel_manager.cell_handler.iterate_column_values(
        excel_manager.current_sheet,
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
            text = text_finder.find_line_starting_with(lines, TARGET_TEXT)
            text = text_replacer.replace(text, REPLACE_TARGET_TEXT, REPLACEMENT_TEXT)
            excel_manager.update_cell(row, columns["title_full"], text)


def separate_title_in_md(columns):
    for row, title_full in excel_manager.cell_handler.iterate_column_values(
        excel_manager.current_sheet,
        column=columns["title_full"],
        start_row=CREATE_BLOG_MD_EXCEL_START_ROW,
    ):
        texts = text_handler.split_string(title_full, SPLIT_TEXT)
        if len(texts) >= 2:
            excel_manager.update_cell(row, columns["title"], texts[0])
            excel_manager.update_cell(row, columns["subtitle"], texts[1])
        elif len(texts) == 1:
            excel_manager.update_cell(row, columns["title"], texts[0])
            excel_manager.update_cell(row, columns["subtitle"], "")


def main():
    excel_manager.set_file_path(CREATE_BLOG_MD_EXCEL_FILE_FULL_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(CREATE_BLOG_MD_EXCEL_SHEET_NAME)
    search_strings = ["folder_name", "title_full", "title", "subtitle"]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=CREATE_BLOG_MD_EXCEL_INDEX_ROW,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if value_validator.has_any_invalid_value_in_array(list(columns.values())):
        return

    get_title_in_md(columns)
    separate_title_in_md(columns)
    excel_manager.save_workbook()


if __name__ == "__main__":
    main()
