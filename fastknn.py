import sys
import statistics
import math
import random

class datapoint:
	def __init__(self,data,label,values=[],id=None):
		self.data=data
		self.label=label
		self.values=[]
		for v in values:
			self.values.append(v)
		self.id = id
		return 


class Knn:
	def __init__(self,filename,k,distfn,
				id_column = None, datacolumns=[],labelcolumn=None,valuecolumns =[]):
		self.trainingdata = []

		self.fastnnhashdict = {}

		self.k = k
		self.idcolumn = id_column
		self.distfn=distfn

		self.rand_vectors = []
		self.rand_vec_size= 5

		self.labelcolumn = labelcolumn #1
		self.datacolumns = [] #[2,3,4,5,6,7]
		for d in range(len(datacolumns)):
			self.datacolumns.append(datacolumns[d])

		self.valuecolumns = []
		for v in range(len(valuecolumns)):
			self.valuecolumns.append(valuecolumns[v])


		for i in range(self.rand_vec_size):
			v=[]
			sum=0
			for j in range(len(self.valuecolumns)):
				v.append(random.random())

			for k in  range(len(v)):
				sum+=v[k]**2

			sum=math.sqrt(sum)

			for m in range(len(v)):
				v[m]=v[m]/sum

			self.rand_vectors.append(v)

		file = open(filename)
		flag=0
		for line in file:
			if(flag==0):
				flag=1
				continue
			line=line.strip("\r\n")
			line_items=line.split(",")
			cur_data=[]
			for i in datacolumns:
				if (line_items[i]==""):
					cur_data.append(0.0)
				else:
					cur_data.append(float(line_items[i]))

			values = []
			for v in self.valuecolumns:
				values.append(float(line_items[v]))

			did = None
			if not(self.idcolumn == None):
				did = line_items[self.idcolumn]

			lbl = None
			if not(labelcolumn == None):
				lbl = line_items[labelcolumn]

			dpt=datapoint(cur_data,lbl,values,did)
			self.add_training_data(dpt)
		file.close()
		print(len(self.fastnnhashdict))
		return

	def add_training_data(self,datapt):
		self.trainingdata.append(datapt)
		h=self.get_fast_hash(datapt)
		if not h in self.fastnnhashdict:
			self.fastnnhashdict[h]=[]
		self.fastnnhashdict[h].append(datapt)

		return

	#fast method starts:
	def get_near_list_fast(hashval):
		return self.fastnnhashdict[hashval]

	def get_fast_hash(self,datapoint):
		# to check: normalize the datapoint.values before the dotproduct.
		def sign(x):
			if x>=0 :
				return 1
			else:
				return -1
		def dotprod(x,y):
			dp =0.0
			for i in range(len(x)):
				dp += x[i]*y[i]
			return dp

		d=[]
		for i in range(len(self.rand_vectors)):
			r = self.rand_vectors[i]
			h = sign(dotprod(r,datapoint.values))
			d.append(h)
		return tuple(d)

	def find_nearest_k_fast(self,datapoint):
		distarr = []
		def myfunc(t):
			return t[0]
		hashval = get_fast_hash(datapoint)
		l = self.get_near_list_fast(hashval)
		for i in range (0,len(l)):
			distarr.append((self.distfn(datapoint,l[i]),i))
		distarr.sort(key=myfunc)
		return distarr[:min(self.k,len(l))]

	def find_nearest_k(self,datapoint):
		distarr = []
		def myfunc(t):
			return t[0]
		for i in range (0,len(self.trainingdata)):
			distarr.append((self.distfn(datapoint,self.trainingdata[i]),i))
		distarr.sort(key=myfunc)
		return distarr[:self.k]

	def classify(self,datapoint,usefastnn=False):
		if usefastnn==True:
			nearest_neighbours=self.find_nearest_k_fast(datapoint)
		else:
			nearest_neighbours=self.find_nearest_k(datapoint)
		labelarray=[]
		for i in nearest_neighbours:
			labelarray.append(self.trainingdata[i[1]].label)
		label = statistics.mode(labelarray)
		return label

	def regress(self,datapoint,omit_zeros =False,usefastnn=False):
		ctr=[0.0]*len(self.valuecolumns)
		if usefastnn==True:
			nearest_neighbours=self.find_nearest_k_fast(datapoint)
		else:
			nearest_neighbours=self.find_nearest_k(datapoint)
		reg_array = [0.0]*len(self.valuecolumns)
		for n in nearest_neighbours:
			for c in range(len(reg_array)):
				if (not(omit_zeros) or (self.trainingdata[n[1]].values[c] >0.0) ):
					reg_array[c] += self.trainingdata[n[1]].values[c]
					ctr[c]+=1

		for c in range(len(reg_array)):
			if ctr[c]>0 :
				reg_array[c] /= ctr[c]

		return reg_array











