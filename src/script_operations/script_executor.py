import subprocess
import sys
import os
from src.log_operations.log_handlers import CustomLogger

logger = CustomLogger(__name__)


class ScriptExecutor:
    """
    外部Pythonスクリプトを実行するためのクラス。
    """

    def __init__(self, python_executable=sys.executable):
        """
        ScriptExecutorクラスのコンストラクタ。

        :param python_executable: 使用するPythonインタープリタのパス。デフォルトは現在のPythonインタープリタ。
        """
        self.python_executable = python_executable
        logger.debug(
            f"ScriptExecutor initialized with Python executable: {self.python_executable}"
        )

    def run_script(self, script_path):
        """
        指定されたPythonスクリプトを実行する。

        :param script_path: 実行するスクリプトのパス
        :raises subprocess.CalledProcessError: スクリプトの実行に失敗した場合
        """
        if not os.path.exists(script_path):
            logger.error(f"Script not found: {script_path}")
            raise FileNotFoundError(f"Script not found: {script_path}")

        try:
            script_name = os.path.splitext(os.path.basename(script_path))[0]

            logger.highlighted_log(f"Starting execution of script: {script_name}")
            result = subprocess.run(
                [self.python_executable, script_path],
                check=True,
                stdout=None,
                stderr=None,
            )
            logger.info(f"Script {script_name} executed successfully")
            return result.returncode
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing script: {script_name}")
            raise

    def run_script_with_args(self, script_path, args):
        """
        指定されたPythonスクリプトを引数付きで実行する。

        :param script_path: 実行するスクリプトのパス
        :param args: スクリプトに渡す引数のリスト
        :raises subprocess.CalledProcessError: スクリプトの実行に失敗した場合
        """
        if not os.path.exists(script_path):
            logger.error(f"Script not found: {script_path}")
            raise FileNotFoundError(f"Script not found: {script_path}")

        try:
            logger.info(f"Starting execution of {script_path} with args: {args}")
            result = subprocess.run(
                [self.python_executable, "-u", script_path] + args,
                check=True,
                stdout=None,
                stderr=None,
            )
            logger.info(f"Script {script_path} executed successfully with args: {args}")
            return result.returncode
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing {script_path} with args: {args}")
            raise
