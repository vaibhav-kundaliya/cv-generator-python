from flask import Flask, request, send_file, Response
from datetime import datetime
import os
from dotenv import load_dotenv
from xhtml2pdf import pisa
from xhtml2pdf.files import pisaFileObject
import io

load_dotenv()
app = Flask(__name__)


@app.route("/", methods=['POST'])
def getPDFfile():
    data = request.json
    css_style = """

        @page {
            
            size: a4 portrait;
            @frame header_frame {           
                -pdf-frame-content: header_content;
                left: 512pt; width: 512pt; top: 40pt; height: 50pt;
            }
            @frame content_frame {          
                left: 50pt; width: 512pt; top: 100pt; height: 632pt;
            }
            @frame footer_frame {           
                -pdf-frame-content: footer_content;
                left: 50pt; width: 512pt; top: 792pt; height: 20pt;
            }
            @frame logo {
                -pdf-frame-content: logo;
            }
        }
        @font-face {
            font-family: 'Nunito Sans';
            src: url('./fonts/Nunito/Nunito-Regular.ttf');
        }
        @font-face {
            font-family: 'Nunito Sans';
            font-weight: bold; 
            src: url('./fonts/Nunito/Nunito-Bold.ttf');
        }
        body {
            font-family: 'Nunito Sans';
        }
        .main-title{
                text-align: center;
        }
        p,li{
            margin: 0
        }
        h1{
            font-size: 24pt;
        }
        h2{
            font-size: 20pt;
            margin-bottom: 0pt;
        }
        h3{
            font-size: 14pt;
            margin-bottom: 0pt;

        }
        h4,p,li{
            font-size: 12pt
        }

    """
    source_html = f"""
    <!DOCTYPE html>
            <html">
                <head>
                    <title>{data['name']} white labeled cv</title>
                    <style>
                        
                        {css_style}
                    </style>
                </head>

                <body>
                    <!-- Content for Static Frame 'header_frame' -->
                        <img src="./logo.png" id="header_content" height=80 alt="logo" />

                    <!-- Content for Static Frame 'footer_frame' -->
                    <div id="footer_content" style="
                                    padding-top: 5pt;
                                    text-align: center;
                                    border-top: 1px solid #000;">sales@iviewlabs.com | www.iviewlabs.com | +91 98250 84654</div>

                    <!-- HTML Content -->
                    <div class="content" id="content">
                        <div class="main-title">
                            <h1>{data['name']} - {data['role']}</h1>
                        </div>
                    </div>
                    
                    <div style="top: 20pt">
                        {data['content']}
                    </div>
                </body>
            </html>
    """
    # filename = data['name']+"_"+str(int(datetime.now().timestamp()))+".pdf"
  
    bufferFile = io.BytesIO()
    pisaFileObject.getNamedFile = lambda self: self.uri
    pisa_status = pisa.CreatePDF(
        source_html, dest=bufferFile  
    )  

    if pisa_status.err:
        raise Exception("Error while creating PDF")

    bufferFile.seek(0)
    return Response(
        bufferFile,
        mimetype='application/pdf',
        headers={"Content-Disposition": "attachment;filename=generated.pdf"}
    )

   

if __name__ == "__main__":
    app.run(os.getenv("HOST"), os.getenv("PORT"), debug=True)


