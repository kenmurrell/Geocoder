from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from geocode import Geocode
from threading import Thread
app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_ROOT, 'data/')
CONFIG_DIR = os.path.join(APP_ROOT, 'config/')
key_file = 'key.xml'
outfile = 'out.csv'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/loading')
def loading():
    i = int(request.args['ctr'])
    ctr = int(i/2)
    return render_template('loading.html', estimate = ctr)

@app.route('/upload', methods=['POST'])
def upload():
    for file in request.files.getlist("file"):
        filename = file.filename
        csv_in = "/".join([DATA_DIR, filename])
        file.save(csv_in)
        key = "/".join([CONFIG_DIR, 'key.xml'])
        engine = Geocode(key)
        csv_out = "/".join([DATA_DIR, outfile])
        i=engine.csv_count(csv_in)
        thr = Thread(target=engine.generate, args=[csv_in, csv_out])
        thr.start()
    return redirect(url_for('loading',ctr=i))

@app.route('/download')
def download():
        return render_template('download.html')

@app.route('/return-files/')
def return_files():
    csv_out = "/".join([DATA_DIR, outfile])
    print(csv_out)
    return send_file(csv_out, as_attachment=True, attachment_filename="out.csv")

if __name__ == '__main__':
    app.secret_key = 'bewbs'
    app.run(threaded=True, debug=True)
