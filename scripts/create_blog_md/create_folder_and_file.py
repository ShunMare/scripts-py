from initialize import *
from scripts.load_env import *
from scripts.initialize import (
    excel_manager,
    value_validator,
    file_handler,
    folder_creator,
    folder_path_handler,
)


def main():
    create_file_list = [CREATE_BLOG_MD_TARGET_FILE_NAME]

    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = ["folder_name"]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=CREATE_BLOG_MD_EXCEL_INDEX_ROW,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if value_validator.has_any_invalid_value_in_array(list(columns.values())):
        return

    folder_names = excel_manager.cell_handler.get_column_values_to_last_row(
        worksheet=excel_manager.current_sheet,
        column=columns["folder_name"],
        start_row=CREATE_BLOG_MD_EXCEL_START_ROW,
    )
    folder_names = excel_manager.remove_nan_from_list(folder_names)
    folder_names = [str(name) for item in folder_names for name in (item if isinstance(item, list) else [item])]
    folder_creator.create_folders(CREATE_BLOG_MD_TARGET_FOLDER_PATH, folder_names)
    for folder_name in folder_names:
        folder_path = folder_path_handler.join_path(
            CREATE_BLOG_MD_TARGET_FOLDER_PATH, folder_name
        )
        file_handler.create_empty_files(folder_path, create_file_list)

    excel_manager.save_workbook()


if __name__ == "__main__":
    main()
