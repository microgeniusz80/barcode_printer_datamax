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
label_width_cm = 5.5
label_height_cm = 2
barcode_height_px = 100  # Reduce vertical height

# === Generate barcode image (no number below)
barcode = Code128(barcode_data, writer=ImageWriter())
barcode_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
barcode.save(barcode_temp.name, options={
    "write_text": False,           # No number
    "module_height": barcode_height_px,
    "quiet_zone": 1,
})
barcode_temp.close()

# === Create PDF label
pdf = FPDF(orientation='L', unit='cm', format=(label_width_cm, label_height_cm))
pdf.set_auto_page_break(False)
pdf.add_page()
pdf.set_margins(0, 0, 0)

# === Add barcode image
pdf.image(barcode_temp.name, x=0, y=0, w=label_width_cm, h=1.0)  # height 1cm

# === Add number text directly below barcode
pdf.set_y(1.0)  # exact 1cm below top
pdf.set_font("Arial", size=10)
pdf.cell(w=label_width_cm, h=0.5, txt=barcode_data, ln=1, align='C')

# === Add 2nd line text if needed
pdf.set_font("Arial", size=8)
pdf.cell(w=label_width_cm, h=0.5, txt="Your second line here", ln=1, align='C')

# === Save PDF
pdf_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
pdf.output(pdf_temp.name)
pdf_temp.close()

# === Print PDF
if platform.system() == "Windows":
    os.startfile(pdf_temp.name, "print")
else:
    subprocess.run(["lp", pdf_temp.name])

# === Cleanup
os.unlink(barcode_temp.name)
# Optionally delete PDF after some time or confirmation
# os.unlink(pdf_temp.name)
