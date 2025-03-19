from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, Transaction , User 
from Forms import TransactionForm
from sqlalchemy import text
from datetime import datetime, timedelta


transactions_bp = Blueprint('transactions', __name__, template_folder='templates', url_prefix='/transactions')

def get_transactions():
    expense_query = text("""
        SELECT category, SUM(amount) AS total_amount 
        FROM "transaction"
        WHERE user_id = :user_id AND transaction_type = 'expense'
        GROUP BY category
        ORDER BY total_amount DESC
        LIMIT 10;
    """)

    earning_query = text("""
        SELECT category, SUM(amount) AS total_amount 
        FROM "transaction"
        WHERE user_id = :user_id AND transaction_type = 'earning'
        GROUP BY category
        ORDER BY total_amount DESC
        LIMIT 10;
    """)
    latest_querry = text("""
     SELECT id, category, amount, transaction_type, date 
     FROM "transaction"
     WHERE user_id = :user_id
     ORDER BY date DESC
     LIMIT 10;
    """)

  
    # Execute queries
    expense_result = db.session.execute(expense_query, {"user_id": session["user_id"]} ).fetchall()
    earning_result = db.session.execute(earning_query, {"user_id": session["user_id"]}).fetchall()
    latest_records = db.session.execute(latest_querry,{"user_id": session["user_id"]}).fetchall()
    # Convert result to dictionary format
    transactions = {
        "expenses": [{"category": row[0], "amount": row[1]} for row in expense_result],
        "earnings": [{"category": row[0], "amount": row[1]} for row in earning_result],
        "past_ten": [
            {
                "id": row[0],
                "category": row[1],
                "amount": row[2],
                "transaction_type": row[3],
                "date": datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S.%f").date() 
            } 
            for row in latest_records
        ]
    }
    return transactions 

def get_earning_expense_report():
     query = text("""
        SELECT transaction_type, SUM(amount) as amount 
        FROM "transaction" 
        WHERE user_id = :user_id 
        GROUP BY transaction_type;
    """)

     report = db.session.execute(query, {"user_id": session["user_id"]}).fetchall()
     earnings = 0
     expenses = 0
     for row in report:
        if row.transaction_type == "earning":
            earnings = row.amount
        elif row.transaction_type == "expense":
            expenses = row.amount
     
     return {"earnings": earnings, "expenses": expenses}

@transactions_bp.route('/', methods=['GET', 'POST'])
def index():
    if "user_name" not in session:
        flash("Login Required!")
        return redirect(url_for('login', next=request.url))
    else:
        flash(f"Hi {session['user_name']}, have a good day!")
    
    
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            user_id=session['user_id'],
            amount=form.amount.data,
            description=form.description.data,
            category=form.category.data,
            transaction_type=form.transaction_type.data,
            date=form.date.data
        ) 
        db.session.add(transaction)
        db.session.commit()
        flash("Transaction added successfully!", "success")
        return redirect(url_for('transactions.index'))

    recent_records = get_transactions().get('past_ten')
    # query = text("""
    #     SELECT transaction_type, SUM(amount) as amount 
    #     FROM "transaction" 
    #     WHERE user_id = :user_id 
    #     GROUP BY transaction_type;
    # """)

    # report = db.session.execute(query, {"user_id": session["user_id"]}).fetchall()
    # earnings = 0
    # expenses = 0
    # for row in report:
    #     if row.transaction_type == "earning":
    #         earnings = row.amount
    #     elif row.transaction_type == "expense":
    #         expenses = row.amount
    report = get_earning_expense_report()

    return render_template('transaction.html', form=form , recent_records = recent_records , earnings=report['earnings'], expenses=report['expenses'])

# API to get transaction data for Chart.js
@transactions_bp.route('/data')
def add_transactions():
    if "user_name" not in session:
        return jsonify({"error": "Login required"}), 401

    transactions = get_transactions()
    return jsonify(transactions)  

# Add delete functionality
@transactions_bp.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    if "user_name" not in session:
        return jsonify({"error": "Login required"}), 401
    
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=session["user_id"]).first()
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        flash("Transaction deleted successfully!", "success")
        recent_records = get_transactions().get('past_ten')
        form = TransactionForm()
        report = get_earning_expense_report()
        return render_template('transaction.html', form=form , recent_records = recent_records , earnings=report['earnings'], expenses=report['expenses'])

        
    else:
        return jsonify({"error": "Transaction not found"}), 404

@transactions_bp.route('/history')
def history():
    if "user_name" not in session:  
        return jsonify({"error": "Login required"}), 401

    # Get all transactions for the logged-in user
    detailed_history = Transaction.query.filter_by(user_id=session["user_id"]).all()

    # Convert the query results to a list of dictionaries
    history_list = [
        {
            "id": transaction.id,
            "category": transaction.category,
            "amount": transaction.amount,
            "transaction_type": transaction.transaction_type,
            "date": transaction.date.strftime("%Y-%m-%d"),  # Format date properly
        }
        for transaction in detailed_history
    ]

    return jsonify(history_list)

