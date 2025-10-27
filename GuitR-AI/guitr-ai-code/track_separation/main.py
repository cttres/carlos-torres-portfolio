import os
import sys
import subprocess
import threading
import traceback
from PyQt5.QtGui import QPainter, QPixmap, QFont
from PyQt5.QtWidgets import (
     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
     QPushButton, QComboBox, QMessageBox, QProgressBar, QSizePolicy, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from theme import light_theme, dark_theme

# === Monkey-patch for compatibility ===
import collections
try:
    collections.MutableSequence
except AttributeError:
    import collections.abc
    collections.MutableSequence = collections.abc.MutableSequence
import numpy as np
if not hasattr(np, 'int'):
    np.int = int
# =======================================

class IsolationWindow(QMainWindow):
    # Signals for thread-safe UI updates
    separation_done = pyqtSignal(str)
    separation_error = pyqtSignal(str)

    def __init__(self, go_back_callback=None):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.setWindowTitle("Track Isolation")
        self.setMinimumSize(800, 600)

        # Connect signals
        self.separation_done.connect(self.on_separation_done)
        self.separation_error.connect(self.on_separation_error)

        # Central widget + layout
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("mainBody")
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(10, 0, 10, 10)

        # Header: theme toggle + title
        header = QWidget(self.central_widget)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 10, 10)
        top_row = QHBoxLayout()
        top_row.addStretch()
        self.theme_button = QPushButton("Dark Mode", header)
        self.theme_button.setObjectName("themeBtn")
        self.theme_button.setFont(QFont("Helvetica", 10))
        self.theme_button.setFixedSize(130, 50)
        self.theme_button.clicked.connect(self.toggleTheme)
        top_row.addWidget(self.theme_button)
        header_layout.addLayout(top_row)
        title = QLabel("Track Isolation", header)
        title.setFont(QFont("Helvetica", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        self.layout.addWidget(header)

        # Instruction
        instr = QLabel("Select a test audio file to isolate the guitar track:", self)
        instr.setFont(QFont("Helvetica", 14))
        instr.setAlignment(Qt.AlignCenter)
        instr.setObjectName("instructionLabel")
        self.layout.addWidget(instr)

        # Locate test_audio folder
        base = os.path.dirname(os.path.abspath(__file__))
        self.test_audio_dir = os.path.join(base, "test_audio")
        if not os.path.isdir(self.test_audio_dir):
            QMessageBox.critical(self, "Error", f"Test audio folder not found:\n{self.test_audio_dir}")
            self.close()
            return

        test_files = [f for f in os.listdir(self.test_audio_dir)
                      if f.lower().endswith((".mp3", ".wav"))]
        if not test_files:
            QMessageBox.critical(self, "Error", "No test audio files found.")
            self.close()
            return

        # Controls: combo + buttons
        self.combo = QComboBox(self)
        self.combo.setObjectName("audioComboBox")    # ← add this line
        self.combo.setFont(QFont("Helvetica", 12))
        self.combo.addItems(test_files)
        
        self.upload_button = QPushButton("Upload", self)
        self.upload_button.setFont(QFont("Helvetica", 12))
        self.upload_button.clicked.connect(self.upload_file)

        # 2) Keep a dict of real paths
        self.file_paths = {name: os.path.join(self.test_audio_dir, name)
                        for name in test_files}
        
        self.run_button = QPushButton("Run Isolation", self)
        self.run_button.setFont(QFont("Helvetica", 14))
        # self.run_button.setFixedWidth(200)
        self.run_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.run_button.clicked.connect(self.run_isolation)
        self.back_button = QPushButton("Back to Main App", self)
        self.back_button.setFont(QFont("Helvetica", 14))
        # self.back_button.setFixedWidth(200)
        self.back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.back_button.clicked.connect(self.go_back)

        card = QWidget(self.central_widget)
        card.setObjectName("cardBody")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)    # internal padding
        card_layout.setSpacing(15)
        card_layout.setAlignment(Qt.AlignTop)

        # Make buttons expand to fill card width
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.run_button.setSizePolicy(size_policy)
        self.back_button.setSizePolicy(size_policy)

        # Add widgets to card
        card_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.combo)
        card_layout.addWidget(self.run_button)
        card_layout.addWidget(self.back_button)
        
        wrapper = QWidget(self.central_widget)
        w_layout = QHBoxLayout(wrapper)
        w_layout.setContentsMargins(0, 60, 200, 0)
        w_layout.addStretch(1)
        w_layout.addWidget(card)
        w_layout.addStretch(2)
        self.layout.addWidget(wrapper)

        # Placeholder for overlay
        # self.overlay = None
        
    def upload_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an audio file",
            "",  # start in cwd
            "Audio Files (*.mp3 *.wav *.flac)"
        )
        if not path:
            return
        name = os.path.basename(path)
        if name in self.file_paths:
            QMessageBox.information(self, "Already added",
                                    f"'{name}' is already in the list.")
        else:
            self.file_paths[name] = path
            self.combo.addItem(name)
        self.combo.setCurrentText(name)

    # And tweak run_isolation to use self.file_paths:
    def run_isolation(self):
        selected = self.combo.currentText()
        in_path = self.file_paths.get(selected)
        if not in_path or not os.path.isfile(in_path):
            QMessageBox.critical(self, "Error", f"File not found:\n{in_path}")
            return
        
        self.run_button.setEnabled(False)

        # Show overlay
        self.overlay = QWidget(self.central_widget)
        self.overlay.setObjectName("loadingPage")
        self.overlay.setStyleSheet("background-color: rgba(255,255,255,0.8);")
        self.overlay.setGeometry(self.central_widget.rect())
        ov_layout = QVBoxLayout(self.overlay)
        ov_layout.setAlignment(Qt.AlignCenter)
        lbl = QLabel("Processing...\nPlease wait", self.overlay)
        lbl.setFont(QFont("Helvetica", 16, QFont.Bold))
        ov_layout.addWidget(lbl)
        self.progress_bar = QProgressBar(self.overlay)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setFixedWidth(200)
        ov_layout.addWidget(self.progress_bar)
        self.overlay.show()

        # Worker thread
        def worker():
            try:
                base_name = os.path.splitext(selected)[0]
                sep_dir = os.path.join(self.test_audio_dir, f"sep_{base_name}")
                os.makedirs(sep_dir, exist_ok=True)
                cmd = [sys.executable, "-m", "demucs", "--out", sep_dir, in_path]
                subprocess.run(cmd, check=True)
                wav_in = os.path.join(sep_dir, "htdemucs", base_name, "other.wav")
                final_wav = os.path.abspath(os.path.join(
                    "..", "chords_recognition", "wav_audio",
                    f"{base_name}_other.wav"
                ))
                os.replace(wav_in, final_wav)
                # Emit success signal
                self.separation_done.emit(sep_dir)
            except Exception as e:
                self.separation_error.emit(str(e))

        threading.Thread(target=worker, daemon=True).start()

    @pyqtSlot(str)
    def on_separation_done(self, sep_dir):
        if self.overlay:
            self.overlay.hide()
            self.overlay.deleteLater()
        self.run_button.setEnabled(True)
        QMessageBox.information(
            self,
            "Separation Complete",
            f"Demucs finished!\n\nAll stems are in:\n{sep_dir}"
        )

    @pyqtSlot(str)
    def on_separation_error(self, msg):
        if self.overlay:
            self.overlay.hide()
            self.overlay.deleteLater()
        self.run_button.setEnabled(True)
        QMessageBox.critical(self, "Error", msg)

    def paintEvent(self, event):
        painter = QPainter(self)
        bg = QPixmap("guitar_bg.jpg") if self.theme_button.text() == "Dark Mode" else QPixmap("guitar_bgD.jpg")
        painter.drawPixmap(self.rect(), bg)

    def go_back(self):
        try:
            cur = os.path.dirname(os.path.abspath(__file__))
            menu_dir = os.path.join(os.path.dirname(cur), "menu")
            script = os.path.join(menu_dir, "main.py")
            self.close()
            subprocess.Popen([sys.executable, script], cwd=menu_dir)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open menu:\n{e}")

    def toggleTheme(self):
        app = QApplication.instance()
        if self.theme_button.text() == "Dark Mode":
            app.setStyleSheet(dark_theme)
            self.theme_button.setText("Light Mode")
        else:
            app.setStyleSheet(light_theme)
            self.theme_button.setText("Dark Mode")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet(light_theme)
        window = IsolationWindow()
        window.show()
        sys.exit(app.exec())
    except Exception:
        traceback.print_exc()