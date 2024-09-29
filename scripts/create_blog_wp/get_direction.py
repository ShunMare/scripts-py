from initialize import *
from scripts.load_env import *
from scripts.initialize import (
    logger,
    excel_manager,
    edge_handler,
    chatgpt_handler,
    file_handler,
    file_reader,
    web_scraper,
    text_converter,
    value_validator,
    text_splitter,
    array_combiner,
    array_remover,
)


def get_direction(start_row, columns):
    """"""
    heading = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["heading"]
    )
    heading_list = text_splitter.split_string_to_lines(heading)
    heading_list = array_remover.remove_elements(heading_list, DIRECTION_REMOVE_TEXT)
    split_num = len(heading_list) / CREATE_BLOG_WP_EXCEL_GROUP_SIZE
    split_num = round(split_num) + 1
    if split_num < 5:
        split_num = 5
    heading_list = array_combiner.merge_elements(heading_list, split_num,"\n")

    for i, heading in enumerate(heading_list):
        excel_manager.update_cell(
            row=start_row + i,
            column=columns["direction"],
            value=heading,
        )
    excel_manager.save_workbook()


def main():
    excel_manager.set_file_path(CREATE_BLOG_WP_EXCEL_FILE_PATH)
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = ["flag", "heading", "direction"]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=CREATE_BLOG_WP_EXCEL_INDEX_ROW,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if value_validator.has_any_invalid_value_in_array(list(columns.values())):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        worksheet=excel_manager.current_sheet, column=columns["flag"]
    )
    for i in range(flag_end_row):
        start_row = i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, start_row, columns["flag"]
        )
        if value_validator.is_single_value_valid(flag):
            logger.prominent_log(
                f"Google get heading, processing group starting at row {start_row}"
            )
            get_direction(start_row, columns)


if __name__ == "__main__":
    main()
