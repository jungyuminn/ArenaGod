import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon
from .champion_grid.champion_grid_view import ChampionGridView
from .champion_rank.champion_rank_view import ChampionRankView
from .champion_detail.champion_detail_view import ChampionDetailView
from .champion_detail.components.champion_header import ChampionHeader
from PyQt6.QtWidgets import QApplication
from config.settings import RESOURCES_PATH
from .widgets.title_bar import TitleBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('ArenaGod', 'ArenaTracker')
        
        # 윈도우 플래그 설정 - 기본 프레임 유지하면서 커스텀 가능하도록
        self.setWindowFlags(
            Qt.WindowType.CustomizeWindowHint |  # 커스텀 윈도우 힌트
            Qt.WindowType.WindowMinMaxButtonsHint |  # 최소/최대화 버튼
            Qt.WindowType.WindowCloseButtonHint  # 닫기 버튼
        )
        
        # 아이콘 설정
        icon_path = os.path.join(RESOURCES_PATH, "icons", "app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 윈도우 설정
        self.setWindowTitle("ArenaGod - JungYM")
        self.init_ui()
    
    def init_ui(self):
        # 메인 컨테이너 위젯 생성
        main_container = QWidget()
        self.setCentralWidget(main_container)
        
        # 메인 레이아웃 설정
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 커스텀 타이틀바 생성
        self.title_bar = TitleBar()
        self.title_bar.darkModeToggled.connect(self.on_dark_mode_changed)
        self.title_bar.gridToggled.connect(self.toggle_grid)
        main_layout.addWidget(self.title_bar)
        
        # 메인 콘텐츠 위젯 생성
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addWidget(content_widget)
        
        # 왼쪽 패널 (통계)
        self.stats_panel = ChampionRankView(
            on_champion_select=self.on_champion_select
        )
        self.stats_panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.stats_panel.setFixedWidth(400)  # 왼쪽 패널 너비 고정
        content_layout.addWidget(self.stats_panel)
        
        # 중앙 패널 (챔피언 그리드)
        self.champion_grid = ChampionGridView(
            on_champion_select=self.on_champion_select,
            on_status_change=self.on_champion_status_change
        )
        self.champion_grid.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        content_layout.addWidget(self.champion_grid)
        
        # 오른쪽 패널 (챔피언 상세 정보)
        self.right_panel = ChampionDetailView()
        self.right_panel.on_champion_status_change = self.on_champion_status_change
        self.right_panel.on_champion_select = self.on_champion_select
        self.right_panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.right_panel.setFixedWidth(600)  # 오른쪽 패널 너비 고정
        content_layout.addWidget(self.right_panel)
        
        # 윈도우 크기 및 위치 설정
        self.setMinimumSize(1500, 760)  # 최소 크기
        self.resize(1500, 1200)  # 기본 크기
        
        # 화면 중앙에 위치
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        # UI 초기화가 완료된 후 저장된 다크모드 설정 불러오기
        is_dark_mode = self.settings.value('dark_mode', True, type=bool)  # 기본값을 True로 변경
        self.title_bar.dark_mode_toggle.setChecked(is_dark_mode)  # 토글 상태 설정
        self.on_dark_mode_changed(is_dark_mode)  # 다크모드 적용
    
    def toggle_dark_mode(self, checked):
        # TODO: 다크모드 전환 로직 구현
        pass

    def toggle_grid(self, show):
        if show:
            self.champion_grid.show()
            # 윈도우 크기 복원
            self.setMinimumWidth(1500)
            self.resize(1500, self.height())
        else:
            self.champion_grid.hide()
            # 윈도우 크기 조정
            self.setMinimumWidth(1000)  # 최소 너비 줄이기
            self.resize(1000, self.height())  # 현재 너비 줄이기
    
    def on_champion_select(self, ko_name, en_name):
        """챔피언 선택 시 호출되는 콜백 함수"""
        self.right_panel.update_champion(ko_name, en_name)
    
    def on_champion_status_change(self, en_name, is_checked):
        """챔피언 상태 변경 시 호출되는 콜백 함수"""
        # 챔피언 그리드의 상태 업데이트
        for champion_frame in self.champion_grid.champions:
            if champion_frame.en_name == en_name:
                champion_frame.button.setChecked(is_checked)
                champion_frame.button.setIcon(champion_frame.checked_icon if is_checked else champion_frame.normal_icon)
                break
        
        # 체크된 챔피언 수 업데이트
        self.champion_grid.update_checked_count()
        
        # 디테일 패널이 현재 해당 챔피언을 보여주고 있다면 상태 업데이트
        if self.right_panel.current_champion and self.right_panel.current_champion[1] == en_name:
            # 헤더의 이미지 체크박스만 업데이트
            for i in range(self.right_panel.content_layout.count()):
                widget = self.right_panel.content_layout.itemAt(i).widget()
                if isinstance(widget, ChampionHeader):
                    widget.champion_image.setChecked(is_checked)
                    widget.champion_image.setIcon(
                        widget.champion_image.checked_icon if is_checked else widget.champion_image.normal_icon
                    )
                    break

    def on_dark_mode_changed(self, checked):
        # 다크모드 설정 저장
        self.settings.setValue('dark_mode', checked)
        
        # 다크모드 상태를 자식 위젯들에게 전달
        self.title_bar.set_dark_mode(checked)
        self.stats_panel.set_dark_mode(checked)
        self.champion_grid.set_dark_mode(checked)
        
        # 오른쪽 패널의 모든 자식 위젯에 다크모드 적용
        self.right_panel.set_dark_mode(checked)
        for child in self.right_panel.findChildren(QWidget):
            if hasattr(child, 'set_dark_mode'):
                child.set_dark_mode(checked)