import os
import sys
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
sys.path.append(project_root)

load_dotenv(dotenv_path, override=True)
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "")
WAIT_TIME_AFTER_PROMPT_LONG = int(os.getenv("WAIT_TIME_AFTER_PROMPT_LONG", 200))
WAIT_TIME_AFTER_PROMPT_SHORT = int(os.getenv("WAIT_TIME_AFTER_PROMPT_SHORT", 100))
WAIT_TIME_AFTER_RELOAD = int(os.getenv("WAIT_TIME_AFTER_RELOAD", 5))
SHORT_WAIT_TIME = float(os.getenv("SHORT_WAIT_TIME", 0.5))
CHATGPT_MODEL_TYPE = os.getenv("CHATGPT_MODEL_TYPE", "4o")
IS_IMAGE_GENERATION_ENABLED = (
    os.getenv("IS_IMAGE_GENERATION_ENABLED", "false").lower() == "true"
)
CHATGPT_PATH = os.getenv("CHATGPT_PATH", "https://chatgpt.com/")
PROMPT_TEMPLATE_PATH = os.getenv("PROMPT_TEMPLATE_PATH", "")
LONG_DESCRIPTION_PROMPT = os.getenv("LONG_DESCRIPTION_PROMPT", "")
GROUP_SIZE = 10
EXCEL_INDEX_ROW = 1
EXCEL_START_ROW = EXCEL_INDEX_ROW + 1
SOURCE_COPILOT_CONVERSATION = "ソース: Copilot との会話"
SUPERSCRIPT_CITATION_PATTERN = r"\s*[⁰¹²³⁴⁵⁶⁷⁸⁹]+:\s*\[[^\]]+\]\([^\)]+\)"
SHORT_DESCRIPTION_PROMPT = os.getenv("SHORT_DESCRIPTION_PROMPT")
KEYWORDS_PROMPT = os.getenv("KEYWORDS_PROMPT")
PERMALINK_PROMPT = os.getenv("PERMALINK_PROMPT")
IMAGE_PROMPT = os.getenv("IMAGE_PROMPT")
TITLE_PROMPT = os.getenv("TITLE_PROMPT")

from src.excel_operations.excel_manager import ExcelManager
from src.web_operations.edge_handler import EdgeHandler
from src.input_operations.keyboard_handler import KeyboardHandler
from src.ai_operations.chatgpt_handler import ChatGPTHandler
from src.text_operations.prompt_generator import PromptGenerator
from src.file_operations.file_processor import FileReader
from src.util_operations.validator import ValueValidator
from src.log_operations.log_handlers import setup_logger
from src.text_operations.text_manager import TextManager

excel_manager = ExcelManager(EXCEL_FILE_PATH)
edge_handler = EdgeHandler(wait_time_after_switch=WAIT_TIME_AFTER_RELOAD)
keyboard_handler = KeyboardHandler(short_wait_time=SHORT_WAIT_TIME)
chatgpt_handler = ChatGPTHandler(
    wait_time_after_reload=WAIT_TIME_AFTER_RELOAD,
    wait_time_after_prompt_short=WAIT_TIME_AFTER_PROMPT_SHORT,
    wait_time_after_prompt_long=WAIT_TIME_AFTER_PROMPT_LONG,
    short_wait_time=SHORT_WAIT_TIME,
    model_type=CHATGPT_MODEL_TYPE,
)
prompt_generator = PromptGenerator(
    WAIT_TIME_AFTER_PROMPT_SHORT,
    WAIT_TIME_AFTER_PROMPT_LONG,
)
text_manager = TextManager()
file_reader = FileReader()
logger = setup_logger(__name__)


def generate_and_process_prompts(start_row, columns):
    """指定されたグループのプロンプトを生成し、処理する"""
    theme = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["theme"]
    )
    heading = excel_manager.cell_handler.get_cell_value(
        excel_manager.current_sheet, start_row, columns["heading"]
    )
    evidences = excel_manager.cell_handler.get_range_values(
        excel_manager.current_sheet, start_row, columns["evidence"], GROUP_SIZE
    )
    if not ValueValidator.has_any_valid_value_in_array(evidences):
        return

    edge_handler.open_url_in_browser(CHATGPT_PATH)

    logger.info("getting md content")
    initial_prompt = file_reader.read_file(PROMPT_TEMPLATE_PATH)
    for i, evidence in enumerate(evidences):
        evidence = text_manager.text_remover.remove_content_after(
            evidence, SOURCE_COPILOT_CONVERSATION
        )
        evidence = text_manager.text_remover.remove_pattern(
            evidence, SUPERSCRIPT_CITATION_PATTERN
        )
        if i == 0:
            prompt = prompt_generator.create_initial_prompt(
                theme, heading, evidence, initial_prompt
            )
        else:
            prompt = prompt_generator.create_additional_prompt(evidence)
        chatgpt_handler.send_prompt_and_generate_content(prompt, repeat_count=2)
    md_content = chatgpt_handler.get_generated_content()

    logger.info("getting title content")
    chatgpt_handler.send_prompt_and_generate_content(TITLE_PROMPT, repeat_count=0)
    title_content = chatgpt_handler.get_generated_content()

    logger.info("sent long description content")
    chatgpt_handler.send_prompt_and_generate_content(
        LONG_DESCRIPTION_PROMPT, repeat_count=0
    )

    logger.info("getting short description content")
    chatgpt_handler.send_prompt_and_generate_content(
        SHORT_DESCRIPTION_PROMPT, repeat_count=0
    )
    description_content = chatgpt_handler.get_generated_content()

    logger.info("getting keywords content")
    chatgpt_handler.send_prompt_and_generate_content(KEYWORDS_PROMPT, repeat_count=0)
    keywords_content = chatgpt_handler.get_generated_content()

    logger.info("getting permalink content")
    chatgpt_handler.send_prompt_and_generate_content(PERMALINK_PROMPT, repeat_count=0)
    link_content = chatgpt_handler.get_generated_content()

    logger.info("getting image content")
    if IS_IMAGE_GENERATION_ENABLED:
        chatgpt_handler.send_prompt_and_generate_content(IMAGE_PROMPT, repeat_count=0)

    excel_manager.update_cell(start_row, columns["md"], md_content)
    excel_manager.update_cell(start_row, columns["title"], title_content)
    excel_manager.update_cell(start_row, columns["description"], description_content)
    excel_manager.update_cell(start_row, columns["keywords"], keywords_content)
    excel_manager.update_cell(start_row, columns["link"], link_content)

    excel_manager.save_workbook()


def main():
    if not excel_manager.load_workbook():
        return

    excel_manager.set_active_sheet(excel_manager.get_sheet_names()[0])
    search_strings = [
        "flag",
        "md",
        "theme",
        "heading",
        "title",
        "description",
        "keywords",
        "evidence",
        "link",
    ]
    column_indices = excel_manager.search_handler.find_multiple_matching_indices(
        worksheet=excel_manager.current_sheet,
        index=EXCEL_INDEX_ROW,
        search_strings=search_strings,
        is_row_flag=True,
    )
    columns = dict(zip(search_strings, column_indices))

    if ValueValidator.has_any_invalid_value_in_array(list(columns.values())):
        return

    flag_end_row = excel_manager.cell_handler.get_last_row_of_column(
        worksheet=excel_manager.current_sheet, column=columns["flag"]
    )
    for i in range(flag_end_row):
        start_row = i * GROUP_SIZE + EXCEL_START_ROW
        flag = excel_manager.cell_handler.get_cell_value(
            excel_manager.current_sheet, start_row, columns["flag"]
        )
        if ValueValidator.is_single_value_valid(flag):
            logger.prominent_log(f"Processing group starting at row {start_row}")
            generate_and_process_prompts(start_row, columns)


if __name__ == "__main__":
    main()
