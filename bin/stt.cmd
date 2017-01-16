#!/home/tong1/work/FRIB/projects/CFS/recsync/client/bin/linux-x86_64/demo

#
# st.cmd template for virtual accelerator
#

epicsEnvSet("ARCH","linux-x86_64")
epicsEnvSet("IOC","iocdemo")
epicsEnvSet("TOP","/home/tong1/work/FRIB/projects/CFS/recsync/client")
epicsEnvSet("EPICS_BASE","/home/tong/APS/epics/base")

## Register all support components
dbLoadDatabase("/home/tong1/work/FRIB/projects/CFS/recsync/client/dbd/demo.dbd",0,0)
demo_registerRecordDeviceDriver(pdbbase) 

var(reccastTimeout, 5.0)
var(reccastMaxHoldoff, 5.0)

epicsEnvSet("IOCNAME", "VAIOC")
epicsEnvSet("ENGINEER", "TONG")
epicsEnvSet("LOCATION", "TRAILER8")

## Load record instances
#dbLoadRecords("../../db/reccaster.db", "P=test:")
#dbLoadRecords("../../db/somerecords.db","P=test:")
dbLoadRecords("VADB")

iocInit()
