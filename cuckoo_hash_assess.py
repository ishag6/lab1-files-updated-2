# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.table = [None]*self.table_size

	def get_rand_bucket_index(self, bucket_idx: int) -> int:
		# you must use this function when you need to evict a random key from a bucket. this function
		# randomly chooses an index from a given cell index. this ensures that the random
		# index chosen by your code and our test script match.
		#
		# for example, if you need to remove a random element from the bucket at table index 5,
		# you will call get_rand_bucket_index(5) to determine which key from that bucket to evict, i.e. if get_random_bucket_index(5) returns 2, you
		# will evict the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, func_id: int) -> int:
		# access h0 via func_id=0, access h1 via func_id=1
		key = int(str(key) + str(self.__num_rehashes) + str(func_id))
		rand.seed(key)
		result = rand.randint(0, self.table_size-1)
		return result

	def get_table_contents(self) -> List[Optional[List[int]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.table

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		for _ in range(0, self.CYCLE_THRESHOLD+1):
			index0 = self.hash_func(key, 0)
			curr_key0 = self.table[index0]

			if(self.table[index0] is None):
				self.table[index0] = [key]
				return True
			
			elif(len(curr_key0) < self.bucket_size):
				self.table[index0].append(key)
				return True

			index1 = self.hash_func(key, 1)
			curr_key1 = self.table[index1]

			if(self.table[index1] is None):
				self.table[index1] = [key]
				return True
			
			elif(len(curr_key1) < self.bucket_size):
				self.table[index1].append(key)
				return True
			 
			else:
				evict_id = self.get_rand_bucket_index(index0)
				temp = self.table[index0][evict_id]
				self.table[index0][evict_id] = key
				key = temp
		return False

	def lookup(self, key: int) -> bool:
		_, index = self.lookup_index(key)
		return index != -1
		

	def delete(self, key: int) -> None:
		index, b_id = self.lookup_index(key)
		del self.table[index][b_id]
		if(len(self.table[index]) == 0):
			self.table[index] = None

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		
		old_table = self.table
		self.table = [None]*self.table_size
		for bucket in old_table:
			if bucket is not None:
				for key in bucket:
					self.insert(key)

	def lookup_index(self, key: int) -> tuple[int, int]:
		index_h0 = self.hash_func(key, 0)
		index_h1 = self.hash_func(key, 1)
		for b_id in range(self.bucket_size):
			if(self.table[index_h0] is not None and len(self.table[index_h0])>b_id and self.table[index_h0][b_id] == key):
				return index_h0, b_id
			elif(self.table[index_h1] is not None and len(self.table[index_h1])>b_id and self.table[index_h1][b_id] == key):
				return index_h1, b_id
			
		return None, -1

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


