import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path, override=True)


def get_env(key, default=None, cast=None):
    value = os.getenv(key, default)
    return cast(value) if cast and value is not None else value


# ===========================
# Common variables
# ===========================
# # time
WAIT_TIME_AFTER_PROMPT_LONG = get_env("WAIT_TIME_AFTER_PROMPT_LONG", 150, int)
WAIT_TIME_AFTER_PROMPT_MEDIUM = get_env("WAIT_TIME_AFTER_PROMPT_MEDIUM", 30, int)
WAIT_TIME_AFTER_PROMPT_SHORT = get_env("WAIT_TIME_AFTER_PROMPT_SHORT", 5, int)
WAIT_TIME_AFTER_RELOAD = get_env("WAIT_TIME_AFTER_RELOAD", 10, int)
WAIT_TIME_AFTER_SWITCH = get_env("WAIT_TIME_AFTER_SWITCH", 5, int)
KEYBOARD_ACTION_SHORT_DELAY = get_env("KEYBOARD_ACTION_SHORT_DELAY", 0.5, float)
# path
DOWNLOAD_FOLDER_DIR_FULL_PATH = get_env("DOWNLOAD_FOLDER_DIR_FULL_PATH")
PROJECT_DIR_FULL_PATH = get_env("PROJECT_DIR_FULL_PATH")
DATA_DIR_NAME = get_env("DATA_DIR_NAME")
SCRIPTS_DIR_NAME = get_env("SCRIPTS_DIR_NAME")
LOGS_DIR_NAME = get_env("LOGS_DIR_NAME")
SRC_DIR_NAME = get_env("SRC_DIR_NAME")
STATISTICS_DIR_NAME = get_env("STATISTICS_DIR_NAME")
# folder name
CREATE_BLOG_WP_DIR_NAME = get_env("CREATE_BLOG_WP_DIR_NAME")
CREATE_BLOG_MD_DIR_NAME = get_env("CREATE_BLOG_MD_DIR_NAME")
CREATE_SNS_DIR_NAME = get_env("CREATE_SNS_DIR_NAME")
STANDALONE_DIR_NAME = get_env("STANDALONE_DIR_NAME")
STACKOVERFLOW_DIR_NAME = get_env("STACKOVERFLOW_DIR_NAME")
# tab index
TAB_COUNT_4O = get_env("TAB_COUNT_4O", 6, int)
TAB_COUNT_4OMINI = get_env("TAB_COUNT_4OMINI", 5, int)
TAB_COUNT_GPTS = get_env("TAB_COUNT_GPTS", 5, int)

# file name
# ----------------------------
# CREATE BLOG WP
# ----------------------------
CREATE_BLOG_WP_GET_THEMES_GOOGLE_FILE_NAME = get_env(
    "CREATE_BLOG_WP_GET_THEMES_GOOGLE_FILE_NAME"
)
CREATE_BLOG_WP_GET_HEADING_GOOGLE_FILE_NAME = get_env(
    "CREATE_BLOG_WP_GET_HEADING_GOOGLE_FILE_NAME"
)
CREATE_BLOG_WP_GET_DIRECTION_FILE_NAME = get_env(
    "CREATE_BLOG_WP_GET_DIRECTION_FILE_NAME"
)
CREATE_BLOG_WP_GET_EVIDENCE_FILE_NAME = get_env("CREATE_BLOG_WP_GET_EVIDENCE_FILE_NAME")
CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT_FILE_NAME = get_env(
    "CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT_FILE_NAME"
)
CREATE_BLOG_WP_GET_ADJUSTED_HTML_FILE_NAME = get_env(
    "CREATE_BLOG_WP_GET_ADJUSTED_HTML_FILE_NAME"
)
CREATE_BLOG_WP_UPLOAD_WP_POST_FILE_NAME = get_env(
    "CREATE_BLOG_WP_UPLOAD_WP_POST_FILE_NAME"
)
# ----------------------------
# CREATE BLOG MD
# ----------------------------
CREATE_BLOG_MD_CHECK_FOLDER_PATH_IN_EXCEL_FILE_NAME = get_env(
    "CREATE_BLOG_MD_CHECK_FOLDER_PATH_IN_EXCEL_FILE_NAME"
)
CREATE_BLOG_MD_CREATE_FOLDER_AND_FILE_FILE_NAME = get_env(
    "CREATE_BLOG_MD_CREATE_FOLDER_AND_FILE_FILE_NAME"
)
CREATE_BLOG_MD_CREATE_BLOG_MD_CHATGPT_FILE_NAME = get_env(
    "CREATE_BLOG_MD_CREATE_BLOG_MD_CHATGPT_FILE_NAME"
)
CREATE_BLOG_MD_GET_TITLE_IN_MD_FILE_NAME = get_env(
    "CREATE_BLOG_MD_GET_TITLE_IN_MD_FILE_NAME"
)
CREATE_BLOG_MD_REPLACE_TEXT_FILE_NAME = get_env("CREATE_BLOG_MD_REPLACE_TEXT_FILE_NAME")
CREATE_BLOG_MD_CREATE_THUMBNAIL_FILE_NAME = get_env(
    "CREATE_BLOG_MD_CREATE_THUMBNAIL_FILE_NAME"
)
CREATE_BLOG_MD_MOVE_TARGET_FOLDERS_FILE_NAME = get_env(
    "CREATE_BLOG_MD_MOVE_TARGET_FOLDERS_FILE_NAME"
)
CREATE_BLOG_MD_DELETE_FILES_IN_FOLDER_FILE_NAME = get_env(
    "CREATE_BLOG_MD_DELETE_FILES_IN_FOLDER_FILE_NAME"
)
# ----------------------------
# CREATE SNS
# ----------------------------
CREATE_SNS_GET_BLOG_SLUG_FILE_NAME = get_env("CREATE_SNS_GET_BLOG_SLUG_FILE_NAME")
CREATE_SNS_GET_BLOG_TITLE_FILE_NAME = get_env("CREATE_SNS_GET_BLOG_TITLE_FILE_NAME")
CREATE_SNS_GET_CONTENT_CHATGPT_FILE_NAME = get_env(
    "CREATE_SNS_GET_CONTENT_CHATGPT_FILE_NAME"
)
CREATE_SNS_UPDATE_POST_CONTENT_GAS_FILE_NAME = get_env(
    "CREATE_SNS_UPDATE_POST_CONTENT_GAS_FILE_NAME"
)
# ----------------------------
# STANDALONE
# ----------------------------
STANDALONE_GET_ELEM_IN_HTML_FILE_NAME = get_env("STANDALONE_GET_ELEM_IN_HTML_FILE_NAME")
STANDALONE_GET_TITLE_IN_MD_FILE_NAME = get_env("STANDALONE_GET_TITLE_IN_MD_FILE_NAME")
STANDALONE_REPLACE_FOLDER_NAME_FILE_NAME = get_env(
    "STANDALONE_REPLACE_FOLDER_NAME_FILE_NAME"
)
# ----------------------------
# STACKOVERFLOW
# ----------------------------
STACKOVERFLOW_GET_SLUG_FILE_NAME = get_env("STACKOVERFLOW_GET_SLUG_FILE_NAME")

# setting
GET_CONTENT_METHOD = get_env("GET_CONTENT_METHOD", "clipboard")
# ChatGPT
CHATGPT_DEFAULT_URL = get_env("CHATGPT_DEFAULT_URL")
CHATGPT_O1_MINI_URL = get_env("CHATGPT_O1_MINI_URL")
CHATGPT_4O_WITH_CANVAS_URL = get_env("CHATGPT_4O_WITH_CANVAS_URL")
CHATGPT_GPTS_BLOG_MASTER_URL = get_env("CHATGPT_GPTS_BLOG_MASTER_URL")
CHATGPT_GPTS_SNS_URL = get_env("CHATGPT_GPTS_SNS_URL")
CHATGPT_GPTS_BROWSER_URL = get_env("CHATGPT_GPTS_BROWSER_URL")
CHATGPT_OUTPUT_TAG = get_env("CHATGPT_OUTPUT_TAG")
CHATGPT_OUTPUT_CLASS_LIST = get_env("CHATGPT_OUTPUT_CLASS_LIST").split(",")
CHATGPT_CANVAS_OUTPUT_CLASS_LIST = get_env("CHATGPT_CANVAS_OUTPUT_CLASS_LIST").split(
    ","
)
CHATGPT_IS_DELETE_CHAT = get_env("CHATGPT_IS_DELETE_CHAT", "false").lower() == "true"
# Bing
BING_URL = get_env("BING_URL")
BING_SOURCE_COPILOT_CONVERSATION = get_env("BING_SOURCE_COPILOT_CONVERSATION")
BING_SUPERSCRIPT_CITATION_PATTERN = get_env("BING_SUPERSCRIPT_CITATION_PATTERN")
BING_OUTPUT_TAG = get_env("BING_OUTPUT_TAG")
BING_OUTPUT_CLASS_LIST = get_env("BING_OUTPUT_CLASS_LIST").split(",")
BING_OUTPUT_ATTRIBUTE_KEY = get_env("BING_OUTPUT_ATTRIBUTE_KEY")
BING_OUTPUT_ATTRIBUTE_VALUE = get_env("BING_OUTPUT_ATTRIBUTE_VALUE")

# ===========================
# Execute variables
# ===========================
EXECUTE_CREATE_BLOG_WP = get_env("EXECUTE_CREATE_BLOG_WP", "false").lower() == "true"
EXECUTE_CREATE_BLOG_MD = get_env("EXECUTE_CREATE_BLOG_MD", "false").lower() == "true"
EXECUTE_CREATE_SNS = get_env("EXECUTE_CREATE_SNS", "false").lower() == "true"
EXECUTE_STANDALONE = get_env("EXECUTE_STANDALONE", "false").lower() == "true"
EXECUTE_STACKOVERFLOW = get_env("EXECUTE_STACKOVERFLOW", "false").lower() == "true"
# Execute create blog wp
EXECUTE_CREATE_BLOG_WP_GET_THEMES_GOOGLE = (
    get_env("EXECUTE_CREATE_BLOG_WP_GET_THEMES_GOOGLE", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_WP_GET_HEADING_GOOGLE = (
    get_env("EXECUTE_CREATE_BLOG_WP_GET_HEADING_GOOGLE", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_WP_GET_DIRECTION = (
    get_env("EXECUTE_CREATE_BLOG_WP_GET_DIRECTION", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_WP_GET_EVIDENCE = (
    get_env("EXECUTE_CREATE_BLOG_WP_GET_EVIDENCE", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT = (
    get_env("EXECUTE_CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_WP_GET_ADJUSTED_HTML = (
    get_env("EXECUTE_CREATE_BLOG_WP_GET_ADJUSTED_HTML", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_WP_UPLOAD_WP_POST = (
    get_env("EXECUTE_CREATE_BLOG_WP_UPLOAD_WP_POST", "false").lower() == "true"
)
# Execute create blog md
EXECUTE_CREATE_BLOG_MD_CREATE_FOLDER_AND_FILE = (
    get_env("EXECUTE_CREATE_BLOG_MD_CREATE_FOLDER_AND_FILE", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_MD_CREATE_BLOG_MD_CHATGPT = (
    get_env("EXECUTE_CREATE_BLOG_MD_CREATE_BLOG_MD_CHATGPT", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_MD_REPLACE_TEXT = (
    get_env("EXECUTE_CREATE_BLOG_MD_REPLACE_TEXT", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_MD_GET_TITLE_IN_MD = (
    get_env("EXECUTE_CREATE_BLOG_MD_GET_TITLE_IN_MD", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_MD_CREATE_THUMBNAIL = (
    get_env("EXECUTE_CREATE_BLOG_MD_CREATE_THUMBNAIL", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_MD_MOVE_TARGET_FOLDERS = (
    get_env("EXECUTE_CREATE_BLOG_MD_MOVE_TARGET_FOLDERS", "false").lower() == "true"
)
EXECUTE_CREATE_BLOG_MD_DELETE_FILES_IN_FOLDERS = (
    get_env("EXECUTE_CREATE_BLOG_MD_DELETE_FILES_IN_FOLDERS", "false").lower() == "true"
)
# Execute create sns
EXECUTE_CREATE_SNS_GET_BLOG_SLUG = (
    get_env("EXECUTE_CREATE_SNS_GET_BLOG_SLUG", "false").lower() == "true"
)
EXECUTE_CREATE_SNS_GET_BLOG_TITLE = (
    get_env("EXECUTE_CREATE_SNS_GET_BLOG_TITLE", "false").lower() == "true"
)
EXECUTE_CREATE_SNS_GET_CONTENT_CHATGPT = (
    get_env("EXECUTE_CREATE_SNS_GET_CONTENT_CHATGPT", "false").lower() == "true"
)
EXECUTE_CREATE_SNS_UPDATE_POST_CONTENT_GAS = (
    get_env("EXECUTE_CREATE_SNS_UPDATE_POST_CONTENT_GAS", "false").lower() == "true"
)
# Execute standalone
EXECUTE_STANDALONE_GET_TITLE_IN_MD = (
    get_env("EXECUTE_STANDALONE_GET_TITLE_IN_MD", "false").lower() == "true"
)
EXECUTE_STANDALONE_GET_TITLE_IN_HTML = (
    get_env("EXECUTE_STANDALONE_GET_TITLE_IN_HTML", "false").lower() == "true"
)
EXECUTE_STANDALONE_REPLACE_FOLDER_NAME = (
    get_env("EXECUTE_STANDALONE_REPLACE_FOLDER_NAME", "false").lower() == "true"
)
# Execute stackoverflow
EXECUTE_STACKOVERFLOW_GET_SLUG = (
    get_env("EXECUTE_STACKOVERFLOW_GET_SLUG", "false").lower() == "true"
)

# ===========================
# Create blog wp variables
# ===========================
# excel
CREATE_BLOG_WP_EXCEL_FILE_NAME = get_env("CREATE_BLOG_WP_EXCEL_FILE_NAME")
CREATE_BLOG_WP_EXCEL_SHEET_NAME = get_env("CREATE_BLOG_WP_EXCEL_SHEET_NAME")
CREATE_BLOG_WP_EXCEL_GROUP_SIZE = get_env("CREATE_BLOG_WP_EXCEL_GROUP_SIZE", 10, int)
CREATE_BLOG_WP_EXCEL_INDEX_ROW = get_env("CREATE_BLOG_WP_EXCEL_INDEX_ROW", 1, int)
CREATE_BLOG_WP_EXCEL_START_ROW = get_env("CREATE_BLOG_WP_EXCEL_START_ROW", 2, int)
CREATE_BLOG_WP_EXCEL_INDEX_STRINGS = get_env(
    "CREATE_BLOG_WP_EXCEL_INDEX_STRINGS"
).split(",")
# get direction
CREATE_BLOG_WP_GET_DIRECTION_REMOVE_TEXT = get_env(
    "CREATE_BLOG_WP_GET_DIRECTION_REMOVE_TEXT"
).split(",")
CREATE_BLOG_WP_GET_DIRECTION_SPLIT_NUM = get_env(
    "CREATE_BLOG_WP_GET_DIRECTION_SPLIT_NUM", 5, int
)
# get evidence
CREATE_BLOG_WP_GET_EVIDENCE_METHOD = get_env("CREATE_BLOG_WP_GET_EVIDENCE_METHOD")
CREATE_BLOG_WP_GET_EVIDENCE_BING_PROMPT = get_env(
    "CREATE_BLOG_WP_GET_EVIDENCE_BING_PROMPT"
)
CREATE_BLOG_WP_GET_EVIDENCE_CHATGPT_PROMPT = get_env(
    "CREATE_BLOG_WP_GET_EVIDENCE_CHATGPT_PROMPT"
)
# ----------------------------
# Chatgpt variables
# ----------------------------
# setting
CREATE_BLOG_WP_CHATGPT_MODEL_TYPE = get_env("CREATE_BLOG_WP_CHATGPT_MODEL_TYPE")
CREATE_BLOG_WP_IS_IMAGE_GENERATION_ENABLED = (
    get_env("CREATE_BLOG_WP_IS_IMAGE_GENERATION_ENABLED", "false").lower() == "true"
)
CREATE_BLOG_WP_PROMPT_TEMPLATE_FULL_PATH = get_env(
    "CREATE_BLOG_WP_PROMPT_TEMPLATE_FULL_PATH"
)
# prompt
CREATE_BLOG_WP_TITLE_PROMPT = get_env("CREATE_BLOG_WP_TITLE_PROMPT")
CREATE_BLOG_WP_LONG_DESCRIPTION_PROMPT = get_env(
    "CREATE_BLOG_WP_LONG_DESCRIPTION_PROMPT"
)
CREATE_BLOG_WP_SHORT_DESCRIPTION_PROMPT = get_env(
    "CREATE_BLOG_WP_SHORT_DESCRIPTION_PROMPT"
)
CREATE_BLOG_WP_KEYWORDS_PROMPT = get_env("CREATE_BLOG_WP_KEYWORDS_PROMPT")
CREATE_BLOG_WP_PERMALINK_PROMPT = get_env("CREATE_BLOG_WP_PERMALINK_PROMPT")
CREATE_BLOG_WP_IMAGE_PROMPT = get_env("CREATE_BLOG_WP_IMAGE_PROMPT")
CREATE_BLOG_WP_THUMBNAIL_IMAGE_PROMPT = get_env("CREATE_BLOG_WP_THUMBNAIL_IMAGE_PROMPT")
CREATE_BLOG_WP_HEADING_PROMPT = get_env("CREATE_BLOG_WP_HEADING_PROMPT")
CREATE_BLOG_WP_ADJUSTED_HTML_INIT_PROMPT = get_env(
    "CREATE_BLOG_WP_ADJUSTED_HTML_INIT_PROMPT"
)
CREATE_BLOG_WP_ADJUSTED_HTML_PROMPT = get_env("CREATE_BLOG_WP_ADJUSTED_HTML_PROMPT")
CREATE_BLOG_WP_ADJUSTED_HTML_COMPLETE_TRUNCATED_PROMPT = get_env(
    "CREATE_BLOG_WP_ADJUSTED_HTML_COMPLETE_TRUNCATED_PROMPT"
)
CREATE_BLOG_WP_ADJUSTED_HTML_FINAL_PROMPT = get_env(
    "CREATE_BLOG_WP_ADJUSTED_HTML_FINAL_PROMPT"
)
# ----------------------------
# WordPress variables
# ----------------------------
CREATE_BLOG_WP_WP_URL = get_env("CREATE_BLOG_WP_WP_URL")
CREATE_BLOG_WP_WP_USERNAME = get_env("CREATE_BLOG_WP_WP_USERNAME")
CREATE_BLOG_WP_WP_APP_PASSWORD = get_env("CREATE_BLOG_WP_WP_APP_PASSWORD")

# ===========================
# Create blog md variables
# ===========================
# excel
CREATE_BLOG_MD_EXCEL_FILE_NAME = get_env("CREATE_BLOG_MD_EXCEL_FILE_NAME")
CREATE_BLOG_MD_EXCEL_SHEET_NAME = get_env("CREATE_BLOG_MD_EXCEL_SHEET_NAME")
CREATE_BLOG_MD_EXCEL_INDEX_ROW = get_env("CREATE_BLOG_MD_EXCEL_INDEX_ROW", 1, int)
CREATE_BLOG_MD_EXCEL_START_ROW = get_env("CREATE_BLOG_MD_EXCEL_START_ROW", 2, int)
CREATE_BLOG_MD_EXCEL_INDEX_STRINGS = get_env(
    "CREATE_BLOG_MD_EXCEL_INDEX_STRINGS"
).split(",")
CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH = get_env(
    "CREATE_BLOG_MD_TARGET_FOLDER_FULL_PATH"
)
CREATE_BLOG_MD_TARGET_MDX_FILE_NAME = get_env("CREATE_BLOG_MD_TARGET_MDX_FILE_NAME")
CREATE_BLOG_MD_TARGET_PNG_FILE_NAME = get_env("CREATE_BLOG_MD_TARGET_PNG_FILE_NAME")
CREATE_BLOG_MD_MOVE_TO_DESTINATION_FOLDER_FULL_PATH = get_env(
    "CREATE_BLOG_MD_MOVE_TO_DESTINATION_FOLDER_FULL_PATH"
)
# thumbnail
CREATE_BLOG_MD_PNG_FONTS_DIR_NAME = get_env("CREATE_BLOG_MD_PNG_FONTS_DIR_NAME")
CREATE_BLOG_MD_PNG_SETTINGS_DIR_NAME = get_env("CREATE_BLOG_MD_PNG_SETTINGS_DIR_NAME")
CREATE_BLOG_MD_PNG_IMAGES_DIR_NAME = get_env("CREATE_BLOG_MD_PNG_IMAGES_DIR_NAME")
CREATE_BLOG_MD_PNG_TAG_NAME = get_env("CREATE_BLOG_MD_PNG_TAG_NAME")
CREATE_BLOG_MD_PNG_CONFIG_NAME = get_env("CREATE_BLOG_MD_PNG_CONFIG_NAME")
CREATE_BLOG_MD_TARGET_TAG_NAME = get_env("CREATE_BLOG_MD_TARGET_TAG_NAME")
CREATE_BLOG_MD_CREATE_THUMBNAIL_SEPARATE_TEXT = get_env(
    "CREATE_BLOG_MD_CREATE_THUMBNAIL_SEPARATE_TEXT"
)
# get title in md
CREATE_BLOG_MD_GET_TITLE_IN_MD_TARGET_TEXT = get_env(
    "CREATE_BLOG_MD_GET_TITLE_IN_MD_TARGET_TEXT"
)
CREATE_BLOG_MD_GET_TITLE_IN_MD_REPLACE_TARGET_TEXT = get_env(
    "CREATE_BLOG_MD_GET_TITLE_IN_MD_REPLACE_TARGET_TEXT"
)
CREATE_BLOG_MD_GET_TITLE_IN_MD_REPLACEMENT_TEXT = get_env(
    "CREATE_BLOG_MD_GET_TITLE_IN_MD_REPLACEMENT_TEXT"
)
CREATE_BLOG_MD_GET_TITLE_IN_MD_SPLIT_TEXT = get_env(
    "CREATE_BLOG_MD_GET_TITLE_IN_MD_SPLIT_TEXT"
)

# ===========================
# Create sns variables
# ===========================
# file name
CREATE_SNS_CREDENTIALS_FILE_NAME = get_env("CREATE_SNS_CREDENTIALS_FILE_NAME")
CREATE_SNS_TOKEN_FILE_NAME = get_env("CREATE_SNS_TOKEN_FILE_NAME")
# excel
CREATE_SNS_EXCEL_FILE_NAME = get_env("CREATE_SNS_EXCEL_FILE_NAME")
CREATE_SNS_EXCEL_SHEET_NAME = get_env("CREATE_SNS_EXCEL_SHEET_NAME")
CREATE_SNS_EXCEL_INDEX_ROW = get_env("CREATE_SNS_EXCEL_INDEX_ROW", 1, int)
CREATE_SNS_EXCEL_START_ROW = get_env("CREATE_SNS_EXCEL_START_ROW", 2, int)
CREATE_SNS_EXCEL_INDEX_STRINGS = get_env("CREATE_SNS_EXCEL_INDEX_STRINGS").split(",")
# prompt
CREATE_SNS_PROMPT = get_env("CREATE_SNS_PROMPT")
# gas
CREATE_SNS_SPREADSHEET_ID = get_env("CREATE_SNS_SPREADSHEET_ID")
CREATE_SNS_SPREADSHEET_SHEET_NAME = get_env("CREATE_SNS_SPREADSHEET_SHEET_NAME")

# ===========================
# Standalone variables
# ===========================
# ----------------------------
# get title in md variables
# ----------------------------
# excel
STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_NAME = get_env(
    "STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_NAME"
)
STANDALONE_GET_TITLE_IN_MD_EXCEL_SHEET_NAME = get_env(
    "STANDALONE_GET_TITLE_IN_MD_EXCEL_SHEET_NAME"
)
STANDALONE_GET_TITLE_IN_MD_EXCEL_INDEX_ROW = get_env(
    "STANDALONE_GET_TITLE_IN_MD_EXCEL_INDEX_ROW", 1, int
)
STANDALONE_GET_TITLE_IN_MD_EXCEL_START_ROW = get_env(
    "STANDALONE_GET_TITLE_IN_MD_EXCEL_START_ROW", 2, int
)
STANDALONE_GET_TITLE_IN_MD_EXCEL_INDEX_STRINGS = get_env(
    "STANDALONE_GET_TITLE_IN_MD_EXCEL_INDEX_STRINGS"
).split(",")
# target info
STANDALONE_GET_TITLE_IN_MD_TARGET_DIR_FULL_PATH = get_env(
    "STANDALONE_GET_TITLE_IN_MD_TARGET_DIR_FULL_PATH"
)
STANDALONE_GET_TITLE_IN_MD_TARGET_FILE_NAME = get_env(
    "STANDALONE_GET_TITLE_IN_MD_TARGET_FILE_NAME"
)
STANDALONE_GET_TITLE_IN_MD_TARGET_TEXT = get_env(
    "STANDALONE_GET_TITLE_IN_MD_TARGET_TEXT"
)
# ----------------------------
# get elem in html variables
# ----------------------------
# excel
STANDALONE_GET_ELEM_IN_HTML_EXCEL_FILE_NAME = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_EXCEL_FILE_NAME"
)
STANDALONE_GET_ELEM_IN_HTML_EXCEL_SHEET_NAME = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_EXCEL_SHEET_NAME"
)
STANDALONE_GET_ELEM_IN_HTML_EXCEL_INDEX_ROW = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_EXCEL_INDEX_ROW", 1, int
)
STANDALONE_GET_ELEM_IN_HTML_EXCEL_START_ROW = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_EXCEL_START_ROW", 2, int
)
STANDALONE_GET_ELEM_IN_HTML_EXCEL_INDEX_STRINGS = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_EXCEL_INDEX_STRINGS"
).split(",")
# html info
STANDALONE_GET_ELEM_IN_HTML_BASE_URL = get_env("STANDALONE_GET_ELEM_IN_HTML_BASE_URL")
STANDALONE_GET_ELEM_IN_HTML_ELEMENT_TO_KEEP = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_ELEMENT_TO_KEEP"
).split(",")
STANDALONE_GET_ELEM_IN_HTML_START_PAGE = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_START_PAGE", 1, int
)
STANDALONE_GET_ELEM_IN_HTML_END_PAGE = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_END_PAGE", 10, int
)
STANDALONE_GET_ELEM_IN_HTML_TAG = get_env("STANDALONE_GET_ELEM_IN_HTML_TAG")
STANDALONE_GET_ELEM_IN_HTML_CLASSES = get_env(
    "STANDALONE_GET_ELEM_IN_HTML_CLASSES"
).split(",")
STANDALONE_GET_ELEM_IN_HTML_ATTRIBUTE = get_env("STANDALONE_GET_ELEM_IN_HTML_ATTRIBUTE")

# ----------------------------
# get elem in html variables
# ----------------------------
# excel
STANDALONE_REPLACE_FOLDER_NAME_EXCEL_FILE_NAME = get_env(
    "STANDALONE_REPLACE_FOLDER_NAME_EXCEL_FILE_NAME"
)
STANDALONE_REPLACE_FOLDER_NAME_EXCEL_SHEET_NAME = get_env(
    "STANDALONE_REPLACE_FOLDER_NAME_EXCEL_SHEET_NAME"
)
STANDALONE_REPLACE_FOLDER_NAME_EXCEL_INDEX_ROW = get_env(
    "STANDALONE_REPLACE_FOLDER_NAME_EXCEL_INDEX_ROW", 1, int
)
STANDALONE_REPLACE_FOLDER_NAME_EXCEL_START_ROW = get_env(
    "STANDALONE_REPLACE_FOLDER_NAME_EXCEL_START_ROW", 2, int
)
STANDALONE_REPLACE_FOLDER_NAME_EXCEL_INDEX_STRINGS = get_env(
    "STANDALONE_REPLACE_FOLDER_NAME_EXCEL_INDEX_STRINGS"
).split(",")
# folder info
STANDALONE_REPLACE_FOLDER_NAME_TARGET_FOLDER_PATH = get_env(
    "STANDALONE_REPLACE_FOLDER_NAME_TARGET_FOLDER_PATH"
)
STANDALONE_REPLACE_FOLDER_NAME_TARGET_TAG_NAME = get_env(
    "STANDALONE_REPLACE_FOLDER_NAME_TARGET_TAG_NAME"
)

# ===========================
# stackoverflow variables
# ===========================
# ----------------------------
# get slug variables
# ----------------------------
# excel
STACKOVERFLOW_GET_SLUG_EXCEL_FILE_NAME = get_env(
    "STACKOVERFLOW_GET_SLUG_EXCEL_FILE_NAME"
)
STACKOVERFLOW_GET_SLUG_EXCEL_SHEET_NAME = get_env(
    "STACKOVERFLOW_GET_SLUG_EXCEL_SHEET_NAME"
)
STACKOVERFLOW_GET_SLUG_EXCEL_INDEX_ROW = get_env(
    "STACKOVERFLOW_GET_SLUG_EXCEL_INDEX_ROW", 1, int
)
STACKOVERFLOW_GET_SLUG_EXCEL_START_ROW = get_env(
    "STACKOVERFLOW_GET_SLUG_EXCEL_START_ROW", 2, int
)
STACKOVERFLOW_GET_SLUG_EXCEL_INDEX_STRINGS = get_env(
    "STACKOVERFLOW_GET_SLUG_EXCEL_INDEX_STRINGS"
).split(",")
