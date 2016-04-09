from numpy import *
from tiger import *
from pdb import set_trace


class anode:

	def __init__(self, parent_node, action):

		# -------- variables --------
		self.bvec = None
		self.level = None
		self.action = None
		self.children = ()
		# ---------------------------

		assert(isinstance(action, int))
		assert(isinstance(parent_node.level, int))
		trans_matrix = trans_p[:,:,action]
		self.bvec = dot(transpose(trans_matrix), parent_node.bvec)
		self.action = action
		self.level = parent_node.level

	def addchildren(self):
		assert(self.children is ())
		for ii in range(num_observes):
			self.children += ( bnode(anode=self, obser=ii), )


class bnode:

	def __init__(self, **kwargs):

		# -------- variables --------
		self.bvec = None
		self.level = None
		self.obser = None
		self.children = ()
		# ---------------------------

		if 'bvec' in kwargs:                            # init root bnode
			self.init_root_bnode(kwargs.get('bvec'))

		elif 'anode' in kwargs and 'obser' in kwargs:   # init non-root bnode
			self.init_non_root_bnode(kwargs.get('anode'), 
			                         kwargs.get('obser'))

		else:
			assert(0)

	def init_root_bnode(self, bvec):
		self.bvec = bvec.copy()
		self.level = 0

	def init_non_root_bnode(self, anode, obser):
		assert(isinstance(obser, int))
		self.bvec = obser_p[:,obser,anode.action] * anode.bvec
		self.bvec /= sum(self.bvec)
		self.level = anode.level + 1
		self.obser = obser

	def addchildren(self):
		assert(self.children is ())
		for ii in range(num_actions):
			self.children += (anode(self, ii),)

def build_tree(depth, tree):
	if depth <= 0:
		return
	else:
		tree.addchildren()
		for achild in tree.children:
			achild.addchildren()
			for bchild in achild.children:
				build_tree(depth-1, bchild)
		return tree

def tree_bnodes(tree, tree_bvecs):
	'''
	extract bnodes of tree, with duplicates
	'''
	tree_bvecs.append(tree.bvec)
	if tree.children is not ():
		for achild in tree.children:
			for bchild in achild.children:
				tree_bnodes(bchild, tree_bvecs)

def unique_bvecs(tree_bvecs):
	ubvecs = []
	EPS = 1e-12
	for ii in range(len(tree_bvecs)):
		if not any( [max(abs(tree_bvecs[ii] - u))<EPS for u in ubvecs] ):
			ubvecs.append(tree_bvecs[ii])
	return ubvecs
		
	


if __name__ == '__main__':
	depth = 6
	tree = bnode(bvec=bvec0)    # init root
	tree = build_tree(depth, tree)

	tree_bvecs = []
	tree_bnodes(tree, tree_bvecs)

	ubvecs = unique_bvecs(tree_bvecs)

	print '----',depth,'level tree summary ----'
	print 'number of unique belief points: ',len(ubvecs)
	print '---- belief points ----'
	print ubvecs
