from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QPushButton, QScrollArea, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter  # Import QPainter here
import os
from PyQt5.QtGui  import QFont, QPalette, QColor

class FretboardPage(QWidget):
    def __init__(self, show_guitar_anatomy_page):
        super().__init__()

        self.show_guitar_anatomy_page = show_guitar_anatomy_page
        #self.theme = theme

        #self.setStyleSheet(self.theme)
        self.init_ui()

    def init_ui(self):
        # paint background rat‐grey
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#343A40"))
        self.setPalette(pal)
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Fretboard")
        title_label.setObjectName("title")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(title_label, 0)


        # Instructions label
        instructions = QLabel("Hover over any fret or string to see the note at that position!")
        instructions.setObjectName("content")
        instructions.setFont(QFont("Segoe UI", 15, QFont.Bold))
        instructions.setStyleSheet("color: white;")
        layout.addWidget(instructions, 0)

        # Create a QGraphicsView and QGraphicsScene to display the fretboard
        self.view = QGraphicsView(self)
        scene = QGraphicsScene()
        self.view.setScene(scene)

        scene.setBackgroundBrush(Qt.transparent)

        # configure view transparency
        self.view.setFrameShape(QFrame.NoFrame)
        self.view.setStyleSheet("background: transparent;")
        self.view.setAttribute(Qt.WA_TranslucentBackground)
        self.view.viewport().setAttribute(Qt.WA_TranslucentBackground)

        # wrap in a transparent scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent;")
        scroll_area.viewport().setStyleSheet("background: transparent;")
        scroll_area.setWidget(self.view)

        layout.addWidget(scroll_area)

        # Load fretboard image
        current_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_directory, "../chords_images", "fretboard.png")
        pixmap = QPixmap(image_path)

        # Scale the image to a smaller size while maintaining the aspect ratio
        scaled_pixmap = pixmap.scaled(int(pixmap.width() * 0.6), 
                                      int(pixmap.height() * 0.6), 
                                      Qt.KeepAspectRatio,
                                      Qt.SmoothTransformation
                                      )

        # Set the scaled image in the scene
        scene.addPixmap(scaled_pixmap)

        # Resize the QGraphicsView to fit the scaled image
        self.fretboard_width = scaled_pixmap.width()
        self.fretboard_height = scaled_pixmap.height()

        # 1) make the scene rect match your image bounds
        scene.setSceneRect(0, 0,
                           self.fretboard_width,
                           self.fretboard_height)

        # 2) enable hover/mouse‐move events on the view & viewport
        self.view.setMouseTracking(True)
        self.view.viewport().setMouseTracking(True)

        # Adjust the QGraphicsView to the size of the image, removing the zoom effect
        self.view.setRenderHint(QPainter.Antialiasing)  # Optional, to improve image rendering

        # Create rectangles for each fret and string
        rect_width = 50  # Width of the clickable area
        rect_height = 50  # Height of the clickable area
        self.note_label = QLabel("", self)
        self.note_label.setObjectName("content")
        self.note_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        self.note_label.setStyleSheet("color: white;")

        layout.addWidget(self.note_label)

        # String and fret positions based on the image size
        string_positions = [self.fretboard_height * (i / 6) for i in range(6)]  # 6 strings
        fret_positions = [self.fretboard_width * (i / 12) for i in range(1, 13)]  # 12 frets

        # Define the notes for each string from open to fret 12
        notes = {
            "E_high": ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"],  # 1st string (highest)
            "B":      ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],  # 2nd string
            "G":      ["G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"],  # 3rd string
            "D":      ["D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D"],  # 4th string
            "A":      ["A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"],  # 5th string
            "E_low":  ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]   # 6th string (lowest)
        }

        def on_hover(event, string_idx, fret_idx):
            string_names = ["E_high", "B", "G", "D", "A", "E_low"]
            note = notes[string_names[string_idx]][fret_idx]
            self.note_label.setText(f"String: {string_names[string_idx]}, Fret: {fret_idx + 1}, Note: {note}")

        # Adjust the position of the rectangles to align them better with the image
        offset_x = 2  # Adjust this value to shift the rects horizontally (left or right)
        offset_y = 2  # Adjust this value to shift the rects vertically (up or down)

        # Create clickable rectangles and bind hover events
        for i, fret_x in enumerate(fret_positions):
            for j, string_y in enumerate(string_positions):
                rect_item = QGraphicsRectItem(fret_x - rect_width // 2 + offset_x, 
                                            string_y - rect_height // 2 + offset_y, 
                                            rect_width, rect_height)
                rect_item.setBrush(Qt.transparent)
                rect_item.setPen(Qt.transparent)
                scene.addItem(rect_item)

                # Bind hover event
                rect_item.setAcceptHoverEvents(True)
                rect_item.hoverMoveEvent = lambda event, si=j, fi=i: on_hover(event, si, fi)

        # Back Button
        back_button = QPushButton("Back to Guitar Anatomy")
        back_button.clicked.connect(self.show_guitar_anatomy_page)
        layout.addWidget(back_button)

        # Set layout properties to remove any margin/spacing issues
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
