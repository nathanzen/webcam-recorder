from flask import Flask, send_from_directory, request

from webcam_recorder import WebcamRecorder

app = Flask(__name__)
wcd_rec = WebcamRecorder()


@app.route("/get_recordings")
def get_recordings():
    return wcd_rec.get_files()


@app.route("/delete_file")
def delete_file():
    wcd_rec.logger.debug("delete_file called")
    args = request.args

    if args.get("path"):
        wcd_rec.delete_file(args.get("path"))
        return "success"

    return "fail"


@app.route('/download_file')
def download_file():
    wcd_rec.logger.debug("download_file called")
    args = request.args

    if (not args.get("dir")) and (not args.get("name")):
        return "missing parameters"

    try:
        return send_from_directory(directory=args["dir"], path=args["name"], as_attachment=True)
    except Exception as e:
        return f"{e}"


@app.route("/")
def index():
    wcd_rec.logger.debug("index called")
    return f"{wcd_rec.app_name}: there's nothing in here"


if __name__ == "__main__":
    app.run()
