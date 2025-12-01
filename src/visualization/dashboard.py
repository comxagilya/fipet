"""Создание визуализаций"""
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
import pandas as pd
import logging
from ..config.settings import Config

logger = logging.getLogger(__name__)

class DashboardCreator:
    """Класс для создания визуализаций"""
    
    def __init__(self):
        plt.style.use(Config.PLOT_STYLE)
        self.colors = Config.COLORS
        
    def create_simple_dashboard(self, macro_df: pd.DataFrame, currency_data: List[Dict]):
        """Создание упрощенного дашборда"""
        logger.info("Создание упрощенного дашборда...")
        
        try:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # 1. Основные тренды
            periods = [f"{row['year']}-{row['half_year']}" for _, row in macro_df.iterrows()]
            ax1.plot(periods, macro_df['key_rate'], marker='o', label='Ключевая ставка', linewidth=2)
            ax1.plot(periods, macro_df['inflation'], marker='s', label='Инфляция', linewidth=2)
            ax1.plot(periods, macro_df['food_inflation'], marker='^', label='Инфляция на продукты', linewidth=2)
            ax1.set_title('Динамика макропоказателей')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
            
            # 2. Изменения ставки
            changes = macro_df['key_rate'].diff().fillna(0)
            colors = ['red' if x > 0 else 'green' if x < 0 else 'gray' for x in changes]
            ax2.bar(periods, changes, color=colors, alpha=0.7)
            ax2.set_title('Изменения ключевой ставки')
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
            
            # 3. Инфляция
            x = np.arange(len(macro_df))
            width = 0.35
            ax3.bar(x - width/2, macro_df['inflation'], width, label='Общая инфляция', alpha=0.7)
            ax3.bar(x + width/2, macro_df['food_inflation'], width, label='Продуктовая инфляция', alpha=0.7)
            ax3.set_title('Сравнение инфляции')
            ax3.set_xticks(x)
            ax3.set_xticklabels(periods, rotation=45)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # 4. Курсы валют
            if currency_data:
                codes = [curr['code'] for curr in currency_data]
                rates = [curr['value'] for curr in currency_data]
                ax4.bar(codes, rates, alpha=0.7)
                ax4.set_title('Курсы валют')
                ax4.grid(True, alpha=0.3)
            else:
                ax4.text(0.5, 0.5, 'Нет данных о валютах', ha='center', va='center', transform=ax4.transAxes)
                ax4.set_title('Курсы валют')
            
            plt.tight_layout()
            plt.savefig('simple_dashboard.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info("Упрощенный дашборд сохранен как simple_dashboard.png")
            
        except Exception as e:
            logger.error(f"Ошибка создания упрощенного дашборда: {e}")
