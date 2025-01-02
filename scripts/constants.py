from enum import Enum
from scripts.load_env import *
from scripts.initialize import (
    folder_path_handler,
    file_path_handler,
)

# ===========================
# constants
# ===========================
# extension and prefix
EXTENSION_HTML = ".html"
EXTENSION_WEBP = ".webp"
DOWNLOAD_HTML_FOLDER_SUFFIX = "_files"


class GetContentMethod(str, Enum):
    CLIPBOARD = "clipboard"
    HTML = "html"
    SHORTCUT = "shortcut"


# ai tool
AI_TOOL_CHATGPT = "chatgpt"
AI_TOOL_BING = "bing"
# model type
MODEL_TYPE_4O = "4o"
MODEL_TYPE_4OMINI = "4omini"
MODEL_TYPE_GPTS = "gpts"

# ===========================
# Create blog wp variables
# ===========================
CREATE_BLOG_WP_DIR_FULL_PATH = folder_path_handler.join_and_normalize_path(
    [PROJECT_DIR_FULL_PATH, SCRIPTS_DIR_NAME, CREATE_BLOG_WP_DIR_NAME]
)
CREATE_BLOG_WP_EXCEL_FILE_FULL_PATH = file_path_handler.join_and_normalize_path(
    [PROJECT_DIR_FULL_PATH, DATA_DIR_NAME, CREATE_BLOG_WP_EXCEL_FILE_NAME]
)
CREATE_BLOG_WP_GET_THEMES_GOOGLE_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_WP_DIR_FULL_PATH, CREATE_BLOG_WP_GET_THEMES_GOOGLE_FILE_NAME
)
CREATE_BLOG_WP_GET_HEADING_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_WP_DIR_FULL_PATH, CREATE_BLOG_WP_GET_HEADING_GOOGLE_FILE_NAME
)
CREATE_BLOG_WP_GET_DIRECTION_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_WP_DIR_FULL_PATH, CREATE_BLOG_WP_GET_DIRECTION_FILE_NAME
)
CREATE_BLOG_WP_GET_EVIDENCE_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_WP_DIR_FULL_PATH, CREATE_BLOG_WP_GET_EVIDENCE_FILE_NAME
)
CREATE_BLOG_WP_CREATE_BLOG_WP_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_WP_DIR_FULL_PATH, CREATE_BLOG_WP_CREATE_BLOG_WP_CHATGPT_FILE_NAME
)
CREATE_BLOG_WP_POST_WP_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_WP_DIR_FULL_PATH, CREATE_BLOG_WP_UPLOAD_WP_POST_FILE_NAME
)

# ===========================
# Create blog md variables
# ===========================
CREATE_BLOG_MD_DIR_FULL_PATH = folder_path_handler.join_and_normalize_path(
    [PROJECT_DIR_FULL_PATH, SCRIPTS_DIR_NAME, CREATE_BLOG_MD_DIR_NAME]
)
CREATE_BLOG_MD_EXCEL_FILE_FULL_PATH = file_path_handler.join_and_normalize_path(
    [PROJECT_DIR_FULL_PATH, DATA_DIR_NAME, CREATE_BLOG_MD_EXCEL_FILE_NAME]
)
CREATE_BLOG_MD_CREATE_FOLDER_AND_FILE_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_MD_DIR_FULL_PATH, CREATE_BLOG_MD_CREATE_FOLDER_AND_FILE_FILE_NAME
)
CREATE_BLOG_MD_CREATE_BLOG_MD_CHATGPT_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_MD_DIR_FULL_PATH, CREATE_BLOG_MD_CREATE_BLOG_MD_CHATGPT_FILE_NAME
)
CREATE_BLOG_MD_REPLACE_TEXT_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_MD_DIR_FULL_PATH, CREATE_BLOG_MD_REPLACE_TEXT_FILE_NAME
)
CREATE_BLOG_MD_GET_TITLE_IN_MD_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_MD_DIR_FULL_PATH, CREATE_BLOG_MD_GET_TITLE_IN_MD_FILE_NAME
)
CREATE_BLOG_MD_CREATE_THUMBNAIL_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_MD_DIR_FULL_PATH, CREATE_BLOG_MD_CREATE_THUMBNAIL_FILE_NAME
)
CREATE_BLOG_MD_MOVE_TARGET_FOLDERS_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_MD_DIR_FULL_PATH, CREATE_BLOG_MD_MOVE_TARGET_FOLDERS_FILE_NAME
)
CREATE_BLOG_MD_DELETE_FILES_IN_FOLDERS_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_BLOG_MD_DIR_FULL_PATH, CREATE_BLOG_MD_DELETE_FILES_IN_FOLDER_FILE_NAME
)

# ===========================
# Create sns variables
# ===========================
CREATE_SNS_DIR_FULL_PATH = folder_path_handler.join_and_normalize_path(
    [PROJECT_DIR_FULL_PATH, SCRIPTS_DIR_NAME, CREATE_SNS_DIR_NAME]
)
CREATE_SNS_CREDENTIALS_FILE_FULL_PATH = file_path_handler.join_and_normalize_path(
    [
        CREATE_SNS_DIR_FULL_PATH,
        STATISTICS_DIR_NAME,
        CREATE_SNS_CREDENTIALS_FILE_NAME,
    ]
)
CREATE_SNS_TOKEN_FILE_FULL_PATH = file_path_handler.join_and_normalize_path(
    [
        CREATE_SNS_DIR_FULL_PATH,
        STATISTICS_DIR_NAME,
        CREATE_SNS_TOKEN_FILE_NAME,
    ]
)
CREATE_SNS_EXCEL_FILE_FULL_PATH = file_path_handler.join_and_normalize_path(
    [PROJECT_DIR_FULL_PATH, DATA_DIR_NAME, CREATE_SNS_EXCEL_FILE_NAME]
)
CREATE_SNS_GET_BLOG_SLUG_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_SNS_DIR_FULL_PATH, CREATE_SNS_GET_BLOG_SLUG_FILE_NAME
)
CREATE_SNS_GET_BLOG_TITLE_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_SNS_DIR_FULL_PATH, CREATE_SNS_GET_BLOG_TITLE_FILE_NAME
)
CREATE_SNS_GET_CONTENT_CHATGPT_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_SNS_DIR_FULL_PATH, CREATE_SNS_GET_CONTENT_CHATGPT_FILE_NAME
)
CREATE_SNS_UPDATE_POST_CONTENT_GAS_FILE_FULL_PATH = file_path_handler.join_path(
    CREATE_SNS_DIR_FULL_PATH, CREATE_SNS_UPDATE_POST_CONTENT_GAS_FILE_NAME
)

# ===========================
# Create standalone variables
# ===========================
STANDALONE_DIR_FULL_PATH = folder_path_handler.join_and_normalize_path(
    [PROJECT_DIR_FULL_PATH, SCRIPTS_DIR_NAME, STANDALONE_DIR_NAME]
)
STANDALONE_GET_TITLE_IN_MD_FILE_FULL_PATH = file_path_handler.join_path(
    STANDALONE_DIR_FULL_PATH, STANDALONE_GET_TITLE_IN_MD_FILE_NAME
)
STANDALONE_GET_TITLE_IN_HTML_FILE_FULL_PATH = file_path_handler.join_path(
    STANDALONE_DIR_FULL_PATH, STANDALONE_GET_ELEM_IN_HTML_FILE_NAME
)
STANDALONE_REPLACE_FOLDER_NAME_FILE_FULL_PATH = file_path_handler.join_path(
    STANDALONE_DIR_FULL_PATH, STANDALONE_REPLACE_FOLDER_NAME_FILE_NAME
)
# ----------------------------
# get title in md variables
# ----------------------------
STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_FULL_PATH = (
    file_path_handler.join_and_normalize_path(
        [
            PROJECT_DIR_FULL_PATH,
            DATA_DIR_NAME,
            STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_NAME,
        ]
    )
)
# ----------------------------
# get elem in html variables
# ----------------------------
STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_FULL_PATH = (
    file_path_handler.join_and_normalize_path(
        [
            PROJECT_DIR_FULL_PATH,
            DATA_DIR_NAME,
            STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_NAME,
        ]
    )
)
# ----------------------------
# get elem in html variables
# ----------------------------
STANDALONE_REPLACE_FOLDER_NAME_EXCEL_FILE_FULL_PATH = (
    file_path_handler.join_and_normalize_path(
        [
            PROJECT_DIR_FULL_PATH,
            DATA_DIR_NAME,
            STANDALONE_GET_TITLE_IN_MD_EXCEL_FILE_NAME,
        ]
    )
)
STANDALONE_REPLACE_FOLDER_NAME_TARGET_FOLDER_FULL_PATH = (
    file_path_handler.join_and_normalize_path(
        [
            STANDALONE_REPLACE_FOLDER_NAME_TARGET_FOLDER_PATH,
            STANDALONE_REPLACE_FOLDER_NAME_TARGET_TAG_NAME,
        ]
    )
)

# ===========================
# Create stackoverflow variables
# ===========================
STACKOVERFLOW_DIR_FULL_PATH = folder_path_handler.join_and_normalize_path(
    [PROJECT_DIR_FULL_PATH, SCRIPTS_DIR_NAME, STACKOVERFLOW_DIR_NAME]
)
STACKOVERFLOW_GET_SLUG_FILE_FULL_PATH = file_path_handler.join_path(
    STACKOVERFLOW_DIR_FULL_PATH, STACKOVERFLOW_GET_SLUG_FILE_NAME
)
# ----------------------------
# get slug variables
# ----------------------------
STACKOVERFLOW_GET_SLUG_EXCEL_FILE_FULL_PATH = file_path_handler.join_and_normalize_path(
    [
        PROJECT_DIR_FULL_PATH,
        DATA_DIR_NAME,
        STACKOVERFLOW_GET_SLUG_EXCEL_FILE_NAME,
    ]
)
