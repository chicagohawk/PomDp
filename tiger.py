from numpy import *
num_states = 2
num_actions = 3
num_observes = 2

# transition probability
T0 = array([[1,0],[0,1]])
T1 = array([[.5,.5],[.5,.5]])
trans_p = dstack([T0,T1,T1])
del T0, T1

# observation probability
Z0 = array([[.85,.15],[.15,.85]])
Z1 = array([[.5,.5],[.5,.5]])
obser_p = dstack([Z0,Z1,Z1])
del Z0, Z1

# immediate reward
R0 = array([-1.,-1.])
R1 = array([-10.,2.])
R2 = array([2.,-10.])
reward = transpose(vstack([R0,R1,R2]))
del R0, R1, R2

# discount
discount = .9

# initial belief
bvec0 = array([.5,.5])
