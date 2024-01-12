import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def train_regression_model(X_data_vac, full_grouped):
    # Переименование колонок
    full_grouped.rename(columns={'Country/Region': 'country', 'Date': 'date'}, inplace=True)

    # Преобразование дат в datetime
    X_data_vac['date'] = pd.to_datetime(X_data_vac['date'])

    # Объединение по колонкам 'country' и 'date'
    merged_data = pd.merge(X_data_vac, full_grouped, on=['country', 'date'], how='inner')

    # Создание объекта LabelEncoder
    label_encoder = LabelEncoder()

    # Применение Label Encoding к колонке 'country'
    merged_data['country_encoded'] = label_encoder.fit_transform(merged_data['country'])

    # Выделение признаков (features) и целевой переменной (target)
    features = merged_data[['total_vaccinations', 'country_encoded', 'Active']]
    features['year'] = pd.to_datetime(merged_data['date']).dt.year
    features['month'] = pd.to_datetime(merged_data['date']).dt.month
    features['day'] = pd.to_datetime(merged_data['date']).dt.day
    target = merged_data['New deaths']

    # Разделение данных на обучающий и тестовый наборы
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Создание и обучение модели линейной регрессии
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Прогнозирование 'New deaths' на тестовых данных
    predictions = model.predict(X_test)

    # Оценка качества модели
    mae = mean_absolute_error(y_test, predictions)

    print(f"Mean Absolute Error: {mae}")

    return model  # Возвращаем обученную модель