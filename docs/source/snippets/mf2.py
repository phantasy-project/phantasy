import matplotlib.pyplot as plt
import numpy as np

from flame import Machine
import flame_utils


latfile = "test.lat"
m = Machine(open(latfile, 'rb'))

ek_out = []
ek0_arr = np.linspace(1, 1000, 20)
for ek0 in ek0_arr:
    bs = flame_utils.BeamState(machine=m)
    bs.ref_IonEk = ek0 * 1000

    fm = flame_utils.ModelFlame()
    fm.bmstate, fm.machine = bs, m

    obs = fm.get_index_by_type(type='bpm')['bpm']
    r,s = fm.run(monitor=obs)

    ek_out.append(s.ref_IonEk)


plt.rcParams['font.size'] = 18
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['figure.dpi'] = 110

plt.plot(ek0_arr, np.array(ek_out)/1e6, 'o--', mfc='r', mec='r', ms=10)
plt.xlabel('$E_k^0\,\mathrm{[keV/u]}$')
plt.ylabel('$E_k^f\,\mathrm{[MeV/u]}$')
#data = fm.collect_data(r, pos=True, ref_IonEk=True)
#plt.plot(data['pos'], data['ref_IonEk'], 'r-')
plt.show()
