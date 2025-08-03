from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from config.font_config import get_font, FontWeight

class StatItem(QWidget):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value
        self.is_dark_mode = False
        self.init_ui(name, value)
    
    def init_ui(self, name, value):
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.value_label = QLabel(value)
        self.value_label.setFont(get_font(16, FontWeight.BOLD))
        
        self.name_label = QLabel(name)
        self.name_label.setFont(get_font(11, FontWeight.MEDIUM))
        
        layout.addWidget(self.value_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        self.apply_style()

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()

    def apply_style(self):
        text_color = 'white' if self.is_dark_mode else '#333333'
        sub_text_color = '#666666' if self.is_dark_mode else '#666666'
        
        self.value_label.setStyleSheet(f"color: {text_color}")
        self.name_label.setStyleSheet(f"color: {sub_text_color}")

class StatsSection(QWidget):
    def __init__(self, stats_data, champion_data):
        super().__init__()
        self.stats_data = stats_data
        self.champion_data = champion_data
        self.is_dark_mode = False
        self.stat_items = []
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if self.stats_data:
            stats_info = [
                ("순위", f"{self.champion_data['rank']}"),
                ("평균 순위", f"{self.stats_data['avg_rank']}"),
                ("1등 확률", f"{self.stats_data['first_rate']}%"),
                ("픽률", f"{self.stats_data['pick_rate']}%"),
                ("밴율", f"{self.stats_data['ban_rate']}%")
            ]
        else:
            stats_info = [
                ("순위", f"{self.champion_data['rank']}위"),
                ("평균 순위", "-"),
                ("1등 확률", "-"),
                ("픽률", "-"),
                ("밴율", "-")
            ]
        
        for name, value in stats_info:
            stat_item = StatItem(name, value)
            self.stat_items.append(stat_item)
            layout.addWidget(stat_item)
        
        self.setLayout(layout)
        self.apply_style()

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()
        # 모든 StatItem에 다크모드 전달
        for stat_item in self.stat_items:
            stat_item.set_dark_mode(is_dark)

    def apply_style(self):
        bg_color = '#1E1E1E' if self.is_dark_mode else 'white'
        self.setStyleSheet(f"background-color: {bg_color}") 