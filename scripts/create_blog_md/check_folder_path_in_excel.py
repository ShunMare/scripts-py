from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    excel_manager,
    value_validator,
    folder_checker,
    folder_path_handler,
)


SEARCH_STRINGS = ["exist", "folder_name"]


def main():
    if not excel_manager.set_info(
        CREATE_BLOG_MD_EXCEL_FILE_FULL_PATH, CREATE_BLOG_MD_EXCEL_SHEET_NAME
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=CREATE_BLOG_MD_EXCEL_INDEX_ROW,
        search_strings=SEARCH_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    for row, folder_name in excel_manager.cell_handler.iterate_column_values(
        column=columns["folder_name"],
        start_row=CREATE_BLOG_MD_EXCEL_START_ROW,
    ):
        if folder_name:
            folder_path = folder_path_handler.join_path(
                CREATE_BLOG_MD_EXCEL_FILE_FULL_PATH, folder_name
            )
            result = folder_checker.check_folder_exists(folder_path)
            if result == False:
                excel_manager.cell_handler.update_cell(row, columns["exist"], result)
            else:
                excel_manager.cell_handler.update_cell(row, columns["exist"], "")
    excel_manager.file_handler.save()


if __name__ == "__main__":
    main()
