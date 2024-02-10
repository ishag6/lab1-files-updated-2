# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		table_id = 0
		for _ in range(0, self.CYCLE_THRESHOLD+1):
			index = self.hash_func(key, table_id)
			if(self.tables[table_id][index] is None):
				self.tables[table_id][index] = key
				return True
			else:
				temp = self.tables[table_id][index]
				self.tables[table_id][index] = key
				key = temp
				table_id = 1 - table_id
		return False

	def lookup(self, key: int) -> bool:
		index, _ = self.lookup_index(key)

		if(index == -1):
			return False
		else:
			return True


	def delete(self, key: int) -> None:
		index, table_id = self.lookup_index(key)
		self.tables[table_id][index] = None


	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		old_tables = self.tables
		self.tables = [[None]*self.table_size for _ in range(2)]
		for table_id in [0, 1]:
			for key in old_tables[table_id]:
				if key is not None:
					self.insert(key)

	def lookup_index(self, key: int) -> tuple[int, int]:
		index0 = self.hash_func(key, 0)
		index1 = self.hash_func(key, 1)
		if(self.tables[0][index0] == key):
			return index0, 0
		elif(self.tables[1][index1]==key):
			return index1, 1
		else:
			return -1, None

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


