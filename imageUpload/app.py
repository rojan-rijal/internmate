import os
from flask import Flask, render_template, request, redirect, send_file
#from s3_demo import list_files, download_file, upload_file

app = Flask(__name__)
UPLOAD_FOLDER = "user_id"
BUCKET = "internmate"

@app.route('/')
def entry_point():
    return 'Hello World!'

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return "file uploaded" 

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
