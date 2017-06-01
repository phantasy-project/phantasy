from flame import Machine
from phantasy import flameutils

# create FLAME machine
latfile = "test.lat"
m = Machine(open(latfile, 'r'))

# create MachineStates object
ms = flameutils.MachineStates(machine=m)

# create ModelFlame object
fm = flameutils.ModelFlame()
# setup machine and state
fm.mstates, fm.machine = ms, m

# setup observers and run flame model
obs = fm.get_index_by_type(type='bpm')['bpm']
r,s = fm.run(monitor=obs)

# get data of intereset from running results
data = fm.collect_data(r, pos=True, x0_env=True, ref_IonEk=True)
