from flask import Flask, request, make_response, send_from_directory, abort
from utility import convert_html_to_pdf
from datetime import datetime
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import cloudinary
import cloudinary.uploader
from memory_profiler import memory_usage

load_dotenv()
app = Flask(__name__)
print(
    "cloud_name",os.getenv("CLOUD_NAME"),
    "api_key",os.getenv("CLOUD_API_KEY"),
    "api_secret",os.getenv("CLOUD_APP_SECRET"),
)
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUD_API_KEY"),
    api_secret=os.getenv("CLOUD_APP_SECRET"),
    secure=True,
)
scheduler = BackgroundScheduler()

@app.before_request
def before_request():
    print("hello")
    request.start_memory = memory_usage()[0] 

@app.after_request
def after_request(response):
    end_memory = memory_usage()  # Capture end memory
    print(end_memory)
    return response

@app.route("/", methods=["POST"])
def getPDFfile():
    data = request.json
    filename = data["name"] + str(int(datetime.now().timestamp())) + ".pdf"
    file_path = convert_html_to_pdf(data, filename)
    # temp = cloudinary.uploader.upload(
    #     file_path,
    #     folder="whiteLabelCV/",
    #     public_id="whitelabelcv",
    #     overwrite=True,
    # )
    # print(temp)
    # return send_file(file_path, as_attachment=True, download_name=data['name']+".pdf")
    return make_response({"fileUrl": request.host_url + "download/" + filename})


@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join("PDFs", filename)
    if os.path.exists(file_path):
        return send_from_directory("PDFs", filename)
    return abort(400, {"message": "Requested CV is not exist"})


def scheduled_task():
    files = os.listdir("PDFs")
    for file in files:
        file_path = os.path.join("PDFs", file)
        if os.path.exists(file_path) and datetime.now().timestamp() - os.path.getctime(
            file_path
        ) >= float(os.getenv("CLR_STORAGE")):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {e}")


scheduler.add_job(scheduled_task, CronTrigger.from_crontab("*/30 * * * *"))

scheduler.start()


if __name__ == "__main__":
    try:
        os.mkdir("PDFs")
    except:
        pass
    app.run(os.getenv("HOST"), os.getenv("PORT"), debug=True)
