# A class from which all fms classes should be derived.
# Includes methods for output of classes to json format.
# The ability to read/dump data from/to json is essential to the
# restartability that we intend.
# nested python dictionaries serve as an intermediate between json
# and the native python class
import simulation
import traj
import numpy as np
import h5py

class fafile(object):
    def __init__(self,h5filename):
        self.h5file = h5py.File(h5filename, "r")
        self.num_traj = len(self.retrieve_amplitudes()[0][:])
        self.labels = self.h5file["sim"].attrs["labels"]
        self.istates = self.h5file["sim"].attrs["istates"]

    def __del__(self):
        self.h5file.close()

    def get_num_traj(self):
        return self.num_traj

    def get_max_state(self):
        return (np.amax(self.istates)+1)

    def compute_expec(self,Op,c,zreal=True):
        expec = np.matmul(c.conjugate(), np.matmul(Op, c))
        if zreal:
            expec = expec.real
        return expec

    def compute_expec_istate_not_normalized(self,Op,c,istate,zreal=True):
        ctmp = np.zeros(len(c),dtype=np.complex128)
        for i in range(len(c)):
            if self.istates[i] == istate:
                ctmp[i] = c[i]
        expec = np.matmul(ctmp.conjugate(), np.matmul(Op, ctmp))
        if zreal:
            expec = expec.real
        return expec
    
    def retrieve_amplitudes(self):
        c = self.h5file["sim/qm_amplitudes"][()]
        return c
        
    def retrieve_Ss(self):
        S = self.h5file["sim/S"][()]
        return S

    def retrieve_num_traj_qm(self):
        ntraj = np.ndarray.flatten(self.h5file["sim/num_traj_qm"][()])
        return ntraj
        
    def retrieve_times(self):
        times = np.ndarray.flatten(self.h5file["sim/quantum_time"][()])
        return times
        
    def compute_norms(self,column_filename=None):
        if column_filename != None:
            of = open(column_filename, 'w')
        
        times = self.retrieve_times()
        ntimes = len(times)
        c = self.retrieve_amplitudes()
        S = self.retrieve_Ss()
        ntraj = self.retrieve_num_traj_qm()
        maxstates = self.get_max_state()
        Nstate = np.zeros((maxstates+1,ntimes))
        for i in range(ntimes):
            nt = ntraj[i]
            c_t = c[i][0:nt]
            nt2 = nt*nt
            S_t = S[i][0:nt2].reshape((nt,nt))
            for ist in range(maxstates):
                Nstate[ist,i] =  self.compute_expec_istate_not_normalized(S_t,c_t,ist)
            Nstate[maxstates,i] = self.compute_expec(S_t,c_t)
            if column_filename != None:
                of.write(str(times[i])+ " "+" ".join(map(str,Nstate[:,i]))+"\n")
        if column_filename != None:
            of.close() 

        return times, Nstate

    def write_xyzs(self):
        for key in self.labels:
            trajgrp = "traj_" + key
            times = self.h5file[trajgrp]['time'][()].flatten()
            ntimes = len(times)
            pos = self.h5file[trajgrp]['positions'][()]
            npos = pos.size / ntimes
            natoms = npos/3
            print "pos.size, ntimes", pos.size, ntimes
            print "npos, natoms", npos, natoms

            filename = trajgrp + ".xyz"
            of = open(filename,"w")

            for itime in range(ntimes):
                of.write(str(natoms)+"\n")
                of.write("T = "+str(times[itime])+"\n")
                for iatom in range(natoms):
                    of.write("C  "+str(pos[itime,3*iatom])+"  "+str(pos[itime,3*iatom+1])+"  "+str(pos[itime,3*iatom+2])+"\n")

            of.close()
