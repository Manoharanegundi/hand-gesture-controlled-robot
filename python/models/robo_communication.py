
import time
import serial
from serial import SerialException


class RobotCommunication:
    """Manage Arduino serial communication with a periodic heartbeat."""

    def __init__(
        self,
        port="COM5",
        baud_rate=9600,
        simulation=False,
        heartbeat_interval=0.3,
    ):
        self.port = port
        self.baud_rate = baud_rate
        self.simulation = simulation
        self.heartbeat_interval = heartbeat_interval

        self.connection = None
        self.last_command = None
        self.last_sent_time = 0.0

    def connect(self):
        if self.simulation:
            print("[SIMULATION] Communication ready.")
            return True

        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=0.1,
                write_timeout=1,
            )

            # Arduino may reset when the serial port opens.
            time.sleep(2)
            self.connection.reset_input_buffer()

            print(f"[CONNECTED] Arduino on {self.port}")
            return True

        except (SerialException, OSError) as error:
            print(f"[CONNECTION ERROR] {error}")
            self.connection = None
            return False

    def send_command(self, command, force=False):
        if command not in {"F", "B", "L", "R", "S"}:
            print(f"[ERROR] Invalid command: {command!r}")
            return False

        now = time.monotonic()

        # Send when the command changes, or refresh the heartbeat.
        command_changed = command != self.last_command
        heartbeat_due = (
            now - self.last_sent_time >= self.heartbeat_interval
        )

        if not force and not command_changed and not heartbeat_due:
            return True

        try:
            if self.simulation:
                print(f"[SIMULATED ARDUINO] {command}")
            else:
                if self.connection is None or not self.connection.is_open:
                    print("[ERROR] Arduino is not connected.")
                    return False

                # Send one command character; Arduino ignores line endings.
                self.connection.write(command.encode("ascii"))
                self.connection.flush()

                if command_changed or force:
                    print(f"[SENT TO ARDUINO] {command}")

            self.last_command = command
            self.last_sent_time = now
            return True

        except (SerialException, OSError) as error:
            print(f"[SEND ERROR] {error}")
            return False

    def disconnect(self):
        try:
            if self.connection is not None and self.connection.is_open:
                self.send_command("S", force=True)
                self.connection.close()
                print("[DISCONNECTED] Serial port closed.")

        except (SerialException, OSError) as error:
            print(f"[DISCONNECT ERROR] {error}")

        finally:
            self.connection = None
            self.last_command = None
            self.last_sent_time = 0.0
