# pip install python-barcode pillow pywin32

import os
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageWin
from barcode import Code128
from barcode.writer import ImageWriter
import win32print
import win32ui
import win32con

# ===== CONFIG =====
PRINTER_NAME = "Datamax O'Neil E4204B Mark III"  # put your exact printer name here
BARCODE_DATA = "55667788"
LINE2_TEXT   = "Product ID 5566"

LABEL_W_CM = 5.5
LABEL_H_CM = 2.0
DPI_RENDER = 300            # render resolution for the PNG we create

# super compact layout
KEEP_TOP_RATIO      = 0.50  # keep top 50% of barcode (crop the rest)
BARCODE_HEIGHT_CM   = 0.45  # 4.5 mm tall barcode
BARCODE_WIDTH_RATIO = 0.40  # 40% of label width
TEXT1_PX = 16               # first line font (smaller)
TEXT2_PX = 12               # second line font (smaller)
TEXT_GAP_PX = 0             # no extra vertical gap

# ===== HELPERS =====
def cm_to_px(cm, dpi=DPI_RENDER):
    return int(round(cm / 2.54 * dpi))

def center_x(canvas_w, obj_w):
    return max(0, (canvas_w - obj_w) // 2)

def load_font(preferred, size_px):
    try:
        return ImageFont.truetype(preferred, size_px)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size_px)
        except Exception:
            return ImageFont.load_default()

def make_barcode_png(tmpdir, data):
    base = os.path.join(tmpdir, "barcode")
    code = Code128(data, writer=ImageWriter())
    path = code.save(base, options={
        "write_text": False,
        "module_height": 50,   # we will crop & scale anyway
        "module_width": 0.25,
        "quiet_zone": 1,
    })
    return path  # ".../barcode.png"

def compose_label_image():
    W = cm_to_px(LABEL_W_CM)
    H = cm_to_px(LABEL_H_CM)
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    with tempfile.TemporaryDirectory() as tmpdir:
        # barcode → crop → scale
        barcode_png = make_barcode_png(tmpdir, BARCODE_DATA)
        bimg = Image.open(barcode_png).convert("L")
        bw, bh = bimg.size
        keep_h = max(1, int(bh * KEEP_TOP_RATIO))
        bimg = bimg.crop((0, 0, bw, keep_h))

        target_h_px = cm_to_px(BARCODE_HEIGHT_CM)
        aspect = bw / keep_h
        max_w = int(W * BARCODE_WIDTH_RATIO)
        target_w_px = min(int(target_h_px * aspect), max_w)
        bimg = bimg.resize((target_w_px, target_h_px), Image.LANCZOS)

        # paste at very top, centered
        bx = center_x(W, target_w_px)
        by = 0
        img.paste(bimg.convert("RGBA"), (bx, by))

        # text runs directly under barcode
        font1 = load_font("Calibri.ttf", TEXT1_PX)
        font2 = load_font("Calibri.ttf", TEXT2_PX)

        t1 = BARCODE_DATA
        t1_w, t1_h = draw.textbbox((0, 0), t1, font=font1)[2:]
        t1_x = center_x(W, t1_w)
        t1_y = by + target_h_px
        draw.text((t1_x, t1_y), t1, fill="black", font=font1)

        t2 = LINE2_TEXT
        t2_w, t2_h = draw.textbbox((0, 0), t2, font=font2)[2:]
        t2_x = center_x(W, t2_w)
        t2_y = t1_y + t1_h + TEXT_GAP_PX
        draw.text((t2_x, t2_y), t2, fill="black", font=font2)

        # If you still overflow, uncomment the assert to catch it:
        # assert t2_y + t2_h <= H, f"Content exceeds label height: {(t2_y + t2_h)} > {H}"

    return img.convert("RGB")

def print_image_exact_size(img, printer_name):
    """
    Print the image at EXACT physical size (no stretching to full page).
    We convert label size (cm) to device pixels using the printer's DPI.
    """
    # Open printer/DC
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)

        # Get printer device DPI
        dpix = hDC.GetDeviceCaps(win32con.LOGPIXELSX)
        dpiy = hDC.GetDeviceCaps(win32con.LOGPIXELSY)

        # Convert our label physical size into device pixels
        dest_w = int(round(LABEL_W_CM / 2.54 * dpix))
        dest_h = int(round(LABEL_H_CM / 2.54 * dpiy))

        # Top-left corner to (0,0). If you want a tiny inset, use (1,1)
        left = 0
        top = 0
        right = left + dest_w
        bottom = top + dest_h

        # Start GDI job
        hDC.StartDoc("Label Image (Exact Size)")
        hDC.StartPage()

        # Draw the bitmap to the exact rectangle (no full-page stretch!)
        dib = ImageWin.Dib(img)
        dib.draw(hDC.GetHandleOutput(), (left, top, right, bottom))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
    finally:
        win32print.ClosePrinter(hPrinter)

if __name__ == "__main__":
    # Compose tiny label image
    label_img = compose_label_image()

    # Optional debug: save to check layout visually
    # label_img.save("debug_label.png")

    # IMPORTANT: In the printer driver, set paper/label size to 5.5 x 2.0 cm.
    # Then this prints at exact size and should NOT advance extra labels.
    print_image_exact_size(label_img, PRINTER_NAME)
    print("✅ Printed compact label at exact physical size.")
