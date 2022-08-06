import logging
import os
import random
import string
from logging.handlers import SysLogHandler

from flask import Flask, send_from_directory, request

# ============ LOGGER ============
project_name = "experiment1a"
app_name = f"{project_name}_{''.join(random.choice(string.ascii_letters) for _ in range(5))}"
formatter = logging.Formatter(f"{app_name}: [%(filename)s:%(lineno)s - %(funcName)20s()] %(message)s", datefmt='%b %d %H:%M:%S')
syslog = SysLogHandler(address=('logs5.papertrailapp.com', 29534))
syslog.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(syslog)
logger.setLevel(logging.DEBUG)
logger.debug("Running module")

# Check if the program is running on render server
render_src_root = os.environ.get("RENDER_SRC_ROOT")

wcd_link = "https://github.com/WebcamDownloader/WebcamDownloader/releases/download/v0.4.4/WebcamDownloaderLinux_18.04_cli"
wcd_name = "WebcamDownloaderLinux_18.04_cli"

app = Flask(__name__)

main_directory = os.path.dirname(__file__)
main_directory = os.path.dirname(main_directory)
download_location = os.path.join(main_directory, "webcams")

if not os.path.exists(download_location):
    os.makedirs(download_location)

executable_file = os.path.join(main_directory, wcd_name)
os.system(f"cd {main_directory} && wget {wcd_link}")  # download the exe file
os.system(f"chmod +x {executable_file}")
os.system(f"{executable_file} settings download-dir {download_location}")

for user in ["ohbabyy_"]:
    os.system(f"{executable_file} add stripchat {user} --autodownload")

os.system(f"{executable_file} download &")


@app.route("/get_recordings")
def get_recordings():
    logger.debug("get_recordings called")

    return [
        {
            "name": file_name,
            "path": os.path.join(download_location, file_name),
            "dir": download_location,
            "size": os.path.getsize(os.path.join(download_location, file_name))
        }

        for file_name in os.listdir(download_location)
        if os.path.isfile(os.path.join(download_location, file_name))
    ]


@app.route("/delete_file")
def get_recordings():
    logger.debug("delete_file called")
    args = request.args

    if args.get("path"):
        os.remove(args.get("path"))
        return "success"

    return "fail"


@app.route('/download_file')
def downloads():
    logger.debug("download_file called")

    args = request.args

    if not args.get("dir"):
        return "missing dir"

    if not args.get("name"):
        return "missing filename"

    try:
        return send_from_directory(directory=args["dir"], path=args["name"], as_attachment=True)
    except Exception as e:
        return f"{e}"


@app.route("/")
def index():
    logger.debug("index called")

    return f"{app_name} there's nothing in here"
