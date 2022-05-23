import sys
import statistics
import math

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
		self.k = k
		
		self.idcolumn = id_column
		self.distfn=distfn
		self.labelcolumn = labelcolumn #1
		self.datacolumns = [] #[2,3,4,5,6,7]
		for d in range(len(datacolumns)):
			self.datacolumns.append(datacolumns[d])

		self.valuecolumns = []
		for v in range(len(valuecolumns)):
			self.valuecolumns.append(valuecolumns[v])

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
		return

	def add_training_data(self,datapt):
		self.trainingdata.append(datapt)
		return

	def find_nearest_k(self,datapoint):
		distarr = []
		def myfunc(t):
			return t[0]
		for i in range (0,len(self.trainingdata)):
			distarr.append((self.distfn(datapoint,self.trainingdata[i]),i))
		distarr.sort(key=myfunc)
		return distarr[:self.k]

	def classify(self,datapoint):
		nearest_neighbours=self.find_nearest_k(datapoint)
		labelarray=[]
		for i in nearest_neighbours:
			labelarray.append(self.trainingdata[i[1]].label)
		label = statistics.mode(labelarray)
		return label

	def regress(self,datapoint,omit_zeros =False):
		ctr=[0.0]*len(self.valuecolumns)
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











