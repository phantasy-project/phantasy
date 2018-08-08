# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QUrl

from .ui_app_pref import Ui_Dialog


class PrefDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(PrefDialog, self).__init__()
        self.parent = parent
        self.setupUi(self)

        # set url and port
        self.lineEdit_url.setText(self.parent._url)
        self.lineEdit_port.setText(self.parent._port)
        # set pagezoom
        self.pageZoom.setCurrentText('{}%'.format(int(self.parent._pageZoom)))

        # events
        self.btn_box.accepted.connect(self.on_accept_btn_box)
        self.btn_box.rejected.connect(self.on_reject_btn_box)

    def on_accept_btn_box(self):
        # url
        url, port = self.lineEdit_url.text(), self.lineEdit_port.text()
        base_url = url.rstrip('/') + ':' + port
        if base_url != self.parent.get_base_url():
            self.parent._url = url
            self.parent._port = port
            self.parent.update_url(QUrl(base_url))

        # pageZoom
        self.parent._pageZoom = float(self.pageZoom.currentText().split('%')[0])
        self.parent.update_pageZoom()
        self.close()

    def on_reject_btn_box(self):
        self.close()
