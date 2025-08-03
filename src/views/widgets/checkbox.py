from PyQt6.QtWidgets import QCheckBox, QStyle, QStyleOptionButton
from PyQt6.QtGui import QPainter, QColor, QPen
from config.font_config import get_font, FontWeight

class CustomCheckBox(QCheckBox):
    def __init__(self, text):
        super().__init__(text)
        self.setFont(get_font(12, FontWeight.MEDIUM))

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isChecked():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor("white"), 2))
            
            opt = QStyleOptionButton()
            opt.initFrom(self)
            rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, opt, self)
            painter.drawLine(rect.x() + 3, rect.y() + 9, rect.x() + 7, rect.y() + 13)
            painter.drawLine(rect.x() + 7, rect.y() + 13, rect.x() + 15, rect.y() + 5)
            painter.end()