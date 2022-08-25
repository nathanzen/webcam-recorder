import calendar
from datetime import datetime

import requests
from flask import Flask, send_from_directory, request

from webcam_recorder import WebcamRecorder

app = Flask(__name__)
wcd_rec = WebcamRecorder(users=["ohbabyy_"])


@app.route("/get_users")
def get_users():
    return wcd_rec.get_users()


@app.route("/get_recordings")
def get_recordings():
    return wcd_rec.get_files()


@app.route("/delete_file")
def delete_file():
    args = request.args

    if args.get("path"):
        wcd_rec.delete_file(args.get("path"))
        return {"message": "success"}

    return {"message": "fail"}


@app.route('/download_file')
def download_file():
    args = request.args

    if (directory := args.get("dir")) and (name := args.get("name")):
        try:
            wcd_rec.logger.debug(f"Uploading {name} to client...")
            return send_from_directory(directory=directory, path=name, as_attachment=True)
        except Exception as e:
            return {"message": f"{e}"}

    return {"message": "missing parameters"}


@app.route('/keep_me_alive')
def keep_me_alive():
    args = request.args

    if (url1 := args.get("a")) and (url2 := args.get("a")):
        now = datetime.now()
        url = url1 if calendar.monthrange(now.year, now.month)[1] // 2 > now.day else url2
        requests.head(url)
        return {"message": "success", "url": url}

    return {"message": "missing parameters"}


@app.route("/")
def index():
    return f"app_name: {wcd_rec.app_name}"
