import os
from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class GasManager:
    """
    GasManager クラスは Google Apps Script の機能を模倣し、
    スプレッドシートの操作や一般的なユーティリティ機能を提供します。
    """

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self):
        self.credentials_path = None
        self.token_path = None
        self.service = None

    def set_auth_paths(
        self, credentials_path: Optional[str] = None, token_path: Optional[str] = None
    ):
        """
        認証情報のパスを設定します。
        :param credentials_path: credentials.json のパス
        :param token_path: token.json のパス
        """
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_CREDENTIALS_PATH", "credentials.json"
        )
        self.token_path = token_path or os.getenv("GOOGLE_TOKEN_PATH", "token.json")

    def generate_new_token(self):
        """
        新しいトークンを生成し、token.json ファイルに保存します。
        """
        if not self.credentials_path:
            raise ValueError(
                "credentials_path が設定されていません。set_auth_paths() を呼び出してください。"
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_path, self.SCOPES
        )
        creds = flow.run_local_server(port=0)

        if not self.token_path:
            self.token_path = "token.json"

        with open(self.token_path, "w") as token:
            token.write(creds.to_json())

        logger.info(f"新しいトークンが生成され、{self.token_path} に保存されました。")

    def get_google_sheets_service(self):
        """Google Sheets API サービスを取得します。"""
        if self.service:
            return self.service

        if not self.credentials_path or not self.token_path:
            raise ValueError(
                "認証情報のパスが設定されていません。set_auth_paths() を呼び出してください。"
            )

        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}"
                    )

                self.generate_new_token()
                creds = Credentials.from_authorized_user_file(
                    self.token_path, self.SCOPES
                )

        self.service = build("sheets", "v4", credentials=creds)
        return self.service

    def get_last_row(self, sheet_id: str, range_name: str) -> int:
        """
        指定されたシートの最終行を取得します。
        :param sheet_id: スプレッドシートの ID
        :param range_name: 範囲名（例：'Sheet1'）
        :return: 最終行の番号
        """
        service = self.get_google_sheets_service()
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        last_row = len(values)
        logger.info(f"Last row of sheet '{range_name}': {last_row}")
        return last_row

    def get_last_column(self, sheet_id: str, range_name: str) -> int:
        """
        指定されたシートの最終列を取得します。
        :param sheet_id: スプレッドシートの ID
        :param range_name: 範囲名（例：'Sheet1'）
        :return: 最終列の番号
        """
        service = self.get_google_sheets_service()
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        last_column = len(values[0]) if values else 0
        logger.info(f"Last column of sheet '{range_name}': {last_column}")
        return last_column

    def get_values(self, sheet_id: str, range_name: str) -> List[List[Any]]:
        """
        指定された範囲の値を2次元配列として取得します。
        :param sheet_id: スプレッドシートの ID
        :param range_name: 範囲名（例：'Sheet1!A1:B10'）
        :return: 2次元配列の値
        """
        service = self.get_google_sheets_service()
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        logger.info(
            f"Retrieved {len(values)}x{len(values[0]) if values else 0} values from range '{range_name}'"
        )
        return values

    def set_values(self, sheet_id: str, range_name: str, values: List[List[Any]]):
        """
        指定された範囲に値を設定します。
        :param sheet_id: スプレッドシートの ID
        :param range_name: 範囲名（例：'Sheet1!A1:B10'）
        :param values: 設定する2次元配列の値
        """
        service = self.get_google_sheets_service()
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        logger.info(
            f"Updated {result.get('updatedCells')} cells in range '{range_name}'"
        )

    def update_gas_content(
        self, spreadsheet_id: str, sheet_name: str, post_content: str
    ):
        """
        GASスプレッドシートの内容を更新します。
        :param spreadsheet_id: スプレッドシートのID
        :param sheet_name: シート名
        :param post_content: 投稿内容
        """
        try:
            service = self.get_google_sheets_service()
            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A:A")
                .execute()
            )
            last_row = len(result.get("values", [])) + 1

            result = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!B2:B")
                .execute()
            )
            existing_content = result.get("values", [])

            if any(row[0] == post_content for row in existing_content):
                logger.info("Content already exists. Skipping update.")
                return

            new_row_content = [[last_row, post_content, 0]]
            service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f"{sheet_name}!A{last_row}",
                valueInputOption="USER_ENTERED",
                body={"values": new_row_content},
            ).execute()

            logger.info(f"Successfully updated GAS spreadsheet with new content")
        except Exception as e:
            logger.error(f"Error updating GAS spreadsheet: {str(e)}")
            raise
