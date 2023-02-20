from flask import Flask, render_template, request, redirect, url_for, flash, abort
import json
import os.path
from werkzeug.utils import secure_filename

# __name__ is just a intiallizer or name of module which is currently running in flask 
app = Flask(__name__)
app.secret_key = 'h43hs25aber5ldws'

@app.route('/')
def home() :
    return render_template('home.html')

# Jinja - template engine - used a lot

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST' :
        urls = {}

        if os.path.exists('urls.json') :
            with open('urls.json') as urls_file :
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys() :
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('home'))

        if 'url' in request.form.keys() :
            urls[request.form['code']] = {'url':request.form['url']}    
        else :
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('E:/A 1 A/URL Shortner/static/userFiles/' + full_name) 
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json', 'w') as url_file:
            # json.dumps() function will convert a subset of Python objects into a json string. Not all objects are convertible and you may need to create a dictionary of data you wish to expose before serializing to JSON. 
            json.dump(urls,url_file)
        return render_template('your_url.html', code=request.form['code'])
    else :
        return redirect(url_for('home'))

# Variable route
@app.route('/<string:code>')
def redirect_to_url(code) :
    if os.path.exists('urls.json') : 
        with open('urls.json') as urls_file :
            urls = json.load(urls_file)
            if code in urls.keys() :
                # For urls only not for files upload
                if 'url' in urls[code].keys() : 
                    return redirect(urls[code]['url'])
                else :
                    return redirect(url_for('static',  filename='userFiles/' + urls[code]['file']))

    return abort(404)

# For 404 not found page 
@app.errorhandler(404)
def page_not_found(error) : 
    return render_template('page_not_found.html'), 404
