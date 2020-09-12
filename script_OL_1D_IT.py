import numpy as np
import matplotlib.colors as color
import matplotlib.axes as axes
import matplotlib.pyplot as pyplot
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
from matplotlib import rc
from numpy import linalg
import cmath
import time
from mpl_toolkits import mplot3d
from random import randint

import os
import sys
path_above_Codes = (sys.path[0]).split('Codes')[0]
sys.path.append(path_above_Codes+'Codes/')
## Import the libraries in the parent folder "Codes"
import lib_GrossPitaevskii as GP
import lib_Manage_files as Mf
import lib_Optical_Honeycomb_Lattice as OHL

rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern']})
rc('text', usetex=True)

############### TEST Imaginary Time ###################
print("script_OL_1D_IT.py is running")

path = path_above_Codes+'Codes/Optical_1D_Lattice_BEC/Self_consistent/Datas_IT'
list_args = ['N','V','U']
split = ['N_','V_','U_']
params_interv = {'U': np.logspace(-6,-3,30),'V': [3.5e-5],\
				'N': [1e5]}
extension = '.npy'
#files_names = Mf.select_files(path,extension,list_args,params_interv,split)
k = 0
for N in params_interv['N']:
	for V in params_interv['V']:
		for U in params_interv['U']:
			start = time.time()

			args_syst = {
			'J' : 1,
			'N' : N,
			'V' : V,
			'Nx' : 201,
			'U' : U,
			'Method' : 'IT',
			'Trap' : 'Harmonic',
			'Symm' : 'Isotropic',
			'syst' : '1D',
			}

			args_syst.update({'sites_dic' : GP.lattice_1D(args_syst)})

			## Kinetic + Trap part of Hamiltonian

			H_KV = GP.H_1D(args_syst)

			#if len(files_names)>0:
			if k==0:
			 	args_init = {
			 	'H_KV' : H_KV,
				'dt' : 1e-1,
				'err_IT' : 1e-9
				}

			else:
				args_init.update({'psi_init' : psi0})

			psi0 = GP.calc_psi0(args_syst,args_init)

			E_funct_IT = GP.energy_functional(psi0,args_syst)

			dt = args_init['dt']
			mu = GP.compute_mu(psi0,dt,args_syst,args_init)#[0]
			print(mu)

			Trap = GP.trap_1D(args_syst)
			U = args_syst['U']
			N = args_syst['N']
			Nx = args_syst['Nx']
			n_TF = (mu-Trap)/U/N
			diff_TF_n0 = np.sum(np.abs(n_TF-abs(psi0)**2))

			data = [args_syst,args_init,mu,psi0,E_funct_IT,H_KV,diff_TF_n0]
			dataID = '1D_%s_%s_%s_Nx_%.1i_J_%.2f_N_%.5e_V_%.3e_U_%.3e' %\
					(args_syst['Method'],args_syst['Trap'],args_syst['Symm'],\
					args_syst['Nx'],args_syst['J'],N,args_syst['V'],args_syst['U'])
			np.save('Datas_IT/'+dataID,data)

			print("For Nx = ", Nx, ", N = ", N, ", U = ", U, ", V = ", V,\
				"it took",time.time()-start,"secondes")

			k += 1