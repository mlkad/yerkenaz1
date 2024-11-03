from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd

# import os
import os

# Определяем относительный путь к файлам данных
file_paths = {
    'trips': os.path.join('data', 'trips.csv'),
    'run_data': os.path.join('data', 'run_data.csv'),
    'dwell_sorted': os.path.join('data', 'dwell_sorted.csv')
}


# Чтение данных
trips = pd.read_csv(file_paths['trips'])
run_data = pd.read_csv(file_paths['run_data'])
dwell_sorted = pd.read_csv(file_paths['dwell_sorted'])

# Объединение данных
data = trips.merge(run_data, on='trip_id').merge(dwell_sorted, on='trip_id')

# Преобразование времени в datetime
data['arrival_time'] = pd.to_datetime(data['arrival_time'], format='%H:%M:%S')
data['departure_time'] = pd.to_datetime(data['departure_time'], format='%H:%M:%S')
data['arrival_hour'] = data['arrival_time'].dt.hour
data['arrival_weekday'] = data['arrival_time'].dt.weekday

# Определение признаков и целевой переменной
X = data[['arrival_hour', 'arrival_weekday', 'dwell_time_in_seconds']]
y = data['arrival_time'].dt.hour + data['arrival_time'].dt.minute / 60

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f'RMSE: {rmse:.2f}')

# Пример предсказания
new_data = pd.DataFrame({'arrival_hour': [8], 'arrival_weekday': [0], 'dwell_time_in_seconds': [30]})
predicted_arrival = model.predict(new_data)
print(f'Предсказанное время прибытия (в часах): {predicted_arrival[0]:.2f}')
