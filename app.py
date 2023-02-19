from flask import Flask, render_template, request, redirect

# __name__ is just a intiallizer or name of module which is currently running in flask 
app = Flask(__name__)

@app.route('/')
def home() :
    return render_template('home.html')

# Jinja - template engine - used a lot

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST' :
        return render_template('your_url.html', code=request.form['code'])
    else :
        return redirect('/')
