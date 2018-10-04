# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog


def get_open_filename(obj, filter=None, caption=None):
    """Get file for reading.

    Parameters
    ----------
    obj :
        Parent widget of QFileDialog.
    filter : str
        File fileters, see `QFileDialog.setNameFilter`,
        e.g. ``JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)``
    caption : str
        Caption of file dialog.

    Returns
    -------
    r : str
        Selected filename.
    """
    filepath, _ = QFileDialog.getOpenFileName(obj, caption, "", filter)
    if not filepath:
        return None
    return filepath


def get_save_filename(obj, filter=None, caption=None):
    """Get file for saving data.

    Parameters
    ----------
    obj :
        Parent widget of QFileDialog.
    filter : str
        File fileters, see `QFileDialog.setNameFilter`,
        e.g. ``JSON Files (*.json);;HDF5 Files (*.hdf5 *.h5)``
    caption : str
        Caption of file dialog.

    Returns
    -------
    r : str
        Selected filename.
    """
    filepath, filter = QFileDialog.getSaveFileName(
            obj, caption, "", filter)
    if not filepath:
        return None
    ext = re.match(r'.*\.(.*)\)', filter).group(1)
    if re.match(r'.*\..*', filepath) is not None:
        filename = re.sub(r'([^.]*)(\.)(.*)', r'\1.{}'.format(ext), filepath)
    else:
        filename = re.sub(r'(.*)', r'\1.{}'.format(ext), filepath)

    return filename

