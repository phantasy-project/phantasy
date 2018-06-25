from flame import Machine
import flame_utils

# create FLAME machine
latfile = "test.lat"
m = Machine(open(latfile, 'rb'))

# create BeamState object
bs = flame_utils.BeamState(machine=m)

# create ModelFlame object
fm = flame_utils.ModelFlame()
# setup machine and state
fm.bmstate, fm.machine = bs, m

# setup observers and run flame model
obs = fm.get_index_by_type(type='bpm')['bpm']
r,s = fm.run(monitor=obs)

# get data of intereset from running results
data = fm.collect_data(r, pos=True, x0_env=True, ref_IonEk=True)
