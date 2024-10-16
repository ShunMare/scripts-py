from src.log_operations.log_handlers import CustomLogger


class ExcelSheetHandler:
    def __init__(self):
        """
        ExcelSheetHandlerの初期化
        """
        self.logger = CustomLogger(__name__)
        self.workbook = None

    def set_workbook(self, workbook):
        """
        ワークブックを設定します。
        :param workbook: 対象のワークブック
        """
        self.workbook = workbook
        self.logger.debug("Workbook has been set successfully.")

    def get_sheet_names(self):
        sheet_names = self.workbook.sheetnames
        self.logger.debug(f"Retrieved sheet names: {sheet_names}")
        return sheet_names

    def set_active_sheet(self, sheet_name):
        if sheet_name in self.workbook.sheetnames:
            active_sheet = self.workbook[sheet_name]
            self.logger.debug(f"Set active sheet to '{sheet_name}'")
            return active_sheet
        else:
            self.logger.debug(f"Sheet '{sheet_name}' not found in the workbook.")
            return None
