from numpy import *
from tiger import *
from belieftree import *
from alphavector import *
from pdb import set_trace
import matplotlib.pyplot as plt
import time

class optimizer:

	def __init__(self, depth):
		'''
		use belief nodes of tree up to 'depth'
		'''
		# -------- variables --------
		self.bnodes = []
		
		# current best policy
		self.policy_best = policy()

		# policy_best's alpha-vector index for bnodes
		self.best_avec_index = None
		
		# policy_best's value for bnodes
		self.best_value = None

		# bnodes not yet improved
		self.bnodes_queued = []

		# index of bnodes_queued in bnodes
		self.bnodes_queued_index = []
		
		# new policy in progress
		self.policy_new  = policy()

		self.iter_count  = 0
		# ---------------------------

		self.init_bnodes(depth)
		self.init_policy()
	
	
	def init_bnodes(self, depth):
		'''
		construct tree and get unique reachable bvecs
		'''
		assert(self.bnodes == [])
		tree = bnode(bvec=bvec0)
		tree = build_tree(depth, tree)
		tree_bvecs = []
		tree_bnodes(tree, tree_bvecs)
		ubvecs = unique_bvecs(tree_bvecs)
		self.bnodes.extend(ubvecs)

	def init_policy(self):
		'''
		initialize lower bound policy
		'''
		avec = reward.min() / (1-discount) * array([1.,1.])
		action = 0
		self.policy_best.append_avec( (avec,action) )

	def get_current_best(self):
		'''
		from policy_best get best avec index and value
		for all bnodes
		'''
		self.best_avec_index = []
		self.best_value = []

		for b in self.bnodes:
			vals = [dot(avec, b) for avec in self.policy_best.avec_pool]
			max_val_ind = vals.index( max(vals) )
			self.best_value.append( vals[max_val_ind] )
			self.best_avec_index.append( max_val_ind )

	def get_rand_queued_bnodes(self):
		'''
		from bnodes_queued get a random sample, its index in bnodes_queued,
		and its index in bnodes
		'''
		rqi = random.randint(0, len(self.bnodes_queued))
		ri =self.bnodes_queued_index[rqi]
		rbnode = self.bnodes_queued[rqi]
		return rbnode, rqi, ri

	def prune_queued_bnodes(self, avec):
		'''
		from bnodes_queued prune belief points improved by avec
		'''
		assert(len(self.bnodes_queued) == len(self.bnodes_queued_index))
		new_val = [dot(avec, b) for b in self.bnodes_queued]
		best_val = [self.best_value[i] for i in self.bnodes_queued_index]

		not_improve_index = [not new_val[ii] >= best_val[ii] for ii in range(len(new_val))]
		update_bnodes_queued = []
		update_bnodes_queued_index = []
		for ii in range(len(not_improve_index)):
			if not_improve_index[ii] is True:
				update_bnodes_queued.append( self.bnodes_queued[ii] )
				update_bnodes_queued_index.append( self.bnodes_queued_index[ii] )
		self.bnodes_queued = update_bnodes_queued
		self.bnodes_queued_index = update_bnodes_queued_index

	
	def perseus_main(self, max_iter):

		while self.iter_count < max_iter:
			print 'iteration', self.iter_count
			self.plot_policy()
			plt.draw()
	
			time.sleep(.1)

			self.get_current_best()
			self.policy_new.avec_pool = []
			self.policy_new.action_pool = []
			self.bnodes_queued = []
			self.bnodes_queued.extend( self.bnodes )
			self.bnodes_queued_index = r_[:len(self.bnodes)]
			
			while len(self.bnodes_queued) is not 0:

				rqb = self.get_rand_queued_bnodes()
				avec_backup = self.policy_best.backup(rqb[0])
				if dot(avec_backup[0], rqb[0]) < self.best_value[rqb[2]]:
					avec_backup = (self.policy_best.avec_pool[
					                    self.best_avec_index[ rqb[2] ] ],
					               self.policy_best.action_pool[
								        self.best_avec_index[ rqb[2] ] ] )
				self.prune_queued_bnodes(avec_backup[0])
				self.policy_new.append_avec( avec_backup )

			self.policy_best = self.policy_new.copy_()
			self.iter_count += 1


	def plot_policy(self):
		for ii in range(len(opt.policy_best.avec_pool)):
			color_rgb = zeros(3)
			color_rgb[opt.policy_best.action_pool[ii]] = 1.
			plt.plot(array([0,1]), opt.policy_best.avec_pool[ii], color=color_rgb,
			         linewidth=1)



if __name__ == '__main__':

	fig = plt.figure()
	plt.axis([0.,1.,-100.,0.])
	plt.ion()
	plt.show()

	opt = optimizer(5)
	opt.perseus_main(100)

	fig_final = plt.figure()
	plt.axis([0.,1.,-5.,0.])
	plt.show()
	opt.plot_policy()
