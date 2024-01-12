import os
import pandas as pd
import numpy as np
import plotly.express as px

def visualize_covid_deaths():
    # Путь к директории для сохранения результатов
    results_dir = './Results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Проверяем наличие файлов
    files_exist = all(os.path.exists(file_path) for file_path in [
        './COVID-19 Dataset/covid_19_clean_complete.csv',
        './COVID-19 Dataset/full_grouped.csv',
        './COVID-19 Dataset/day_wise.csv',
        './COVID-19 Dataset/worldometer_data.csv'
    ])

    # Если файлы существуют, загружаем данные
    if files_exist:
        full_grouped = pd.read_csv('./COVID-19 Dataset/full_grouped.csv')
        full_grouped['Date'] = pd.to_datetime(full_grouped['Date'])

        country_wise = pd.read_csv('./COVID-19 Dataset//country_wise_latest.csv')
        country_wise = country_wise.replace('', np.nan).fillna(0)

        # Создаем график
        fig = px.choropleth(full_grouped, locations="Country/Region", 
                            color=np.log(full_grouped["Deaths"]),
                            locationmode='country names', hover_name="Country/Region", 
                            animation_frame=full_grouped["Date"].dt.strftime('%Y-%m-%d'),
                            title='Число смертей за все время', color_continuous_scale=px.colors.sequential.matter)
        fig.update(layout_coloraxis_showscale=False)
        
        # Показываем график
        fig.show()

        # Сохраняем HTML в папку "Results"
        html_file_path = os.path.join(results_dir, 'Death_over_time.html')
        fig.write_html(html_file_path)

        # Вызываем функции для дополнительных графиков
        plot_stacked(full_grouped, 'Confirmed', results_dir)
       # plot_line(full_grouped, 'Confirmed')
        plot_deaths_vs_confirmed(country_wise, results_dir)

        print(f'График сохранен в {html_file_path}')
    else:
        print('Не все файлы с данными существуют. Пожалуйста, убедитесь в их наличии.')

def plot_stacked(full_grouped, col, results_dir):
    # Создаем график
    fig = px.bar(full_grouped, x="Date", y=col, color='Country/Region', 
                 height=600, title=col, 
                 color_discrete_sequence=px.colors.cyclical.mygbm)
    fig.update_layout(showlegend=True)

    # Показываем график
    fig.show()

    # Сохраняем HTML в папку "Results"
    html_file_path = os.path.join(results_dir, f'{col}_over_time.html')
    fig.write_html(html_file_path)

    print(f'График сохранен в {html_file_path}')

def plot_line(full_grouped, col):
    # Создаем график
    fig = px.line(full_grouped, x="Date", y=col, color='Country/Region', 
                  height=600, title=col, 
                  color_discrete_sequence=px.colors.cyclical.mygbm)
    fig.update_layout(showlegend=True)

    # Показываем график
    fig.show()

def plot_deaths_vs_confirmed(country_wise, results_dir):
    # Создаем график
    fig = px.scatter(country_wise.sort_values('Deaths', ascending=False).iloc[:20, :], 
                 x='Confirmed', y='Deaths', color='Country/Region', size='Confirmed', 
                 height=700, text='Country/Region', log_x=True, log_y=True, 
                 title='Смертность/заражения (Масштаб log10)')
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis_rangeslider_visible=True)
    fig.show()


    # Сохраняем HTML в папку "Results"
    html_file_path = os.path.join(results_dir, 'Deaths_vs_Confirmed_time.html')
    fig.write_html(html_file_path)

    print(f'График сохранен в {html_file_path}')



if __name__ == "__main__":
    visualize_covid_deaths()
