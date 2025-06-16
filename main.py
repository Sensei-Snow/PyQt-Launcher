#-----------------------------------------------------------------Importations
import sys
import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QPushButton
from PyQt6 import uic
from PyQt6.QtCore import Qt
import subprocess
import json
import platform

#-----------------------------------------------------------------Qt Launcher Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #-----------------------------------------------------------------Set Style
        uic.loadUi("qt-launcher.ui", self)

        QApplication.setStyle("Windows")  # Fusion or WindowsVista

        self.setWindowTitle("Qt Launcher")

        icon_path = "assets/logo_qt.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"[ERROR] -- File : {icon_path} not found.")

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        #-----------------------------------------------------------------Events
        self.windowsvista_button.clicked.connect(lambda: self.open_pyqt6_designer("windowsvista"))
        self.windows_button.clicked.connect(lambda: self.open_pyqt6_designer("windows"))
        self.fusion_button.clicked.connect(lambda: self.open_pyqt6_designer("fusion"))
        self.macintosh_button.clicked.connect(lambda: self.open_pyqt6_designer("macintosh"))
        self.gtk_button.clicked.connect(lambda: self.open_pyqt6_designer("gtk"))

    #-----------------------------------------------------------------Open PyQt Designer Method
    def open_pyqt6_designer(self, style):

        with open("config.json", "r") as f:
            config = json.load(f)

        designer_path = config["qt-designer_path"]

        if os.path.exists(designer_path):
            system = platform.system().lower()

            if system == "windows":
                valid_styles = ["windowsvista", "windows", "fusion"]
            elif system == "linux":
                valid_styles = ["fusion", "gtk", "windows"]
            elif system == "darwin":
                valid_styles = ["macintosh", "fusion"]
            else:
                valid_styles = ["fusion"]

            style = style.lower()

            if style not in valid_styles:
                print(f"[ERROR] -- Style : {style} not supported.")
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("[ERROR]")
                msg.setText("An error has occurred")
                msg.setInformativeText(f"Style : {style} not supported.")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                return

            try:
                subprocess.Popen([designer_path, "-style", style])
            except Exception as e:
                print(f"[ERROR] -- An error has occurred during the setup of PyQt6 Designer : {e}.")
        else:
            print(f"[ERROR] -- File : {designer_path} not found.")

        self.close()

#-----------------------------------------------------------------Main code -> Show The Window
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())