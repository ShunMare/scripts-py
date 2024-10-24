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
    text_replacer,
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

    folder_list = list(
        folder_lister.list_folders_with_prefix(
            folder_path=STANDALONE_REPLACE_FOLDER_NAME_TARGET_FOLDER_FULL_PATH,
            folder_prefix="",
        )
    )

    replacement_folder_list = folder_list.copy()
    for i in range(len(replacement_folder_list)):
        folder_name = replacement_folder_list[i]
        new_folder_name = STANDALONE_REPLACE_FOLDER_NAME_TARGET_TAG_NAME + "-" + folder_name
        replacement_folder_list[i] = new_folder_name

    excel_manager.cell_handler.insert_array_column_wise(
        start_row=STANDALONE_REPLACE_FOLDER_NAME_EXCEL_START_ROW,
        start_column=columns["folder_name"],
        data=folder_list,
    )
    excel_manager.cell_handler.insert_array_column_wise(
        start_row=STANDALONE_REPLACE_FOLDER_NAME_EXCEL_START_ROW,
        start_column=columns["new_folder_name"],
        data=replacement_folder_list,
    )
    excel_manager.file_handler.save()

    # for i in range(len(replacement_folder_list)):
    #     folder_renamer.rename_folder_in_directory(
    #         directory=STANDALONE_REPLACE_FOLDER_NAME_TARGET_FOLDER_FULL_PATH,
    #         old_name=folder_list[i],
    #         new_name=replacement_folder_list[i],
    #     )


if __name__ == "__main__":
    main()
