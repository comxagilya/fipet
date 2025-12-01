"""Экспорт данных в различные форматы"""
import pandas as pd
from typing import List, Dict
import csv
import json
import logging

logger = logging.getLogger(__name__)

class DataExporter:
    """Класс для экспорта данных"""
    
    @staticmethod
    def export_to_csv(data: List[Dict], filename: str, fieldnames: List[str] = None) -> bool:
        """Безопасный экспорт в CSV"""
        try:
            if not data:
                logger.warning(f"Нет данных для экспорта в {filename}")
                return False
            
            if not fieldnames:
                fieldnames = list(data[0].keys())
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            
            logger.info(f"Данные экспортированы в {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка экспорта в CSV {filename}: {e}")
            return False
    
    @staticmethod
    def export_dataframe_to_csv(df: pd.DataFrame, filename: str) -> bool:
        """Экспорт DataFrame в CSV"""
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"DataFrame экспортирован в {filename}")
            return True
        except Exception as e:
            logger.error(f"Ошибка экспорта DataFrame в {filename}: {e}")
            return False
    
    @staticmethod
    def export_to_json(data: Dict, filename: str) -> bool:
        """Экспорт данных в JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Данные экспортированы в {filename}")
            return True
        except Exception as e:
            logger.error(f"Ошибка экспорта в JSON {filename}: {e}")
            return False
