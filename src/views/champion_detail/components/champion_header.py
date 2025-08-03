from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QColor, QPen, QIcon
from config.font_config import get_font, FontWeight
from config.settings import IMAGES_PATH
from data.champions.skills import get_champion_skills
import os

class ChampionImage(QPushButton):
    def __init__(self, image_path, is_checked=False, on_click=None):
        super().__init__()
        self.setFixedSize(80, 80)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self.on_click = on_click
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.normal_icon = QIcon(self.create_rounded_image(pixmap, False))
            self.checked_icon = QIcon(self.create_rounded_image(pixmap, True))
            
            self.setChecked(is_checked)
            self.setIcon(self.checked_icon if is_checked else self.normal_icon)
            self.setIconSize(QSize(80, 80))
            
            if on_click:
                self.clicked.connect(self.on_button_clicked)
        else:
            champion_name = os.path.basename(image_path)
            direct_path = os.path.join(IMAGES_PATH, "champions", champion_name)

            pixmap = QPixmap(direct_path)
            if not pixmap.isNull():
                print("Successfully loaded image from direct path")
                self.normal_icon = QIcon(self.create_rounded_image(pixmap, False))
                self.checked_icon = QIcon(self.create_rounded_image(pixmap, True))
                
                self.setChecked(is_checked)
                self.setIcon(self.checked_icon if is_checked else self.normal_icon)
                self.setIconSize(QSize(80, 80))
                
                if on_click:
                    self.clicked.connect(self.on_button_clicked)
            else:
                print(f"Failed to load image from direct path")
                self.setText("No IMG")
    
    def create_rounded_image(self, pixmap, is_checked):
        scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
        
        result = QPixmap(scaled_pixmap.size())
        result.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, 80, 80, 10, 10)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled_pixmap)
        
        if is_checked:
            painter.fillRect(result.rect(), QColor(0, 0, 0, 120))
            painter.setPen(QPen(QColor(255, 255, 255), 3))
            painter.drawLine(25, 40, 35, 50)
            painter.drawLine(35, 50, 55, 30)
        
        painter.end()
        return result
    
    def on_button_clicked(self):
        if self.on_click:
            self.setIcon(self.checked_icon if self.isChecked() else self.normal_icon)
            self.on_click(self.isChecked())
    
    def setChecked(self, checked):
        super().setChecked(checked)
        if hasattr(self, 'checked_icon') and hasattr(self, 'normal_icon'):
            self.setIcon(self.checked_icon if checked else self.normal_icon)

class TierLabel(QLabel):
    def __init__(self, tier, tier_style):
        super().__init__(str(tier))
        self.setFixedSize(24, 24)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(get_font(11, FontWeight.BLACK))
        self.setStyleSheet(f"""
            QLabel {{
                color: {tier_style['color']};
                background: {tier_style['background']};
                border: 2px solid white;
                border-radius: 12px;
                padding: 2px;
                font-weight: {tier_style['font_weight']};
            }}
        """)

class SynergyChampion(QPushButton):
    def __init__(self, ko_name, en_name, image_path, on_click=None):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
            }
            QPushButton:hover {
                border: 1px solid #d0d0d0;
                background-color: #f5f5f5;
            }
        """)
        
        print(f"\nSynergyChampion - Loading image:")
        print(f"Image path: {image_path}")
        print(f"File exists: {os.path.exists(image_path)}")
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            rounded_pixmap = self.create_rounded_image(pixmap)
            self.setIcon(QIcon(rounded_pixmap))
            self.setIconSize(QSize(40, 40))
            
            self.setToolTip(ko_name)
            self.setToolTipDuration(0)
            
            if on_click:
                self.clicked.connect(lambda: on_click(ko_name, en_name))
        else:
            print(f"Failed to load image: {image_path}")
            champion_name = os.path.basename(image_path)
            direct_path = os.path.join(IMAGES_PATH, "champions", champion_name)
            print(f"Trying direct path: {direct_path}")
            print(f"Direct path exists: {os.path.exists(direct_path)}")
            
            pixmap = QPixmap(direct_path)
            if not pixmap.isNull():
                print("Successfully loaded image from direct path")
                rounded_pixmap = self.create_rounded_image(pixmap)
                self.setIcon(QIcon(rounded_pixmap))
                self.setIconSize(QSize(40, 40))
                
                self.setToolTip(ko_name)
                self.setToolTipDuration(0)
                
                if on_click:
                    self.clicked.connect(lambda: on_click(ko_name, en_name))
            else:
                print(f"Failed to load image from direct path")
                self.setText("No IMG")
    
    def create_rounded_image(self, pixmap):
        scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
        rounded_pixmap = QPixmap(scaled_pixmap.size())
        rounded_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, 40, 40, 6, 6)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()
        
        return rounded_pixmap

class SkillImage(QWidget):
    def __init__(self, image_path, skill_key):
        super().__init__()
        self.setFixedSize(32, 32)
        
        layout = QWidget()
        layout.setFixedSize(32, 32)
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
            
            rounded_pixmap = QPixmap(32, 32)
            rounded_pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(rounded_pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            path = QPainterPath()
            path.addRoundedRect(0, 0, 32, 32, 6, 6)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()
            
            image_label = QLabel()
            image_label.setFixedSize(32, 32)
            image_label.setPixmap(rounded_pixmap)
            image_label.setParent(layout)
        
        key_label = QLabel(skill_key)
        key_label.setFixedSize(16, 16)
        key_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        key_label.setStyleSheet("""
            QLabel {
                color: white;
                background: rgba(0, 0, 0, 0.8);
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
                padding-bottom: 1px;
            }
        """)
        key_label.setParent(layout)
        key_label.move(16, 16)
        key_label.raise_()
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(layout)
        self.setLayout(main_layout)

class ChampionHeader(QWidget):
    def __init__(self, ko_name, en_name, image_path, tier_style, synergy_champions=None, on_image_click=None, on_synergy_click=None, is_checked=False):
        super().__init__()
        self.ko_name = ko_name
        self.en_name = en_name
        self.image_path = image_path
        self.tier_style = tier_style
        self.synergy_champions = synergy_champions or []
        self.on_image_click = on_image_click
        self.on_synergy_click = on_synergy_click
        self.is_checked = is_checked
        self.is_dark_mode = False
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        image_container = QWidget()
        image_container.setFixedSize(80, 80)
        
        self.champion_image = ChampionImage(self.image_path, is_checked=self.is_checked, on_click=self.on_image_click)
        self.champion_image.setParent(image_container)
        
        tier_label = TierLabel(self.tier_style["tier"], self.tier_style)
        tier_label.setParent(image_container)
        tier_label.move(52, 52)
        tier_label.raise_()
        
        right_container = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        
        self.name_label = QLabel(self.ko_name)
        self.name_label.setFont(get_font(24, FontWeight.BOLD))
        
        name_skills_container = QWidget()
        name_skills_layout = QHBoxLayout()
        name_skills_layout.setContentsMargins(0, 0, 0, 0)
        name_skills_layout.setSpacing(24)
        name_skills_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        name_skills_layout.addWidget(self.name_label)
        
        skills = get_champion_skills(self.ko_name)
        if skills:
            skills_container = QWidget()
            skills_layout = QHBoxLayout()
            skills_layout.setContentsMargins(0, 0, 0, 0)
            skills_layout.setSpacing(4)
            skills_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            
            arrow_style = "color: #666666;" if not self.is_dark_mode else "color: #999999;"
            
            for i, skill in enumerate(skills):
                skill_image_path = os.path.join(IMAGES_PATH, "skills", f"{self.ko_name}_{skill['key']}.png").replace("\\", "/")
                skill_widget = SkillImage(skill_image_path, skill['key'])
                skills_layout.addWidget(skill_widget)
                
                if i < len(skills) - 1:
                    arrow_label = QLabel("→")
                    arrow_label.setStyleSheet(arrow_style)
                    arrow_label.setFont(get_font(14, FontWeight.BOLD))
                    skills_layout.addWidget(arrow_label)
            
            skills_container.setLayout(skills_layout)
            name_skills_layout.addWidget(skills_container)
        
        name_skills_container.setLayout(name_skills_layout)
        right_layout.addWidget(name_skills_container)
        
        if self.synergy_champions:
            synergy_grid = QWidget()
            synergy_layout = QHBoxLayout()
            synergy_layout.setSpacing(10)
            synergy_layout.setContentsMargins(0, 0, 0, 0)
            
            for champ in self.synergy_champions:
                image_path = os.path.join(IMAGES_PATH, "champions", f"{champ['en_name']}.png")
                btn = SynergyChampion(
                    champ["ko_name"],
                    champ["en_name"],
                    image_path,
                    self.on_synergy_click
                )
                synergy_layout.addWidget(btn)
            
            synergy_grid.setLayout(synergy_layout)
            right_layout.addWidget(synergy_grid)
        
        right_container.setLayout(right_layout)
        
        layout.addWidget(image_container)
        layout.addWidget(right_container, 1)
        self.setLayout(layout)
        
        self.apply_style()

    def set_dark_mode(self, is_dark):
        self.is_dark_mode = is_dark
        self.apply_style()

    def apply_style(self):
        text_color = 'white' if self.is_dark_mode else '#333333'
        self.name_label.setStyleSheet(f"color: {text_color}")
        
        arrow_style = "color: #999999;" if self.is_dark_mode else "color: #666666;"
        for child in self.findChildren(QLabel):
            if child.text() == "→":
                child.setStyleSheet(arrow_style)