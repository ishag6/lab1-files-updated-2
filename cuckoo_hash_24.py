# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24_Delete:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10
		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def get_rand_idx_from_bucket(self, bucket_idx: int, table_id: int) -> int:
		# you must use this function when you need to displace a random key from a bucket during insertion (see the description in requirements.py). 
		# this function randomly chooses an index from a given bucket for a given table. this ensures that the random 
		# index chosen by your code and our test script match.
		# 
		# for example, if you are inserting some key x into table 0, and hash_func(x, 0) returns 5, and the bucket in index 5 of table 0 already has 4 elements,
		# you will call get_rand_bucket_index(5, 0) to determine which key from that bucket to displace, i.e. if get_random_bucket_index(5, 0) returns 2, you
		# will displace the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx) + str(table_id)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[List[int]]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.
	
	def insert(self, key: int) -> bool:
		table_id = 0
		for _ in range(0, self.CYCLE_THRESHOLD+1):
			index = self.hash_func(key, table_id)
			curr_key = self.tables[table_id][index]

			if(self.tables[table_id][index] is None):
				self.tables[table_id][index] = [key]
				return True
			
			elif(len(curr_key) < self.bucket_size):
				self.tables[table_id][index].append(key)
				return True 
			
			else:
				evict_id = self.get_rand_idx_from_bucket(index, table_id)
				temp = self.tables[table_id][index][evict_id]
				self.tables[table_id][index][evict_id] = key
				key = temp
				table_id = 1 - table_id
		return False

	def lookup(self, key: int) -> bool:
		_, _, index = self.lookup_index(key)
		return index != -1

	def delete(self, key: int) -> None:
		table_id, index, b_id = self.lookup_index(key)
		del self.tables[table_id][index][b_id]
		if(len(self.tables[table_id][index]) == 0):
			self.tables[table_id][index] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		old_tables = self.tables
		self.tables = [[None]*self.table_size for _ in range(2)]
		for table_id in [0, 1]:
			for bucket in old_tables[table_id]:
				if bucket is not None:
					for key in bucket:
						self.insert(key)

	def lookup_index(self, key: int) -> tuple[int, int, int]:
		index_t0 = self.hash_func(key, 0)
		index_t1 = self.hash_func(key, 1)
		for b_id in range(self.bucket_size):
			if(self.tables[0][index_t0] is not None and len(self.tables[0][index_t0])>b_id and self.tables[0][index_t0][b_id] == key):
				return 0, index_t0, b_id
			elif(self.tables[1][index_t1] is not None and len(self.tables[1][index_t1])>b_id and self.tables[1][index_t1][b_id] == key):
				return 1, index_t1, b_id
			
		return None, None, -1


	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


