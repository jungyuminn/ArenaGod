from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath
from config.font_config import get_font, FontWeight
from config.settings import IMAGES_PATH
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

class ChampionRankItem(QFrame):
    def __init__(self, rank, champion_data, on_click=None):
        super().__init__()
        self.rank = rank
        self.champion_data = champion_data
        self.on_click = on_click
        self.is_dark_mode = False
        self.init_ui()
        self.apply_style()
    
    def get_tier(self, rank):
        """순위에 따른 티어 반환"""
        if rank <= 34:
            return ("1", "#999999")
        elif rank <= 68:
            return ("2", "#999999")
        elif rank <= 102:
            return ("3", "#999999")
        elif rank <= 136:
            return ("4", "#999999")
        else:
            return ("5", "#999999")

    def get_tier_style(self, tier):
        """티어별 스타일 반환"""
        tier_styles = {
            "1": {
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4E54C8, stop:1 #8F94FB)",
                "font_weight": "900",
                "width": "24"
            },
            "2": {
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF6B6B, stop:1 #FF8E8E)",
                "font_weight": "900",
                "width": "24"
            },
            "3": {
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7ED56F, stop:1 #9EF01A)",
                "font_weight": "800",
                "width": "24"
            },
            "4": {
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #98B2D1, stop:1 #B3C4DB)",
                "font_weight": "700",
                "width": "24"
            },
            "5": {
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #A1A1A1, stop:1 #B8B8B8)",
                "font_weight": "700",
                "width": "24"
            }
        }
        return tier_styles.get(tier, tier_styles["5"])

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 3, 10, 3)
        
        # 순위
        self.rank_label = QLabel(f"{self.rank}")
        self.rank_label.setFont(get_font(13, FontWeight.BOLD))
        self.rank_label.setFixedWidth(35)
        self.rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        
        spacer = QWidget()
        
        # 챔피언 이미지
        image_container = self.create_image_container()
        
        # 챔피언 이름
        self.name_label = self.create_name_label()
        
        # 티어 표시
        self.tier_label = self.create_tier_label()
        
        # 승률
        self.winrate_label = self.create_winrate_label()
        
        # 챔피언 이름과 티어 사이의 간격
        name_tier_spacer = QWidget()
        
        layout.addWidget(self.rank_label)
        layout.addWidget(spacer)
        layout.addWidget(image_container)
        layout.addWidget(self.name_label, 1)
        layout.addWidget(name_tier_spacer)
        layout.addWidget(self.tier_label)
        layout.addWidget(self.winrate_label)
        
        self.setLayout(layout)
        self.setFixedHeight(42)
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def create_image_container(self):
        image_container = QFrame()
        image_container.setFixedSize(36, 36)
        image_container.setStyleSheet("background: transparent; border: none")
        
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(0)
        
        image_label = QLabel()
        image_path = self.champion_data['image_path']
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
            
            rounded = QPixmap(scaled_pixmap.size())
            rounded.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            path = QPainterPath()
            path.addRoundedRect(0, 0, 32, 32, 8, 8)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            image_label.setPixmap(rounded)
            
        image_label.setStyleSheet("border: none")
        image_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return image_container

    def create_name_label(self):
        name_label = QLabel(self.champion_data['ko_name'])
        name_label.setFont(get_font(12, FontWeight.BOLD))
        name_label.setMinimumWidth(120)
        name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        return name_label

    def create_tier_label(self):
        tier_value = self.champion_data['tier']
        tier_style = self.get_tier_style(tier_value)
        tier_label = QLabel(f"{tier_value}")
        tier_label.setFont(get_font(11, FontWeight.BLACK))
        tier_label.setStyleSheet(f"""
            QLabel {{
                color: {tier_style['color']};
                background: {tier_style['background']};
                border: none;
                border-radius: 12px;
                padding: 4px 2px;
                font-weight: {tier_style['font_weight']};
            }}
        """)
        tier_label.setFixedWidth(int(tier_style['width']))
        tier_label.setFixedHeight(24)
        tier_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        return tier_label

    def create_winrate_label(self):
        winrate = self.champion_data['winrate']
        winrate_label = QLabel(f"{winrate:.1f}%")
        winrate_label.setFont(get_font(11, FontWeight.BOLD))
        winrate_label.setFixedWidth(60)
        winrate_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return winrate_label

    def apply_style(self):
        bg_color = '#1E1E1E' if self.is_dark_mode else 'white'
        text_color = 'white' if self.is_dark_mode else '#333333'
        border_color = '#333333' if self.is_dark_mode else '#eeeeee'
        hover_color = '#2D2D2D' if self.is_dark_mode else '#f5f5f5'
        sub_text_color = '#666666' if self.is_dark_mode else '#999999'
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 0;
                margin: 0;
                border-bottom: 1px solid {border_color}
            }}
            QFrame:hover {{
                background-color: {hover_color}
            }}
        """)
        
        self.rank_label.setStyleSheet(f"color: {sub_text_color}; background: transparent; border: none")
        self.name_label.setStyleSheet(f"color: {text_color}; background: transparent; border: none")
        self.winrate_label.setStyleSheet(f"color: {sub_text_color}; background: transparent; border: none")

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()

    def mousePressEvent(self, event):
        if self.on_click:
            self.on_click(self.champion_data['ko_name'], self.champion_data['en_name']) 