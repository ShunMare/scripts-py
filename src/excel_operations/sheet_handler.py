from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class ExcelSheetHandler:
    @staticmethod
    def get_sheet_names(workbook):
        sheet_names = workbook.sheetnames
        logger.info(f"Retrieved sheet names: {sheet_names}")
        return sheet_names

    @staticmethod
    def set_active_sheet(workbook, sheet_name):
        if sheet_name in workbook.sheetnames:
            active_sheet = workbook[sheet_name]
            logger.info(f"Set active sheet to '{sheet_name}'")
            return active_sheet
        else:
            logger.warning(f"Sheet '{sheet_name}' not found in the workbook.")
            return None
