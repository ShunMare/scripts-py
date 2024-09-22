import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path, override=True)


def get_env(key, default=None, cast=None):
    value = os.getenv(key, default)
    return cast(value) if cast and value is not None else value


# **Common variables**
EXCEL_FILE_PATH = get_env("EXCEL_FILE_PATH")
WAIT_TIME_AFTER_PROMPT_LONG = get_env("WAIT_TIME_AFTER_PROMPT_LONG", 200, int)
WAIT_TIME_AFTER_PROMPT_MEDIUM = get_env("WAIT_TIME_AFTER_PROMPT_MEDIUM", 100, int)
WAIT_TIME_AFTER_PROMPT_SHORT = get_env("WAIT_TIME_AFTER_PROMPT_SHORT", 5, int)
WAIT_TIME_AFTER_RELOAD = get_env("WAIT_TIME_AFTER_RELOAD", 5, int)
SHORT_WAIT_TIME = get_env("SHORT_WAIT_TIME", 0.5, float)
GET_CONTENT_METHOD = get_env("GET_CONTENT_METHOD")
DOWNLOAD_FOLDER_PATH = get_env("DOWNLOAD_FOLDER_PATH")
EXCEL_GROUP_SIZE = get_env("EXCEL_GROUP_SIZE", 10, int)
EXCEL_INDEX_ROW = get_env("EXCEL_INDEX_ROW", 1, int)
EXCEL_START_ROW = get_env("EXCEL_START_ROW", 2, int)
SCRIPT_BASE_DIR = get_env("SCRIPT_BASE_DIR", "")
SCRIPT_CREATE_BLOG_DETAIL_DIR = get_env("SCRIPT_CREATE_BLOG_DETAIL_DIR", "")
SCRIPT_CREATE_BLOG_INSTA_DIR = get_env("SCRIPT_CREATE_BLOG_INSTA_DIR", "")
EXECUTE_GET_THEMES_GOOGLE = (
    get_env("EXECUTE_GET_THEMES_GOOGLE", "true").lower() == "true"
)
EXECUTE_GET_HEADING_GOOGLE = (
    get_env("EXECUTE_GET_HEADING_GOOGLE", "true").lower() == "true"
)
EXECUTE_GET_EVIDENCE_BING = (
    get_env("EXECUTE_GET_EVIDENCE_BING", "true").lower() == "true"
)
EXECUTE_CREATE_BLOG_CHATGPT = (
    get_env("EXECUTE_CREATE_BLOG_CHATGPT", "true").lower() == "true"
)
EXECUTE_UPLOAD_WP_POST = get_env("EXECUTE_UPLOAD_WP_POST", "true").lower() == "true"

# **ChatGPT related variables**
CHATGPT_MODEL_TYPE = get_env("CHATGPT_MODEL_TYPE", "4o")
IS_IMAGE_GENERATION_ENABLED = (
    get_env("IS_IMAGE_GENERATION_ENABLED", "false").lower() == "true"
)
CHATGPT_URL = get_env("CHATGPT_URL", "https://chatgpt.com/")
PROMPT_TEMPLATE_PATH = get_env("PROMPT_TEMPLATE_PATH")
TITLE_PROMPT = get_env("TITLE_PROMPT")
LONG_DESCRIPTION_PROMPT = get_env("LONG_DESCRIPTION_PROMPT")
SHORT_DESCRIPTION_PROMPT = get_env("SHORT_DESCRIPTION_PROMPT")
KEYWORDS_PROMPT = get_env("KEYWORDS_PROMPT")
PERMALINK_PROMPT = get_env("PERMALINK_PROMPT")
IMAGE_PROMPT = get_env("IMAGE_PROMPT")
CHATGPT_OUTPUT_ELEMENT = get_env("CHATGPT_OUTPUT_ELEMENT", "div")
CHATGPT_OUTPUT_CLASS_LIST = get_env(
    "CHATGPT_OUTPUT_CLASS_LIST", "markdown,prose"
).split(",")
CHATGPT_TMP_FILE_NAME = get_env("CHATGPT_TMP_FILE_NAME", "create_blog_chatgpt")
SOURCE_COPILOT_CONVERSATION = get_env(
    "SOURCE_COPILOT_CONVERSATION", "ソース: Copilot との会話"
)
SUPERSCRIPT_CITATION_PATTERN = get_env(
    "SUPERSCRIPT_CITATION_PATTERN",
    r"\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]+:\s*\[[^\]]+\]\([^\)]+\)",
)
GET_CONTENT_METHOD = os.getenv("GET_CONTENT_METHOD", "clipboard")

# **Bing related variables**
BING_URL = os.getenv("BING_URL")
BING_OUTPUT_ELEMENT = os.getenv("BING_OUTPUT_ELEMENT")
BING_OUTPUT_CLASS_LIST = get_env("BING_OUTPUT_CLASS_LIST").split(",")
BING_TMP_FILE_NAME = os.getenv("BING_TMP_FILE_NAME")

# **WordPress related variables**
WP_URL = get_env("WP_URL")
WP_USERNAME = get_env("WP_USERNAME")
WP_APP_PASSWORD = get_env("WP_APP_PASSWORD")

# **Google related variables**
HEADING_PROMPT = get_env("HEADING_PROMPT")
