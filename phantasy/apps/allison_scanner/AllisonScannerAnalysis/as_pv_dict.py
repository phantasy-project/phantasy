artemis_x = dict(

bias_on = 'ISEG:5230096:0:1:0:Control:setOn',
bias_status = 'ISEG:5230096:0:1:0:isOn',
bias_set_voltage = 'ISEG:5230096:0:1:0:VoltageSet',
bias_measure_voltage = 'ISEG:5230096:0:1:0:VoltageMeasure',

enable_on = 'FE_SCS1:EMS_D0739:ENNEG_CMD_DRV1',
enable_status = 'FE_SCS1:EMS_D0739:ENNEG_RCMD_DRV1',

pos_start = 'FE_SCS1:EMS_D0739:DRV1_scan2.P1SP',
pos_end = 'FE_SCS1:EMS_D0739:DRV1_scan2.P1EP',
pos_step = 'FE_SCS1:EMS_D0739:DRV1_scan2.P1SI',
pos_count = 'FE_SCS1:EMS_D0739:DRV1_scan2.NPTS',

settling_time = 'FE_SCS1:EMS1_D0739:scan1.PDLY',

vol_start = 'FE_SCS1:EMS_D0739:DRV1_scan1.P1SP',
vol_end = 'FE_SCS1:EMS_D0739:DRV1_scan1.P1EP',
vol_step = 'FE_SCS1:EMS_D0739:DRV1_scan1.P1SI',
vol_count = 'FE_SCS1:EMS_D0739:DRV1_scan1.NPTS',

scan_start = 'FE_SCS1:EMS_D0739:DRV1_scan2.EXSC',
scan_status = 'FE_SCS1:EMS1_D0739:scan2.FAZE',

pos_default = 'FE_SCS1:STPC01_D0739:POSH.VAL',
pos_readback = 'FE_SCS1:EMS_D0739:DRV2.RBV',
scanner_out = 'FE_SCS1:EMS_D0739:LMPOS_RSTS_DRV2',
scanner_in = 'FE_SCS1:EMS_D0739:LMNEG_RSTS_DRV2',

data = 'FE_SCS1:EMS1_D0739:Det1Data',

interlock_reset = 'FE_SCS1:DIAG_D0739:RST_CMD',
interlock_status = 'FE_SCS1:EMS_D0739:LMPOS_LTCH_DRV1')

artemis_y = dict(

bias_on = 'ISEG:5230096:0:1:0:Control:setOn',
bias_status = 'ISEG:5230096:0:1:0:isOn',
bias_set_voltage = 'ISEG:5230096:0:1:0:VoltageSet',
bias_measure_voltage = 'ISEG:5230096:0:1:0:VoltageMeasure',

enable_on = 'FE_SCS1:EMS_D0739:ENNEG_CMD_DRV2',
enable_status = 'FE_SCS1:EMS_D0739:ENNEG_RCMD_DRV2',

pos_start = 'FE_SCS1:EMS_D0739:DRV2_scan2.P1SP',
pos_end = 'FE_SCS1:EMS_D0739:DRV2_scan2.P1EP',
pos_step = 'FE_SCS1:EMS_D0739:DRV2_scan2.P1SI',
pos_count = 'FE_SCS1:EMS_D0739:DRV2_scan2.NPTS',

settling_time = 'FE_SCS1:EMS2_D0739:scan1.PDLY',

vol_start = 'FE_SCS1:EMS_D0739:DRV2_scan1.P1SP',
vol_end = 'FE_SCS1:EMS_D0739:DRV2_scan1.P1EP',
vol_step = 'FE_SCS1:EMS_D0739:DRV2_scan1.P1SI',
vol_count = 'FE_SCS1:EMS_D0739:DRV2_scan1.NPTS',

scan_start = 'FE_SCS1:EMS_D0739:DRV2_scan2.EXSC',
scan_status = 'FE_SCS1:EMS2_D0739:scan2.FAZE',

pos_default = 'FE_SCS1:STPC01_D0739:POSV.VAL',
pos_readback = 'FE_SCS1:EMS_D0739:DRV1.RBV',
scanner_out = 'FE_SCS1:EMS_D0739:LMPOS_RSTS_DRV2',
scanner_in = 'FE_SCS1:EMS_D0739:LMNEG_RSTS_DRV2',

data = 'FE_SCS1:EMS2_D0739:Det1Data',

interlock_reset = 'FE_SCS1:DIAG_D0739:RST_CMD',
interlock_status = 'FE_SCS1:EMS_D0739:LMPOS_LTCH_DRV2')

venus_x = dict()
venus_y = dict()


pv_dict = dict(

artemis_x = artemis_x,
artemis_y = artemis_y,
venus_x = venus_x,
venus_y = venus_y

)
