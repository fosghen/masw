import random
import numpy as np
from dc_fast import dc_fast
from joblib import Parallel, delayed
# from multiprocessing import cpu_count

def GWOmp(disp_data, freq, nummode, model_range, vs2vp, wave, max_iter):

    # disp_data = disp_data.reshape((len(disp_data), 1))
    disp_data = np.squeeze(disp_data)

    tests_num = 10
    
    vs_min = model_range['vs_up']
    vs_max = model_range['vs_down']
    thk_min = model_range['thk_up']
    thk_max = model_range['thk_down']
    
    agents_num = (np.size(np.squeeze(thk_min)) + np.size(np.squeeze(vs_min)))*10
    
    results = Parallel(n_jobs=tests_num)(delayed(GWO)(i, disp_data, freq, nummode, vs_min, vs_max, thk_min, thk_max, agents_num, max_iter, vs2vp, wave) for i in range(tests_num))
    
    vs = np.zeros((len(np.squeeze(vs_min)), tests_num))
    thk = np.zeros((np.size(np.squeeze(thk_min)), tests_num))
    convergence_curve = np.zeros((max_iter, tests_num))

    for i in range(tests_num):
        vs[:, i] = np.squeeze(results[i][0])
        thk[:, i] = np.squeeze(results[i][1])
        convergence_curve[:, i] = np.squeeze(results[i][2])
        
    vp = np.int32(vs*vs2vp)
    rho = np.int32(0.61*vp**0.18*1000)
    mse = np.zeros(tests_num)
    for ii in range(tests_num):
        dc = dc_fast(nummode, freq, vs[:, ii], vp[:, ii], rho[:, ii], thk[:, ii], wave=wave).T.flatten()
        dc[np.where(disp_data == 0)] = 0
        mse[ii] = np.mean((disp_data - dc)**2)
    ind_min = np.argmin(mse)
    
    return vs[:, ind_min], thk[:, ind_min]

def GWO(test_iter,disp_data,freq,nummode,vs_min,vs_max,thk_min,thk_max,SearchAgents_no,Max_iter,vs2vp,wave):

    thk_dim = np.size(np.squeeze(thk_min))
    vs_dim = len(np.squeeze(vs_min))
    dim = thk_dim + vs_dim
    rg_thk = thk_max - thk_min
    rg_vs = vs_max - vs_min

    Convergence_curve_out = np.zeros((Max_iter))    
        
    lb=0.0
    ub=1.0

    # initialize alpha, beta, and delta_pos
    Alpha_pos=np.zeros(dim)
    Alpha_score=float("inf")

    Beta_pos=np.zeros(dim)
    Beta_score=float("inf")

    Delta_pos=np.zeros(dim)
    Delta_score=float("inf")

    if not isinstance(lb, list):
        lb = [lb] * dim
    if not isinstance(ub, list):
        ub = [ub] * dim

    #Initialize the positions of search agents
    Positions = np.zeros((SearchAgents_no, dim))

    for i in range(dim):
        Positions[:, i] = np.random.uniform(0,1, SearchAgents_no) * (ub[i] - lb[i]) + lb[i]

    velocity = 0.8*np.random.randn(SearchAgents_no,dim)
    w = 0.5+random.random()/2

    # Main loop
    for l in range(0,Max_iter):
        for i in range(0,SearchAgents_no):

            # Return back the search agents that go beyond the boundaries of the search space
            for j in range(dim):
                Positions[i,j]=np.clip(Positions[i,j], lb[j], ub[j])

            # Calculate objective function for each search agent
            thk_l = Positions[i,0:thk_dim]*rg_thk + thk_min
            vs_l = Positions[i,thk_dim:]*rg_vs + vs_min

            freq = np.array([np.squeeze(freq)])
            vs_l = np.array([np.squeeze(vs_l)])
            thk_l = np.array([np.squeeze(thk_l)])
        
            if (vs_l[:,-1] < vs_l[:,-2]):
                vs_l[:,-1] = vs_l[:,-2]+50
            vp = np.int32(vs_l*vs2vp)
            rho = np.int32(0.61*vp**0.18*1000)
            disp = dc_fast(nummode, freq, vs_l, vp, rho, thk_l, wave=wave).T.flatten()
            disp[np.where(disp_data == 0)] = 0
            fitness = np.linalg.norm(disp-disp_data)**4

            # Update Alpha, Beta, and Delta

            if fitness<Alpha_score :
                Delta_score=Beta_score  # Update delte #!!!!!!!!!!!!!!!
                Delta_pos=Beta_pos.copy() #!!!!!!!!!!!!!!!
                Beta_score=Alpha_score  # Update beta #!!!!!!!!!!!!!!!
                Beta_pos=Alpha_pos.copy() #!!!!!!!!!!!!!!!
                Alpha_score=fitness; # Update alpha
                Alpha_pos=Positions[i,:].copy()
                thk_out = thk_l.copy()
                vs_out = vs_l.copy()


            if (fitness>Alpha_score and fitness<Beta_score ):
                Delta_score=Beta_score  # Update delte #!!!!!!!!!!!!!!!
                Delta_pos=Beta_pos.copy() #!!!!!!!!!!!!!!!
                Beta_score=fitness  # Update beta
                Beta_pos=Positions[i,:].copy()


            if (fitness>Alpha_score and fitness>Beta_score and fitness<Delta_score):                 
                Delta_score=fitness # Update delta
                Delta_pos=Positions[i,:].copy()


        a=2-l*((2)/Max_iter); # a decreases linearly fron 2 to 0

        # Update the Position of search agents including omegas
        for i in range(0,SearchAgents_no):
            for j in range (0,dim):     

                r1=random.random()                    
                A1=2*a*r1-a;
                D_alpha=abs(0.5*Alpha_pos[j]-w*Positions[i,j]);
                X1=Alpha_pos[j]-A1*D_alpha; 


                r1=random.random()
                A2=2*a*r1-a;
                D_beta=abs(0.5*Beta_pos[j]-w*Positions[i,j]);
                X2=Beta_pos[j]-A2*D_beta; 


                r1=random.random()
                A3=2*a*r1-a;
                D_delta=abs(0.5*Delta_pos[j]-w*Positions[i,j]);
                X3=Delta_pos[j]-A3*D_delta;


                r2=random.random()
                r3=random.random()

                velocity[i,j] = w*(velocity[i,j]+0.5*r1*(X1-Positions[i,j])+0.5*r2*(X2-Positions[i,j])+0.5*r3*(X3-Positions[i,j]))
                Positions[i,j] = Positions[i,j]+velocity[i,j]


        Convergence_curve_out[l]=Alpha_score;
    
    
    return vs_out,thk_out,Convergence_curve_out
    

