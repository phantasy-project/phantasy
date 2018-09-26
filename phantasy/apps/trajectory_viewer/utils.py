# -*- coding: utf-8 -*-

import os

from mpl4qt.widgets.utils import MatplotlibCurveWidgetSettings


def find_conf():
    """Find configuration file (JSON) for matplotlibcurvewidget,
    searching the following locations:
    * ~/.phantasy/apps/mpl_settings_tv.json
    * /etc/phanasy/apps/mpl_settings_tv.json
    * package root location for this app/config/mpl_settings_tv.json
    """
    home_conf = os.path.expanduser('~/.phantasy/apps/mpl_settings_tv.json')
    sys_conf = '/etc/phantasy/apps/mpl_settings_tv.json'
    if os.path.isfile(home_conf):
        return home_conf
    elif os.path.isfile(sys_conf):
        return sys_conf
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(basedir, 'config/mpl_settings_tv.json')


def apply_mplcurve_settings(mplcurveWidget, json_path=None):
    """Apply JSON settings read from *json_path* to *mplcurveWidget*.
    
    Parameters
    ----------
    mplcurveWidget : MatplotlibCurveWidget
        Instance of MatplotlibCurveWidget.
    json_path : str
        Path of JSON settings file.
    """
    if json_path is None:
        json_path = find_conf()
    s = MatplotlibCurveWidgetSettings(json_path)
    mplcurveWidget.apply_mpl_settings(s)
        

