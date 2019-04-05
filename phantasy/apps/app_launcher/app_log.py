#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QFileSystemWatcher


class LogWidget(QWidget):
    def __init__(self, logfile):
        super(self.__class__, self).__init__()

        self.setWindowTitle("FRIB High-level Physics Applications - Logs")

        textEdit = QTextEdit(self)
        textEdit.setStyleSheet(
                "QTextEdit {\n"
                "  font-family: monospace;\n"
                "}")
        textEdit.setReadOnly(True)
        self.textEdit = textEdit

        vbox = QVBoxLayout()
        vbox.addWidget(textEdit)
        self.setLayout(vbox)

        fm = QFileSystemWatcher(self)
        fm.addPath(logfile)
        fm.fileChanged.connect(self.on_log_updated)

    def sizeHint(self):
        return QSize(1200, 600)

    def on_log_updated(self, p):
        with open(p, 'r') as f:
            self.textEdit.setText(f.read())
