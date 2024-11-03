from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Загрузка обученной модели
model = joblib.load('your_model_filename.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        new_data = pd.DataFrame({
            'arrival_hour': [data['arrival_hour']],
            'arrival_weekday': [data['arrival_weekday']],
            'dwell_time_in_seconds': [data['dwell_time_in_seconds']]
        })
        predicted_arrival = model.predict(new_data)
        return jsonify({'predicted_arrival': predicted_arrival[0]})
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
