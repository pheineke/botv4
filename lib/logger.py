import inspect, os
from datetime import datetime

class Logger:
    def __init__(self):
        caller_file = os.path.basename(inspect.stack()[1].filename)
        current_file = str(os.path.splitext(caller_file)[0])
        try:
            current_file.removeprefix("module-")
        except AttributeError:
            pass
        self.current_file = current_file
        self.make_logfile()

    def make_logfile(self):
        log_dir = os.path.join('log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, f"{self.current_file}.log")
        self.log_file = log_file  # Always assign log_file
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                self.write("Log file created.")

    def write(self, message):
        with open(self.log_file, 'a') as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{self.current_file}] [{current_time}] {message}\n")

    def log(self, message):
        self.write(message)
