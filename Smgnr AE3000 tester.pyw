import sys
import subprocess

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QCheckBox, QDoubleSpinBox, QSpinBox,
    QPushButton, QTextEdit
)
from PyQt5.QtCore import Qt

class TestPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAMOGONER AE3000 Test Panel")
        self.init_ui()

    def init_ui(self):

        vbox = QVBoxLayout(self)

        form = QFormLayout()
        vbox.addLayout(form)

        self.ip_edit = QLineEdit("192.168.1.44")
        form.addRow("IP адрес:", self.ip_edit)

        self.mode_check = QCheckBox("Тестовый режим ON")
        form.addRow("Режим:", self.mode_check)

        self.t1_spin = QDoubleSpinBox()
        self.t1_spin.setRange(-50.0, 150.0)
        self.t1_spin.setSingleStep(0.1)
        self.t1_spin.setValue(0.0)
        form.addRow("T₁ (куб):", self.t1_spin)

        self.t2_spin = QDoubleSpinBox()
        self.t2_spin.setRange(-50.0, 150.0)
        self.t2_spin.setSingleStep(0.1)
        self.t2_spin.setValue(0.0)
        form.addRow("T₂ (охлажд.):", self.t2_spin)

        self.liq_spin = QSpinBox()
        self.liq_spin.setRange(0, 1023)
        self.liq_spin.setValue(0)
        form.addRow("Перелив (liq):", self.liq_spin)

        self.thermo_check = QCheckBox("Thermostat = 1")
        form.addRow("Термостат:", self.thermo_check)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.on_send)
        vbox.addWidget(self.send_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        vbox.addWidget(self.output)

    def on_send(self):
        ip = self.ip_edit.text().strip()
        mode = "on" if self.mode_check.isChecked() else "off"
        url = f"http://{ip}/test?mode={mode}"

        if mode == "on":
            t1 = self.t1_spin.value()
            t2 = self.t2_spin.value()
            liq = self.liq_spin.value()
            thermo = "1" if self.thermo_check.isChecked() else "0"
            url += f"&t1={t1:.1f}&t2={t2:.1f}&liq={liq}&thermo={thermo}"

        cmd = ["curl", "-s", url]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.output.append(f"> {' '.join(cmd)}")
            self.output.append(result.stdout.strip() or "[no output]")
        except subprocess.CalledProcessError as e:
            self.output.append(f"Ошибка при выполнении curl:\n{e.stderr}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestPanel()
    w.resize(400, 300)
    w.show()
    sys.exit(app.exec_())
