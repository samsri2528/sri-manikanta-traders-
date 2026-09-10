from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'samsri2528'  # Session secret key

# Temporary in-memory databases for demonstration
bank_deposits = []
expenses = []

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Admin login check
        if username == 'admin' and password == 'manikanta123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Username or Password', 'danger')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', deposits=bank_deposits, expenses=expenses)

# Staff can add Bank Deposit without owner password
@app.route('/add_bank_deposit', methods=['GET', 'POST'])
def add_bank_deposit():
    if request.method == 'POST':
        date = request.form.get('deposit_date')
        amount = request.form.get('deposit_amount')
        description = request.form.get('description')
        
        # Save entry directly
        bank_deposits.append({'date': date, 'amount': amount, 'description': description})
        flash('Bank Deposit entry saved successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('add_bank_deposit.html')

# Staff can add Expense entry without owner password
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form.get('expense_date')
        purpose = request.form.get('expense_purpose')
        amount = request.form.get('expense_amount')
        
        # Save entry directly
        expenses.append({'date': date, 'purpose': purpose, 'amount': amount})
        flash('Expense entry saved successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('add_expense.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
