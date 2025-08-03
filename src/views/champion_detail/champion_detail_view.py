import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QFrame, QScrollArea, QStackedWidget, QHBoxLayout)
from PyQt6.QtCore import Qt, QSize
from data.champions.rankings import CHAMPION_RANKINGS
from data.champions.stats import get_champion_stats
from data.champions.synergies import get_champion_synergies
from data.champions.augments import get_champion_augments
from data.champions.items import get_champion_items
from data.champions.champions import get_champion_by_ko
from config.font_config import get_font, FontWeight
from services.data_service import DataService
from .components.augment_section import AugmentSection
from .components.item_section import StartItemsSection, CoreBuildSection, PrismaticItemSection
from .components.champion_header import ChampionHeader
from .components.stats_section import StatsSection
from config.settings import CHAMPIONS_PATH

class ChampionDetailView(QWidget):
    def __init__(self):
        super().__init__()
        self.data_service = DataService()
        self.current_champion = None
        self.on_champion_status_change = None
        self.on_champion_select = None
        self.is_dark_mode = False
        self.augment_title = None
        
        self.setToolTipDuration(0)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.content = QWidget()
        self.content.setFixedWidth(580)
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        self.default_label = QLabel("챔피언을 선택하세요")
        self.default_label.setFont(get_font(12, FontWeight.MEDIUM))
        self.default_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.content_layout.addWidget(self.default_label)
        self.scroll.setWidget(self.content)
        layout.addWidget(self.scroll)
        
        self.apply_style()

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()
        if self.augment_title:
            self.augment_title.setStyleSheet(f"color: {'white' if is_dark else '#333333'}")

    def apply_style(self):
        bg_color = '#1E1E1E' if self.is_dark_mode else 'white'
        text_color = 'white' if self.is_dark_mode else '#333333'
        scroll_bg = '#2D2D2D' if self.is_dark_mode else '#f0f0f0'
        scroll_handle = '#666666' if self.is_dark_mode else '#cccccc'
        placeholder_color = '#666666' if self.is_dark_mode else '#999999'
        
        self.setStyleSheet(f"background-color: {bg_color}")
        
        try:
            self.scroll.setStyleSheet(f"""
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
                QScrollBar:horizontal {{
                    border: none;
                    background: {scroll_bg};
                    height: 8px;
                    margin: 0px 0px 0px 0px;
                }}
                QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
                    background: {scroll_handle};
                    min-height: 20px;
                    border-radius: 4px;
                }}
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                    border: none;
                    background: none;
                }}
            """)
        except (RuntimeError, AttributeError):
            pass
        
        try:
            self.content.setStyleSheet(f"background-color: {bg_color}")
        except (RuntimeError, AttributeError):
            pass
        
        try:
            if hasattr(self, 'default_label') and self.default_label is not None:
                self.default_label.setStyleSheet(f"""
                    color: {placeholder_color};
                    padding: 500px 0 0 200px;
                    background: transparent;
                """)
        except (RuntimeError, AttributeError):
            pass

    def sizeHint(self):
        return QSize(400, super().sizeHint().height())

    def get_tier_style(self, tier):
        tier_styles = {
            "1": {
                "tier": "1",
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4E54C8, stop:1 #8F94FB)",
                "font_weight": "900",
                "width": "24"
            },
            "2": {
                "tier": "2",
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF6B6B, stop:1 #FF8E8E)",
                "font_weight": "900",
                "width": "24"
            },
            "3": {
                "tier": "3",
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7ED56F, stop:1 #9EF01A)",
                "font_weight": "900",
                "width": "24"
            },
            "4": {
                "tier": "4",
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #98B2D1, stop:1 #B3C4DB)",
                "font_weight": "900",
                "width": "24"
            },
            "5": {
                "tier": "5",
                "color": "white",
                "background": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #A1A1A1, stop:1 #B8B8B8)",
                "font_weight": "900",
                "width": "24"
            }
        }
        return tier_styles.get(str(tier), tier_styles["5"])

    def update_champion(self, ko_name, en_name):
        self.current_champion = (ko_name, en_name)
        
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        champion_data = None
        for champ in CHAMPION_RANKINGS:
            if champ["name"] == ko_name:
                champion_data = champ
                break
        
        if not champion_data:
            self.default_label.setText("해당 챔피언 정보를 찾을 수 없습니다.")
            self.default_label.setStyleSheet("color: #999999")
            return

        # 헤더 섹션
        image_path = os.path.join(CHAMPIONS_PATH, f"{en_name}.png")
        
        synergy_champions = []
        for champ_name in get_champion_synergies(ko_name):
            champion = get_champion_by_ko(champ_name)
            if champion:
                synergy_champions.append({
                    "ko_name": champ_name,
                    "en_name": champion["en"],
                    "image_path": os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                        "resources", "images", "champions", f"{champion['en']}.png"
                    )
                })
        
        is_checked = self.data_service.get_champion_status(en_name)
        
        header = ChampionHeader(
            ko_name=ko_name,
            en_name=en_name,
            image_path=image_path,
            tier_style=self.get_tier_style(champion_data["tier"]),
            synergy_champions=synergy_champions,
            on_image_click=self.on_image_clicked,
            on_synergy_click=self.on_synergy_champion_click,
            is_checked=is_checked
        )
        if self.is_dark_mode:
            header.set_dark_mode(True)
        self.content_layout.addWidget(header)
        
        # 통계 섹션
        stats = StatsSection(get_champion_stats(ko_name), champion_data)
        if self.is_dark_mode:
            stats.set_dark_mode(True)
        self.content_layout.addWidget(stats)

        # 증강 섹션
        augments = get_champion_augments(ko_name)
        if augments:
            header = QWidget()
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(16, 8, 16, 0)
            
            self.augment_title = QLabel("증강체")
            self.augment_title.setFont(get_font(14, FontWeight.BOLD))
            if self.is_dark_mode:
                self.augment_title.setStyleSheet("color: white")
            header_layout.addWidget(self.augment_title)
            
            header.setLayout(header_layout)
            self.content_layout.addWidget(header)
            
            sections = QWidget()
            sections_layout = QHBoxLayout()
            sections_layout.setContentsMargins(0, 0, 0, 0) 
            sections_layout.setSpacing(0)
            
            silver_page = AugmentSection(augments["silver"], "silver")
            silver_page.setFixedWidth(200)
            
            gold_page = AugmentSection(augments["gold"], "gold")
            gold_page.setFixedWidth(200)
            
            prismatic_page = AugmentSection(augments["prismatic"], "prismatic")
            prismatic_page.setFixedWidth(200)
            
            if self.is_dark_mode:
                silver_page.set_dark_mode(True)
                gold_page.set_dark_mode(True)
                prismatic_page.set_dark_mode(True)
            
            sections_layout.addWidget(silver_page)
            sections_layout.addWidget(gold_page)
            sections_layout.addWidget(prismatic_page)
            sections_layout.addStretch()
            
            sections.setLayout(sections_layout)
            self.content_layout.addWidget(sections)

        items_row = QWidget()
        items_layout = QHBoxLayout()
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(0)
        
        start_items_section = StartItemsSection(ko_name, self.is_dark_mode)
        if self.is_dark_mode:
            start_items_section.set_dark_mode(True)
        start_items_section.setFixedWidth(290)
        items_layout.addWidget(start_items_section)
        
        # 전설 아이템 섹션
        items = get_champion_items(ko_name)
        if items and items.get("core"):
            core_section = CoreBuildSection(items["core"])
            if self.is_dark_mode:
                core_section.set_dark_mode(True)
            core_section.setFixedWidth(290) 
            items_layout.addWidget(core_section)
        
        items_row.setLayout(items_layout)
        self.content_layout.addWidget(items_row)
        
        # 프리즘 아이템 섹션
        if items and items.get("prismatic"):
            prismatic_section = PrismaticItemSection(items["prismatic"], self.is_dark_mode)
            if self.is_dark_mode:
                prismatic_section.set_dark_mode(True)
            self.content_layout.addWidget(prismatic_section)

        self.content_layout.addStretch()

    def on_image_clicked(self, is_checked):
        if self.current_champion:
            ko_name, en_name = self.current_champion
            self.data_service.set_champion_status(en_name, is_checked)
            if self.on_champion_status_change:
                self.on_champion_status_change(en_name, is_checked)

    def on_synergy_champion_click(self, ko_name, en_name):
        if self.on_champion_select:
            self.on_champion_select(ko_name, en_name) 