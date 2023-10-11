import sys
import socket
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal

HOST = socket.gethostname()
PORT = 40808
k = 1

class SocketThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.sendall(b'I connected.')
            while True:
                data = client.recv(1024)
                self.data_received.emit(data.decode())

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        global k
        self.setWindowTitle("Change picture when you press a button")
        self.setGeometry(100, 100, 400, 300)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(800, 600)
        self.pix = "1234.jpg"
        self.pixmap1 = QPixmap(self.pix)
        self.image_label.setPixmap(self.pixmap1)
        layout.addWidget(self.image_label)
        central_widget.setLayout(layout)
        self.socket_thread = SocketThread()
        self.socket_thread.data_received.connect(self.update_data)
        self.socket_thread.start()


    def update_data(self, data):
        global k
        a = ["123.jpg", "1234.jpg", "1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg",
             "6.jpg", "7.jpg"]
        # print(f"Received: {data}")
        self.pix = a[k-1]
        k += 1
        if k == len(a):
            k = 0
        self.pixmap1 = QPixmap(self.pix)
        self.image_label.setPixmap(self.pixmap1)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())

