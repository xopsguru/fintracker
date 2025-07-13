from app import app, db, Transaction
import pytest
from flask import url_for
from datetime import datetime, timedelta

def test_dashboard_route(client):
    """Test dashboard route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Dashboard' in response.data
    assert b'Total Income' in response.data
    assert b'Total Expenses' in response.data

def test_add_transaction_get(client):
    """Test add transaction form display"""
    response = client.get('/add')
    assert response.status_code == 200
    assert b'Add New Transaction' in response.data
    assert b'Description' in response.data
    assert b'Category' in response.data
    assert b'Amount' in response.data

def test_add_income_transaction(client, sample_transaction):
    """Test adding an income transaction"""
    sample_transaction['category'] = 'Income'
    response = client.post('/add', data=sample_transaction, follow_redirects=True)
    assert response.status_code == 200
    assert b'Transaction added successfully' in response.data
    
    # Verify transaction was added to database
    with client.application.app_context():
        transaction = Transaction.query.first()
        assert transaction.description == sample_transaction['description']
        assert transaction.amount > 0

def test_add_expense_transaction(client, sample_transaction):
    """Test adding an expense transaction"""
    sample_transaction['category'] = 'Food'
    response = client.post('/add', data=sample_transaction, follow_redirects=True)
    assert response.status_code == 200
    assert b'Transaction added successfully' in response.data
    
    # Verify transaction was added to database
    with client.application.app_context():
        transaction = Transaction.query.first()
        assert transaction.description == sample_transaction['description']
        assert transaction.amount < 0

def test_report_route(client):
    """Test report route"""
    response = client.get('/report')
    assert response.status_code == 200
    assert b'Transaction History' in response.data
    assert b'Category Distribution' in response.data
    assert b'Monthly Summary' in response.data

def test_sysinfo_route(client):
    """Test system info route"""
    response = client.get('/sysinfo')
    assert response.status_code == 200
    assert b'CPU Usage' in response.data
    assert b'Memory Usage' in response.data
    assert b'Disk Usage' in response.data

def test_transaction_calculations(client):
    """Test income and expense calculations"""
    # Add test transactions
    transactions = [
        {'description': 'Salary', 'category': 'Income', 'amount': 50000.00},
        {'description': 'Rent', 'category': 'Housing', 'amount': 15000.00},
        {'description': 'Groceries', 'category': 'Food', 'amount': 5000.00}
    ]
    
    for t in transactions:
        client.post('/add', data=t, follow_redirects=True)
    
    response = client.get('/')
    assert response.status_code == 200
    
    # Verify calculations
    with client.application.app_context():
        total_income = sum(t.amount for t in Transaction.query.all() if t.amount > 0)
        total_expenses = sum(abs(t.amount) for t in Transaction.query.all() if t.amount < 0)
        assert total_income == 50000.00
        assert total_expenses == 20000.00 