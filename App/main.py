from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
from modules import CoG_Updater

# flask app
app = Flask(__name__)

# Config app
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.tsv', '.txt']


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    # get request data
    files = request.files
    ts = request.form['userTS']

    # create user folder
    path = os.path.join("uploads", ts)
    os.mkdir(path)

    for f in files:
        # get file
        uploaded_file = files.get(f)

        # set file name
        uploaded_file.filename = secure_filename(uploaded_file.filename)

        # save as stk.tsv if the file
        if "SellerToolKit_Cost_of_Goods" in uploaded_file.filename:
            uploaded_file.filename = secure_filename("stk.tsv")

        # save file
        uploaded_file.save(f"./uploads/{ts}/{uploaded_file.filename}")

    # run CoG updater module
    CoG_Updater(ts).run()

    # return download url
    return url_for('cog') + f"?ts={ts}"


@app.route('/cog', methods=["GET"])
def cog():
    # get request data
    ts = request.args.get('ts', '')

    if ts:
        try:
            # return updated file
            return send_file(f'../uploads/{ts}/updated_stk.txt', mimetype='txt', attachment_filename='updated_stk.txt', as_attachment=True)
        except Exception as e:
            # return 400 if an error occurs while reading the updated file
            print(e)
            return 400, "Error reading the updated file."
    else:
        # return 403 if TS (timestamp) is empty
        return 403, "Session ID can't be empty."
