#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def pm_processor(elem):
    import time, random
    time.sleep(random.random() * 2 + 1)
    r = {'xcen': random.random(),
         'ycen': random.random(),
         'xrms': random.random(),
         'yrms': random.random(),
         'cxy': random.random(),}
    results_for_ioc = {
        'xcen': r['xcen'], 'ycen': r['ycen'],
        'xrms': r['xrms'], 'yrms': r['yrms'],
        'cxy': r['cxy']}
    for k, v in results_for_ioc.items():
        setattr(elem, k.upper(), v)
    return

    import sys
    sys.path.append('/files/shared/ap/phyapp_notebooks/ProfileMonitorAnalysis/')
    from phantasy.recipes import save_all_settings
    from datetime import datetime
    import json
    import profilemonitor_plot_util
    import profilemonitor_scan_util

    pm_plot = profilemonitor_plot_util.profilemonitor_plot(batch=True)
    pm_scan = profilemonitor_scan_util.profilemonitor_scan()
    starttime = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn_json = 'pm_' + starttime + '.json'

    datad = save_all_settings(segments=["LEBT", "MEBT"], machine="FRIB")

    #
    pms = [elem.name]
    npm = len(pms)
    for i in range(npm):
        res = pm_scan.execute(pms[i])
        try:
            datad[pms[i]] = pm_plot.execute(res)
        except:
            print('error happend')

    ## pack all PM data and optical element settings in one json file
    with open(fn_json, 'w') as outfile:
        json.dump(
            datad,
            outfile,
            ensure_ascii=False,
            indent=4,
            sort_keys=True,
            separators=(',', ': '))

    # sync results to IOC
    # results_for_ioc = {
    #     'xcen': r['xcen'], 'ycen': r['ycen'],
    #     'xrms': r['xrms'], 'yrms': r['yrms'],
    #     'cxy': r['cxy']}
    # for k, v in results_for_ioc.items():
    #     setattr(elem, k.upper(), v)


def vd_processor(elem):
    import time
    time.sleep(0.5)

