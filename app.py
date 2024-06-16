from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from ai_model import predict_expense
from config import Config
from database import db, init_db
from models import Expense

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)
CORS(app)


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Server error"}), 500


@app.route("/expenses", methods=["POST"])
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
def get_expenses():
    query = request.args.get("q", "")
    filters = parse_query(query)

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


def parse_query(query):
    filters = {}
    if query:
        queries = query.split(" ")
        for q in queries:
            if ":" in q:
                key, value = q.split(":", 1)
                if key == "amount":
                    filters["amount"] = float(value)
                elif key == "category":
                    filters["category"] = value
                elif key == "currency":
                    filters["currency"] = value
                elif key == "date":
                    filters["date"] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                elif key == "description":
                    filters["description"] = value
                elif key == "after":
                    filters["date"] = filters.get("date", {})
                    filters["date"]["$gte"] = datetime.strptime(value, "%Y/%m/%d")
                elif key == "before":
                    filters["date"] = filters.get("date", {})
                    filters["date"]["$lte"] = datetime.strptime(value, "%Y/%m/%d")

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
def get_predicted_expense(category):
    try:
        predicted_amount = predict_expense(category)
        return jsonify({"category": category, "predicted_amount": predicted_amount})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
