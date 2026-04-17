# PyMuPDF - Calculate the percentage of the page height filled with text blocks.

from dataclasses import dataclass

import pymupdf


@dataclass
class Margin:
    """Margin in points
    1 inch = 72 points
    1 cm = 28.35 points
    x0 = left, y0 = top, x1 = right, y1 = bottom
    y0 is margin top, usually the header
    y1 is margin bottom, usually the footer
    """

    top: float
    bottom: float
    left: float
    right: float


def page_height_usage(page: pymupdf.Page, margins: Margin):
    """
    Calculate the percentage of the page height filled with text blocks.
    Notes:
      - after page.set_cropbox(content_rect), the context of space changes.
        That means that any position now is relative to the new cropbox.
      - This function may need optimization if your document has multiple
        columns, images, or other elements that may affect the height usage.
    """
    # x0 = left, y0 = top, x1 = right, y1 = bottom
    # Get the page dimensions
    page_rect = page.rect

    # Define the content area excluding
    # header and footer and margins
    content_rect = pymupdf.Rect(
        page_rect.x0 + margins.left,
        page_rect.y0 + margins.top,
        page_rect.x1 - margins.right,
        page_rect.y1 - margins.bottom,
    )

    height_available = content_rect.height
    height_usage = float(0)
    print("height_available", height_available)

    page.set_cropbox(content_rect)

    text_blocks = page.get_text("blocks")

    for block in text_blocks:
        # print(block)
        # y1 is basically (in this context) the distance to the top of our
        # content area (cropbox)
        y1 = block[3]
        # only couting the block that's farthest from the top
        if y1 > height_usage:
            height_usage = y1

    print("height_usage", height_usage)
    filled_percentage = (height_usage / height_available) * 100
    return filled_percentage


doc = pymupdf.open("pdfs/example.pdf")

# Define the margins (in points)
# That way we define that header, footer, and left and right margins are not part of the content area.
# This basically will define the cropbox that will be used to calculate the height usage.
margin = Margin(top=77, bottom=30, left=35, right=35)

for page in doc:
    print("Cropbox:", page.cropbox)
    filled_percentage = page_height_usage(page, margin)
    print(
        f"Page {page.number + 1}: has {filled_percentage:.2f}% of its height content area filled."
    )
    print("-" * 80 + "\n")
