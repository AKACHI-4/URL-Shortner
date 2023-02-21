from flask import Flask

# This file will automatically called by flask to setup our application

def create_app(test_config=None) : 
    app = Flask(__name__) # __name__ is just a intiallizer or name of module which is currently running in flask 
    app.secret_key = 'h43hs25aber5ldws'

    # Importing blueprint
    from . import urlshort
    app.register_blueprint(urlshort.bp)


    return app
