import os
import pandas as pd
import pickle
from statsmodels.tsa.statespace.sarimax import SARIMAX

def train_sarimax_models(full_grouped, models_dir='./models'):
    unique_countries = full_grouped['Country/Region'].unique()

    # Цикл для прогнозирования активных случаев SARIMAX для каждой страны
    for country in unique_countries:
        country_data = full_grouped[full_grouped['Country/Region'] == country]
        
        #
        country_data = country_data[['Date', 'Active']]
        country_data['Date'] = pd.to_datetime(country_data['Date'])
        country_data.set_index('Date', inplace=True)
        
        # Разделение данных на обучающий и тестовый наборы
        train = country_data.iloc[:-30]  # Последние 30 дней оставляем для теста
        test = country_data.iloc[-30:]
        
        # Обучение модели SARIMAX
        order = (1, 1, 1)  
        seasonal_order = (1, 1, 1, 12)  
        
        model = SARIMAX(train['Active'], order=order, seasonal_order=seasonal_order)
        result = model.fit()
        
        # Сохранение модели и параметров
        model_sarima = {
            'order': order,
            'seasonal_order': seasonal_order,
            'params': result.params.tolist()
        }
        
        model_filename = os.path.join(models_dir, f'{country}_SARIMA_model.pkl')
        with open(model_filename, 'wb') as model_file:
            pickle.dump(model_sarima, model_file)


