"""Сбор данных с API ЦБ"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict
import logging
from ..config.settings import Config

logger = logging.getLogger(__name__)

class CBRDataCollector:
    """Класс для работы с API Центробанка"""
    
    def __init__(self, base_url: str = Config.BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Retail Analysis Bot 1.0'
        })
    
    def get_currency_rates(self) -> List[Dict]:
        """Получение текущих курсов валют ЦБ РФ"""
        logger.info("Загрузка курсов валют с сайта ЦБ...")
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            response.encoding = 'windows-1251'
            
            root = ET.fromstring(response.content)
            currencies = []
            
            for valute in root.findall('Valute'):
                try:
                    code = valute.find('CharCode').text
                    if code in Config.CURRENCIES:
                        currency_data = {
                            'date': datetime.now().strftime(Config.DATE_FORMAT),
                            'code': code,
                            'name': valute.find('Name').text.strip(),
                            'nominal': int(valute.find('Nominal').text),
                            'value': float(valute.find('Value').text.replace(',', '.'))
                        }
                        
                        if self._validate_currency_data(currency_data):
                            currencies.append(currency_data)
                        else:
                            logger.warning(f"Пропущена некорректная валюта: {code}")
                            
                except (ValueError, AttributeError) as e:
                    logger.error(f"Ошибка парсинга валюты: {e}")
                    continue
            
            logger.info(f"Успешно загружено {len(currencies)} валют")
            return currencies
            
        except requests.RequestException as e:
            logger.error(f"Ошибка сети при загрузке курсов: {e}")
            return []
        except ET.ParseError as e:
            logger.error(f"Ошибка парсинга XML: {e}")
            return []
    
    def _validate_currency_data(self, data: Dict) -> bool:
        """Проверка корректности данных о валютах"""
        required_fields = ['date', 'code', 'name', 'nominal', 'value']
        if not all(field in data for field in required_fields):
            logger.error(f"Отсутствуют обязательные поля в данных валюты: {data}")
            return False
        
        if data['value'] <= 0:
            logger.warning(f"Некорректное значение курса валюты: {data['value']}")
            return False
            
        return True
