import os
import tempfile
import platform
import subprocess
from fpdf import FPDF
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

# === Config ===
barcode_data = "55667788"
second_line_text = "Product ID 5566"
label_width_cm = 5.5
label_height_cm = 1.9  # Reduced to avoid overflow
barcode_crop_percent = 0.6
barcode_scale = 0.45  # Further reduce size

# === Generate barcode (no number)
with tempfile.TemporaryDirectory() as tmpdir:
    barcode_file = os.path.join(tmpdir, "barcode.png")
    barcode = Code128(barcode_data, writer=ImageWriter())
    barcode.save(barcode_file, options={
        "write_text": False,
        "module_height": 60,   # shorter barcode
        "quiet_zone": 1,
    })

    # === Crop and Resize
    with Image.open(barcode_file) as img:
        width, height = img.size
        crop_height = int(height * barcode_crop_percent)
        img_cropped = img.crop((0, 0, width, crop_height))
        new_width = int(width * barcode_scale)
        img_resized = img_cropped.resize((new_width, crop_height), Image.LANCZOS)

        final_img_path = os.path.join(tmpdir, "barcode_final.png")
        img_resized.save(final_img_path)

    # === PDF Setup
    pdf = FPDF(unit="cm", format=(label_width_cm, label_height_cm))
    pdf.set_auto_page_break(False)
    pdf.set_margins(0, 0, 0)
    pdf.add_page()

    # === Barcode Position
    barcode_h_cm = 0.6
    barcode_w_cm = label_width_cm * barcode_scale
    x_center = (label_width_cm - barcode_w_cm) / 2
    y_cursor = 0

    pdf.image(final_img_path, x=x_center, y=y_cursor, w=barcode_w_cm, h=barcode_h_cm)
    y_cursor += barcode_h_cm

    # === Text lines
    line_h1 = 0.35
    pdf.set_font("Arial", size=7)
    pdf.set_xy(0, y_cursor)
    pdf.cell(label_width_cm, line_h1, barcode_data, align='C')
    y_cursor += line_h1

    line_h2 = 0.35
    pdf.set_font("Arial", size=6)
    pdf.set_xy(0, y_cursor)
    pdf.cell(label_width_cm, line_h2, second_line_text, align='C')
    y_cursor += line_h2

    # === Check total height used
    assert y_cursor <= label_height_cm, f"Content exceeds label height: {y_cursor:.2f} > {label_height_cm}"

    # === Save and Print
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        pdf_path = tmp_pdf.name
        pdf.output(pdf_path)

    if platform.system() == "Windows":
        os.startfile(pdf_path, "print")
    else:
        subprocess.run(["lp", pdf_path])
