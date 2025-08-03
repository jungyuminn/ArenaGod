import os
import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from views.main_window import MainWindow
from config.font_config import init_fonts
from config.settings import RESOURCES_PATH

def main():
    app = QApplication(sys.argv)
    
    if os.name == 'nt':
        myappid = 'ArenaGod.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        icon_path = os.path.join(RESOURCES_PATH, "icons", "app_icon.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
    
    init_fonts()
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
