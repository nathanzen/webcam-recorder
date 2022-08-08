from flask import Flask, send_from_directory, request

from webcam_recorder import WebcamRecorder
from datetime import datetime
import requests


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

    if (not args.get("dir")) and (not args.get("name")):
        return {"message": "missing parameters"}

    try:
        wcd_rec.logger.debug(f"Uploading {args['name']} to client...")
        return send_from_directory(directory=args["dir"], path=args["name"], as_attachment=True)
    except Exception as e:
        return {"message": f"{e}"}


@app.route('/keep_me_alive')
def download_file():
    args = request.args

    url_1 = args.get("a")
    url_2 = args.get("b")

    if (not url_1) and (not url_2):
        return {"message": "missing parameters"}

    if datetime.now().day < 15:
        requests.head(url_1)
        return {"message": "success", "url": url_1}
    else:
        requests.head(url_2)
        return {"message": "success", "url": url_2}


@app.route("/")
def index():
    return f"app_name: {wcd_rec.app_name}"
