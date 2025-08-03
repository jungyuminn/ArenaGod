from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt, QSize, QRect, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QPainter, QColor
from config.font_config import get_font, FontWeight

class ToggleSwitch(QCheckBox):
    def __init__(self, text):
        super().__init__(text)
        self.setFont(get_font(12, FontWeight.BOLD))
        self._handle_position = 1 if self.isChecked() else 0
        self._text_color = "#333333"  # 기본 텍스트 색상
        
        self.animation = QPropertyAnimation(self, b"handle_position")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)

    def setChecked(self, checked):
        super().setChecked(checked)
        # 애니메이션 실행
        self.animation.stop()
        self.animation.setStartValue(self._handle_position)
        self.animation.setEndValue(1 if checked else 0)
        self.animation.start()

    def mousePressEvent(self, event):
        if self.hitButton(event.position().toPoint()):
            checked = not self.isChecked()
            self.setChecked(checked)
        
    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position
        
    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    def set_text_color(self, color):
        self._text_color = color
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        switch_width = 46
        switch_height = 24
        text_width = painter.fontMetrics().horizontalAdvance(self.text())
        total_width = switch_width + text_width + 10
        
        text_rect = QRect(switch_width + 10, 0, text_width, self.height())
        painter.setPen(QColor(self._text_color))
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter, self.text())

        # 트랙 색상 애니메이션
        if self.isChecked():
            track_color = QColor(
                int(224 + (78 - 224) * self._handle_position),
                int(224 + (84 - 224) * self._handle_position),
                int(224 + (200 - 224) * self._handle_position)
            )
        else:
            track_color = QColor(
                int(78 + (224 - 78) * (1 - self._handle_position)),
                int(84 + (224 - 84) * (1 - self._handle_position)),
                int(200 + (224 - 200) * (1 - self._handle_position))
            )
            
        track_rect = QRect(0, (self.height() - switch_height) // 2, switch_width, switch_height)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track_color)
        painter.drawRoundedRect(track_rect, switch_height // 2, switch_height // 2)

        handle_size = switch_height - 6
        start_x = 3
        end_x = switch_width - handle_size - 3
        current_x = start_x + (end_x - start_x) * self._handle_position

        handle_rect = QRect(
            int(current_x),
            (self.height() - handle_size) // 2,
            handle_size,
            handle_size
        )
        painter.setBrush(QColor("white"))
        painter.drawEllipse(handle_rect)

    def sizeHint(self):
        return QSize(
            46 + self.fontMetrics().horizontalAdvance(self.text()) + 10,
            max(24, self.fontMetrics().height() + 2)
        )

    def minimumSizeHint(self):
        return self.sizeHint()

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)