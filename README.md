# AI-Powered Expense Tracker API

This is an AI-powered expense tracker API built using Flask. It allows users to track expenses, view expense summaries, and get expense predictions based on historical data.

## Features

- **Add Expense:** Add a new expense with details such as amount, category, description, and currency.
- **View Expenses:** Retrieve a list of all recorded expenses.
- **View Single Expense:** Retrieve details of a single expense by its ID.
- **Predict Expense:** Get a predicted expense amount for a given category using a simple AI model.
- **Error Handling:** Robust error handling for common issues.
- **Security Measures:** Basic security measures including CORS and graceful error handling.

## Requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- Scikit-learn
- Pandas
- Requests
- python-dotenv

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/brunodagostino/AI-Expense-Tracker.git
    cd AI-Expense-Tracker
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database:**

    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. **Run the Application:**

    ```bash
    python app.py
    ```

## API Endpoints

### Add Expense

- **URL:** `/expenses`
- **Method:** `POST`
- **Body:**
    ```json
    {
        "amount": 25.5,
        "category": "food",
        "description": "Lunch",
        "currency": "USD"
    }
    ```
- **Response:**
    ```json
    {
        "id": 1
    }
    ```

### Get All Expenses

- **URL:** `/expenses`
- **Method:** `GET`
- **Response:**
    ```json
    [
        {
            "id": 1,
            "amount": 25.5,
            "category": "food",
            "description": "Lunch",
            "date": "2023-06-16 14:55:00",
            "currency": "USD"
        }
    ]
    ```

### Get Single Expense

- **URL:** `/expenses/{expense_id}`
- **Method:** `GET`
- **Response:**
    ```json
    {
        "id": 1,
        "amount": 25.5,
        "category": "food",
        "description": "Lunch",
        "date": "2023-06-16 14:55:00",
        "currency": "USD"
    }
    ```

### Predict Expense

- **URL:** `/predict_expense/{category}`
- **Method:** `GET`
- **Response:**
    ```json
    {
        "category": "food",
        "predicted_amount": 23.4
    }
    ```

## Error Handling

- **404 Not Found:**
    ```json
    {
        "error": "Not found"
    }
    ```

- **500 Server Error:**
    ```json
    {
        "error": "Server error"
    }
    ```

## Configuration

The application uses a configuration file (`config.py`) to manage settings. Update the `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI` as needed.

## License

This project is licensed under the GNU License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project uses the following libraries:
- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [Scikit-learn](https://scikit-learn.org/)
- [Pandas](https://pandas.pydata.org/)
- [Requests](https://requests.readthedocs.io/)

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any changes or improvements.

## Contact

For any questions or feedback, please contact me.