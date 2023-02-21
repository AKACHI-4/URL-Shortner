from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

#blueprint - allow us to some sort of organisation
bp = Blueprint('urlshort',__name__)

@bp.route('/')
def home() :
    return render_template('home.html', codes=session.keys())

# Jinja - template engine - used a lot

@bp.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST' :
        urls = {}

        if os.path.exists('urls.json') :
            with open('urls.json') as urls_file :
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys() :
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))

        if 'url' in request.form.keys() :
            urls[request.form['code']] = {'url':request.form['url']}    
        else :
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('E:/A 1 A/URL Shortner/urlShort/static/userFiles/' + full_name) 
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json', 'w') as url_file:
            # json.dumps() function will convert a subset of Python objects into a json string. Not all objects are convertible and you may need to create a dictionary of data you wish to expose before serializing to JSON. 
            json.dump(urls,url_file)
            # save user data into the cookies 
            session[request.form['code']] = True

        return render_template('your_url.html', code=request.form['code'])
    else :
        return redirect(url_for('urlshort.home'))

# Variable route
@bp.route('/<string:code>')
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

# Displaying custom error page 
@bp.errorhandler(404)
def page_not_found(error) : 
    return render_template('page_not_found.html'), 404

# Introduce JSON API 
# jsonify - To convert keys into the JSON format and store using
@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
