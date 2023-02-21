# Specific file that pytest is going to be looking for whenever it's going to be running tests 

import pytest
from urlshort import create_app

# Create two fixtures which help to establish the testing situation 

@pytest.fixture
def app():
    app = create_app()
    yield app

# This fixture is to get a client so that the testing framework can act as if it was a browser and testing out the project for us.
@pytest.fixture
def client(app):
    return app.test_client()

