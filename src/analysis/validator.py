"""Валидация данных"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class DataValidator:
    """Валидатор данных"""
    
    @staticmethod
    def validate_macro_data(data: Dict) -> bool:
        """Проверка корректности макроэкономических данных"""
        required_fields = ['year', 'half_year', 'key_rate', 'inflation', 'food_inflation']
        if not all(field in data for field in required_fields):
            logger.error(f"Отсутствуют обязательные поля в макроданных: {data}")
            return False
        
        if not (2000 <= data['year'] <= 2030):
            logger.warning(f"Некорректный год: {data['year']}")
            return False
            
        return True
