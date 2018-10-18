from PyQt5.QtWidgets import QDialog, QComboBox, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class PopComboBoxDialog(QDialog):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        self.init_ui()
        self.setWindowFlags(Qt.FramelessWindowHint)

    def init_ui(self):
        cbb = self.cbb = QComboBox(self)
        cbb.addItems(('Peak', 'Valley'))

        btn = QPushButton("OK", self)
        btn.clicked.connect(self.on_ok)

        box = QHBoxLayout()
        box.addWidget(cbb)
        box.addWidget(btn)

        self.setLayout(box)

    def on_ok(self):
        self.close()
        self.setResult(self.cbb.currentIndex())


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    dlg = MyDialog()
    r = dlg.exec_()
    print(r)

    app.exec_()
