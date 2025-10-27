import sys
from PyQt5.QtWidgets import QApplication
from menu_window import SplashWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashWindow()
    sys.exit(app.exec_())
