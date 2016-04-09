from numpy import *
from tiger import *
from pdb import set_trace

class policy:

	def __init__(self):
		
		# -------- variables --------
		self.avec_pool = []      # alpha-vector pool
		self.action_pool = []    # action corresponding to avec_pool
		# ---------------------------


	def backup(self, bvec):

		# -------- inner max --------
		alpha_az = zeros([num_actions, num_observes], 'i')
		for ia in range(num_actions):
			for iz in range(num_observes):
				action_belief = dot(transpose(trans_p[:,:,ia]), bvec)
				value = [sum(avec * obser_p[:,iz,ia] * action_belief) for
				         avec in self.avec_pool]
				alpha_az[ia,iz] = value.index(max(value))

		# --- alpha vector update ---
		avec_new_pool = []    # candidate alpha-vector indexed by action
		for ia in range(num_actions):
			alpha_new = copy( reward[:,ia] )
			for iz in range(num_observes):
				alpha_new += discount * \
							 sum( self.avec_pool[alpha_az[ia,iz]] 
							 * obser_p[:,iz,ia] * trans_p[:,:,ia], 1 )
			avec_new_pool.append(alpha_new)

		# -------- outer max --------
		action_value = [dot(avec, bvec) for avec in avec_new_pool]
		best_action = action_value.index(max(action_value))

		# -- return updated alpha-vector & best action --
		return avec_new_pool[best_action], best_action

	def append_avec(self, avec_action):
		'''
		append a tuple of (avec, action) to pool
		'''
		assert(isinstance(avec_action, tuple))
		assert(len(avec_action) is 2)
		assert(isinstance(avec_action[0], ndarray))
		assert(isinstance(avec_action[1], int))
		self.avec_pool.append(avec_action[0])
		self.action_pool.append(avec_action[1])

	def copy_(self):
		copolicy = policy()
		copolicy.avec_pool.extend(self.avec_pool)
		copolicy.action_pool.extend(self.action_pool)
		return copolicy



if __name__ == '__main__':
	pol = policy()
	pol.avec_pool = [array([0.1,-0.3]), array([0.,0.1])]

	bvec = array([.4,.6])
	temp = pol.backup(bvec)


