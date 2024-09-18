import subprocess
import sys
import os
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
sys.path.append(project_root)

from src.log_operations.log_handlers import setup_logger

load_dotenv(dotenv_path, override=True)

logger = setup_logger(__name__)


def run_script(script_path):
    try:
        logger.info(f"Starting execution of {script_path}")
        result = subprocess.run(
            [sys.executable, script_path], check=True, capture_output=True, text=True
        )
        logger.info(f"Script {script_path} executed successfully")
        logger.info(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing {script_path}")
        logger.error(f"Error message: {e.stderr}")
        raise


def main():
    GET_EVIDENCE_NAME = "get_evidence_bing.py"
    CREATE_BLOG_NAME = "create_blog_chatgpt.py"
    base_dir = os.getenv("SCRIPT_BASE_DIR", "")

    get_evidence_full_path = os.path.join(base_dir, GET_EVIDENCE_NAME)
    create_blog_full_path = os.path.join(base_dir, CREATE_BLOG_NAME)

    try:
        run_script(get_evidence_full_path)
        run_script(create_blog_full_path)
        logger.info(
            "Bing evidence retrieval and ChatGPT blog creation completed successfully"
        )
    except Exception as e:
        logger.error(
            f"An error occurred during the blog content generation process: {str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
