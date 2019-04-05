#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

import psutil

from .ui.ui_vainfo import Ui_Form


class VAProcessInfoWidget(QWidget, Ui_Form):
    def __init__(self, pid, parent=None):
        super(self.__class__, self).__init__()

        # UI:
        self.setupUi(self)

        self.setWindowTitle("Virtual Accelerator Info")

        # process
        try:
            self.process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            QMessageBox.warning(self, "", "No such process",
                    QMessageBox.Ok)
            return

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.on_update_info)

    def sizeHint(self):
        return QSize(600, 200)

    def show_widget(self):
        self.refresh_timer.start(1000)
        self.adjustSize()
        self.show()

    def on_update_info(self):
        """Update va process info.
        """
        try:
            self.pid_label.setText('{}'.format(self.process.pid))
            self.cpu_label.setText('{:.1f}%'.format(self.process.cpu_percent()))
            self.mem_label.setText('{0:.1f} KiB, {1:.2f}%'.format(
                self.process.memory_info()[0]/2.0**10,
                self.process.memory_percent()))
            self.cmdline_label.setText(' '.join(self.process.cmdline()))
        except psutil.NoSuchProcess:
            self.close()

    def closeEvent(self, e):
        try:
            self.refresh_timer.stop()
        except:
            pass
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
