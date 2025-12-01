"""Анализ ритейл-данных"""
import pandas as pd
import numpy as np
from typing import Dict, List
import logging
from ..config.settings import Config

logger = logging.getLogger(__name__)

class RetailAnalyzer:
    """Анализатор ритейл-данных"""
    
    def __init__(self, macro_data: pd.DataFrame):
        self.macro_data = macro_data
        self.analysis_results = {}
    
    def calculate_correlations(self) -> Dict:
        """Расчет корреляций между показателями"""
        logger.info("Расчет корреляций...")
        
        try:
            correlations = self.macro_data[['key_rate', 'inflation', 'food_inflation']].corr()
            
            self.analysis_results['correlations'] = {
                'rate_inflation': round(correlations.loc['key_rate', 'inflation'], 3),
                'rate_food_inflation': round(correlations.loc['key_rate', 'food_inflation'], 3),
                'inflation_food': round(correlations.loc['inflation', 'food_inflation'], 3)
            }
            
            logger.info("Корреляции рассчитаны")
            return self.analysis_results['correlations']
            
        except Exception as e:
            logger.error(f"Ошибка расчета корреляций: {e}")
            return {}
    
    def analyze_trends(self) -> pd.DataFrame:
        """Анализ трендов показателей"""
        logger.info("Анализ трендов...")
        
        try:
            trends_df = self.macro_data.copy()
            
            # Расчет изменений
            trends_df['rate_change'] = trends_df['key_rate'].diff()
            trends_df['inflation_change'] = trends_df['inflation'].diff()
            trends_df['food_inflation_change'] = trends_df['food_inflation'].diff()
            
            # Классификация периодов
            trends_df['risk_level'] = trends_df.apply(
                lambda x: self._classify_risk_level(x['key_rate'], x['food_inflation']), 
                axis=1
            )
            
            self.analysis_results['trends'] = trends_df
            logger.info("Тренды проанализированы")
            return trends_df
            
        except Exception as e:
            logger.error(f"Ошибка анализа трендов: {e}")
            return pd.DataFrame()
    
    def _classify_risk_level(self, key_rate: float, food_inflation: float) -> str:
        """Классификация уровня риска для ритейла"""
        if key_rate > 12 and food_inflation > 15:
            return "КРИТИЧЕСКИЙ"
        elif key_rate > 8 or food_inflation > 10:
            return "ВЫСОКИЙ"
        elif key_rate > 5 or food_inflation > 7:
            return "ПОВЫШЕННЫЙ"
        else:
            return "НОРМАЛЬНЫЙ"
    
    def generate_insights(self) -> Dict:
        """Генерация инсайтов для ритейла"""
        logger.info("Генерация инсайтов...")
        
        try:
            latest = self.macro_data.iloc[-1]
            previous = self.macro_data.iloc[-2]
            
            insights = {
                'current_period': f"{latest['year']}-{latest['half_year']}",
                'key_rate': {
                    'current': latest['key_rate'],
                    'trend': 'рост' if latest['key_rate'] > previous['key_rate'] else 'снижение',
                    'change': abs(latest['key_rate'] - previous['key_rate'])
                },
                'inflation_gap': latest['food_inflation'] - latest['inflation'],
                'recommendations': self._generate_recommendations(latest)
            }
            
            self.analysis_results['insights'] = insights
            logger.info("Инсайты сгенерированы")
            return insights
            
        except Exception as e:
            logger.error(f"Ошибка генерации инсайтов: {e}")
            return {}
    
    def _generate_recommendations(self, data: pd.Series) -> List[str]:
        """Генерация рекомендаций для ритейла"""
        recommendations = []
        
        if data['key_rate'] > 10:
            recommendations.extend([
                "Снизить зависимость от кредитного финансирования",
                "Пересмотреть ценовую политику с учетом дорогих денег"
            ])
        
        if data['food_inflation'] > data['inflation'] + 2:
            recommendations.extend([
                "Увеличить долю товаров с стабильной себестоимостью",
                "Активнее развивать private label бренды"
            ])
        
        if data['key_rate'] > 12:
            recommendations.append("Рассмотреть оптимизацию издержек")
        
        return recommendations if recommendations else ["Текущая стратегия адекватна"]
