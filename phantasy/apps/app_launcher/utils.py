# -*- coding: utf-8 -*-

import os

from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser

DEFAULT_ICON_PATH = "/usr/share/phantasy/assets/icons/default.png"


def find_dconf():
    """Find parameter configuration file for wire-scanners.
    searching the following locations:
    * ~/.phantasy/app_launcher.ini
    * /etc/phantasy/app_launcher.ini
    * package location: apps/app_launcher/config/app_launcher.ini
    """
    home_conf = os.path.expanduser('~/.phantasy/app_launcher.ini')
    sys_conf = '/etc/phantasy/app_launcher.ini'
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(basedir, 'config/app_launcher.ini')


class AppDataModel(QStandardItemModel):
    """App data model.

    """

    def __init__(self, parent, app_items, **kws):
        # app_items: list of AppItem instances.
        super(self.__class__, self).__init__(parent)
        self._v = parent
        self._app_items = app_items

        # header
        self.header = self.h_name, self.h_desc = ('Name', 'Description')
        self.ids = self.i_name, self.i_desc = range(len(self.header))

    def set_header(self):
        for i, s in zip(self.ids, self.header):
            self.setHeaderData(i, Qt.Horizontal, s)

    def set_data(self):
        for app in self._app_items:
            item00 = QStandardItem(app.name)
            item00.cmd = app.cmd
            item00.setIcon(QIcon(QPixmap(app.icon_path)))
            item01 = QStandardItem(app.desc)
            row = (item00, item01)
            [i.setEditable(False) for i in row]
            self.appendRow(row)

    def set_model(self):
        self.set_data()
        self.set_header()
        self._v.setModel(self)
        self.__post_init_ui(self._v)

    def __post_init_ui(self, v):
        # view properties
        #v.setStyleSheet("font-family: monospace;")
        v.setIconSize(QSize(24, 24))
        v.setAlternatingRowColors(True)
        try:
            # tree
            v.header().setStretchLastSection(True)
        except:
            # table
            v.horizontalHeader().setStretchLastSection(True)
        v.setSortingEnabled(True)
        self.sort(self.i_name, Qt.AscendingOrder)
        for i in self.ids:
            v.resizeColumnToContents(i)
        for i in range(self.rowCount()):
            v.resizeRowToContents(i)
        v.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #v.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class AppItem(object):
    def __init__(self, name, desc, cmd, icon_path):
        super(self.__class__, self).__init__()
        self.name = name
        self.desc = desc
        self.cmd = cmd
        self.icon_path = icon_path

# app conf
path_conf = find_dconf()
conf = ConfigParser()
conf.read(path_conf)

data = []
for k,v in conf.items():
    if k == 'DEFAULT':
        continue
    icon_path = v.get('icon', DEFAULT_ICON_PATH)
    if not os.path.isfile(icon_path):
        icon_path = DEFAULT_ICON_PATH
    app_item = AppItem(k, v.get('desc'), v.get('exec'), icon_path)
    data.append(app_item)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QWidget, QTableView, QTreeView, QTextEdit, QVBoxLayout
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QSize
    import sys
    from subprocess import Popen

    class MyApp(QWidget):
        def __init__(self):
            super(self.__class__, self).__init__()

            v = QTableView(self)
            self.v = v
            model = AppDataModel(v, data)
            model.set_model()

            text_edit = QTextEdit(self)

            vbox = QVBoxLayout()
            vbox.addWidget(v, 1)
            vbox.addWidget(text_edit, 0)
            self.setLayout(vbox)

            # events
            self.v.doubleClicked.connect(self.on_launch_app)

        def on_launch_app(self, index):
            item = self.v.model().item(index.row(), 0)
            Popen(item.cmd, shell=True)

        def sizeHint(self):
            return QSize(800, 600)

    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    w.adjustSize()

    sys.exit(app.exec_())