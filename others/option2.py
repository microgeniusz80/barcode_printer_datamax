import os

dpl_code = b"\x02L\r\nD31\r\n191300001000011STARTFILE TEST\r\nQ1\r\nZ\r\n"

with open("C:\\temp\\label.dpl", "wb") as f:
    f.write(dpl_code)

# Trigger default print for the file using associated app
os.startfile("C:\\temp\\label.dpl", "print")
