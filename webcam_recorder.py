import logging
import os
import random
import string
from logging import Formatter
from logging.handlers import SysLogHandler


class WebcamRecorder:
    LINK = "https://github.com/WebcamDownloader/WebcamDownloader/releases/download/v0.4.4/WebcamDownloaderLinux_18.04_cli"

    def __init__(self, users):
        self.users = users

        self.app_name = f"{self.__class__.__name__}_{''.join(random.choice(string.ascii_letters) for _ in range(5))}"

        syslog = SysLogHandler(address=('logs5.papertrailapp.com', 29534))
        syslog.setFormatter(Formatter(f"{self.app_name}: [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s",
                                      datefmt='%b %d %H:%M:%S'))

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(syslog)
        logger.debug(f"Running {self.app_name}")
        self.logger = logger

        module_dir = os.path.dirname(__file__)
        self.download_dir = module_dir + "/downloads"

        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        os.system(f"cd {module_dir} && wget \"{self.LINK}\"")
        executable_file = os.path.join(module_dir, os.path.basename(self.LINK))
        os.system(f"chmod +x {executable_file}")

        os.system(f"{executable_file} settings download-dir {self.download_dir}")

        for user in users:
            os.system(f"{executable_file} add stripchat {user} --autodownload")

        os.system(f"{executable_file} download &")

    def get_files(self):
        self.logger.debug("get_recordings called")

        return [{
            "name": file_name,
            "path": os.path.join(self.download_dir, file_name),
            "dir": self.download_dir,
            "size": os.path.getsize(os.path.join(self.download_dir, file_name))
        } for file_name in os.listdir(self.download_dir)
            if os.path.isfile(os.path.join(self.download_dir, file_name))]

    def get_users(self):
        self.logger.debug("get_users called")

        return self.users

    @staticmethod
    def delete_file(path):
        os.remove(path)
