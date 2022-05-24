import sys
import random
import math
from knn import *

def dist_eq(x,y):
	sum_of_sq=0
	for i in range(len(x.data)):
		sum_of_sq += pow(x.data[i]-y.data[i],2) 
	distance = math.sqrt(sum_of_sq)
	return distance

def dist_dot_prod(x,y):
	dp =0.0
	for i in range(len(x.data)):
		dp += x.data[i]*y.data[i]
	return dp

def cosine_distance(x,y):
	dp =0.0
	nx =0.0
	ny=0.0
	#print(f"len(x) = {len(x.data)} len(y) = {len(y.data)}")
	for i in range(len(x.data)):
		dp += x.data[i]*y.data[i]
		nx+=x.data[i]**2
		ny+=y.data[i]**2
	nx=math.sqrt(nx)
	ny=math.sqrt(ny)
	inv_arg= dp/(nx*ny)
	return math.acos(inv_arg)

def main():
	train_file_name = sys.argv[1]
	test_file_name = sys.argv[2]
	k = int(sys.argv[3])

	## We added a fake item id 0 when preparing the data, so
	## the nitems is 1682 +1
	nitems = 1683
	
	idcol = 0
	datacols = range(1,nitems+1)
	labelcol = None
	valuecols = range(1,nitems+1)
	
	knn_train = Knn(train_file_name,k,cosine_distance,
					id_column = idcol, 
					datacolumns=datacols,
					labelcolumn=labelcol,
					valuecolumns = valuecols)

	#run the test
	def make_datapoint(line_items):
		d=[]
		for l in line_items[1:-2]:
			d.append(float(l))
		dp=datapoint(d,None,d,line_items[0])
		return dp
		
	test_file = open(test_file_name)
	accuracy=0
	nusers=0
	for line in test_file:
		line = line.rstrip("\r\n")
		line_items = line.split(",")
		dp=make_datapoint(line_items)
		rating_array=knn_train.regress(dp,omit_zeros =True)
		#as the last eement is the actual rating
		actual_value= float(line_items[-1]) 
		#second last column is the column dropped, rating array does not include user id.
		index = int(line_items[-2])-1
		predicted_value=rating_array[index]
		
		accuracy+=(predicted_value-actual_value)**2
		print(f"done user {nusers}. Predicted Rating = {predicted_value} Actual Rating = {actual_value}")
		nusers+=1
	accuracy = math.sqrt(accuracy)
	accuracy/=nusers
	print(accuracy)
	return

if __name__ == "__main__":
	main()
