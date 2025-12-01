"""Основной пайплайн анализа"""
import pandas as pd
from datetime import datetime
from typing import List, Dict
import logging
from ..data.collector import CBRDataCollector
from ..data.exporter import DataExporter
from ..analysis.analyzer import RetailAnalyzer
from ..analysis.validator import DataValidator
from ..visualization.dashboard import DashboardCreator
from ..database.sql_generator import SQLGenerator
from ..config.settings import Config

logger = logging.getLogger(__name__)

class RetailAnalysisPipeline:
    """Основной пайплайн анализа ритейла"""
    
    def __init__(self):
        self.collector = CBRDataCollector()
        self.exporter = DataExporter()
        self.visualizer = DashboardCreator()
    
    def run_full_analysis(self):
        """Запуск полного анализа"""
        logger.info("ЗАПУСК ПОЛНОГО АНАЛИЗА ДЛЯ 'ЛЕНТЫ'")
        
        try:
            # 1. Сбор данных
            currency_data = self.collector.get_currency_rates()
            macro_df = self._create_macro_data()
            
            if macro_df.empty:
                logger.error("Не удалось создать макроэкономические данные")
                return
            
            # 2. Аналитика
            analyzer = RetailAnalyzer(macro_df)
            correlations = analyzer.calculate_correlations()
            trends_df = analyzer.analyze_trends()
            insights = analyzer.generate_insights()
            
            # 3. Визуализация
            self.visualizer.create_simple_dashboard(macro_df, currency_data)
            
            # 4. Экспорт данных
            self._export_all_data(currency_data, macro_df, trends_df, insights, correlations)
            
            # 5. Генерация SQL
            SQLGenerator.export_queries_to_files()
            
            # 6. Финальный отчет
            self._generate_final_report(insights, correlations, currency_data)
            
            logger.info("АНАЛИЗ УСПЕШНО ЗАВЕРШЕН!")
            
        except Exception as e:
            logger.error(f"КРИТИЧЕСКАЯ ОШИБКА В ПАЙПЛАЙНЕ: {e}")
            raise
    
    def _create_macro_data(self) -> pd.DataFrame:
        """Создание макроэкономических данных"""
        logger.info("Создание макроэкономических данных...")
        
        try:
            validated_data = []
            for data in Config.MACRO_DATA:
                if DataValidator.validate_macro_data(data):
                    validated_data.append(data)
                else:
                    logger.warning(f"Пропущены некорректные макроданные: {data}")
            
            df = pd.DataFrame(validated_data)
            self.exporter.export_dataframe_to_csv(df, 'macro_data.csv')
            
            logger.info(f"Создано {len(df)} записей макроданных")
            return df
            
        except Exception as e:
            logger.error(f"Ошибка создания макроданных: {e}")
            return pd.DataFrame()
    
    def _export_all_data(self, currency_data: List[Dict], macro_df: pd.DataFrame,
                        trends_df: pd.DataFrame, insights: Dict, correlations: Dict):
        """Экспорт всех данных"""
        logger.info("Экспорт всех данных...")
        
        # CSV файлы
        self.exporter.export_to_csv(currency_data, 'currency_rates.csv')
        self.exporter.export_dataframe_to_csv(trends_df, 'trends_analysis.csv')
        
        # JSON файлы
        self.exporter.export_to_json({
            'insights': insights,
            'correlations': correlations,
            'generated_at': datetime.now().isoformat()
        }, 'analysis_insights.json')
        
        logger.info("Все данные экспортированы")
    
    def _generate_final_report(self, insights: Dict, correlations: Dict, currency_data: List[Dict]):
        """Генерация финального отчета"""
        logger.info("\n" + "=" * 60)
        logger.info("ИТОГОВЫЙ ОТЧЕТ ДЛЯ 'ЛЕНТЫ'")
        logger.info("=" * 60)
        
        logger.info(f"Текущий период: {insights.get('current_period', 'N/A')}")
        logger.info(f"Ключевая ставка: {insights.get('key_rate', {}).get('current', 'N/A')}%")
        logger.info(f"Корреляция ставка-инфляция: {correlations.get('rate_inflation', 'N/A')}")
