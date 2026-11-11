
import time
import serial

PORT = "COM5"
BAUD_RATE = 9600

try:
    with serial.Serial(PORT, BAUD_RATE, timeout=2) as arduino:
        print("Connected to Arduino on", PORT)

        # Arduino Uno may reset when the serial port opens
        time.sleep(2)
        arduino.reset_input_buffer()

        for command in ["F", "B", "L", "R", "S"]:
            arduino.write((command + "\n").encode("ascii"))
            arduino.flush()

            print("Sent command:", command)
            time.sleep(0.5)

        # Allow time for any Arduino response
        time.sleep(0.5)
        response = arduino.read_all().decode(
            "utf-8", errors="replace"
        )

        if response:
            print("Arduino response:")
            print(response)
        else:
            print("No text response received.")
            print("The sketch currently may not acknowledge commands.")

except serial.SerialException as error:
    print("Serial connection failed:", error)
    print("Check COM5 and close Arduino Serial Monitor.")
