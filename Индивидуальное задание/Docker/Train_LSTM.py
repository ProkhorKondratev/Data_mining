import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def create_models(X_data_vac):
    # Путь к папке, где будут сохраняться модели
    models_dir = './models'

    # Проверка наличия папки и создание, если она не существует
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    # Исключаем некоторые страны
    excluded_countries = [
        'Bonaire Sint Eustatius and Saba', 'Fiji', 'Falkland Islands', 'Niue', 'Nigeria',
        'Pitcairn', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
        'Saint Helena', 'Tonga', 'Tokelau', 'Timor', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Turkmenistan'
    ]
    X_data_vac = X_data_vac[~X_data_vac['country'].isin(excluded_countries)]

    # Пример для всех стран
    countries = X_data_vac['country'].unique()

    for country in countries:
        country_data = X_data_vac[X_data_vac['country'] == country]
        country_data['date'] = pd.to_datetime(country_data['date'])
        country_data.set_index('date', inplace=True)
        print(country)
        # Масштабирование данных
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(country_data[['total_vaccinations']])

        # Подготовка данных для LSTM
        X, y = [], []
        for i in range(len(scaled_data) - 10):  # Примерное окно данных
            X.append(scaled_data[i:i+10])
            y.append(scaled_data[i+10])
        X, y = np.array(X), np.array(y)

        # Создание модели LSTM
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')

        # Обучение модели
        model.fit(X, y, epochs=100, batch_size=32)

        # Сохранение модели в папку
        model_filename = f'./models/{country}_LSTM_vaccination_model.h5'
        model.save(model_filename)



