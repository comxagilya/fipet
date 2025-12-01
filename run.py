#!/usr/bin/env python3
"""
Основной скрипт для запуска анализа ритейла
"""

import sys
import os
import logging

# Добавляется src в путь Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pipeline.main_pipeline import RetailAnalysisPipeline

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('retail_analysis.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def main():
    """Основная функция"""
    logger = setup_logging()
    
    print("\n" + "=" * 70)
    print("АНАЛИЗ МАКРОЭКОНОМИЧЕСКИХ ДАННЫХ ДЛЯ РИТЕЙЛА 'ЛЕНТА'")
    print("=" * 70)
    
    try:
        pipeline = RetailAnalysisPipeline()
        pipeline.run_full_analysis()
        
        print("\n Анализ завершен!")
        print("📁 Созданные файлы:")
        print("  • currency_rates.csv - курсы валют")
        print("  • macro_data.csv - макроэкономические данные")
        print("  • simple_dashboard.png - визуализация")
        print("  • sql_queries.sql - SQL запросы")
        print("  • retail_analysis.log - лог выполнения")
        
    except KeyboardInterrupt:
        logger.info("Анализ прерван пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
