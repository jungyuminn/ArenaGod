import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea, 
                           QFrame, QHBoxLayout, QLineEdit)
from PyQt6.QtCore import Qt
from config.font_config import get_font, FontWeight
from data.champions.champions import get_champion_by_ko
from data.champions.rankings import CHAMPION_RANKINGS
from .components.champion_rank_item import ChampionRankItem
from config.settings import IMAGES_PATH
from utils.search_utils import match_text

class ChampionRankView(QWidget):
    def __init__(self, on_champion_select=None):
        super().__init__()
        self.on_champion_select = on_champion_select
        self.setFixedWidth(400)
        self.is_dark_mode = False
        self.init_ui()
        self.apply_style()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.create_border())

        search_container = self.create_search_container()
        main_layout.addWidget(search_container)
        main_layout.addWidget(self.create_border())

        header = self.create_header()
        main_layout.addWidget(header)
        main_layout.addWidget(self.create_border())

        scroll = self.create_scroll_area()
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
        self.setObjectName("championRankView")
        self.setMinimumWidth(400)

    def create_border(self):
        border = QFrame()
        border.setObjectName("border")
        border.setFixedHeight(1)
        return border

    def create_search_container(self):
        search_container = QWidget()
        search_container.setObjectName("searchContainer")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 10, 15, 10)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("챔피언 검색")
        self.search_input.setFont(get_font(12, FontWeight.BOLD))
        self.search_input.setObjectName("searchInput")
        self.search_input.textChanged.connect(self.filter_champions)
        
        search_layout.addWidget(self.search_input)
        return search_container

    def create_header(self):
        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(15, 10, 15, 10)
        header_layout.setSpacing(10)

        headers = [
            ("순위", 35, Qt.AlignmentFlag.AlignCenter),
            ("", 36, Qt.AlignmentFlag.AlignCenter),
            ("챔피언", 120, Qt.AlignmentFlag.AlignLeft),
            ("티어", 30, Qt.AlignmentFlag.AlignCenter),
            ("승률", 60, Qt.AlignmentFlag.AlignRight)
        ]

        self.header_labels = []
        for text, width, alignment in headers:
            label = QLabel(text)
            if width:
                if text == "챔피언":
                    label.setMinimumWidth(width)
                else:
                    label.setFixedWidth(width)
            label.setFont(get_font(12, FontWeight.BOLD))
            label.setAlignment(alignment | Qt.AlignmentFlag.AlignVCenter)
            header_layout.addWidget(label, 1 if text == "챔피언" else 0)
            self.header_labels.append(label)

        header.setLayout(header_layout)
        header.setObjectName("header")
        return header

    def create_scroll_area(self):
        scroll = QScrollArea()
        scroll.setObjectName("scrollArea")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QWidget()
        content.setObjectName("scrollContent")
        self.scroll_layout = QVBoxLayout(content)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        self.update_rankings(CHAMPION_RANKINGS)
        scroll.setWidget(content)
        return scroll

    def update_rankings(self, rankings):
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)
        
        for rank, champion_data in enumerate(rankings, 1):
            champion_info = get_champion_by_ko(champion_data['name'])
            
            if champion_info:
                item_data = {
                    'ko_name': champion_data['name'],
                    'en_name': champion_info['en'],
                    'tier': champion_data['tier'],
                    'winrate': float(champion_data['winrate'].rstrip('%')),
                    'image_path': os.path.join(IMAGES_PATH, "champions", f"{champion_info['en']}.png")
                }
                
                rank_item = ChampionRankItem(
                    rank=rank,
                    champion_data=item_data,
                    on_click=self.on_champion_select
                )
                self.scroll_layout.addWidget(rank_item)
        
        self.scroll_layout.addStretch()

    def filter_champions(self, search_text):
        for i in range(self.scroll_layout.count() - 1):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, ChampionRankItem):
                champion_name = widget.champion_data['ko_name']
                should_show = match_text(search_text, champion_name)
                widget.setVisible(should_show)

    def apply_style(self):
        bg_color = '#1E1E1E' if self.is_dark_mode else 'white'
        border_color = '#333333' if self.is_dark_mode else '#eeeeee'
        text_color = 'white' if self.is_dark_mode else '#333333'
        placeholder_color = '#666666' if self.is_dark_mode else '#999999'
        
        self.setStyleSheet(f"""
            QWidget#championRankView {{
                background-color: {bg_color};
            }}
            
            QWidget#border {{
                background-color: {border_color};
            }}
            
            QWidget#searchContainer, QWidget#header {{
                background-color: {bg_color};
            }}
            
            QWidget#scrollContent {{
                background-color: {bg_color};
            }}
            
            QScrollArea {{
                background-color: {bg_color};
                border: none;
            }}
        """)
        
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 8px 12px;
                background: {bg_color};
                color: {text_color};
            }}
            QLineEdit:focus {{
                border: 1px solid {'#555555' if self.is_dark_mode else '#999999'};
            }}
            QLineEdit::placeholder {{
                color: {placeholder_color};
            }}
        """)
        
        for label in self.header_labels:
            label.setStyleSheet(f"color: {placeholder_color};")
        
        scroll = self.findChild(QScrollArea)
        if scroll:
            scroll.setStyleSheet(f"""
                QScrollBar:vertical {{
                    border: none;
                    background: {border_color};
                    width: 8px;
                    margin: 0px 0px 0px 0px;
                }}
                QScrollBar::handle:vertical {{
                    background: {'#666666' if self.is_dark_mode else '#cccccc'};
                    min-height: 20px;
                    border-radius: 4px;
                }}
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    border: none;
                    background: none;
                }}
            """)
        
        for i in range(self.scroll_layout.count() - 1):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, ChampionRankItem):
                widget.set_dark_mode(self.is_dark_mode)

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style() 