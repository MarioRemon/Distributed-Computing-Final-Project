import sys
import threading
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

#define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255,255,255)
grey = (211,211,211)

class PygameWindow(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.running = True
        self.car_image = None
        self.car_pixmap = None
        self.tree_group = pygame.sprite.Group()
        self.Pr_group = pygame.sprite.Group()

    def run(self):
        pygame.init()
        pygame.display.set_caption("Pygame with PyQt5")
        pygame_screen = pygame.Surface((300, 300))
        clock = pygame.time.Clock()

        self.car_image = pygame.image.load('Img/car.png')
        self.car_pixmap = self.convert_pygame_image(self.car_image)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame_screen.fill((255, 255, 255))
            pygame_screen.blit(self.car_image, (0, 0))

            self.car_pixmap = self.convert_pygame_image(pygame_screen)
            self.parent.update_pygame_label()

            clock.tick(60)

        pygame.quit()

    def convert_pygame_image(self, pygame_image):
        image_data = pygame.image.tostring(pygame_image, "RGBA")
        image_qt = QImage(image_data, pygame_image.get_width(), pygame_image.get_height(), QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(image_qt)
        return pixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat Room")
        self.setGeometry(100, 100, 1100, 700)

        chat_widget = QWidget(self)
        chat_widget.setGeometry(10, 10, 780, 680)

        self.chat_history = QTextBrowser(chat_widget)
        self.chat_history.setGeometry(10, 10, 760, 660)
        self.chat_history.setFont(QFont("Arial", 12))

        self.chat_input = QLineEdit(self)
        self.chat_input.setGeometry(800, 10, 290, 660)
        self.chat_input.setFont(QFont("Arial", 12))
        self.chat_input.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send", self)
        self.send_button.setGeometry(800, 680, 290, 20)
        self.send_button.setFont(QFont("Arial", 12))
        self.send_button.clicked.connect(self.send_message)

        self.pygame_label = QLabel(chat_widget)
        self.pygame_label.setGeometry(800, 10, 290, 660)
        self.pygame_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(chat_widget)

        input_widget = QWidget(self)
        input_widget.setGeometry(800, 10, 290, 700)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(self.send_button)

        input_widget.setLayout(input_layout)
        layout.addWidget(input_widget)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def send_message(self):
        message = self.chat_input.text()
        if message:
            formatted_message = f"{message}"
            self.chat_history.append(formatted_message)
            self.chat_input.clear()

    def update_pygame_label(self):
        self.pygame_label.setPixmap(self.pygame_thread.car_pixmap)

    def run_pygame_window(self):
        self.pygame_thread = PygameWindow(self)
        self.pygame_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    window.run_pygame_window()

    sys.exit(app.exec_())
