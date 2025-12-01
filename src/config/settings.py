"""Конфигурация приложения"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Основные настройки приложения"""
    
    # API Settings
    CURRENCIES = ['USD', 'EUR', 'CNY', 'GBP', 'JPY']
    BASE_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
    DATE_FORMAT = '%Y-%m-%d'
    
    # Макроэкономические данные
    MACRO_DATA = [
        {'year': 2021, 'half_year': 'H1', 'key_rate': 4.25, 'inflation': 5.7, 'food_inflation': 7.2},
        {'year': 2021, 'half_year': 'H2', 'key_rate': 4.25, 'inflation': 8.4, 'food_inflation': 10.8},
        {'year': 2022, 'half_year': 'H1', 'key_rate': 9.50, 'inflation': 16.7, 'food_inflation': 20.5},
        {'year': 2022, 'half_year': 'H2', 'key_rate': 7.50, 'inflation': 12.0, 'food_inflation': 15.3},
        {'year': 2023, 'half_year': 'H1', 'key_rate': 7.50, 'inflation': 3.2, 'food_inflation': 4.1},
        {'year': 2023, 'half_year': 'H2', 'key_rate': 15.00, 'inflation': 7.5, 'food_inflation': 9.2},
        {'year': 2024, 'half_year': 'H1', 'key_rate': 16.00, 'inflation': 6.8, 'food_inflation': 8.1}
    ]
    
    # Настройки визуализации
    PLOT_STYLE = 'seaborn-v0_8'
    FIGURE_SIZE = (16, 12)
    COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B']
    
    # Логирование
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'retail_analysis.log'
