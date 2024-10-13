from typing import Tuple, List
from PIL import ImageDraw, ImageFont
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)

LINE_SPACING = 50


class TextDrawer:
    def draw_multiline_text(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        color: str,
        x: int,
        y: int,
        width: int,
        height: int,
        horizontal_align: str,
        vertical_align: str,
    ) -> None:
        """
        Draw multiline text on an image with specified alignment.

        :param draw: ImageDraw object to draw on
        :param text: Text to be drawn
        :param font: Font to be used
        :param color: Color of the text
        :param x: X-coordinate of the text
        :param y: Y-coordinate of the text
        :param width: Width of the text area
        :param height: Height of the text area
        :param horizontal_align: Horizontal alignment ('left', 'center', 'right')
        :param vertical_align: Vertical alignment ('top', 'middle', 'bottom')
        """
        logger.debug(f"Drawing multiline text: '{text[:20]}...'")

        lines = text.split("\n")
        line_heights = self._get_line_heights(draw, lines, font)
        total_height = sum(line_heights) + (len(lines) - 1) * LINE_SPACING

        y = self._calculate_initial_y(y, height, total_height, vertical_align)

        for line in lines:
            line_width, line_height = self._get_line_dimensions(draw, line, font)
            line_x = self._calculate_line_x(x, width, line_width, horizontal_align)

            logger.debug(f"Drawing line at ({line_x}, {y}): '{line[:20]}...'")
            draw.text((line_x, y), line, font=font, fill=color)
            y += line_height + LINE_SPACING

    def _get_line_heights(
        self, draw: ImageDraw.ImageDraw, lines: List[str], font: ImageFont.FreeTypeFont
    ) -> List[int]:
        """Calculate the height of each line."""
        return [draw.textbbox((0, 0), line, font=font)[3] for line in lines]

    def _calculate_initial_y(
        self, y: int, height: int, total_height: int, vertical_align: str
    ) -> int:
        """Calculate the initial y position based on vertical alignment."""
        if vertical_align == "middle":
            return int(height - total_height) / 2
        elif vertical_align == "bottom":
            return int(height - total_height - 10)
        return y

    def _get_line_dimensions(
        self, draw: ImageDraw.ImageDraw, line: str, font: ImageFont.FreeTypeFont
    ) -> Tuple[int, int]:
        """Get the width and height of a single line of text."""
        line_bbox = draw.textbbox((0, 0), line, font=font)
        return line_bbox[2] - line_bbox[0], line_bbox[3] - line_bbox[1]

    def _calculate_line_x(
        self, x: int, width: int, line_width: int, horizontal_align: str
    ) -> int:
        """Calculate the x position for a line based on horizontal alignment."""
        if horizontal_align == "center":
            return int((width - line_width) / 2)
        elif horizontal_align == "right":
            return int(width - line_width - 10)
        return x
