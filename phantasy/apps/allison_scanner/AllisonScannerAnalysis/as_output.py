import numpy as np
import json

def save_output(perform_scan, results, name):

    if perform_scan:
        import phantasy
        mp = phantasy.MachinePortal(machine ='FRIB', segment = 'LEBT')
        lat = mp.work_lattice_conf
        lat.sync_settings (data_source ='control' )

    # save the data in JSON format
    with open(name + '_Data.json','w') as outfile:
        json.dump(results,outfile,indent = 4)
        if perform_scan:
            json.dump(lat.settings , outfile)
