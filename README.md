

# Fake Account Detection System

A machine learning-based web application that detects potentially fake social media accounts by analyzing account features and predicting whether an account is genuine or fake.

## Features

- Detects potentially fake social media accounts using machine learning.
- Uses a Random Forest classifier for account classification.
- Provides a user-friendly interface built with HTML, CSS, and JavaScript.
- Uses Flask to handle backend operations and connect the frontend with the machine learning model.
- Includes a separate script for training the machine learning model.

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn, Random Forest Classifier
- **Data Processing:** Pandas, NumPy

## Project Structure

```text
Fake-Account-Detection/
│
├── app.py          # Flask backend
├── train.py        # Model training script
├── templates/      # HTML templates
├── static/         # CSS, JavaScript, and assets
├── model.pkl       # Trained model (if generated)
├── requirements.txt
└── README.md
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone <your-repository-url>
   cd Fake-Account-Detection
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Train the machine learning model:

   ```bash
   python train.py
   ```

4. Run the Flask application:

   ```bash
   python app.py
   ```

5. Open the local URL displayed in the terminal, usually:

   `http://127.0.0.1:5000/`

## How It Works

1. The user enters the required social media account details.
2. The Flask backend receives the input.
3. The trained Random Forest model processes the account features.
4. The application displays the prediction to the user.

## Future Improvements

- Add more account features for better detection.
- Improve model performance using additional training data.
- Enhance the user interface and user experience.

## Disclaimer

This project is developed for educational purposes. Predictions are based on the trained model and should not be treated as definitive proof that an account is fake or genuine.

## Author

Raj Kushwaha
