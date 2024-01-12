# RUN.py

from Loader import scrape_coronavirus_data, load_coronavirus_data, load_vaccination_data
from Data_html_Deaths import visualize_covid_deaths
from Data_html_vactination import  visualize_vaccination_animation
from fold_data import merge_html_files

def main():
    # Шаг 1: Загрузка и обработка данных
    scrape_coronavirus_data()
    coronavirus_data = load_coronavirus_data()
    vaccination_data = load_vaccination_data()

    # Шаг 2: Визуализация данных
    visualize_covid_deaths()
    visualize_vaccination_animation()

    merge_html_files(result_folder='Results')


if __name__ == "__main__":
    main()
