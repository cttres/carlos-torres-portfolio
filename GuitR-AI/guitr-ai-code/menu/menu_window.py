import sys
import os
import subprocess
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize, Qt

class SplashWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Frameless window with black background
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: black;")

        # Background logo
        logo_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), '.', 'GuitR-AILogo.png')
        )
        self.logo_label = QLabel(self)
        pixmap = QPixmap(logo_path)
        if pixmap.isNull():
            print(f"❌ Failed to load splash logo: {logo_path}")
        else:
            self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)

        # Show fullscreen
        self.showFullScreen()

        # allow the pixmap to scale to the label’s size
        self.logo_label.setScaledContents(True)

        # compute “half‐screen” geometry
        full = self.rect()                  # QRect(0,0, W, H)
        w2 = full.width()  // 2
        h2 = full.height() // 2
        x  = (full.width()  - w2) // 2      # center horizontally
        y  = (full.height() - h2) // 2      # center vertically

        # apply it
        self.logo_label.setGeometry(x, y, w2, h2)
        self.logo_label.lower()

        # Start button
        self.start_btn = QPushButton("Start", self)
        self.start_btn.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.start_btn.setStyleSheet(
            "background-color: #3498db; color: white; padding: 10px; border-radius: 10px;"
        )
        self.start_btn.setFixedSize(200, 60)
        self.start_btn.clicked.connect(self.open_menu)
        self.start_btn.show()

        # Exit button
        self.exit_btn = QPushButton("✕", self)
        self.exit_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.exit_btn.setStyleSheet(
            "background-color: transparent; color: white; border: none;"
        )
        self.exit_btn.setFixedSize(40, 40)
        self.exit_btn.clicked.connect(QApplication.instance().quit)
        self.exit_btn.show()

        # Position elements
        self.position_elements()
        # Ensure buttons are on top of logo
        self.start_btn.raise_()
        self.exit_btn.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Resize logo
        if hasattr(self, 'logo_label'):
            self.logo_label.setGeometry(self.rect())
        # Reposition and raise buttons
        if hasattr(self, 'start_btn'):
            self.position_elements()
            self.start_btn.raise_()
        if hasattr(self, 'exit_btn'):
            self.exit_btn.raise_()

    def position_elements(self):
        # Center start button lower near bottom
        if hasattr(self, 'start_btn'):
            btn = self.start_btn
            x = (self.width() - btn.width()) // 2
            # Move the button lower: use 0.85 of height
            y = int(self.height() * 0.92)
            btn.move(x, y)
        # Position exit button at top-right
        if hasattr(self, 'exit_btn'):
            eb = self.exit_btn
            margin = 10
            eb.move(self.width() - eb.width() - margin, margin)

    def open_menu(self):
        from menu_window import MenuWindow
        self.menu = MenuWindow()
        self.menu.show()
        self.close()

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menu")
        self.showFullScreen()
        self.setStyleSheet("background-color: #2c3e50;")

        # Exit button for menu
        self.exit_btn = QPushButton("✕", self)
        self.exit_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.exit_btn.setStyleSheet("background-color: transparent; color: white; border: none;")
        self.exit_btn.setFixedSize(40, 40)
        self.exit_btn.clicked.connect(QApplication.instance().quit)
        self.exit_btn.show()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 20, 50, 20)
        layout.setSpacing(max(20, int(self.height() * 0.05)))
        self.main_layout = layout

        # Load icons
        isolation_icon = QIcon("isolation.png")
        if isolation_icon.isNull():
            print("isolation.png not found.")
        guitar_icon = QIcon("guitar_icon.png")
        if guitar_icon.isNull():
            guitar_icon = self.get_fallback_guitar_icon()
        tutorial_icon = QIcon("tutorial.png")
        if tutorial_icon.isNull():
            print("tutorial.png not found.")

        # Button style and font
        button_style = """
            QPushButton {
                background-color: #3498db;
                border: none;
                border-radius: 15px;
                padding: 10px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f6391;
            }
        """
        custom_font = QFont("Segoe UI", 18, QFont.Bold)

        # Create and add buttons
        for text, icon, handler in [
            ("Isolation", isolation_icon, self.open_track_separation_main),
            ("Recognition", guitar_icon, self.open_chord_recognition_main),
            ("Tutorial", tutorial_icon, self.open_chord_tutorial_main)
        ]:
            btn = QPushButton(f"     {text}")
            btn.setIcon(icon)
            btn.setStyleSheet(button_style)
            btn.setFont(custom_font)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
            self.buttons.append(btn)

        # Position exit button on menu
        self.exit_btn.move(self.width() - self.exit_btn.width() - 10, 10)
        self.exit_btn.raise_()
        self.update_dynamic_properties()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reposition exit button
        if hasattr(self, 'exit_btn'):
            self.exit_btn.move(self.width() - self.exit_btn.width() - 10, 10)
            self.exit_btn.raise_()
        self.update_dynamic_properties()

    def update_dynamic_properties(self):
        # Update icon sizes
        icon_size = max(32, int(self.height() * 0.15))
        for btn in self.buttons:
            btn.setIconSize(QSize(icon_size, icon_size))
        # Update spacing
        spacing = max(20, int(self.height() * 0.05))
        if hasattr(self, 'main_layout'):
            self.main_layout.setSpacing(spacing)

    def open_track_separation_main(self):
        self._open_script("track_separation")

    def open_chord_recognition_main(self):
        self._open_script("chords_recognition")

    def open_chord_tutorial_main(self):
        self._open_script("tutorial")

    def _open_script(self, folder):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(current_dir, "..", folder, "main.py")
        subprocess.Popen([sys.executable, target], cwd=os.path.join(current_dir, "..", folder))
        self.close()

    def get_fallback_guitar_icon(self):
        b64 = (
            b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABTklEQVQ4T2P4////"
            b"8/h9+CRWr4T4j58+U4G/AwMFBcGoiCXb9++s+G0yEbiC8YxcIBqwzwiF98QBJZ"
            b"D9+8+cfk2/fv3xBz/F7vDm8OTL4Em6wQvEV4fBgh6F+DC/H3L///2Za4dOjSX6J"
            b"7cDqEG8+yAkpDwDGcKAGn7Ic0zRIv2ASmQ84DXnvvKu+/l3mAApBsOGRxerDcH+Z"
            b"E/EMXy4kxfCEYv+gP2fyQFLBP/Fftl+GcrR7+G/d7/KGAsRkMmUAp2HqPUUljMAv"
            b"4OSZ7r0BZEDZO8Cz5CGdT1JGBQKo+OwsgSySgn/wmVA8CXLx5MnHsUikQijmGBON"
            b"HZ2kC7dOhQjxIHnzmrrNBmZwf+90sNVVDA0St4iA6pBk4ZcTpCUxRDVl9yQkFOVc"
            b"VDmmBgcCRYgwZeufO0l4GFIFAPWjaeCX2ZuBAAAAAElFTkSuQmCC"
        )
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(b64))
        return QIcon(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashWindow()
    sys.exit(app.exec_())
