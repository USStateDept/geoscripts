class _Node:
	def __init__(self,data):
		self.data = data
		self.next = None
	
class LinkedList:

	def __init__(self):
		self.length = 0
		self._root = None
		
	# Returns true if a node is added (skips duplicates)
	def add(self,nation):
		nation = str(nation)
		if self.length == 0:
			self._root = _Node(nation)
			self.length += 1
			return True
		else:
			prevNode = None
			curNode = self._root
			while curNode is not None:
				if nation == curNode.data: # duplicate
					return False
				if nation < curNode.data: # prepend
					newNode = _Node(nation)
					newNode.next = curNode
					if prevNode is None:
						self._root = newNode
					else:
						prevNode.next = newNode
					self.length += 1
					return True				
				else: # nation > curNode.data
					prevNode = curNode
					curNode = curNode.next
			prevNode.next = _Node(nation) # append
			self.length += 1
			return True
