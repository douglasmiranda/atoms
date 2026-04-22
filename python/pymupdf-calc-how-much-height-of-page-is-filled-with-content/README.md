# PyMuPDF - Calculate how much height of a page is filled with content

Estimate how much of a PDF page's usable vertical area is occupied by text blocks.

This snippet:
- Defines a content area by excluding top, bottom, left, and right margins.
- Crops the page to that content area.
- Reads text blocks and finds the farthest block position on the Y axis.
- Computes the filled percentage as:

$$
	\text{filled percentage} = \frac{\text{height usage}}{\text{height available}} \times 100
$$

## Files

- `calc.py`: script with `Margin` dataclass and `page_height_usage(page, margins)`.
- `requirements.txt`: pinned dependency (`pymupdf==1.27.2.2`).
- `pdfs/example.pdf`: sample input used by the script.

## Requirements

- Python 3.10+ (recommended)
- PyMuPDF (see `requirements.txt`)

## Install

```bash
pip install -r requirements.txt
```

## Run

From this directory:

```bash
python calc.py
```

The script opens `pdfs/example.pdf`, applies the configured margins, and prints one percentage per page.

## Margin Meaning

`Margin` values are in points:
- 1 inch = 72 points
- 1 cm = 28.35 points

Coordinates:
- `x0` = left
- `y0` = top
- `x1` = right
- `y1` = bottom

In this snippet, `top` and `bottom` are used to ignore header/footer regions.

## Important Notes

- `page.set_cropbox(content_rect)` changes the page coordinate context used afterward in this run.
- The current approach is text-block based (`page.get_text("blocks")`), so very complex layouts (multiple columns, images, floating elements) may require extra logic.
- This measures vertical usage (how far content reaches downward), not area coverage.

## Customization

Edit the margin values in `calc.py`:

```python
margin = Margin(top=77, bottom=30, left=35, right=35)
```

Then run again to match your document layout and ignore non-content regions more accurately.
