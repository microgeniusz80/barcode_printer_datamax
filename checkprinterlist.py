import win32print

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
for p in printers:
    print(p[2])  # p[2] is the printer name
