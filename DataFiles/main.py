import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from URLFeatureExtraction import featureExtraction  # Ensure this module is in the same directory

# Step 1: Load the dataset
data = pd.read_csv("5.urldata.csv")  # Replace with the actual path to the file

# Step 2: Preprocess the data
# Exclude 'Domain' column and use only numerical features for training
X = data.iloc[:, 1:-1]  # Features (exclude 'Domain' and 'Label')
y = data.iloc[:, -1]    # Target ('Label')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 4: Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Step 5: Take user input and predict
def predict_url(url):
    # Extract features from the input URL
    features = featureExtraction(url)
    prediction = model.predict([features])[0]
    return "Phishing URL" if prediction == 1 else "Legitimate URL"

# Example: Test with user input
if __name__ == "__main__":
    url = input("Enter a URL: ")
    result = predict_url(url)
    print("The URL is:", result)
