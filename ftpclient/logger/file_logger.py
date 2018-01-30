import os.path
import logging

__all__ = ["FtpClientFileLogger"]


class FtpClientFileLogger:
    def __init__(self, path_to_results_dir, log_file_name):
        if not os.path.exists(path_to_results_dir):
            os.makedirs(path_to_results_dir)

        self.path_to_log_file = os.path.join(path_to_results_dir, log_file_name)
        if os.path.exists(self.path_to_log_file):
            os.remove(self.path_to_log_file)

        self.fh = logging.FileHandler(self.path_to_log_file)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(self.formatter)

        self.logger = logging.getLogger('FtpClientLogger')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.fh)
