import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
)
from PyQt5.QtGui    import QPixmap, QFont
from PyQt5.QtCore   import Qt

class TutorialPage(QWidget):
    def __init__(self, show_anatomy_page, show_strumming_page, show_usage_page):
        super().__init__()
        self.show_anatomy_page   = show_anatomy_page
        self.show_strumming_page = show_strumming_page
        self.show_usage_page     = show_usage_page
        self.init_ui()

    def init_ui(self):
        # ─── Background Image ─────────────────────────────
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True)
        img = os.path.join(os.path.dirname(__file__),
                           "..", "chords_images", "background.png")
        pix = QPixmap(img)
        if pix.isNull():
            print("❌ Failed to load background:", img)
        else:
            self.background_label.setPixmap(pix)
        self.background_label.lower()

        # ─── Transparent Overlay ───────────────────────────
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background: transparent;")
        # Enable mouse events on the overlay (so buttons work)
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        # Layout for all your controls
        olay = QVBoxLayout(self.overlay)
        olay.setContentsMargins(20, 20, 20, 20)
        olay.setSpacing(10)

        # Title
        title = QLabel("Welcome to the GuitR-AI Tutorial")
        title.setStyleSheet("color:white; font-size:45px; font-weight:bold;")
        title.setAlignment(Qt.AlignLeft)
        olay.addWidget(title)

        # Navigation buttons
        for text, cb in [
            ("Guitar Anatomy",    self.show_anatomy_page),
            ("Strumming Patterns",self.show_strumming_page),
            ("How to Use the App",self.show_usage_page),
        ]:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 14))
            btn.setStyleSheet("""
                background-color: white;
                color:            black;
                border:           1px solid #ccc;
                border-radius:    5px;
                padding:          8px;
            """)
            btn.clicked.connect(cb)
            olay.addWidget(btn)

        # ─── Exit Button on the Overlay ───────────────────
        self.exit_btn = QPushButton("✕", self.overlay)
        self.exit_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.exit_btn.setStyleSheet(
            "background:transparent; color:white; border:none;"
        )
        self.exit_btn.setFixedSize(40, 40)
        self.exit_btn.clicked.connect(QApplication.instance().quit)
        self.exit_btn.show()

    def resizeEvent(self, event):
        # 1) Stretch the background image to fill the page
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # 2) Stretch the overlay to cover too
        self.overlay.setGeometry(0, 0, self.width(), self.height())

        # 3) Pin the exit-button at top-right of the overlay
        m = 16
        self.exit_btn.move(
            self.width()  - self.exit_btn.width()  - m,
            m
        )
        super().resizeEvent(event)



# import tkinter as tk
# from PIL import Image, ImageTk
# import os


# def show_tutorial_page(root, go_back_callback):
#     # Clear the window and set the size for the tutorial page
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.geometry("800x600")

#     # Configure the root grid to allow centering
#     root.grid_rowconfigure(0, weight=1)
#     root.grid_columnconfigure(0, weight=1)

#     tutorial_frame = tk.Frame(root, bg="#d3d3d3")
#     tutorial_frame.grid(row=0, column=0, sticky="nsew")  # Fill available space

#     # Configure the tutorial_frame grid to center elements
#     tutorial_frame.grid_columnconfigure(0, weight=1)
#     tutorial_frame.grid_rowconfigure(0, weight=0)

#     title_label = tk.Label(tutorial_frame, text="Learning Center", font=("Helvetica", 24, "bold"), bg="#d3d3d3")
#     title_label.grid(row=0, column=0, pady=20, sticky="n")

#     # Buttons
#     anatomy_button = tk.Button(tutorial_frame, text="Guitar Anatomy", font=("Helvetica", 14),
#                                command=lambda: show_guitar_anatomy(root, go_back_callback))
#     anatomy_button.grid(row=2, column=0, pady=10)

#     strumming_button = tk.Button(tutorial_frame, text="Strumming Patterns", font=("Helvetica", 14),
#                                  command=lambda: show_strumming_patterns(root, go_back_callback))
#     strumming_button.grid(row=3, column=0, pady=10)

#     app_usage_button = tk.Button(tutorial_frame, text="How to Use App", font=("Helvetica", 14),
#                                  command=lambda: show_how_to_use_app(root, go_back_callback))
#     app_usage_button.grid(row=4, column=0, pady=10)

#     # Back button
#     back_button = tk.Button(tutorial_frame, text="Back to Main Menu", font=("Helvetica", 12),
#                             command=go_back_callback)
#     back_button.grid(row=5, column=0, pady=20)

#     # Additional row configuration for centering
#     tutorial_frame.grid_rowconfigure(6, weight=1)  # Push everything up slightly


# def show_guitar_anatomy(root, go_back_callback):
#     # Display a brief explanation and image of the guitar anatomy
#     for widget in root.winfo_children():
#         widget.destroy()
#     anatomy_frame = tk.Frame(root, bg="#d3d3d3")
#     anatomy_frame.grid(row=0, column=0, sticky="nsew")  # Use grid for layout

#     anatomy_title = tk.Label(anatomy_frame, text="Guitar Anatomy", font=("Helvetica", 24, "bold"), bg="#d3d3d3")
#     anatomy_title.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")  # Title spans two columns

#     base_path = os.path.dirname(os.path.abspath(__file__))
#     image_path = os.path.join(base_path, "chords_images", "guitar_anatomy.png")

#     try:
#         image = Image.open(image_path)  # Open image using absolute path
#         image = image.resize((400, 500), Image.LANCZOS)
#         guitar_img = ImageTk.PhotoImage(image)
    
#         img_label = tk.Label(anatomy_frame, image=guitar_img, bg="#d3d3d3")
#         img_label.image = guitar_img  # Keep reference
#         img_label.grid(row=1, column=1, padx=20, pady=10)  # Place image on the right
#     except Exception as e:
#         print("Error loading guitar anatomy image:", e)
#         error_label = tk.Label(anatomy_frame, text="Image not found!", font=("Helvetica", 14, "bold"), fg="red", bg="#d3d3d3")
#         error_label.grid(row=1, column=0, columnspan=2, pady=10)

#     fretboard_button = tk.Button(anatomy_frame, text="STUDY THE FRETBOARD HERE", font=("Helvetica", 14),
#                                  command=lambda: show_fretboard_page(root, go_back_callback))
#     fretboard_button.grid(row=4, column=1, pady=10)

#     # Create button frames for both left and right sections
#     left_button_frame = tk.Frame(anatomy_frame, bg="#d3d3d3")
#     left_button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="e")  # Left side

#     right_button_frame = tk.Frame(anatomy_frame, bg="#d3d3d3")
#     right_button_frame.grid(row=1, column=2, padx=20, pady=10, sticky="w")  # Right side

#     # Label to display descriptions (initially empty)
#     description_label = tk.Label(anatomy_frame, text="", font=("Helvetica", 12), bg="#d3d3d3", wraplength=400, justify="center")
#     description_label.grid(row=2, column=1, pady=10)

#     # Tooltip Label (initially hidden)
#     tooltip = tk.Label(root, text="", font=("Helvetica", 10), bg="white", fg="black", relief="solid", borderwidth=1, wraplength=200)
#     tooltip.place_forget()  # Hide initially

#     # Function to show tooltip near the cursor
#     def show_tooltip(event, text):
#         tooltip.config(text=text)
#         # Get the button's position
#         x = event.widget.winfo_rootx()
#         y = event.widget.winfo_rooty()

#         # Move the tooltip up above the button (adjust for better spacing)
#         y -= 75  # Move the tooltip 30 pixels above the button

#         # Position tooltip just slightly to the right of the button
#         x += event.widget.winfo_width() + 10
#         tooltip.place(x=x, y=y)

#     # Function to hide tooltip
#     def hide_tooltip(event):
#         tooltip.place_forget()

#     # Button Definitions
#     button_definitions = {
#         "Headstock": "The headstock is the top part of the guitar's neck where the tuning pegs are located. It's where you adjust the strings to tune the guitar.",
#         "Nut": "The nut is a small piece at the top of the neck that holds the strings in place and sets their height above the fretboard.",
#         "Fretboard": "The fretboard is the flat part of the neck where you press the strings to change the pitch. It has metal strips called frets that divide the neck into sections.",
#         "Sound Hole": "The sound hole is the round hole in the body of an acoustic guitar that allows the sound to escape and makes the guitar louder.",
#         "Strap Button": "The strap button is a small metal knob on the guitar where you attach a guitar strap so you can play standing up.",
#         "String": "The strings are the thin wires stretched across the guitar. When you pluck or strum them, they vibrate to produce sound.",
#         "Tuning Machine": "The tuning machines (or tuners) are the pegs on the headstock that you turn to tighten or loosen the strings, which changes their pitch to tune the guitar.",
#         "Saddle": "The saddle is a small piece on the bridge where the strings rest. It helps set the string height and influences the sound quality.",
#         "Bridge": "The bridge is the part of the guitar where the strings are anchored on the body. It helps transfer the string vibrations to the body, which creates sound.",
#         "Pickguard": "The pickguard is a protective piece of plastic on the guitar’s body, usually beneath the strings or sound hole, that prevents scratches from strumming or picking.",
#         "Neck": "The neck is the long part of the guitar that connects the headstock to the body. It holds the fretboard and allows you to press the strings to play different notes.",
#         "Body": "The body is the large part of the guitar that houses the bridge, sound hole (on acoustic), and pickups (on electric). It amplifies the sound of the strings."
#     }

#     # Left Side Buttons
#     left_labels = ["Headstock", "Nut", "Fretboard", "Sound Hole", "Strap Button", "String"]
#     for i, label in enumerate(left_labels):
#         button = tk.Button(left_button_frame, text=label, font=("Helvetica", 12), width=15)
#         button.grid(row=i, column=0, pady=5, sticky="w")
#         button.bind("<Enter>", lambda e, l=label: show_tooltip(e, button_definitions[l]))  # Show tooltip on hover
#         button.bind("<Leave>", hide_tooltip)  # Hide tooltip when mouse leaves

#     # Right Side Buttons
#     right_labels = ["Tuning Machine", "Saddle", "Bridge", "Pickguard", "Neck", "Body"]
#     for i, label in enumerate(right_labels):
#         button = tk.Button(right_button_frame, text=label, font=("Helvetica", 12), width=15)
#         button.grid(row=i, column=0, pady=5, sticky="w")
#         button.bind("<Enter>", lambda e, l=label: show_tooltip(e, button_definitions[l]))  # Show tooltip on hover
#         button.bind("<Leave>", hide_tooltip)  # Hide tooltip when mouse leaves

#     # For now, just a simple back button to return to the tutorial page
#     back_button = tk.Button(anatomy_frame, text="Back to Learning Center", font=("Helvetica", 12), command=lambda: show_tutorial_page(root, go_back_callback))
#     back_button.grid(row=5, column=1, pady=20, sticky="s")  # Place it in column 1 (center)


# # Notes for each string from open position up to fret 12 (Standard tuning: E A D G B E)
# notes = {
#     "E_high": ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"],  # 1st string (highest)
#     "B":      ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],  # 2nd string
#     "G":      ["G#", "A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"],  # 3rd string
#     "D":      ["D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D"],  # 4th string
#     "A":      ["A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A"],  # 5th string
#     "E_low":  ["F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#", "E"]   # 6th string (lowest)
# }


# def show_fretboard_page(root, go_back_callback):
#     # For now, just a placeholder for the Fretboard page
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.geometry("800x600")

#     # Configure root grid
#     root.grid_rowconfigure(0, weight=1)
#     root.grid_columnconfigure(0, weight=1)

#     fretboard_frame = tk.Frame(root, bg="#d3d3d3")
#     fretboard_frame.grid(row=0, column=0, sticky="nsew")

#     # Configure grid to center elements
#     fretboard_frame.grid_columnconfigure(0, weight=1)
#     fretboard_frame.grid_rowconfigure(1, weight=0)  # Push content up
#     fretboard_frame.grid_rowconfigure(2, weight=1)  # Prevent pushing content down
#     fretboard_frame.grid_rowconfigure(3, weight=0)  # Adjust bottom empty space
#     fretboard_frame.grid_rowconfigure(4, weight=1) # Back button row

#     fretboard_title = tk.Label(fretboard_frame, text="Fretboard", font=("Helvetica", 24, "bold"), bg="#d3d3d3")
#     fretboard_title.grid(row=0, column=0, pady=20)

#     # Instructional text
#     instructions = tk.Label(
#         fretboard_frame,
#         text="Hover over any fret or string to see the note at that position!\n"
#              "You'll see the string name, fret number, and the corresponding musical note displayed instantly.",
#         font=("Helvetica", 14),
#         bg="#d3d3d3",
#         fg="#333333",
#         wraplength=600,
#         justify="center"
#     )
#     instructions.grid(row=1, column=0, pady=(10, 10))  # Adjust padding to fit neatly

#     # Load and display the fretboard image
#     base_path = os.path.dirname(os.path.abspath(__file__))
#     image_path = os.path.join(base_path, "chords_images", "fretboard.png")  # Path to the fretboard image

#     try:
#         image = Image.open(image_path)
#         img_width, img_height = image.size  # Get actual image size
#         fretboard_img = ImageTk.PhotoImage(image)

#         # Create Canvas with the exact size of the image
#         canvas = tk.Canvas(fretboard_frame, width=img_width, height=img_height, bg="#d3d3d3", highlightthickness=0)
#         canvas.grid(row=2, column=0, padx=20, pady=10)

#         # Display the image inside the canvas
#         canvas.create_image(0, 0, anchor="nw", image=fretboard_img)
#         canvas.image = fretboard_img  # Keep reference to prevent garbage collection

#         # Label to show the note when hovering
#         note_label = tk.Label(fretboard_frame, text="", font=("Helvetica", 16, "bold"), bg="#d3d3d3", fg="black")
#         note_label.grid(row=3, column=0, pady=10)

#         # Approximate positions of frets and strings based on image size
#         fret_positions = [int(img_width * (i / 12)) for i in range(1, 13)]
#         string_positions = [int(img_height * (i / 6)) for i in range(6)]

#         # Function to show the note on hover
#         def on_hover(event, string_idx, fret_idx):
#             string_names = ["E_high", "B", "G", "D", "A", "E_low"]
#             note = notes[string_names[string_idx]][fret_idx]
#             note_label.config(text=f"String: {string_names[string_idx]}, Fret: {fret_idx + 1}, Note: {note}")

#         # Adjust the clickable areas for each fret and string
#         rect_width = 30  # Width of the clickable area
#         rect_height = 30  # Height of the clickable area

#         # Add invisible clickable/hoverable areas for each fret and string
#         for i, fret_x in enumerate(fret_positions):
#             for j, string_y in enumerate(string_positions):
#                 canvas.create_rectangle(
#                     fret_x - rect_width // 2,  # Adjust starting x position for even width
#                     string_y - rect_height // 2,  # Adjust starting y position for consistent height
#                     fret_x + rect_width // 2,  # Adjust ending x position
#                     string_y + rect_height // 2,  # Adjust ending y position
#                     outline="", fill="", tags=f"fret_{i}_{j}"
#                 )
#                 canvas.tag_bind(f"fret_{i}_{j}", "<Motion>", lambda event, si=j, fi=i: on_hover(event, si, fi))


#     except Exception as e:
#         print("Error loading fretboard image:", e)
#         error_label = tk.Label(fretboard_frame, text="Image not found!", font=("Helvetica", 14, "bold"), fg="red", bg="#d3d3d3")
#         error_label.grid(row=2, column=0, columnspan=3, pady=10)

#     back_button = tk.Button(fretboard_frame, text="Back to Guitar Anatomy", font=("Helvetica", 12), command=lambda: show_guitar_anatomy(root, go_back_callback))
#     back_button.grid(row=4, column=0, pady=(15, 5))

# def show_strumming_patterns(root, go_back_callback):
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.geometry("800x600")

#     # Configure root grid
#     root.grid_rowconfigure(0, weight=1)
#     root.grid_columnconfigure(0, weight=1)

#     strumming_frame = tk.Frame(root, bg="#d3d3d3")
#     strumming_frame.grid(row=0, column=0, sticky="nsew")

#     # Configure grid to center elements
#     strumming_frame.grid_columnconfigure(0, weight=1)
#     strumming_frame.grid_rowconfigure(0, weight=1)  # Push content up
#     strumming_frame.grid_rowconfigure(3, weight=0)  # Prevent pushing content down
#     strumming_frame.grid_rowconfigure(4, weight=1)  # Adjust bottom empty space

#     strumming_title = tk.Label(strumming_frame, text="Strumming Patterns", font=("Helvetica", 24, "bold"), bg="#d3d3d3")
#     strumming_title.grid(row=1, column=0, pady=(10, 5))

#     strumming_text = tk.Label(strumming_frame, text="Strumming patterns explanation will go here.", font=("Helvetica", 16), bg="#d3d3d3")
#     strumming_text.grid(row=2, column=0, pady=(5, 10))

#     back_button = tk.Button(strumming_frame, text="Back to Learning Center", font=("Helvetica", 12), command=lambda: show_tutorial_page(root, go_back_callback))
#     back_button.grid(row=3, column=0, pady=(15, 5))

# def show_how_to_use_app(root, go_back_callback):
#     # Clear the window and set up the page
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.geometry("800x600")

#     # Configure root grid
#     root.grid_rowconfigure(0, weight=1)
#     root.grid_columnconfigure(0, weight=1)

#     app_usage_frame = tk.Frame(root, bg="#d3d3d3")
#     app_usage_frame.grid(row=0, column=0, sticky="nsew")

#     # Configure grid to center elements
#     app_usage_frame.grid_columnconfigure(0, weight=1)
#     app_usage_frame.grid_rowconfigure(0, weight=1)  # Push content up
#     app_usage_frame.grid_rowconfigure(3, weight=0)  # Prevent pushing content down
#     app_usage_frame.grid_rowconfigure(4, weight=1)  # Adjust bottom empty space

#     app_usage_title = tk.Label(app_usage_frame, text="How to Use the App", font=("Helvetica", 24, "bold"), bg="#d3d3d3")
#     app_usage_title.grid(row=1, column=0, pady=(10, 5))

#     app_usage_text = tk.Label(app_usage_frame, text="App usage tutorial goes here.", font=("Helvetica", 16), bg="#d3d3d3")
#     app_usage_text.grid(row=2, column=0, pady=(5, 10))

#     back_button = tk.Button(app_usage_frame, text="Back to Learning Center", font=("Helvetica", 12), command=lambda: show_tutorial_page(root, go_back_callback))
#     back_button.grid(row=3, column=0, pady=(15, 5))
