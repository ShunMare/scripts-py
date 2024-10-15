from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    file_handler,
    folder_creator,
    folder_path_handler,
)


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

    folder_names = excel_manager.cell_handler.get_column_values_to_last_row(
        column=columns["folder_name"],
        start_row=CREATE_BLOG_MD_EXCEL_START_ROW,
    )
    logger.info("remove nan from list")
    folder_names = excel_manager.data_processor.remove_nan_from_list(folder_names)
    folder_names = [
        str(name)
        for item in folder_names
        for name in (item if isinstance(item, list) else [item])
    ]

    logger.info("create folders")
    folder_creator.create_folders(CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH, folder_names)
    for folder_name in folder_names:
        folder_path = folder_path_handler.join_and_normalize_path(
            CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH, folder_name
        )
        file_handler.create_empty_files(
            folder_path, [CREATE_BLOG_MD_TARGET_MDX_FILE_NAME]
        )

    excel_manager.file_handler.save()


if __name__ == "__main__":
    main()
