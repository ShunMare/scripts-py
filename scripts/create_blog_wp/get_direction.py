import math
from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    text_splitter,
    array_combiner,
    array_remover,
)


def get_direction(start_row, columns):
    heading = excel_manager.cell_handler.get_cell_value(start_row, columns["heading"])
    heading_list = text_splitter.split_string_to_lines(heading)
    heading_list = array_remover.remove_elements(
        heading_list, CREATE_BLOG_WP_GET_DIRECTION_REMOVE_TEXT
    )
    split_num = len(heading_list) / CREATE_BLOG_WP_EXCEL_GROUP_SIZE
    split_num = math.ceil(split_num)
    if split_num < CREATE_BLOG_WP_GET_DIRECTION_SPLIT_NUM:
        split_num = CREATE_BLOG_WP_GET_DIRECTION_SPLIT_NUM
    heading_list = array_combiner.merge_elements(heading_list, split_num, "\n")

    for i, heading in enumerate(heading_list):
        excel_manager.cell_handler.update_cell(
            row=start_row + i,
            column=columns["direction"],
            value=heading,
        )
    excel_manager.file_handler.save()


def main():
    if not excel_manager.set_info(
        CREATE_BLOG_WP_EXCEL_FILE_FULL_PATH, CREATE_BLOG_WP_EXCEL_SHEET_NAME
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=CREATE_BLOG_WP_EXCEL_INDEX_ROW,
        search_strings=CREATE_BLOG_WP_EXCEL_INDEX_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        column=columns["flag"]
    )
    for i in range(flag_end_row):
        start_row = i * CREATE_BLOG_WP_EXCEL_GROUP_SIZE + CREATE_BLOG_WP_EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
        if value_validator.is_valid(flag):
            logger.prominent_log(
                f"Google get heading, processing group starting at row {start_row}"
            )
            get_direction(start_row, columns)


if __name__ == "__main__":
    main()
