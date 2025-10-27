from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QScrollArea, QSizePolicy, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
from PyQt5.QtGui  import QFont, QPalette, QColor

class StrummingPatternsPage(QWidget):
    def __init__(self, show_tutorial_page):
        super().__init__()
        self.show_tutorial_page = show_tutorial_page
        self.init_ui()

    def init_ui(self):
        # paint background rat‐grey
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor("#343A40"))
        self.setPalette(pal)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(10)

        title = QLabel("Strumming Patterns")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title, 0)

        combo = QComboBox()
        combo.addItems(["Choose a category…", "Techniques", "Genres", "Difficulty Levels"])
        combo.currentIndexChanged.connect(self.update_patterns)
        layout.addWidget(combo, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent;")
        scroll_area.viewport().setStyleSheet("background: transparent;")

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        self.pattern_layout = QVBoxLayout(content_widget)
        scroll_area.setWidget(content_widget)

        # give scroll_area all the extra vertical space
        layout.addWidget(scroll_area, 1)

        # now your Back button at bottom-right
        back = QPushButton("Back to Tutorial")
        back.setFont(QFont("Segoe UI", 14))
        back.setStyleSheet("color: black; background: white;")
        back.clicked.connect(self.show_tutorial_page)
        layout.addWidget(back, 0, Qt.AlignRight)

        self.setLayout(layout)

    def update_patterns(self, index):
        if index == 0:
            return
        
        # Clear existing patterns
        for i in reversed(range(self.pattern_layout.count())):
            widget = self.pattern_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        selected_category = self.sender().currentText()

        if selected_category == "Techniques":
            self.display_techniques_patterns()
        elif selected_category == "Genres":
            self.display_genres_patterns()
        elif selected_category == "Difficulty Levels":
            self.display_difficulty_patterns()

    def display_techniques_patterns(self):
        techniques = ["Downstroke", "Upstroke", "Alternating Strum"]
        for technique in techniques:
            button = QPushButton(technique)
            button.setStyleSheet("background: white; color: black;")
            button.clicked.connect(lambda checked, t=technique: self.display_text_patterns(t))
            self.pattern_layout.addWidget(button)

    def display_text_patterns(self, technique):
        # Clear previous pattern views (but keep top 3 widgets: title, dropdown, scroll)
        while self.pattern_layout.count() > 3:
            widget = self.pattern_layout.takeAt(3).widget()
            if widget is not None:
                widget.deleteLater()

        # Define strumming text patterns
        text_patterns = {
            "Downstroke": [
                {
                    "pattern": "Down - Down - Down - Down",
                    "visual": "D      D      D      D",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Pause - Down - Pause",
                    "visual": "D      -      D      -",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Down - Pause - Down",
                    "visual": "D      D      -      D",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Pause - Down - Down - Pause",
                    "visual": "-       D      D      -",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Pause - Down - Down - Down",
                    "visual": " -      D      D      D",
                    "timing": "1  &  2  &  3  &  4  &"
                }
                
            ],
            "Upstroke": [
                {
                    "pattern": "Up - Up - Up - Up",
                    "visual": "    U      U      U      U",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Up - Pause - Up - Pause",
                    "visual": "    U       -      U       -",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Up - Up - Pause - Up",
                    "visual": "    U      U      -      U",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Pause - Up - Up - Pause",
                    "visual": "     -       U      U      -",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Pause - Up - Up - Up",
                    "visual": "     -      U      U      U",
                    "timing": "1  &  2  &  3  &  4  &"
                }
            ],
            "Alternating Strum": [
                {
                    "pattern": "Down - Up - Down - Up - Down - Up - Down - Up",
                    "visual": "D  U D U  D  U D  U",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Up - Down - Up - Down - Pause - Pause - Pause",
                    "visual": "D  U  D  U  D  -  -  -",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Pause - Down - Pause - Down - Up - Down - Pause",
                    "visual": "D  -  D  -  D  U  D  -",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Up - Down - Up - Down - Pause - Down - Pause",
                    "visual": "D  U  D  U  D  -  D  -",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Pause - Pause - Pause - Down - Up - Down - Pause",
                    "visual": "D  -   -   -   D  U  D  -",
                    "timing": "1  &  2  &  3  &  4  &"
                }
            ]
        }
        font = QFont("Arial", 14)
        #line_height = 30  # Fix each label's height

        def make_label(text):
            label = QLabel(text)
            label.setFont(font)
            #label.setFixedHeight(line_height)
            label.setAlignment(Qt.AlignLeft)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            return label

        for pat in text_patterns.get(technique, []):
            group_widget = QWidget()
            group_layout = QVBoxLayout(group_widget)

            # Prevent stretching
            group_layout.setSpacing(10)
            group_layout.setContentsMargins(0, 0, 0, 30)  # space *after* pattern group

            # Create labels
            pattern_label = make_label(f"<b>{pat['pattern']}</b>")
            visual_label = make_label(pat['visual'])
            timing_label = make_label(pat['timing'])

            # Add labels tightly
            group_layout.addWidget(pattern_label, 0)
            group_layout.addWidget(visual_label, 0)
            group_layout.addWidget(timing_label, 0)

            self.pattern_layout.addWidget(group_widget)



    def display_genres_patterns(self):
        genres = ["Rock", "Pop", "Blues", "Jazz", "Country", "Classical"]
        for genre in genres:
            button = QPushButton(genre)
            button.setStyleSheet("background: white; color: black;")
            button.clicked.connect(lambda checked, g=genre: self.display_genre_patterns(g))
            self.pattern_layout.addWidget(button)

    def display_genre_patterns(self, genre):
        # Clear previous genre pattern views
        while self.pattern_layout.count() > 3:
            widget = self.pattern_layout.takeAt(3).widget()
            if widget is not None:
                widget.deleteLater()

        genre_patterns = {
            "Rock": [
                {
                    "pattern": "Down - Down - Down - Down",
                    "visual": "D      D      D      D",
                    "timing": "1  2  3  4"
                },
                {
                    "pattern": "Down - Down - Up - Up - Down - Up",
                    "visual": "D  D  U  U  D  U",
                    "timing": "1 2 & & 4 &"
                }
            ],
            "Pop": [
                {
                    "pattern": "Down - Down - Up - Up - Down - Up",
                    "visual": "D  D  U  U  D  U",
                    "timing": "1 2 & & 4 &"
                },
                {
                    "pattern": "Down - Up - Down - Up - Down - Up",
                    "visual": "D  U  D  U  D  U",
                    "timing": "1 & 2 & 3 &"
                }
            ],
            "Blues": [
                {
                    "pattern": "Down - - - Down - Up -",
                    "visual": "D      -      D      U",
                    "timing": "1 & 2 & 3 & 4 & (shuffle)"
                },
                {
                    "pattern": "Down - Up - Down - Up (swing feel)",
                    "visual": "D  U  D  U",
                    "timing": "1 & 2 &"
                }
            ]
        }

        font = QFont("Arial", 14)

        def make_label(text):
            label = QLabel(text)
            label.setFont(font)
            label.setAlignment(Qt.AlignLeft)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            return label

        for pat in genre_patterns.get(genre, []):
            group_widget = QWidget()
            group_layout = QVBoxLayout(group_widget)
            group_layout.setSpacing(10)
            group_layout.setContentsMargins(0, 0, 0, 30)

            pattern_label = make_label(f"<b>{pat['pattern']}</b>")
            visual_label = make_label(pat['visual'])
            timing_label = make_label(pat['timing'])

            group_layout.addWidget(pattern_label, 0)
            group_layout.addWidget(visual_label, 0)
            group_layout.addWidget(timing_label, 0)

            self.pattern_layout.addWidget(group_widget)


    def display_difficulty_patterns(self):
        levels = ["Easy", "Medium", "Hard"]
        for level in levels:
            button = QPushButton(level)
            button.setStyleSheet("background: white; color: black;")
            button.clicked.connect(lambda checked, l=level: self.display_difficulty_level_patterns(l))
            self.pattern_layout.addWidget(button)

    def display_difficulty_level_patterns(self, level):
        while self.pattern_layout.count() > 3:
            widget = self.pattern_layout.takeAt(3).widget()
            if widget is not None:
                widget.deleteLater()

        difficulty_patterns = {
            "Easy": [
                {
                    "pattern": "Down - Down - Down - Down",
                    "visual": "D     D     D     D",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Pause - Down - Pause",
                    "visual": "D     -     D     -",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Down - Pause - Down",
                    "visual": "D     D     -     D",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Up - Down - Up",
                    "visual": "D  U  D  U",
                    "timing": "1  &  2  &"
                },
                {
                    "pattern": "Down - Pause - Down - Up",
                    "visual": "D     -     D     U",
                    "timing": "1  &  2  &"
                }
            ],
            "Medium": [
                {
                    "pattern": "Down - Up - Down - Up - Down - Pause - Down - Up",
                    "visual": "D  U  D  U  D  -  D  U",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Up - Down - Pause - Down - Up - Pause - Up",
                    "visual": "D  U  D  -  D  U  -  U",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Down - Up - Down - Up",
                    "visual": "D  D  U  D  U",
                    "timing": "1 2 & 3 &"
                },
                {
                    "pattern": "Down - Up - Up - Down - Down",
                    "visual": "D  U  U  D  D",
                    "timing": "1 & & 3 4"
                },
                {
                    "pattern": "Down - Down - Up - Up - Down - Down",
                    "visual": "D  D  U  U  D  D",
                    "timing": "1 2 & & 3 4"
                }
            ],
            "Hard": [
                {
                    "pattern": "Down - Up - Down - Up - Down - Up - Down - Up",
                    "visual": "D  U  D  U  D  U  D  U",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Up - Down - Pause - Up - Down - Pause - Up",
                    "visual": "D  U  D  -  U  D  -  U",
                    "timing": "1  &  2  &  3  &  4  &"
                },
                {
                    "pattern": "Down - Down - Up - Down - Up - Down - Up",
                    "visual": "D  D  U  D  U  D  U",
                    "timing": "1 2 & 3 & 4 &"
                },
                {
                    "pattern": "Down - Up - Pause - Up - Down - Up - Down - Pause",
                    "visual": "D  U  -  U  D  U  D  -",
                    "timing": "1 & - & 3 & 4 -"
                },
                {
                    "pattern": "Down - Up - Down - Up - Down - Up - Pause - Up",
                    "visual": "D  U  D  U  D  U  -  U",
                    "timing": "1 & 2 & 3 & 4 &"
                }
            ]
        }

        font = QFont("Arial", 14)

        def make_label(text):
            label = QLabel(text)
            label.setFont(font)
            label.setAlignment(Qt.AlignLeft)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            return label

        for pat in difficulty_patterns.get(level, []):
            group_widget = QWidget()
            group_layout = QVBoxLayout(group_widget)
            group_layout.setSpacing(10)
            group_layout.setContentsMargins(0, 0, 0, 30)

            pattern_label = make_label(f"<b>{pat['pattern']}</b>")
            visual_label = make_label(pat['visual'])
            timing_label = make_label(pat['timing'])

            group_layout.addWidget(pattern_label, 0)
            group_layout.addWidget(visual_label, 0)
            group_layout.addWidget(timing_label, 0)

            self.pattern_layout.addWidget(group_widget)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = StrummingPatternsPage()
    w.resize(800,600)
    w.show()
    sys.exit(app.exec_())