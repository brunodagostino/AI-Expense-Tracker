from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

from ai_model import predict_expense
from config import Config
from database import db, init_db
from models import Expense

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)
CORS(app)

with app.app_context():
    db.create_all()

auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    if token == app.config["API_KEY"]:
        return token
    return None


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Server error"}), 500


@app.route("/expenses", methods=["POST"])
@auth.login_required
def add_expense():
    data = request.get_json()
    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description")
    currency = data.get("currency", "USD")

    if not amount or not category:
        return jsonify({"error": "Amount and category are required"}), 400

    expense = Expense(
        amount=amount, category=category, description=description, currency=currency
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({"id": expense.id}), 201


@app.route("/expenses", methods=["GET"])
@auth.login_required
def get_expenses():
    amount = request.args.get("amount")
    category = request.args.get("category")
    currency = request.args.get("currency")
    description = request.args.get("description")
    after = request.args.get("after")
    before = request.args.get("before")
    date_range = request.args.get("date_range")

    filters = parse_query(
        amount, category, currency, description, after, before, date_range
    )

    expenses = Expense.query.filter_by(**filters).all()
    return jsonify(
        [
            {
                "id": exp.id,
                "amount": exp.amount,
                "category": exp.category,
                "description": exp.description,
                "date": exp.date.strftime("%Y-%m-%d %H:%M:%S"),
                "currency": exp.currency,
            }
            for exp in expenses
        ]
    )


def parse_query(amount, category, currency, description, after, before, date_range):
    filters = {}
    if amount:
        filters["amount"] = float(amount)
    if category:
        filters["category"] = category
    if currency:
        filters["currency"] = currency
    if description:
        filters["description"] = description
    if after:
        filters["date"] = filters.get("date", {})
        filters["date"]["$gte"] = datetime.strptime(after, "%Y-%m-%d")
    if before:
        filters["date"] = filters.get("date", {})
        filters["date"]["$lte"] = datetime.strptime(before, "%Y-%m-%d")

    # Handle combined date filters
    if "date" in filters:
        date_filters = filters.pop("date")
        if isinstance(date_filters, dict):
            if "$gte" in date_filters and "$lte" in date_filters:
                filters["date"] = db.and_(
                    Expense.date >= date_filters["$gte"],
                    Expense.date <= date_filters["$lte"],
                )
            elif "$gte" in date_filters:
                filters["date"] = Expense.date >= date_filters["$gte"]
            elif "$lte" in date_filters:
                filters["date"] = Expense.date <= date_filters["$lte"]

    return filters


@app.route("/expenses/<int:expense_id>", methods=["GET"])
@auth.login_required
def get_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    return jsonify(
        {
            "id": expense.id,
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description,
            "date": expense.date.strftime("%Y-%m-%d %H:%M:%S"),
            "currency": expense.currency,
        }
    )


@app.route("/predict_expense/<category>", methods=["GET"])
@auth.login_required
def get_predicted_expense(category):
    try:
        predicted_amount = predict_expense(category)
        return jsonify({"category": category, "predicted_amount": predicted_amount})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
