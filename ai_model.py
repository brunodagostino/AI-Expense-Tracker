import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Sample data for training
data = pd.DataFrame(
    {
        "amount": [10, 20, 30, 40, 50],
        "category": ["food", "transport", "accommodation", "food", "transport"],
    }
)

# Encode categorical data
label_encoder = LabelEncoder()
data["category_encoded"] = label_encoder.fit_transform(data["category"])

# Train a simple model
X = data[["category_encoded"]]
y = data["amount"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = LinearRegression()
model.fit(X_train, y_train)


def predict_expense(category: str) -> float:
    category_encoded = label_encoder.transform([category])
    prediction = model.predict([[category_encoded[0]]])
    return prediction[0]
