import serial
import time

# Replace with the correct COM port (check in Device Manager after pairing HC-06)
PORT = 'COM7'
BAUD = 9600

try:
    bt = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # Give time for HC-06 to connect

    print(f"Connected to {PORT}")
    bt.write(b'hello\n')  # Send the trigger word
    print("Sent 'hello' to HC-06")

except Exception as e:
    print("Error:", e)

finally:
    if 'bt' in locals() and bt.is_open:
        bt.close()
        print("Connection closed.")
