from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    text_finder,
)


def main():
    if not excel_manager.set_info(
        STACKOVERFLOW_GET_SLUG_EXCEL_FILE_FULL_PATH,
        STACKOVERFLOW_GET_SLUG_EXCEL_SHEET_NAME,
    ):
        return
    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=STACKOVERFLOW_GET_SLUG_EXCEL_INDEX_ROW,
        search_strings=STACKOVERFLOW_GET_SLUG_EXCEL_INDEX_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    for row, link in excel_manager.cell_handler.iterate_column_values(
        column=columns["link"],
        start_row=STACKOVERFLOW_GET_SLUG_EXCEL_START_ROW,
    ):
        pattern = r"/questions/\d+/([^/?]+)"
        slug = text_finder.extract_pattern(link, pattern)
        excel_manager.cell_handler.update_cell(row, columns["slug"], slug)

    excel_manager.file_handler.save()


if __name__ == "__main__":
    main()
