import os
import pandas as pd
import numpy as np
import plotly.express as px
import math

def visualize_vaccination_animation():
    # Путь к директории для сохранения результатов
    results_dir = './Results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Проверяем наличие файла
    file_path = "./COVID-19 World Vaccination Progress/country_vaccinations.csv"
    if os.path.exists(file_path):
        vacc_df = pd.read_csv(file_path)

        # Замена названий стран
        replacements = {
            "Czechia": "Czech Republic", 
            "United States": "USA", 
            "United Kingdom": "UK", 
            "Isle of Man": "Isle Of Man",
            "Republic of Ireland": "Ireland",
            "Northern Cyprus" : "Cyprus"
        }
        vacc_df['country'] = vacc_df['country'].replace(replacements)

        # Исключение определенных стран
        countries_to_exclude = ['England', 'Scotland', 'Wales', 'Northern Ireland']
        vacc_df = vacc_df[~vacc_df['country'].isin(countries_to_exclude)]

        # Добавление отсутствующих дат и стран
        dates = vacc_df.date.unique().tolist()
        dates.extend(['2020-12-12', '2020-12-13']) 

        countries = vacc_df.country.unique().tolist()

        short = vacc_df[['date', 'country', 'total_vaccinations']]

        keys = list(zip(short.date.tolist(), short.country.tolist()))
        missing_data = []

        for date in dates:
            for country in countries:
                idx = (date, country)
                if idx not in keys:
                    if date == min(dates):
                        missing_data.append({"date": date, "country": country, "total_vaccinations": 0})
                    else:
                        missing_data.append({"date": date, "country": country, "total_vaccinations": None})

        missing_df = pd.DataFrame(missing_data)

        short = pd.concat([short, missing_df], ignore_index=True)

        short = short.sort_values(['country', 'date'])

        short['total_vaccinations'] = short.groupby('country')['total_vaccinations'].fillna(method='ffill')

        short['log_scale'] = short['total_vaccinations'].apply(lambda x: math.log2(x + 1) if x else None)

        # Создаем график
        fig = px.choropleth(short, 
                            locations="country", 
                            locationmode='country names',
                            color="log_scale", 
                            hover_name="country", 
                            hover_data=['log_scale', 'total_vaccinations'],
                            animation_frame="date",
                            color_continuous_scale="BuGn")

        title = "Вакцинации - по данным ВОЗ"
        fig.update_layout(title=title, title_x=0.5, coloraxis_showscale=False)
        fig.update_layout(coloraxis={"cmax": 25, "cmin": 0})

        # Показываем график
        fig.show()

        # Сохраняем HTML в папку "Results"
        html_file_path = os.path.join(results_dir, 'vaccination_animation.html')
        fig.write_html(html_file_path)

        print(f'График сохранен в {html_file_path}')
    else:
        print('Файл с данными о вакцинации не существует. Пожалуйста, убедитесь в его наличии.')

if __name__ == "__main__":
    visualize_vaccination_animation()
