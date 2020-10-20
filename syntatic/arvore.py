# Class responsible for creating a tree


class Arvore:
	def __init__(self, type, children=None, leaf=''):
		"""
		:param type:
		:param children: Child
		:param leaf: leaf
		"""
		self.type = type
		if children:
			self.children = children
		else:
			self.children = []
		self.leaf = leaf

	def __str__(self):
		return self.type


def print_tree(node: Arvore, level=""):
	"""
	Func for printing the tree
	:param node:
	:param level:
	:return: no return
	"""
	if node is not None:
		print("%s└── %s %s" % (level, node.type, node.leaf))
		for son in node.children:
			print_tree(son, level+"│\t")
