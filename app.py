from flask import Flask, render_template, request, redirect, url_for,session
import requests
import json
import subprocess

app = Flask(__name__)

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/')
def index():
	return redirect(url_for('home_page'))

@app.route('/classify', methods=['GET'])
def classify_page():
    try:
        url = request.args.get('homepage')
    except Exception as e:
        return render_template('classify.html',error= 'No Input detected', retJson='No request')
    
    try:
        r = requests.get(url)
        retJson = {}
        with open('temp.jpg', 'wb') as f:
            f.write(r.content)
            proc =  subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            ret = proc.communicate()[0]
            proc.wait()
            with open('text.txt') as g:
                retJson = json.load(g)
            return render_template('classify.html', retJson=retJson)
    except:
        return render_template('classify.html', error='Invalid URL', retJson='Invalid Image URL' )

if __name__ =='__main__':
    app.run(debug=True)