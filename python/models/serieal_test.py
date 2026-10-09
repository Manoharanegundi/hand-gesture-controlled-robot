
import serial
import time

print("Connecting to Arduino on COM5...")

try:
    arduino = serial.Serial("COM5", 9600, timeout=2)

    # Allow the Arduino time to reset
    time.sleep(2)

    print("Connected to Arduino!")

    # Send STOP command only
    arduino.write(b"S")
    print("Sent command: S (STOP)")

    time.sleep(1)
    arduino.close()

    print("Serial test complete!")

except serial.SerialException as error:
    print("Serial connection failed:", error)