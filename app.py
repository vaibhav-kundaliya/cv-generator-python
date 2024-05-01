from flask import Flask, request, make_response, send_file, abort, send_from_directory,after_this_request
from utility import convert_html_to_pdf
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/", methods=['POST'])
def getPDFfile():
    data = request.json
    filename = data['name']+str(int(datetime.now().timestamp()))+".pdf"
    file_path = convert_html_to_pdf(data, filename)
    # return send_file(file_path, as_attachment=True, download_name=data['name']+".pdf")
    return make_response({"fileUrl":request.host_url+"download/"+filename})
   

@app.route('/download/<filename>')
def download_file(filename):
    @after_this_request
    def delete_file(response):
        try:
            # File path to delete
            file_path = os.path.join('PDFs', filename)
            if os.path.exists(file_path):
                os.remove(file_path)  # Delete the file
                print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {e}")
        
        return response  # Return the original response
    
    return send_from_directory('PDFs', filename)

if __name__ == "__main__":
    try:
        os.mkdir("PDFs")
    except:
        pass
    app.run(os.getenv("HOST"), os.getenv("PORT"), debug=True)


