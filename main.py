import os
import sys
import subprocess
import pandas as pd
from PySide6.QtWidgets import ( QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QLabel, QFileDialog,
)


GITHUB_URL = "https://github.com/rtsrooia-s/Exe4.1"


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Grades Correction App"))
        layout.addWidget(QLabel(f"GitHub: {GITHUB_URL}"))
        self.setLayout(layout)


class GradesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grades Correction")

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

        self.about_window = None

        self._build_ui()
        self._load_stylesheet()

    def _build_ui(self):
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        self.select_file_btn = QPushButton("Select File")
        self.select_file_btn.clicked.connect(self.on_select_file)

        self.about_btn = QPushButton("About")
        self.about_btn.clicked.connect(self.on_open_about)

        top_layout.addWidget(self.select_file_btn)
        top_layout.addWidget(self.about_btn)
        main_layout.addLayout(top_layout)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        main_layout.addWidget(self.table)

        bonus_layout = QHBoxLayout()
        bonus_layout.addWidget(QLabel("Bonus Points:"))
        self.bonus_spinbox = QSpinBox()
        self.bonus_spinbox.setRange(-100, 100)
        self.bonus_spinbox.editingFinished.connect(self.on_bonus_enter)
        bonus_layout.addWidget(self.bonus_spinbox)

        self.update_file_btn = QPushButton("Update File")
        self.update_file_btn.clicked.connect(self.on_update_file)
        bonus_layout.addWidget(self.update_file_btn)

        main_layout.addLayout(bonus_layout)
        self.setLayout(main_layout)

    def _load_stylesheet(self):
        qss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def update_table_from_lists(self):
        self.table.clearContents()
        row_count = max(50, len(self.student_ids))
        self.table.setRowCount(row_count)

        for i in range(len(self.student_ids)):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.student_ids[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))

    def on_select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Grades File", "", "CSV Files (*.csv)")
        if not file_path:
            return
        
        self.selected_file = file_path
        df = pd.read_csv(self.selected_file)

        self.student_ids = df["ID"].tolist()
        self.original_grades = df["Grade"].tolist()
        self.corrected_grades = (self.original_grades)

        self.update_table_from_lists()

    def on_bonus_enter(self):
        bonus = self.bonus_spinbox.value()
        self.corrected_grades = [min(100, g + bonus) for g in self.original_grades]
        self.update_table_from_lists()

    def on_update_file(self):
       if not self.selected_file:
            return

       df = pd.read_csv(self.selected_file)
       df["Grade"] = self.corrected_grades
       df.to_csv(self.selected_file, index=False)
        
       if self.selected_file:
            if sys.platform.startswith("win"):
                os.startfile(self.selected_file)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.selected_file], check=False)
            else:
                subprocess.run(["xdg-open", self.selected_file], check=False)

    def on_open_about(self):
        if self.about_window is None:
            self.about_window = AboutWindow()
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradesWindow()
    window.show()
    sys.exit(app.exec())