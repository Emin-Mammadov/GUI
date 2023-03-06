import sys
import json
import pyqtgraph as pg
import imageio.v2 as io
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QWidget, QMainWindow, QFileDialog,
    QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox,
    QShortcut, QMenuBar, QAction, QMenu
)
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence
import os


class ImageLabel(QLabel):
    """Custom QLabel widget to display images"""

    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.path = ''
        self.setWindowTitle("Emin Mammadov")
        self.resize(1200, 800)
        self.setAcceptDrops(True)

        self.label = QLabel("")
        self.photoViewer = ImageLabel()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.label)

        button1 = QPushButton("Load a file")
        button1.clicked.connect(self.get_image)
        mainLayout.addWidget(button1)

        button2 = QPushButton("Save the file")
        button2.clicked.connect(self.save)
        mainLayout.addWidget(button2)

        mainLayout.addWidget(self.photoViewer)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self.save)

    def get_image(self):
        """Open a file dialog and load an image"""

        filename, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Image files (*.jpg *.png)")
        if not filename:
            return

        self.path = filename
        self.label.setText(filename)

        pixmap = QPixmap(filename)
        self.photoViewer.setPixmap(pixmap)

    def save(self):
        """Save the displayed image to file"""

        if not self.path:
            return

        try:
            image = io.imread(self.path)
            save_path = os.path.join(
                os.path.expanduser("~"), "Desktop", "saved.png")
            io.imsave(save_path, image)

            message = QMessageBox()
            message.setText("Image was successfully saved to Desktop")
            message.exec()
        except:
            message = QMessageBox()
            message.setText("Error! Image cannot be saved!")
            message.exec()

    def dragEnterEvent(self, event):
        """Handle drag enter event"""

        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """Handle drag move event"""

        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle drop event"""
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.path = event.mimeData().urls()[0].toLocalFile()       #Getting the path of the file
            self.set_image(self.path)     

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        """Display the drag and dropped image"""
        self.photoViewer.setPixmap(QPixmap(file_path))

def main():
    """Run the application"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
