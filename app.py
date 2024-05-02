from flask import Flask, request, make_response, send_from_directory, abort
from utility import convert_html_to_pdf
from datetime import datetime
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

load_dotenv()
app = Flask(__name__)

scheduler = BackgroundScheduler()

@app.route("/", methods=['POST'])
def getPDFfile():
    data = request.json
    filename = data['name']+str(int(datetime.now().timestamp()))+".pdf"
    file_path = convert_html_to_pdf(data, filename)
    # return send_file(file_path, as_attachment=True, download_name=data['name']+".pdf")
    return make_response({"fileUrl":request.host_url+"download/"+filename})
   

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join('PDFs', filename)
    if os.path.exists(file_path):
        return send_from_directory('PDFs', filename)
    return abort(400, {"message":"Requested CV is not exist"})

def scheduled_task():
    files = os.listdir("PDFs")
    for file in files:
        file_path = os.path.join('PDFs', file)
        if os.path.exists(file_path) and datetime.now().timestamp() - os.path.getctime(file_path) >= float(os.getenv('CLR_STORAGE')):
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


