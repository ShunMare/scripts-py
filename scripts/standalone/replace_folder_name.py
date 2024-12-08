from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    folder_renamer,
)


def main():
    if not excel_manager.set_info(
        STANDALONE_REPLACE_FOLDER_NAME_EXCEL_FILE_FULL_PATH,
        STANDALONE_REPLACE_FOLDER_NAME_EXCEL_SHEET_NAME,
    ):
        return
    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=STANDALONE_REPLACE_FOLDER_NAME_EXCEL_INDEX_ROW,
        search_strings=STANDALONE_REPLACE_FOLDER_NAME_EXCEL_INDEX_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    folder_list = []
    for row, folder_name in excel_manager.cell_handler.iterate_column_values(
        column=columns["folder_name"],
        start_row=STANDALONE_REPLACE_FOLDER_NAME_EXCEL_START_ROW,
    ):
        folder_list.append(
            excel_manager.cell_handler.get_cell_value(row, columns["folder_name"])
        )

    replacement_folder_list = []
    for row, folder_name in excel_manager.cell_handler.iterate_column_values(
        column=columns["new_folder_name"],
        start_row=STANDALONE_REPLACE_FOLDER_NAME_EXCEL_START_ROW,
    ):
        replacement_folder_list.append(
            excel_manager.cell_handler.get_cell_value(row, columns["new_folder_name"])
        )

    for i in range(len(replacement_folder_list)):
        logger.info(folder_list[i])
        logger.info(replacement_folder_list[i])
        folder_renamer.rename_folder_in_directory(
            directory=STANDALONE_REPLACE_FOLDER_NAME_TARGET_FOLDER_FULL_PATH,
            old_name=folder_list[i],
            new_name=replacement_folder_list[i],
        )


if __name__ == "__main__":
    main()
