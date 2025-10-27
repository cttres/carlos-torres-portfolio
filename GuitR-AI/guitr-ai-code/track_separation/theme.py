light_theme = """
QMainWindow {
    background-color: transparent;
}


/* Remove or reduce white overlay */
QWidget#mainBody {
    background-color: transparent; /* remove white overlay entirely */
}

/* Optional: card-like container (if you gave it this objectName) */
QWidget#cardBody {
  background-color: rgba(255,255,255,230); /* solid white */
  border-radius: 20px;
  padding: 30px;
}

QLabel#titleLabel {
    font-size: 20px;
    font-weight: bold;
    color: #2c3e50;
    background-color: rgba(255, 255, 255, 180);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    color: #000000;
}

QPushButton {
    background-color: #8AC6D1;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
    margin: 8px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #9BD2DC;
}

QPushButton:pressed {
    background-color: #78B9C2;
}

QComboBox {
    background-color: white;
    border: 1px solid #bbb;
    border-radius: 6px;
    padding: 6px;
    min-width: 200px;
    color: #2c3e50;
}

QLabel {
    color: #000000; /* also black */
}

#instructionLabel {
    color: #000000; /* also black */
}
"""

dark_theme = """
/* fill the window with your dark background pixmap */
QMainWindow {
    border-image: url(bg/guitar_bgD.jpg) 0 0 0 0 stretch stretch;
}

/* reset all widgets to transparent by default */
* {
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
    font-family: "Helvetica";
}

/* tooltips */
QToolTip {
    color: #999999;
    background-color: #071013;
    border: none;
    padding: 4px;
}

/* main body still transparent so we see the pixmap */
QWidget#mainBody {
    background: transparent;
}

/* header container stays transparent */
QWidget#header {
    background: transparent;
    margin: 0;
    padding: 0;
}

/* title label in header */
QLabel#titleLabel, QWidget#header QLabel {
    font-family: "Helvetica";
    font-weight: bold;
    font-size: 20px;
    color: #FFFFFF;
    margin: 0;
    padding: 0;
}

/* instruction text */
QLabel#instructionLabel {
    color: #DFE0E2;
    font-size: 14px;
}

/* standard labels */
QLabel {
    color: #DFE0E2;
}

QPushButton#themeBtn {
    background-color: #1D70A2;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
    margin: 8px;
    font-size: 14px;
}
QPushButton#themeBtn:hover {
    background-color: #378EBF;   /* same “feel” you liked earlier */
}
QPushButton#themeBtn:pressed {
    background-color: #155A85;   /* a slightly darker press state of 1D70A2 */
}

/* standard buttons */
QPushButton {
    background-color: #BA1F49;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
    margin: 8px;
    font-size: 14px;
}
/* hover and pressed states */
QPushButton:hover {
    background-color: #9E1A3D;
}
QPushButton:pressed {
    background-color: #7F1431;
}

/* isolate “card” widgets */
QWidget#cardBody {
    background-color: rgba(0, 0, 0, 150);
    border-radius: 20px;
    padding: 30px;
    max-width: 200px;
    min-width: 200px;
}

QComboBox#audioComboBox {
    background-color: #FFFFFF;        /* white background */
    color: #2c3e50;                   /* dark text */
    border: 1px solid #CCCCCC;        /* same light-mode border */
    border-radius: 6px;
    padding: 4px 30px 4px 8px;
    min-width: 180px;
    max-width: 180px;
}

/* drop-down arrow area */
QComboBox#audioComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: none;
}

/* the little arrow itself */
QComboBox#audioComboBox::down-arrow {
    width: 12px;
    height: 12px;
}

/* make QMessageBox fully opaque & dark background */
QMessageBox {
    background-color: #303030;      /* solid dark grey */
    border: 1px solid #555555;
    border-radius: 8px;
}

/* all labels inside a QMessageBox */
QMessageBox QLabel {
    color: #FFFFFF;                /* bright white text */
}

/* the standard icon area (if you want to tweak it) */
QMessageBox QLabel#qt_msgbox_icon_label {
    /* leave default or override */
}

/* buttons in the dialog */
QMessageBox QPushButton {
    background-color: #BA1F49;
    color: white;
    border-radius: 6px;
    padding: 6px 12px;
}

QWidget#loadingPage {
    background-color: rgba(255, 255, 255, 0.9); /* almost-opaque white */
}

QWidget#loadingPage QLabel {
    color: #000000;                /* full black text */
    background: transparent;
}

/* style the indeterminate bar track */
QWidget#loadingPage QProgressBar {
    background-color: #EEEEEE;     /* light grey track */
    border: 1px solid #CCCCCC;
    border-radius: 6px;
    height: 12px;
}

/* the moving “chunk” */
QWidget#loadingPage QProgressBar::chunk {
    background-color: #8AC6D1;     /* your light-blue accent */
}
"""
