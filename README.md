# AI-Powered Expense Tracker API

This is an AI-powered expense tracker API built using Flask and using SQLite as the database.

## Features

- **Add Expense:** Add a new expense with details such as amount, category, description, and currency.
- **View Expenses:** Retrieve a list of all recorded expenses.
- **View Single Expense:** Retrieve details of a single expense by its ID.
- **Predict Expense:** Get a predicted expense amount for a given category using a simple AI model.
- **API Key Authentication:** Secure API endpoints with API key authentication.

## Requirements

- Python 3.7+
- Flask

## Installation

### Local Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/brunodagostino/AI-Expense-Tracker.git
    cd AI-Expense-Tracker
    ```

2. **Create a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**

    Create a `.env` file in the project root with the following content:

    ```ini
    SECRET_KEY=your_secret_key
    DATABASE_URL=sqlite:///expenses.db
    API_KEYS=your_api_key
    ```

5. **Initialize the Database:**

    ```bash
    flask shell
    from app import db
    db.create_all()
    exit()
    ```

6. **Run the Application:**

    ```bash
    flask run
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

The application uses environment variables for configuration. Update the `.env` file for local development.

## License

This project is licensed under the GNU License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project uses the following libraries:

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/)

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any changes or improvements.

## Contact

For any questions or feedback, please contact me.