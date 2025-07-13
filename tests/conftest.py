import os
import sys
import pytest
from pathlib import Path

# Add the root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app import app as flask_app, db

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    return flask_app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def sample_transaction():
    return {
        'description': 'Test Transaction',
        'category': 'Test',
        'amount': 100.00
    } 