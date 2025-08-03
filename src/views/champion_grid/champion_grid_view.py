import os
from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, 
                           QVBoxLayout, QFrame, QScrollArea, QLineEdit, QHBoxLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QResizeEvent
from data.champions.champions import get_champion_data
from config.font_config import get_font, FontWeight
from services.data_service import DataService
from ..widgets.toggle_switch import ToggleSwitch
from ..widgets.combo_box import IOSStyleComboBox
from .components.champion_frame import ChampionFrame
from config.settings import IMAGES_PATH
from utils.search_utils import match_text

class ChampionGridView(QWidget):
    MIN_COLUMNS = 1
    MAX_COLUMNS = 8
    CHAMPION_WIDTH = 100

    def __init__(self, on_champion_select=None, on_status_change=None):
        super().__init__()
        self.champions = []
        self.data_service = DataService()
        self.on_champion_select = on_champion_select
        self.on_status_change = on_status_change
        self.is_dark_mode = False
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        search_container = self.create_search_container()
        self.main_layout.addWidget(search_container)
        
        border = QFrame()
        border.setObjectName("border")
        border.setFixedHeight(1)
        self.main_layout.addWidget(border)
        
        scroll = self.create_scroll_area()
        self.main_layout.addWidget(scroll)
        
        self.apply_style()

    def create_search_container(self):
        container = QWidget()
        container.setObjectName("searchContainer")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        search_box = QWidget()
        search_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        search_layout = QHBoxLayout(search_box)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("챔피언 검색")
        self.search_input.setFont(get_font(12, FontWeight.BOLD))
        self.search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_input.setObjectName("searchInput")
        self.search_input.textChanged.connect(self.filter_champions)
        search_layout.addWidget(self.search_input)
        
        self.sort_combo = IOSStyleComboBox()
        self.sort_combo.addItems(["가나다순", "우승한 순", "우승 안한 순"])
        self.sort_combo.currentIndexChanged.connect(self.filter_champions)
        
        self.show_unchecked = ToggleSwitch("비우승만")
        self.show_unchecked.stateChanged.connect(self.filter_champions)

        win_count_container = self.create_win_count_container()
        
        separator = self.create_separator()

        layout.addWidget(search_box)
        layout.addWidget(separator)
        layout.addWidget(self.sort_combo)
        layout.addWidget(self.show_unchecked)
        layout.addWidget(win_count_container)
        
        return container

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()

    def apply_style(self):
        bg_color = '#1E1E1E' if self.is_dark_mode else 'white'
        border_color = '#333333' if self.is_dark_mode else '#eeeeee'
        text_color = 'white' if self.is_dark_mode else '#333333'
        placeholder_color = '#666666' if self.is_dark_mode else '#999999'
        scroll_bg = '#2D2D2D' if self.is_dark_mode else '#f0f0f0'
        scroll_handle = '#666666' if self.is_dark_mode else '#cccccc'
        
        self.setStyleSheet(f"""
            QWidget#searchContainer {{
                background-color: {bg_color};
            }}
            
            QWidget#border {{
                background-color: {border_color};
            }}
            
            QLineEdit#searchInput {{
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 8px 12px;
                background: {bg_color};
                color: {text_color};
            }}
            
            QLineEdit#searchInput:focus {{
                border: 1px solid {'#555555' if self.is_dark_mode else '#999999'};
            }}
            
            QLineEdit#searchInput::placeholder {{
                color: {placeholder_color};
            }}
            
            QScrollArea {{
                border: none;
                background-color: {bg_color};
            }}
            
            QScrollBar:vertical {{
                border: none;
                background: {scroll_bg};
                width: 8px;
                margin: 0px 0px 0px 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background: {scroll_handle};
                min-height: 20px;
                border-radius: 4px;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
        """)
        
        self.show_unchecked.set_text_color(text_color)
        
        self.sort_combo.set_dark_mode(self.is_dark_mode)
        
        self.content.setStyleSheet(f"background-color: {bg_color};")
        
        for champion in self.champions:
            champion.set_dark_mode(self.is_dark_mode)

    def create_win_count_container(self):
        container = QWidget()
        container.setFixedWidth(60)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(6)

        self.checked_count_label = QLabel()
        self.checked_count_label.setFont(get_font(14, FontWeight.BLACK))
        self.checked_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.checked_count_label.setStyleSheet("""
            color: #4E54C8;
            padding: 4px 8px;
            border-radius: 4px;
            background: rgba(78, 84, 200, 0.1);
            min-width: 30px;  /* 최소 너비 설정 */
        """)
        self.update_checked_count()

        layout.addWidget(self.checked_count_label)
        return container

    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("""
            QFrame {
                background: none;
                border: none;
                border-left: 1px solid #e0e0e0;
                margin: 8px 0;
            }
        """)
        return separator

    def create_border(self):
        border = QFrame()
        border.setStyleSheet("QFrame { background-color: white; border-bottom: 1px solid #eeeeee }")
        border.setFixedHeight(1)
        return border

    def create_scroll_area(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.content = QWidget()
        
        self.grid = QGridLayout(self.content)
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        self.create_champion_frames()
        
        scroll.setWidget(self.content)
        return scroll

    def create_champion_frames(self):
        champions = get_champion_data()
        
        for ko_name, en_name, _ in champions:
            champion_frame = ChampionFrame(
                ko_name, 
                en_name, 
                None,
                self.data_service,
                on_name_click=self.on_champion_select,
                on_status_change=self.on_champion_status_change
            )
            self.champions.append(champion_frame)

        self.organize_grid()
        self.update_checked_count()

    def filter_champions(self, _=None):
        search_text = self.search_input.text()
        sort_option = self.sort_combo.currentText()
        show_only_unchecked = self.show_unchecked.isChecked()
        
        visible_champions = []
        for champion in self.champions:
            name_match = match_text(search_text, champion.ko_name)
            check_match = not show_only_unchecked or not champion.button.isChecked()
            should_show = name_match and check_match
            champion.setVisible(should_show)
            if should_show:
                visible_champions.append(champion)
        
        if sort_option == "가나다순":
            visible_champions.sort(key=lambda x: x.ko_name)
        elif sort_option == "우승한 순":
            visible_champions.sort(key=lambda x: (not x.button.isChecked(), x.ko_name))
        else:
            visible_champions.sort(key=lambda x: (x.button.isChecked(), x.ko_name))
        
        self.organize_filtered_grid(visible_champions)

    def organize_grid(self):
        if hasattr(self, 'search_input') and self.search_input.text():
            visible_champions = [c for c in self.champions if c.isVisible()]
        else:
            visible_champions = self.champions
            
        available_width = self.width() - 20
        columns = max(self.MIN_COLUMNS, 
                     min(self.MAX_COLUMNS, 
                         available_width // self.CHAMPION_WIDTH))
        
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                self.grid.removeWidget(item.widget())
        
        for i, champion_frame in enumerate(visible_champions):
            row = i // columns
            col = i % columns
            if columns == 1:
                self.grid.addWidget(champion_frame, row, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)
            else:
                self.grid.addWidget(champion_frame, row, col)

    def organize_filtered_grid(self, visible_champions):
        available_width = self.width() - 20 
        columns = max(self.MIN_COLUMNS, 
                     min(self.MAX_COLUMNS, 
                         available_width // self.CHAMPION_WIDTH))
        
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                self.grid.removeWidget(item.widget())
        
        for i, champion_frame in enumerate(visible_champions):
            row = i // columns
            col = i % columns
            if columns == 1:
                self.grid.addWidget(champion_frame, row, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)
            else:
                self.grid.addWidget(champion_frame, row, col)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.organize_grid()

    def update_checked_count(self):
        checked_count = sum(1 for champion in self.champions if champion.button.isChecked())
        self.checked_count_label.setText(f"{checked_count}")

    def on_champion_status_change(self, en_name, is_checked):
        if self.on_status_change:
            self.on_status_change(en_name, is_checked)
        self.update_checked_count() 