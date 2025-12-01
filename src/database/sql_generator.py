"""Генератор SQL-запросов"""
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class SQLGenerator:
    """Генератор SQL-запросов"""
    
    @staticmethod
    def generate_queries() -> Dict:
        """Генерация SQL-запросов"""
        
        queries = {
            'mysql_8_plus': {
                'analysis_trends': """
                    SELECT 
                        year,
                        half_year,
                        key_rate,
                        inflation,
                        food_inflation,
                        LAG(key_rate) OVER (ORDER BY year, half_year) as prev_key_rate,
                        key_rate - LAG(key_rate) OVER (ORDER BY year, half_year) as rate_change
                    FROM macro_data 
                    ORDER BY year, half_year;
                """
            },
            
            'mysql_legacy': {
                'analysis_trends': """
                    SELECT 
                        m1.year,
                        m1.half_year,
                        m1.key_rate,
                        m1.inflation,
                        m1.food_inflation,
                        m2.key_rate as prev_key_rate,
                        (m1.key_rate - m2.key_rate) as rate_change
                    FROM macro_data m1
                    LEFT JOIN macro_data m2 ON (
                        (m1.year = m2.year AND m1.half_year = 'H2' AND m2.half_year = 'H1') 
                        OR 
                        (m1.year = m2.year + 1 AND m1.half_year = 'H1' AND m2.half_year = 'H2')
                    )
                    ORDER BY m1.year, m1.half_year;
                """
            },
            
            'common': {
                'current_rates': """
                    SELECT * FROM currency_rates 
                    WHERE date = (SELECT MAX(date) FROM currency_rates);
                """
            }
        }
        
        return queries
    
    @staticmethod
    def export_queries_to_files():
        """Экспорт SQL-запросов в файлы"""
        queries = SQLGenerator.generate_queries()
        
        with open('sql_queries.sql', 'w', encoding='utf-8') as f:
            f.write("-- SQL ЗАПРОСЫ ДЛЯ АНАЛИЗА РИТЕЙЛА\n\n")
            
            f.write("-- MySQL 8.0+\n")
            for name, query in queries['mysql_8_plus'].items():
                f.write(f"-- {name}\n{query}\n\n")
            
            f.write("-- MySQL 5.7 и ниже\n")
            for name, query in queries['mysql_legacy'].items():
                f.write(f"-- {name}\n{query}\n\n")
        
        logger.info("SQL-запросы экспортированы в sql_queries.sql")
