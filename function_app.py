import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

import base64
import io
import json
import fitz


@app.route(route="http_pdfimage")
def http_pdfimage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    base64_string = req.get_body()
    
    if base64_string:
        try:
            fileString = json.loads(base64_string)["base64_string"]
            logging.info("Requesting file processing")
            fileList = finalpdf2imageb64str(fileString)
            logging.info("Process Complete")
            return func.HttpResponse(json.dumps(fileList), mimetype="application/json", status_code=200)
            # logging.info(file_list)
        except ValueError:
            return func.HttpResponse(ValueError,status_code=500)










# Function to convert Pixmap to base64 string
def pixmap_to_base64(pixmap):
    img_bytes = pixmap.tobytes()
    b64_string = base64.b64encode(img_bytes).decode()
    return b64_string


# PDf to image Base64 conversion 
def finalpdf2imageb64str(b64str):
    # Decode base64 string
    decoded_pdf = base64.b64decode(b64str)
    # Convert bytes to BytesIO object
    pdf_bytes_io = io.BytesIO(decoded_pdf)
    # Open the PDF file from BytesIO
    doc = fitz.open("pdf", pdf_bytes_io)
    # Count variable is to get the number of pages in the pdf
    count = doc.page_count
    b64image = []
    for i in range(count):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        # Convert Pixmap to base64 string
        b64_string = pixmap_to_base64(pix)
        b64image.append(b64_string)
    doc.close()

    return b64image