from flask import Flask, request, make_response, send_from_directory, abort, send_file
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
    filename = data['name']+"_"+str(int(datetime.now().timestamp()))+".pdf"
    file_path = convert_html_to_pdf(data, filename)
    return send_file(file_path, as_attachment=True, download_name=filename)
   

if __name__ == "__main__":
    app.run(os.getenv("HOST"), os.getenv("PORT"), debug=True)


