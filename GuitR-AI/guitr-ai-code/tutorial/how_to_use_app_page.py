# /tutorial/how_to_use_app_page.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui  import QFont, QPalette, QColor

class HowToUseAppPage(QWidget):
    def __init__(self, show_tutorial_page):
        super().__init__()

        self.show_tutorial_page = show_tutorial_page
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
        title = QLabel("🎸 How to Use the App")
        title.setObjectName("title")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignTop)
        layout.addWidget(title)

        # Usage Description Content (rich text)
        usage_text = """

        <h3>1. 🧪 Track Isolation</h3>
        <p>
        The <b>Isolation</b> page lets you extract the guitar track from a full song.
        </p>
        <ul>
            <li><b>Step 1:</b> Choose one of the test clips from the drop-down menu or upload your own audio file.</li>
            <li><b>Either select your own file or use one of the test clips:</li>
                <ul>
                    <li>test_clip0.mp3</li>
                    <li>test_clip1.mp3</li>
                    <li>test_clip2.mp3</li>
                </ul>
            </li>
            <li><b>Step 2:</b> Click the <i>Run Isolation</i> button.</li>
            <li><b>Step 3:</b> Wait a few minutes while the tool isolates the guitar track.</li>
            <li><b>Step 4:</b> Once complete, the isolated track is saved to your computer.</li>
        </ul>
        <p><i>Tip: Use the Dark Mode toggle to switch between light and dark themes.</i></p>

        <h3>2. 🎵 Chord Recognition</h3>
        <p>
        The <b>Recognition</b> page analyzes the isolated guitar track and shows chords in real-time.
        </p>
        <ul>
            <li><b>Step 1:</b> Click the folder icon to select your saved isolated track.</li>
            <li><b>Step 2:</b> The app will analyze the track (just a few seconds).</li>
            <li><b>Step 3:</b> The track plays with:
                <ul>
                    <li>Current chord name</li>
                    <li>Chord diagram (finger positions)</li>
                    <li>A progress bar that fills before switching chords</li>
                    <li>Two upcoming chords shown in advance</li>
                </ul>
            </li>
            <li><b>Step 4:</b> Use the playback bar at the bottom to:
                <ul>
                    <li>Play/Pause</li>
                    <li>Adjust volume</li>
                    <li>See song length</li>
                </ul>
            </li>
        </ul>
        <p><i>Enjoy!</i></p>
        """

        usage_description = QLabel(usage_text)
        usage_description.setObjectName("content")
        usage_description.setWordWrap(True)
        usage_description.setFont(QFont("Segoe UI", 18, QFont.Bold))
        usage_description.setStyleSheet("color: white;")
        usage_description.setTextFormat(Qt.RichText)
        usage_description.setAlignment(Qt.AlignTop)
        layout.addWidget(usage_description)

        # Back button to return to the tutorial page
        back_button = QPushButton("Back to Tutorial")
        back_button.clicked.connect(self.show_tutorial_page)
        layout.addWidget(back_button)

        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        self.setLayout(layout)

