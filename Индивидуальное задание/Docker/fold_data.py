import os

def merge_html_files(result_folder='Results'):
    # Формируем пути к файлам в папке "Results"
    file_paths = [os.path.join(result_folder, f) for f in [
        'Death_over_time.html',
        'vaccination_animation.html',
        'Deaths_vs_Confirmed_time.html',
        'Confirmed_over_time.html'
    ]]

    # Читаем содержимое файлов
    content_list = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            content_list.append(file.read())

    # Объединение содержимого файлов в одну строку с измененными стилями
    combined_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Четыре карты: Заражения, смерти, вакцинации</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            /* Изменение стилей раздела */
            .charts-container {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 40px; /* Увеличение пространства между картами */
            }}
            .chart {{
                width: 100%; /* 100% ширины для каждой карты */
                height: 500px; /* Высота карт */
            }}
        </style>
    </head>
    <body>

    <div class="charts-container">
        <div class="chart">
            <h2>Число смертей за все время</h2>
            {content_list[0]}
        </div>

        <div class="chart">
            <h2>Вакцинации - по данным ВОЗ</h2>
            {content_list[1]}
        </div>

        <div class="chart">
            <h2>Смерти vs Заражения</h2>
            {content_list[2]}
        </div>

        <div class="chart">
            <h2>Заражения за все время</h2>
            {content_list[3]}
        </div>
    </div>

    </body>
    </html>
    '''

    # Сохранение объединенного содержимого в файл
    with open(os.path.join('объединенные_карты.html'), 'w', encoding='utf-8') as file:
        file.write(combined_content)

# Вызов функции, чтобы код не выполнялся при импорте модуля
if __name__ == "__main__":
    merge_html_files()