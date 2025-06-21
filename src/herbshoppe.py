from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QLabel, QMenuBar, QMenu
)
from PySide6.QtGui import QAction

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kräuter-Tool")
        self.resize(800, 600)

        # Menüleiste
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Datei")

        load_action = QAction("Charaktergruppe laden", self)
        export_action = QAction("Kräuterliste exportieren", self)

        file_menu.addAction(load_action)
        file_menu.addAction(export_action)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_tab("Charakterinventar (Kräuter)"), "Inventar")
        tabs.addTab(self.create_tab("Allgemeine Kräuteranzeige"), "Kräuterliste")
        tabs.addTab(self.create_tab("Kräutersuche"), "Suche")
        tabs.addTab(self.create_tab("Kräuterladen"), "Laden")

        self.setCentralWidget(tabs)

    def create_tab(self, title):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(title))
        tab.setLayout(layout)
        return tab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
