from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QCursor
import os
from PyQt5.QtGui  import QFont, QPalette, QColor

class GuitarAnatomyPage(QWidget):
    def __init__(self, show_tutorial_page, show_fretboard_page):
        super().__init__()

        self.show_tutorial_page = show_tutorial_page
        self.show_fretboard_page = show_fretboard_page
        #self.theme = theme

        #self.setStyleSheet(self.theme)
        self.init_ui()

    def init_ui(self):
        # paint background rat‐grey
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#343A40"))
        self.setPalette(pal)
        # Outer layout
        outer_layout = QVBoxLayout(self)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Scroll content container
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        # Title
        title_label = QLabel("Guitar Anatomy")
        title_label.setObjectName("title")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(title_label)

        # Load image
        current_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_directory, "../chords_images", "guitar_anatomy.png")

        try:
            pixmap = QPixmap(image_path)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(600, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(image_label)
        except Exception as e:
            print("Error loading guitar anatomy image:", e)
            layout.addWidget(QLabel("Image not found!"))

        # Buttons layout
        button_layout = QHBoxLayout()
        left_frame = QFrame()
        left_layout = QVBoxLayout()
        left_frame.setLayout(left_layout)
        button_layout.addWidget(left_frame)

        right_frame = QFrame()
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)
        button_layout.addWidget(right_frame)

        layout.addLayout(button_layout)

        button_definitions = {
            "Headstock": "The headstock is the top part of the guitar's neck...",
            "Nut": "The nut is a small piece at the top of the neck...",
            "Fretboard": "The fretboard is the flat part of the neck...",
            "Sound Hole": "The sound hole is the round hole in the body...",
            "Strap Button": "The strap button is a small metal knob...",
            "String": "The strings are the thin wires stretched...",
            "Tuning Machine": "The tuning machines are the pegs...",
            "Saddle": "The saddle is a small piece on the bridge...",
            "Bridge": "The bridge is the part of the guitar...",
            "Pickguard": "The pickguard is a protective piece of plastic...",
            "Neck": "The neck is the long part of the guitar...",
            "Body": "The body is the large part of the guitar..."
        }

        left_labels = ["Headstock", "Nut", "Fretboard", "Sound Hole", "Strap Button", "String"]
        right_labels = ["Tuning Machine", "Saddle", "Bridge", "Pickguard", "Neck", "Body"]

        for label in left_labels:
            button = QPushButton(label)
            button.setToolTip(button_definitions[label])
            button.setCursor(QCursor(Qt.PointingHandCursor))
            left_layout.addWidget(button)

        for label in right_labels:
            button = QPushButton(label)
            button.setToolTip(button_definitions[label])
            button.setCursor(QCursor(Qt.PointingHandCursor))
            right_layout.addWidget(button)

        fretboard_button = QPushButton("Go to Fretboard Page")
        fretboard_button.clicked.connect(self.show_fretboard_page)
        layout.addWidget(fretboard_button)

        # Navigation buttons
        back_button = QPushButton("Back to Tutorial Menu")
        back_button.clicked.connect(self.show_tutorial_page)
        layout.addWidget(back_button)

        # Set content and apply to scroll area
        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)
        self.setLayout(outer_layout)




        

