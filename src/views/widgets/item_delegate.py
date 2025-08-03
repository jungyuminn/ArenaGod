from PyQt6.QtWidgets import QStyledItemDelegate, QStyle
from PyQt6.QtGui import QPainter, QColor, QPalette
from PyQt6.QtCore import Qt
from config.font_config import get_font, FontWeight

class IOSStyleItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.palette.setColor(QPalette.ColorRole.Highlight, QColor(78, 84, 200, 25))
        option.palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#4E54C8"))
        
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            
        painter.setPen(QColor("#4E54C8") if option.state & QStyle.StateFlag.State_Selected else QColor("#333333"))
        text = index.data()
        text_rect = option.rect.adjusted(12, 0, -12, 0)
        painter.setFont(get_font(12, FontWeight.BOLD))
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter, text)