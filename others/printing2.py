import subprocess

dpl = b"""
\x02L
S2.2,0.8
H30
R20
D11
150050001000011HELLO DPL
Q1
Z
"""

with open("C:\\Users\\ilyas\\Desktop\\test.dpl", "wb") as f:
    f.write(dpl)

subprocess.run(["notepad.exe", "/p", "C:\\Users\\ilyas\\Desktop\\test.dpl"])
