from openpyxl.utils.exceptions import IllegalCharacterError
import pandas as pd
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class ExcelCellHandler:
    @staticmethod
    def update_cell(worksheet, row, column, value):
        """
        指定されたセルに値を更新します。
        :param worksheet: 対象のワークシート
        :param row: 行番号
        :param column: 列番号
        :param value: 書き込む値
        :return: True: 成功、False: エラー発生
        """
        try:
            worksheet.cell(row=row, column=column, value=value)
            logger.info(f"Successfully updated cell at row {row}, column {column}")
            return True
        except IllegalCharacterError:
            logger.error(
                "IllegalCharacterError: Unable to save content due to invalid characters."
            )
            return False
        except Exception as e:
            logger.error(f"An error occurred while updating the cell: {str(e)}")
            return False

    @staticmethod
    def is_cell_empty_or_match(worksheet, row, column, expected_value=None):
        """
        指定されたセルが空か、指定された値と一致するかを確認します。
        :param worksheet: 対象のワークシート
        :param row: 行番号
        :param column: 列番号
        :param expected_value: チェックしたい期待値（任意）
        :return: True: 空または一致、False: 不一致
        """
        cell_value = worksheet.cell(row=row, column=column).value
        if pd.isna(cell_value) or cell_value is None or cell_value == "":
            logger.info(f"Cell at row {row}, column {column} is empty")
            return True
        if expected_value is not None:
            result = str(cell_value) == str(expected_value)
            logger.info(
                f"Cell at row {row}, column {column} {'matches' if result else 'does not match'} expected value"
            )
            return result
        logger.info(f"Cell at row {row}, column {column} is not empty")
        return False

    @staticmethod
    def iterate_column_values(worksheet, column: int, start_row: int = 1):
        """
        指定された列の指定された行から最終行までを繰り返し、行番号と値を返すジェネレータ。
        :param worksheet: 対象のワークシート
        :param column: 列番号 (例: 3はC列)
        :param start_row: 開始行 (デフォルトは1行目)
        :yield: (行番号, セルの値) のタプル
        """
        logger.info(f"Iterating column {column} values from row {start_row}")
        for row in range(start_row, worksheet.max_row + 1):
            value = worksheet.cell(row=row, column=column).value
            logger.debug(f"Row {row}, Column {column}: {value}")
            yield row, value

    @staticmethod
    def get_column_values_to_last_row(worksheet, column: int, start_row: int = 1):
        """
        指定された列の指定された行から最終行までのセルの値を配列で返す。
        :param worksheet: 対象のワークシート
        :param column: 列番号 (例: 3はC列)
        :param start_row: 開始行 (デフォルトは1行目)
        :return: 指定された列の開始行から最終行までの値を含むリスト
        """
        values = []
        for row in range(start_row, worksheet.max_row + 1):
            value = worksheet.cell(row=row, column=column).value
            values.append(value)
        logger.info(
            f"Retrieved {len(values)} values from column {column}, starting at row {start_row}"
        )
        return values

    @staticmethod
    def get_cell_value(worksheet, row: int, column: int):
        """
        指定されたセルの値を取得します。
        :param worksheet: 対象のワークシート
        :param row: 行番号
        :param column: 列番号
        :return: セルの値
        """
        try:
            value = worksheet.cell(row=row, column=column).value
            logger.info(f"Retrieved value from row {row}, column {column}: {value}")
            return value
        except Exception as e:
            logger.error(
                f"An error occurred while getting the cell value at row {row}, column {column}: {str(e)}"
            )
            return None

    @staticmethod
    def get_cell_value_by_column_letter(worksheet, row: int, column_letter: str):
        """
        列文字（A, B, C...）を使用して指定されたセルの値を取得します。
        :param worksheet: 対象のワークシート
        :param row: 行番号
        :param column_letter: 列文字（例: 'A', 'B', 'C'...）
        :return: セルの値
        """
        try:
            value = worksheet[f"{column_letter}{row}"].value
            logger.info(
                f"Retrieved value from row {row}, column {column_letter}: {value}"
            )
            return value
        except Exception as e:
            logger.error(
                f"An error occurred while getting the cell value at row {row}, column {column_letter}: {str(e)}"
            )
            return None

    @staticmethod
    def get_range_values(worksheet, start_row: int, column: int, num_rows: int):
        """
        指定された行の指定された列から、指定された行数分のデータを配列で返します。
        :param worksheet: 対象のワークシート
        :param start_row: 開始行
        :param column: 列番号
        :param num_rows: 取得する行数
        :return: セルの値のリスト
        """
        values = []
        for row in range(start_row, start_row + num_rows):
            value = worksheet.cell(row=row, column=column).value
            values.append(value)
        logger.info(
            f"Retrieved {len(values)} values from column {column}, starting at row {start_row}, for {num_rows} rows"
        )
        return values

    @staticmethod
    def get_last_row_of_column(worksheet, column: int) -> int:
        """
        指定された列の最終行（データが存在する最後の行）の行番号を返します。
        :param worksheet: 対象のワークシート
        :param column: 列番号 (例: 3はC列)
        :return: 最終行の行番号
        """
        last_row = worksheet.max_row
        while last_row > 0:
            if worksheet.cell(row=last_row, column=column).value is not None:
                logger.info(f"Last row with data in column {column}: {last_row}")
                return last_row
            last_row -= 1
        logger.info(f"No data found in column {column}")
        return 0
