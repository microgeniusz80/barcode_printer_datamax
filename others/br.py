import ctypes
import win32print

# Exact printer name from Devices and Printers
printer_name = "Datamax-O'Neil E-4204B Mark III"

# Your raw DPL content
raw_data = b"\x02L\r\nD31\r\n191300001000011PYTHON RAW PRINT\r\nQ1\r\nZ\r\n"
data_len = len(raw_data)

# Windows structures
class DOCINFO(ctypes.Structure):
    _fields_ = [("pDocName", ctypes.c_wchar_p),
                ("pOutputFile", ctypes.c_wchar_p),
                ("pDataType", ctypes.c_wchar_p)]

# Open printer
printer_handle = win32print.OpenPrinter(printer_name)

# Prepare doc info
doc_info = DOCINFO()
doc_info.pDocName = "Python DPL Raw"
doc_info.pOutputFile = None
doc_info.pDataType = "RAW"

# Start document
job_id = win32print.StartDocPrinter(printer_handle, 1, doc_info)
win32print.StartPagePrinter(printer_handle)

# Send raw bytes
written = ctypes.windll.winspool.drv.WritePrinter(printer_handle, raw_data, data_len, ctypes.byref(ctypes.c_ulong()))

# End print job
win32print.EndPagePrinter(printer_handle)
win32print.EndDocPrinter(printer_handle)
win32print.ClosePrinter(printer_handle)

print(f"✅ Sent {data_len} bytes to printer using ctypes")
