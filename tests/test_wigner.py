import numpy as np
import pyspawn        

seed=28396

pyspawn.import_methods.into_simulation(pyspawn.qm_integrator.rk2)
pyspawn.import_methods.into_simulation(pyspawn.qm_hamiltonian.adiabatic)

pyspawn.import_methods.into_traj(pyspawn.potential.terachem_cas)
pyspawn.import_methods.into_traj(pyspawn.classical_integrator.vv)
    
traj1 = pyspawn.traj()

t0 = 0.0

timestep = 10.0

tfinal = 10.0

ndims = 18

nstates = 2

istate = 0

pos = mom = np.zeros(ndims)

wid = 6.0* np.ones(ndims)

atoms = ['C', 'C', 'H', 'H', 'H', 'H']    

m = np.asarray([21864.0, 21864.0, 21864.0,
                21864.0, 21864.0, 21864.0,
                1822.0, 1822.0, 1822.0,
                1822.0, 1822.0, 1822.0,
                1822.0, 1822.0, 1822.0,
                1822.0, 1822.0, 1822.0])

tc_options = {
    "method":       'hf',
    "basis":        '6-31g**',
    "atoms":        atoms,
    "charge":       0,
    "spinmult":     1,
    "closed_shell": True,
    "restricted":   True,
    
    "precision":    "double",
    "threall":      1.0e-20,
    }

exshift = 78.0

traj1.init_traj(t0,ndims,pos,mom,wid,m,nstates,istate,"00")

traj1.set_spawnthresh(100.0)

traj1.set_tc_options(tc_options)

traj1.initial_wigner(seed)

print "pos", traj1.get_positions()

sim = pyspawn.simulation()

sim.add_traj(traj1)

sim.set_timestep_all(timestep)

sim.set_mintime_all(t0)

sim.set_maxtime_all(tfinal)

sim.set_qm_energy_shift(exshift)

sim.init_amplitudes_one()

sim.propagate()







