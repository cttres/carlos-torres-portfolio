 # === Monkey Patch for Python 3.11 Compatibility ===
import collections
try:
    collections.MutableSequence
except AttributeError:
    import collections.abc
    collections.MutableSequence = collections.abc.MutableSequence
# ================================================

# --- Monkey Patch for NumPy deprecation of np.int and np.float ---
import numpy as np
if not hasattr(np, 'int'):
    np.int = int
if not hasattr(np, 'float'):
    np.float = float
# -----------------------------------------------------

import os
import sys
import traceback
import subprocess
import base64

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QLabel, QVBoxLayout, QWidget,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QPainterPath
from PyQt5.QtCore import Qt, QTimer, QUrl, QRect, QRectF

from interface import *
from chords import *
from key import *
from tempo import *

# Import themes from theme.py (make sure theme.py is in the same folder)
from theme import light_theme, dark_theme

# --- Mapping chords and their chord image paths ---
CHORD_IMAGE_MAP = {
    "A": "a-major-1.png",
    "Am": "a-minor-1.png",
    "B": "b-major-1.gif",
    "Bm": "b-minor-1.png",
    "C": "c-major-1.png",
    "Cm": "c-minor-1.gif",
    "D": "d-major-1.png",
    "Dm": "d-minor-1.gif",
    "E": "e-major-1.png",
    "Em": "e-minor-1.png",
    "F": "f-major-1.png",
    "Fm": "f-minor-1.gif",
    "G": "g-major-1.png",
    "Gm": "g-minor-3.gif",
    # Extend this mapping as needed.
}

# --------------------------------------------
# Custom widget for chord progress background
# with rounded background and progress fill.
# --------------------------------------------
class ChordProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # A float between 0.0 and 1.0 to represent the progress.
        self.progress_fraction = 0.0
        # Default colors – these will be overridden by updateThemeColors().
        self.progress_color = QColor("#706993")
        self.base_color = QColor("#23B5D3")
        # Corner radius for the background.
        self.corner_radius = 20

    def setProgress(self, fraction):
        """Update the progress fraction (0.0 to 1.0) and repaint."""
        self.progress_fraction = max(0.0, min(fraction, 1.0))
        self.update()

    def setCornerRadius(self, radius):
        """Allow setting the container's corner radius on the fly."""
        self.corner_radius = radius
        self.update()

    def updateThemeColors(self, is_dark):
        """Set widget colors based on the current theme.
           Dark mode uses a red-ish background; light mode uses blue-ish."""
        if is_dark:
            self.base_color = QColor("#330D33")  # Red-ish for dark mode.
            self.progress_color = QColor("#706993")
        else:
            self.base_color = QColor("#12a4c2")  # Blue-ish for light mode.
            self.progress_color = QColor("#23B5D3")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        rectF = QRectF(rect)
        path = QPainterPath()
        path.addRoundedRect(rectF, float(self.corner_radius), float(self.corner_radius))
        painter.setClipPath(path)

        painter.fillRect(rect, self.base_color)
        
        progress_width = int(rect.width() * self.progress_fraction)
        if progress_width > 0:
            progress_rect = QRect(rect.x(), rect.y(), progress_width, rect.height())
            painter.fillRect(progress_rect, self.progress_color)
        
        super().paintEvent(event)


# ---------------------
# Main Application Code
# ---------------------
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Replace the right-side "DeChord!" text with a new logo image.
        self.ui.appNameLabel.clear()
        new_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RightLogo.png")
        if os.path.exists(new_logo_path):
            self.ui.appNameLabel.setPixmap(
                QPixmap(new_logo_path).scaled(120, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        
        # Remove unwanted footer widgets.
        if hasattr(self.ui, "authorLabel"):
            self.ui.authorLabel.setParent(None)
            self.ui.authorLabel.deleteLater()
        if hasattr(self.ui, "githubBtn"):
            self.ui.githubBtn.setParent(None)
            self.ui.githubBtn.deleteLater()
        
        # Replace the single current chord button with a chord container widget.
        parent_widget = self.ui.currentChordBtn.parent()
        layout = parent_widget.layout()
        old_btn_index = layout.indexOf(self.ui.currentChordBtn)
        layout.removeWidget(self.ui.currentChordBtn)
        self.ui.currentChordBtn.hide()
        
        self.chordContainer = ChordProgressWidget(parent_widget)
        self.chordContainer.setCornerRadius(30)
        
        self.currentChordLayout = QVBoxLayout(self.chordContainer)
        self.currentChordLayout.setContentsMargins(0, 0, 0, 0)
        self.currentChordLayout.setSpacing(0)
        
        if not hasattr(self.ui, "currentChordNameLabel"):
            self.ui.currentChordNameLabel = QLabel()
            self.ui.currentChordNameLabel.setObjectName("currentChordNameLabel")
            self.ui.currentChordNameLabel.setAlignment(Qt.AlignCenter)
            self.ui.currentChordNameLabel.setStyleSheet("background: transparent;")
        
        if not hasattr(self.ui, "currentChordImageLabel"):
            self.ui.currentChordImageLabel = QLabel()
            self.ui.currentChordImageLabel.setObjectName("currentChordImageLabel")
            self.ui.currentChordImageLabel.setAlignment(Qt.AlignCenter)
            self.ui.currentChordImageLabel.setStyleSheet("background: transparent;")
        
        default_logo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "chords_images",
            "GuitR-AILogo.png"
        )
        if os.path.exists(default_logo_path):
            default_pixmap = QPixmap(default_logo_path)
            default_pixmap = self.roundCornersPixmap(default_pixmap, radius=20)
            self.ui.currentChordImageLabel.setPixmap(default_pixmap)
        
        self.currentChordLayout.addWidget(self.ui.currentChordNameLabel)
        self.currentChordLayout.addWidget(self.ui.currentChordImageLabel)
        
        layout.insertWidget(old_btn_index, self.chordContainer)
        
        if hasattr(self.ui, "minimizeBtn"):
            self.ui.minimizeBtn.hide()
        if hasattr(self.ui, "closeBtn"):
            self.ui.closeBtn.hide()
        
        # Add "Back to Menu" Button next to the theme toggle button.
        self.backMenuButton = QPushButton("Back to Menu", self)
        self.backMenuButton.setFixedSize(150, 40)
        # Set an initial style for dark mode.
        self.backMenuButton.setStyleSheet("""
            QPushButton {
                background-color: #440D44;
                border: none;
                border-radius: 2px;
                padding: 5px;
                font-size: 12px;
                color: white;
                min-width: 75px;
                max-width: 75px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f6391;
            }
        """)
        self.backMenuButton.clicked.connect(self.go_back_to_menu)
        try:
            theme_parent = self.ui.themeBtn.parent()
            theme_layout = theme_parent.layout()
            if theme_layout is not None:
                index = theme_layout.indexOf(self.ui.themeBtn)
                theme_layout.insertWidget(index + 1, self.backMenuButton)
            else:
                raise Exception("Theme button layout not found.")
        except Exception as e:
            if self.ui.centralwidget is not None and self.ui.centralwidget.layout() is not None:
                self.ui.centralwidget.layout().addWidget(self.backMenuButton)
            else:
                layout_new = QVBoxLayout(self)
                layout_new.addWidget(self.backMenuButton)
                self.setLayout(layout_new)
        
        self.show()
        
        self.offset = None
        self.chords = []
        self.chord_index = 0
        self.start_time = None
        self.is_muted = False
        
        self.is_dark = True  
        self.load_stack = 1
        self.setAcceptDrops(True)
        
        from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.update_chords)
        self.player.durationChanged.connect(self.update_duration)
        self.player.stateChanged.connect(self.update_state)
        self.player.mediaStatusChanged.connect(self.update_media)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        
        self.ui.minimizeBtn.clicked.connect(lambda: self.showMinimized())
        self.ui.closeBtn.clicked.connect(lambda: self.close())
        self.ui.mediaOpenBtn.clicked.connect(self.load_audio)
        self.ui.mediaPlayBtn.clicked.connect(self.play_pause)
        self.ui.prePrevChordBtn.clicked.connect(self.play_pause)
        self.ui.prevChordBtn.clicked.connect(self.play_pause)
        self.ui.nxtChordBtn.clicked.connect(self.play_pause)
        self.ui.postNxtChordBtn.clicked.connect(self.play_pause)
        self.ui.themeBtn.clicked.connect(self.toggle_theme)
        self.ui.saveChordsBtn.clicked.connect(self.export_chords)
        self.ui.seekNxtBtn.clicked.connect(lambda: self.seek(10000))
        self.ui.seekPrevBtn.clicked.connect(lambda: self.seek(-10000))
        self.ui.mediaMuteBtn.clicked.connect(self.mute_unmute)
        self.ui.volumeSlider.sliderMoved.connect(self.set_volume)
        self.ui.mediaProgressSlider.sliderPressed.connect(lambda: self.timer.stop())
        self.ui.mediaProgressSlider.sliderMoved.connect(self.set_position)
        self.ui.mediaProgressSlider.sliderReleased.connect(lambda: self.timer.start(100))
        
        self.resize(1200, 800)
        self.setMinimumSize(1024, 768)
        
        # Force initial update of the chord container colors.
        self.chordContainer.updateThemeColors(self.is_dark)
        # Also set the initial backMenuButton style.
        self.updateBackMenuButtonStyle(self.is_dark)
    
    def roundCornersPixmap(self, pixmap, radius):
        size = pixmap.size()
        rounded = QPixmap(size)
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, size.width(), size.height()), float(radius), float(radius))
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return rounded

    def updateBackMenuButtonStyle(self, is_dark):
        """Update the back menu button style to match the theme."""
        if is_dark:
            style = """
                QPushButton {
                    background-color: #440D44;
                    border: none;
                    border-radius: 15px;
                    padding: 10px;
                    font-size: 12px;
                    color: white;
                    min-width: 75px;
                    max-width: 75px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #1f6391;
                }
            """
        else:
            style = """
                QPushButton {
                    background-color: #12a4c2;
                    border: none;
                    border-radius: 2px;
                    padding: 5px;
                    font-size: 12px;
                    color: black;
                    min-width: 75px;
                    max-width: 75px;
                }
                QPushButton:hover {
                    background-color: #23B5D3;
                }
                QPushButton:pressed {
                    background-color: #2980b9;
                }
            """
        self.backMenuButton.setStyleSheet(style)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.ui.themeBtn.setIcon(QIcon(":/icons/sun.svg" if self.is_dark else ":/icons/moon.svg"))
        if self.is_dark:
            self.setStyleSheet(dark_theme)
        else:
            self.setStyleSheet(light_theme)
        self.load_stack = 1 if self.is_dark else 2
        self.chordContainer.updateThemeColors(self.is_dark)
        # Update the "Back to Menu" button to match the new theme.
        self.updateBackMenuButtonStyle(self.is_dark)

    def update_position(self):
        position = self.player.position()
        self.ui.mediaProgressSlider.setValue(position)
        self.ui.currentPlayedLabel.setText(f'{position // 60000}:{(position % 60000) // 1000:02d}')
        self.update_chords(position)

    def update_duration(self, duration):
        self.ui.mediaProgressSlider.setRange(0, duration)
        self.ui.mediaDurationLabel.setText(f'{duration // 60000}:{(duration % 60000) // 1000:02d}')

    def play_pause(self):
        if self.player.state() == self.player.PlayingState:
            self.player.pause()
            self.timer.stop()
        else:
            self.player.play()
            self.timer.start(100)

    def seek(self, milliseconds):
        new_position = self.player.position() + milliseconds
        if new_position < 0 or new_position > self.player.duration():
            self.set_position(0)
            self.player.stop()
        else:
            self.player.setPosition(new_position)
            self.update_chords(new_position)

    def set_position(self, position):
        self.player.setPosition(position)
        self.update_chords(position)

    def mute_unmute(self):
        self.is_muted = not self.is_muted
        self.player.setMuted(self.is_muted)
        self.ui.mediaMuteBtn.setIcon(QIcon(":/icons/volume-x.svg" if self.is_muted else ":/icons/volume-2.svg"))
        self.ui.volumeSlider.setEnabled(not self.is_muted)

    def update_chords(self, position):
        current_time = position
        if self.chord_index > 0 and self.chord_index < len(self.chords) and self.chords[self.chord_index][1] > current_time / 1000.0:
            self.chord_index = 0
        while self.chord_index < len(self.chords) and self.chords[self.chord_index][1] <= current_time / 1000.0:
            self.chord_index += 1

        pre_previous_chord = previous_chord = current_chord = next_chord = post_next_chord = None
        if self.chord_index < len(self.chords):
            current_chord = self.chords[self.chord_index][2]
            current_chord_start_time = self.chords[self.chord_index][0]
            current_chord_end_time = self.chords[self.chord_index][1]
            if self.chord_index > 0:
                previous_chord = self.chords[self.chord_index - 1][2]
            if self.chord_index > 1:
                pre_previous_chord = self.chords[self.chord_index - 2][2]
            if self.chord_index + 1 < len(self.chords):
                next_chord = self.chords[self.chord_index + 1][2]
            if self.chord_index + 2 < len(self.chords):
                post_next_chord = self.chords[self.chord_index + 2][2]

            chord_duration = current_chord_end_time - current_chord_start_time
            time_elapsed = (current_time / 1000.0) - current_chord_start_time
            if chord_duration > 0:
                progress_fraction = time_elapsed / chord_duration
                self.chordContainer.setProgress(progress_fraction)

        self.ui.prePrevChordBtn.setText(f"{pre_previous_chord}" if pre_previous_chord else "")
        self.ui.prevChordBtn.setText(f"{previous_chord}" if previous_chord else "")
        self.ui.nxtChordBtn.setText(f"{next_chord}" if next_chord else "")
        self.ui.postNxtChordBtn.setText(f"{post_next_chord}" if post_next_chord else "")

        if current_chord:
            self.ui.currentChordNameLabel.setText(current_chord)
            chord_image_filename = CHORD_IMAGE_MAP.get(current_chord)
            if chord_image_filename:
                chord_image_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "chords_images",
                    chord_image_filename
                )
                if os.path.exists(chord_image_path):
                    pixmap = QPixmap(chord_image_path)
                    pixmap = self.roundCornersPixmap(pixmap, radius=20)
                    self.ui.currentChordImageLabel.setPixmap(pixmap)
                else:
                    self.ui.currentChordImageLabel.clear()
            else:
                self.ui.currentChordImageLabel.clear()
        else:
            self.ui.currentChordNameLabel.setText("")
            default_logo_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "chords_images",
                "GuitR-AILogo.png"
            )
            if os.path.exists(default_logo_path):
                default_pixmap = QPixmap(default_logo_path)
                default_pixmap = self.roundCornersPixmap(default_pixmap, radius=20)
                self.ui.currentChordImageLabel.setPixmap(default_pixmap)
            else:
                self.ui.currentChordImageLabel.clear()

    def update_media(self, status):
        from PyQt5.QtMultimedia import QMediaPlayer
        if status == QMediaPlayer.EndOfMedia:
            self.timer.stop()
            self.set_position(0)
            self.chord_index = 0
            self.update_chords(0)
            self.player.stop()
            self.ui.mediaPlayBtn.setIcon(QIcon(u":/icons/play.svg"))

    def set_volume(self, volume):
        self.player.setVolume(volume)

    def update_state(self, state):
        icons = {self.player.PlayingState: "pause.svg", self.player.PausedState: "play.svg"}
        self.ui.mediaPlayBtn.setIcon(QIcon(f":/icons/{icons.get(state, 'play.svg')}"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def load_audio(self, fileName=None):
        if not fileName:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(
                self, "Open Audio File", "",
                "Audio Files (*.wav *.mp3 *.m4a *.aac)", options=options
            )
        if fileName:
            self.timer.stop()
            self.player.stop()
            from PyQt5.QtMultimedia import QMediaContent
            self.player.setMedia(QMediaContent())
            self.ui.mediaProgressSlider.setValue(0)
            self.chord_index = 0
            self.ui.keyLabel.clear()
            self.audio_file = fileName
            self.media_title = fileName.split("/")[-1].rsplit(".", 1)[0]
            self.ui.mediaTitleLabel.setText(self.media_title)
            self.ui.errGif.start()
            self.ui.loadingGif.start()
            self.ui.appStacks.setCurrentIndex(self.load_stack)
            self.chord_thread = ChordRecognitionThread(fileName)
            self.chord_thread.result.connect(self.on_chords_recognized)
            self.chord_thread.start()
            self.tempo_thread = TempoDetectionThread(fileName)
            self.tempo_thread.result.connect(self.on_tempo_detected)
            self.tempo_thread.start()
            self.key_thread = KeyRecognitionThread(fileName)
            self.key_thread.result.connect(self.on_key_recognized)
            self.key_thread.start()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))

    def on_tempo_detected(self, tempo):
        self.tempo = tempo
        current_text = self.ui.keyLabel.text()
        if current_text:
            updated_text = f"{current_text}  |  {tempo} BPM"
            self.ui.keyLabel.setText(updated_text)
        else:
            self.ui.keyLabel.setText(f"{tempo} BPM")
        self.ui.keyLabel.show()

    def on_chords_recognized(self, chords):
        self.chords = chords
        self.ui.appStacks.setCurrentIndex(0)
        self.ui.errGif.stop()
        self.ui.loadingGif.stop()
        self.play_pause()
        self.ui.mediaProgressSlider.setEnabled(True)
        self.ui.chordSlider.setEnabled(True)
        self.ui.mediaPlayBtn.setEnabled(True)
        self.ui.seekPrevBtn.setEnabled(True)
        self.ui.seekNxtBtn.setEnabled(True)
        self.ui.saveChordsBtn.setEnabled(True)

    def on_key_recognized(self, key):
        self.key = key
        current_text = self.ui.keyLabel.text()
        if current_text:
            updated_text = f"{current_text}  |  {key}"
            self.ui.keyLabel.setText(updated_text)
        else:
            self.ui.keyLabel.setText(key)
        self.ui.keyLabel.show()

    def export_chords(self):
        if self.chords:
            os.makedirs('./export', exist_ok=True)
            file_path = f"./export/{self.media_title}.txt"
            with open(file_path, 'w') as file:
                for chord in self.chords:
                    start_time, end_time, chord_label = chord
                    file.write(f"({self.format_time(start_time)} - {self.format_time(end_time)}): {chord_label}\n")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.load_audio(urls[0].toLocalFile())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Minus:
            self.showMinimized()
        if event.key() == Qt.Key_T:
            self.ui.themeBtn.click()
        if event.key() == Qt.Key_P:
            self.ui.mediaPlayBtn.click()
        if event.key() == Qt.Key_V:
            self.ui.mediaPlayBtn.click()
        if event.key() == Qt.Key_Left:
            self.ui.seekPrevBtn.click()
        if event.key() == Qt.Key_Right:
            self.ui.seekNxtBtn.click()
        if event.key() == Qt.Key_C:
            self.ui.seekPrevBtn.click()
        if event.key() == Qt.Key_B:
            self.ui.seekNxtBtn.click()
        if event.key() == Qt.Key_M:
            self.ui.mediaMuteBtn.click()
        if event.key() == Qt.Key_O:
            self.ui.mediaOpenBtn.click()
        if event.key() == Qt.Key_E:
            self.ui.saveChordsBtn.click()

    def format_time(self, s):
        seconds = s % 60
        minutes = (s / 60) % 60
        hours = (s / (60 * 60)) % 24
        if int(hours) > 0:
            return "%02d:%02d:%02d" % (hours, minutes, round(seconds))
        else:
            return "%02d:%02d" % (minutes, round(seconds))
    
    def go_back_to_menu(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            menu_dir = os.path.join(parent_dir, "menu")
            menu_main_script = os.path.join(menu_dir, "main.py")
            self.close()
            subprocess.Popen([sys.executable, menu_main_script], cwd=menu_dir)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open the menu:\n{str(e)}")

def handle_exception(exc_type, exc_value, exc_traceback):
    traceback.print_exception(exc_type, exc_value, exc_traceback)

sys.excepthook = handle_exception

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(dark_theme)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())