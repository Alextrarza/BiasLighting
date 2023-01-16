import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget

class ScreenCalibrator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        brightness_label = QLabel("Brightness")
        contrast_label = QLabel("Contrast")
        gamma_label = QLabel("Gamma")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.gamma_slider = QSlider(Qt.Horizontal)
        
        layout = QVBoxLayout()
        layout.addWidget(brightness_label)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(contrast_label)
        layout.addWidget(self.contrast_slider)
        layout.addWidget(gamma_label)
        layout.addWidget(self.gamma_slider)
        self.setLayout(layout)
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Screen Calibrator')
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenCalibrator()
    sys.exit(app.exec_())


