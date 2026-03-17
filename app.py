from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Expense table model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# Home page - show expenses
@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

# Add expense
@app.route('/add', methods=['GET','POST'])
def add_expense():
    if request.method == 'POST':
        item = request.form['item']
        amount = float(request.form['amount'])
        category = request.form['category']

        new_expense = Expense(item=item, amount=amount, category=category)
        db.session.add(new_expense)
        db.session.commit()
        return redirect('/')

    return render_template('add.html')

# Delete expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect('/')

# Update expense
@app.route('/update/<int:id>', methods=['GET','POST'])
def update_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return redirect('/')

    if request.method == 'POST':
        expense.item = request.form['item']
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']

        db.session.commit()
        return redirect('/')

    return render_template('update.html', expense=expense)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
