# -*-coding:UTF-8 -*

import numpy

def member(crit_eval):
	
	row = numpy.shape(crit_eval)[0]
	col = numpy.shape(crit_eval)[1]
	crit_eval = numpy.reshape(crit_eval.transpose(),(1,-1))
	checklist = numpy.ones((row,1),dtype=bool)
	front = numpy.zeros((row,1),dtype=bool)
	
	for s in range(0,row):
		t=s
		if checklist[t] == False:
			continue
			
		checklist[t] = False
		coldominatedflag = True
		
		for i in range(t+1,row):
			if checklist[i] == False:
				continue
				
			checklist[i] = False
			
			j1 = i
			j2 = t
			for j in range(0,col):
				if (crit_eval[0,j1] < crit_eval[0,j2]):
					checklist[i] = True
					break
					
				j1 += row
				j2 += row
				
			if checklist[i] == False:
				continue
				
			coldominatedflag = False
			
			j1 = i
			j2 = t
			for j in range(0,col):
				if crit_eval[0,j1] > crit_eval[0,j2]:
					coldominatedflag = True
					break
				
				j1 += row
				j2 += row	
			
			if coldominatedflag == False:
				front[t] = False
				checklist[i] = False
				coldominatedflag = True
				t = i
				
		front[t] = coldominatedflag
		if t > s:
			for i in range(s+1,t):
				if checklist[i] == False:
					continue
					
				checklist[i] = False
				
				j1 = i
				j2 = t
				for j in range(0,col):
					if crit_eval[0,j1] < crit_eval[0,j2]:
						checklist[i] = True
						break
						
					j1 += row
					j2 += row

	del checklist
	return front