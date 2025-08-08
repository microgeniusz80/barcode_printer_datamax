import win32print
import win32ui

# Change this to match your printer name exactly
printer_name = "Datamax-O'Neil E-4204B Mark III"

# DPL command to print "HELLO"
# This is a very basic label
dpl_data = b"""
^L
D11
H10
191100400200HELLO
Q1
Z
"""

# Open the printer
printer_handle = win32print.OpenPrinter(printer_name)

# Start a raw print job
job_info = ("LabelJob", None, "RAW")
win32print.StartDocPrinter(printer_handle, 1, job_info)
win32print.StartPagePrinter(printer_handle)

# Send the DPL command
win32print.WritePrinter(printer_handle, dpl_data)

# End the job
win32print.EndPagePrinter(printer_handle)
win32print.EndDocPrinter(printer_handle)
win32print.ClosePrinter(printer_handle)

print("✅ DPL sent to printer.")
