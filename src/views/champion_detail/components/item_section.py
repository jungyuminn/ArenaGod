from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QSize, QPointF, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QLinearGradient, QColor, QPen
from config.font_config import get_font, FontWeight
from config.settings import IMAGES_PATH
from data.champions.start_items import get_champion_start_items
import os

class ItemImage(QLabel):
    def __init__(self, item_name, size=40, radius=6, item_type="legendary"):
        super().__init__()
        self.setFixedSize(size, size)
        self.item_type = item_type
        self.radius = radius
        self.is_dark_mode = False
        self.item_name = item_name
        self.apply_style()
        self.setToolTip(item_name)
        self.setToolTipDuration(0)
        self.load_image(item_name, size, radius, item_type)

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()

    def apply_style(self):
        tooltip_color = 'white' if self.is_dark_mode else '#333333'
        self.setStyleSheet(f"""
            QLabel {{
                background-color: transparent;
                border-radius: {self.radius}px;
            }}
            QToolTip {{
                color: {tooltip_color};
            }}
        """)
        self.setToolTip(self.item_name)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.item_type == "prismatic":
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0.0, QColor("#FF6B6B"))  # 빨강
            gradient.setColorAt(0.2, QColor("#FFD93D"))  # 노랑
            gradient.setColorAt(0.4, QColor("#6BCB77"))  # 초록
            gradient.setColorAt(0.6, QColor("#4D96FF"))  # 파랑
            gradient.setColorAt(0.8, QColor("#9B59B6"))  # 보라
            gradient.setColorAt(1.0, QColor("#FF6B6B"))  # 다시 빨강
            
            pen = QPen()
            pen.setWidth(3)
            pen.setBrush(gradient)
            painter.setPen(pen)

            pen_width = pen.width()
            half_pen = pen_width // 2 
            painter.drawRoundedRect(
                int(half_pen), 
                int(half_pen),
                int(self.width() - pen_width), 
                int(self.height() - pen_width),
                self.radius,
                self.radius
            )
            painter.end()

    def load_image(self, item_name, size, radius, item_type):
        if item_type == "start_item":
            boots_path = os.path.join(IMAGES_PATH, "items", "boots", f"{item_name}.png")
            if os.path.exists(boots_path):
                image_path = boots_path
            else:
                image_path = os.path.join(IMAGES_PATH, "items", "start_items", f"{item_name}.png")
        else:
            image_path = os.path.join(IMAGES_PATH, "items", item_type, f"{item_name}.png")
        
        print(f"\nItemImage - Loading image:")
        print(f"Image path: {image_path}")
        print(f"File exists: {os.path.exists(image_path)}")
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                image_size = size - (6 if item_type == "prismatic" else 0)
                scaled_pixmap = pixmap.scaled(image_size, image_size, Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
                rounded_pixmap = QPixmap(scaled_pixmap.size())
                rounded_pixmap.fill(Qt.GlobalColor.transparent)
                
                painter = QPainter(rounded_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                
                mask = QPainterPath()
                mask.addRoundedRect(0, 0, image_size, image_size, radius-2 if item_type == "prismatic" else radius, radius-2 if item_type == "prismatic" else radius)
                painter.setClipPath(mask)
                painter.drawPixmap(0, 0, scaled_pixmap)
                painter.end()
                
                final_pixmap = QPixmap(size, size)
                final_pixmap.fill(Qt.GlobalColor.transparent)
                
                painter = QPainter(final_pixmap)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                x = (size - image_size) // 2
                y = (size - image_size) // 2
                painter.drawPixmap(x, y, rounded_pixmap)
                painter.end()
                
                self.setPixmap(final_pixmap)

class StartItemsSection(QWidget):
    def __init__(self, champion_ko, is_dark_mode=False):
        super().__init__()
        self.champion_ko = champion_ko
        self.is_dark_mode = is_dark_mode
        self.arrows = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 0, 0, 0)
        layout.setSpacing(0)
        
        self.title = QLabel("시작 아이템")
        self.title.setFont(get_font(14, FontWeight.BOLD))
        self.title.setContentsMargins(0, 4, 0, 4)
        layout.addWidget(self.title)
        
        start_items = get_champion_start_items(self.champion_ko)
        
        items_container = QWidget()
        items_layout = QHBoxLayout()
        items_layout.setContentsMargins(6, 0, 0, 0)
        items_layout.setSpacing(12)
        items_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        if start_items and start_items.get('starting_item'):
            image = ItemImage(start_items['starting_item']['name'], size=35, radius=6, item_type="start_item")
            image.set_dark_mode(self.is_dark_mode)
            items_layout.addWidget(image)

            arrow = QLabel("→")
            arrow.setFont(get_font(14, FontWeight.BOLD))
            arrow.setFixedHeight(35)
            arrow.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.arrows.append(arrow)
            items_layout.addWidget(arrow)
        
        if start_items and start_items.get('boots'):
            image = ItemImage(start_items['boots']['name'], size=35, radius=6, item_type="start_item")
            image.set_dark_mode(self.is_dark_mode)
            items_layout.addWidget(image)
        
        items_layout.addStretch()
        items_container.setLayout(items_layout)
        layout.addWidget(items_container)
        
        self.setLayout(layout)
        self.apply_style()
    
    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()
    
    def apply_style(self):
        text_color = 'white' if self.is_dark_mode else '#333333'
        arrow_color = '#999999' if self.is_dark_mode else '#666666'
        
        self.title.setStyleSheet(f"color: {text_color}; padding: 4px 0px 4px 0px;")
        
        for arrow in self.arrows:
            arrow.setStyleSheet(f"color: {arrow_color};")

class CoreBuildSection(QWidget):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.is_dark_mode = False
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.title = QLabel("전설 아이템")
        self.title.setFont(get_font(14, FontWeight.BOLD))
        self.title.setContentsMargins(0, 4, 0, 4)
        layout.addWidget(self.title)
        
        items_container = QWidget()
        items_layout = QHBoxLayout()
        items_layout.setContentsMargins(6, 0, 0, 0)
        items_layout.setSpacing(12)
        items_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.arrows = []
        
        for idx, item_name in enumerate(self.items):
            image = ItemImage(item_name, size=35, radius=6)
            items_layout.addWidget(image)
            
            if idx < len(self.items) - 1:
                arrow = QLabel("→")
                arrow.setFont(get_font(14, FontWeight.BOLD))
                arrow.setFixedHeight(35)
                arrow.setAlignment(Qt.AlignmentFlag.AlignVCenter)
                self.arrows.append(arrow)
                items_layout.addWidget(arrow)
        
        items_layout.addStretch()
        items_container.setLayout(items_layout)
        layout.addWidget(items_container)
        
        self.setLayout(layout)
        self.apply_style()

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()
        
        for child in self.findChildren(ItemImage):
            child.set_dark_mode(is_dark)

    def apply_style(self):
        text_color = 'white' if self.is_dark_mode else '#333333'
        arrow_color = '#999999' if self.is_dark_mode else '#666666'
        
        self.title.setStyleSheet(f"color: {text_color}; padding: 4px 0px 4px 0px;")
        
        for arrow in self.arrows:
            arrow.setStyleSheet(f"color: {arrow_color};")

class PrismaticItemSection(QWidget):
    def __init__(self, items, is_dark_mode=False):
        super().__init__()
        self.items = items
        self.is_dark_mode = is_dark_mode
        self.header_labels = []
        self.item_rows = []
        self.dividers = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 0, 0, 0) 
        layout.setSpacing(0)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 8)
        
        self.title = QLabel("프리즘 아이템")
        self.title.setFont(get_font(14, FontWeight.BOLD))
        
        headers = ["평균 순위", "1등 확률", "픽률", "승률"]
        
        for text in headers:
            label = QLabel(text)
            label.setFont(get_font(11, FontWeight.BOLD))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedWidth(80)
            self.header_labels.append(label)
        
        header_layout.addWidget(self.title)
        header_layout.addStretch()
        for label in self.header_labels:
            header_layout.addWidget(label)
        
        layout.addLayout(header_layout)
        
        divider = self.create_divider()
        self.dividers.append(divider)
        layout.addWidget(divider)
        
        for idx, item in enumerate(self.items):
            if idx > 0:
                divider = self.create_divider()
                self.dividers.append(divider)
                layout.addWidget(divider)
            row = PrismaticItemRow(item, self.is_dark_mode)
            self.item_rows.append(row)
            layout.addWidget(row)
        
        self.setLayout(layout)
        self.apply_style()
    
    def create_divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFixedHeight(1)
        return divider

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()

        for row in self.item_rows:
            row.set_dark_mode(is_dark)

    def apply_style(self):
        text_color = 'white' if self.is_dark_mode else '#333333'
        sub_text_color = '#666666'
        border_color = '#333333' if self.is_dark_mode else '#eeeeee'
        
        self.title.setStyleSheet(f"color: {text_color};")
        
        for label in self.header_labels:
            label.setStyleSheet(f"color: {sub_text_color};")
        
        for divider in self.dividers:
            divider.setStyleSheet(f"border: none; background-color: {border_color};")

class PrismaticItemRow(QWidget):
    def __init__(self, item, is_dark_mode=False):
        super().__init__()
        self.item = item
        self.is_dark_mode = is_dark_mode
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 8, 0, 8)
        
        name_container = QWidget()
        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(12)
        
        image = ItemImage(self.item["name"], size=35, radius=6, item_type="prismatic")
        image.set_dark_mode(self.is_dark_mode)
        self.name_label = QLabel(self.item["name"])
        self.name_label.setFont(get_font(12, FontWeight.BOLD))
        
        name_layout.addWidget(image)
        name_layout.addWidget(self.name_label)
        name_container.setLayout(name_layout)
        
        stats = [
            (self.item["avg_rank"], False),
            (self.item["first_rate"], False),
            (self.item["pick_rate"], False),
            (self.item["win_rate"], True)
        ]
        
        self.stat_labels = []
        for value, is_win_rate in stats:
            label = QLabel(value)
            label.setFont(get_font(12, FontWeight.BOLD))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedWidth(80)
            self.stat_labels.append((label, is_win_rate))
        
        layout.addWidget(name_container)
        layout.addStretch()
        for label, _ in self.stat_labels:
            layout.addWidget(label)
        
        self.setLayout(layout)
        self.apply_style()

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()
        
        for child in self.findChildren(ItemImage):
            child.set_dark_mode(is_dark)

    def apply_style(self):
        text_color = 'white' if self.is_dark_mode else '#333333'
        sub_text_color = '#666666'
        
        self.name_label.setStyleSheet(f"color: {text_color};")
        
        for label, is_win_rate in self.stat_labels:
            color = '#4E54C8' if is_win_rate else sub_text_color
            label.setStyleSheet(f"color: {color}; font-weight: bold;") 