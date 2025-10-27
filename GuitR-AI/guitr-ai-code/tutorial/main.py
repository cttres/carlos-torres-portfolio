import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget,
    QWidget, QVBoxLayout, QPushButton
)
from guitar_anatomy_page import GuitarAnatomyPage
from tutorial_page import TutorialPage
from strumming_patterns_page import StrummingPatternsPage
from how_to_use_app_page import HowToUseAppPage
from fretboard_page import FretboardPage
from theme import light_theme, dark_theme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GuitR-AI Tutorial")
        self.theme = dark_theme

        # stacked widget holds all “pages”
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # build each page and add it
        self.create_main_menu()
        self.create_tutorial_page()
        self.create_anatomy_page()
        self.create_strumming_page()
        self.create_usage_page()
        self.create_fretboard_page()

        # show tutorial first (or change to main menu if preferred)
        self.show_tutorial_page()

    def create_main_menu(self):
        self.main_menu_page = QWidget()
        self.main_menu_page.setStyleSheet(self.theme)

        layout = QVBoxLayout()

        tutorial_btn = QPushButton("Go to Tutorial Page")
        tutorial_btn.clicked.connect(self.show_tutorial_page)
        layout.addWidget(tutorial_btn)

        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)   # closes the QMainWindow
        layout.addWidget(exit_btn)

        self.main_menu_page.setLayout(layout)
        self.stacked_widget.addWidget(self.main_menu_page)

    def create_tutorial_page(self):
        self.tutorial_page = TutorialPage(
            show_anatomy_page   = self.show_anatomy_page,
            show_strumming_page = self.show_strumming_page,
            show_usage_page     = self.show_usage_page,
        )
        self.stacked_widget.addWidget(self.tutorial_page)

    def create_anatomy_page(self):
        self.anatomy_page = GuitarAnatomyPage(
            show_tutorial_page=self.show_tutorial_page,
            show_fretboard_page=self.show_fretboard_page
        )
        self.stacked_widget.addWidget(self.anatomy_page)

    def create_strumming_page(self):
        self.strumming_page = StrummingPatternsPage(
            show_tutorial_page=self.show_tutorial_page
        )
        self.stacked_widget.addWidget(self.strumming_page)

    def create_usage_page(self):
        self.usage_page = HowToUseAppPage(
            show_tutorial_page=self.show_tutorial_page
        )
        self.stacked_widget.addWidget(self.usage_page)

    def create_fretboard_page(self):
        self.fretboard_page = FretboardPage(
            show_guitar_anatomy_page=self.show_anatomy_page
        )
        self.stacked_widget.addWidget(self.fretboard_page)

    # navigation helpers
    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu_page)

    def show_tutorial_page(self):
        self.stacked_widget.setCurrentWidget(self.tutorial_page)

    def show_anatomy_page(self):
        self.stacked_widget.setCurrentWidget(self.anatomy_page)

    def show_strumming_page(self):
        self.stacked_widget.setCurrentWidget(self.strumming_page)

    def show_usage_page(self):
        self.stacked_widget.setCurrentWidget(self.usage_page)

    def show_fretboard_page(self):
        self.stacked_widget.setCurrentWidget(self.fretboard_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # Launch in full-screen mode
    window.showFullScreen()
    sys.exit(app.exec_())
