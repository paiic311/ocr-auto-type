from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox, QRubberBand
from PySide6.QtCore import Qt, QRect, Signal, QSize, QTimer
from PySide6.QtGui import QPainter, QPen, QColor
import sys
import tkinter as tk
import mss
from mss.tools import to_png
import easyocr
import pyautogui
import time

class AreaSelector():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title ("Select Area")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.root.bind("<Button-1>", self.mouse_down)
        self.root.bind("<B1-Motion>", self.mouse_move)
        self.root.bind("<ButtonRelease-1>", self.mouse_up)
        self.root.mainloop()

    def mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def mouse_move(self, event):
        self.end_x = event.x
        self.end_y = event.y

        self.canvas.delete("selection")

        self.canvas.create_rectangle(
            self.start_x,
            self.start_y,
            self.end_x,
            self.end_y,
            outline="red",
            width=2,
            tags="selection"
        )

    def mouse_up(self, event):
        left = min(self.start_x, self.end_x)
        top = min(self.start_y, self.end_y)
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)

        self.result = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }
        self.root.destroy()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowTitle("P A.I")
        self.resize(400, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #252836;
                color: white;
                border: 1px solid #5FFBF1;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D16BA5;
            }
            QPushButton:pressed {
                background-color: #7A5CFF;
            }
        """)
        self.title_label = QLabel("OCR Auto Typer")
        self.select_area_button = QPushButton("Select Area")
        self.select_area_button.clicked.connect(self.select_area_clicked)
        self.title_label.setAlignment(Qt.AlignCenter)

        ### BUTTON START
        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet("""
            QPushButton{
                background-color: #00C853;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00E676;
            }
            QPushButton:pressed {
                background-color: #00B248;
            }
        """)
        self.start_button.setFixedHeight(40)
        self.start_button.clicked.connect(self.start_clicked)

        ### BUTTON STOP
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #FF1744;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF4569;
            }
            QPushButton:pressed {
                background-color: #D5002F;
            }
        """)
        self.stop_button.setFixedHeight(40)
        self.stop_button.clicked.connect(self.stop_clicked)

        self.status_label = QLabel("Status: Berhenti 🔴", self)
        self.status_label.resize(200, 20)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.select_area_button)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

        self.capture_area = None
        self.running = False
        self.last_text = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.monitor_ocr)
        self.reader = easyocr.Reader(['en'])

    def start_clicked(self):
        if self.capture_area is None:
            self.status_label.setText("Status: Pilih area dulu! ⚠️")
            return
        self.running = True
        self.last_text = ""
        self.timer.start(500)
        self.status_label.setText("Status: Membaca teks 🟢")
        self.capture_screen()

        time.sleep(1)
        # pyautogui.write(self.text)

    def monitor_ocr(self):
        if not self.running:
            return
        
        self.capture_screen()

        current_text = self.text.lower().strip()
        if current_text != self.last_text:
            pyautogui.write(self.text)
            self.last_text = current_text

    def stop_clicked(self):
        self.running = False
        self.timer.stop()
        self.status_label.setText("Status: Berhenti 🔴")

    def select_area_clicked(self):
        selector = AreaSelector()

        self.capture_area = selector.result

    
    def capture_screen(self):
        with mss.MSS() as sct:
            img = sct.grab(self.capture_area)
            to_png(img.rgb, img.size, output="capture.png")

        print(" SELESAI CAPTURE ")
        result = self.reader.readtext("capture.png")
        self.text = " ".join(item[1] for item in result)
        print("\n===== HASIL DARI OCR =====")
        print(self.text)
        print("=====================\n")
app = QApplication(sys.argv)

window = MainWindow()


window.show()

sys.exit(app.exec())
