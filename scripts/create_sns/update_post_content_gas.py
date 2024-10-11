from initialize import *
from scripts.load_env import *
from scripts.constants import *
from scripts.initialize import (
    logger,
    excel_manager,
    value_validator,
    file_validator,
    gas_manager,
)


def update_gas_content(start_row, columns):
    if not file_validator.check_token_file(CREATE_SNS_TOKEN_FILE_FULL_PATH):
        gas_manager.set_auth_paths(
            CREATE_SNS_CREDENTIALS_FILE_FULL_PATH, CREATE_SNS_TOKEN_FILE_FULL_PATH
        )
        gas_manager.generate_new_token()

    gas_manager.set_auth_paths(
        CREATE_SNS_CREDENTIALS_FILE_FULL_PATH, CREATE_SNS_TOKEN_FILE_FULL_PATH
    )

    post_content = excel_manager.cell_handler.get_cell_value(
        start_row, columns["post_content"]
    )
    if not post_content:
        logger.warning(f"Empty post_content found at row {start_row}")
        return

    try:
        logger.debug(f"Attempting to update GAS with content: {post_content[:100]}...")
        gas_manager.update_gas_content(
            CREATE_SNS_SPREADSHEET_ID, CREATE_SNS_SPREADSHEET_SHEET_NAME, post_content
        )
        logger.info(
            f"Successfully updated GAS spreadsheet with content from row {start_row}"
        )
    except Exception as e:
        logger.error(f"Error updating GAS spreadsheet: {str(e)}", exc_info=True)
        if "invalid_grant" in str(e):
            logger.info("Token might be invalid. Attempting to regenerate...")
            try:
                gas_manager.update_gas_content(
                    CREATE_SNS_SPREADSHEET_ID,
                    CREATE_SNS_SPREADSHEET_SHEET_NAME,
                    post_content,
                )
                logger.info(
                    f"Successfully updated GAS spreadsheet after token regeneration"
                )
            except Exception as e2:
                logger.error(
                    f"Error updating GAS spreadsheet after token regeneration: {str(e2)}",
                    exc_info=True,
                )


SEARCH_STRINGS = ["flag", "slug", "post_content"]


def main():
    if not excel_manager.set_info(
        CREATE_SNS_EXCEL_FILE_FULL_PATH, CREATE_SNS_EXCEL_SHEET_NAME
    ):
        return

    columns = excel_manager.search_handler.find_and_map_column_indices(
        index=CREATE_SNS_EXCEL_INDEX_ROW,
        search_strings=SEARCH_STRINGS,
    )
    if value_validator.any_invalid(columns):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        column=columns["flag"]
    )
    for start_row in range(CREATE_SNS_EXCEL_START_ROW, flag_end_row + 1):
        flag = excel_manager.cell_handler.get_cell_value(start_row, columns["flag"])
        if value_validator.is_valid(flag):
            logger.prominent_log(f"Updating GAS content, processing row {start_row}")
            update_gas_content(start_row, columns)


if __name__ == "__main__":
    main()
