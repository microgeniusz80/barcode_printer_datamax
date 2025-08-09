import os

# Save DPL as a .txt file (so Notepad can open it)
dpl_path = "C:\\Users\\ilyas\\Desktop\\label.txt"

dpl_data = b"""
\x02L
S2.2,0.8
H100
R30
D11
150050001000011HELLO WORLD
Q1
Z
"""



with open(dpl_path, "wb") as f:
    f.write(dpl_data)

# Print using Notepad (auto-associated with .txt)
os.startfile(dpl_path, "print")
