# -*- coding: utf-8 -*-

from collections import OrderedDict
import getpass


# data sheet templates
# quad scan
def qs_data_sheet_template():
    s = OrderedDict()

    # task
    task_dict = OrderedDict()
    task_dict['user'] = getpass.getuser() #'<str, who does this task>'
    task_dict['start'] = '<timestamp, when does this task start>'
    task_dict['stop'] = '<timestamp, when does this task stop>'
    task_dict['duration'] = '<float, how long does this task last, in sec>'
    task_dict['n_iteration'] = '<int, number of scan iterations>'
    task_dict['n_shot'] = '<int, number of DAQ events within each iteration>'
    task_dict['n_dim'] = '<int, dimension of all monitors>'
    task_dict['scan_range'] = '<list, array of scan values>'
    task_dict['t_wait'] = '<float, wait time before the start of new iteration, in sec>'
    task_dict['daq_rate'] = '<float, DAQ rate during each iteration>'

    s.update({'task': task_dict})

    # devices
    dev_dict = OrderedDict()
    dev_dict['alter_element'] = {
            'name': '<str, element name>',
            'readback_pv': '<str, readback pv name>',
            'setpoint_pv': '<str, setpoint pv name>',
    }
    dev_dict['monitors'] = [
            {'name':'<str, element name>', 'readback_pv': '<str, readback pv name>'}
    ] # add other monitors

    s.update({'devices': dev_dict})

    # data
    data_dict = OrderedDict()
    data_dict['created'] = '<timestamp, when is the data file created>'
    data_dict['filepath'] = '<str, path of the data file>'
    data_dict['shape'] = '<tuple, shape of the data array>'
    data_dict['array'] = '<numpy array, scan output data>'

    s.update({'data': data_dict})

    return s


SHEET_TEMPLATES = {'Quad Scan': qs_data_sheet_template()}
