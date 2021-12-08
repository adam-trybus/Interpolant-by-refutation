#!/usr/bin/env python
# coding: utf-8

## Programs used in Rozko, Trybus, Skura, 'A new method for finding interpolants: theoretical and practical considerations'
## a collection of functions used to run the experiments

import time
from truthtable import *
from interpolant import *
from results50000 import *
from results100000 import *


def con_count(Formula):
	count = 0
	for chars in Formula:
		if chars == 'c' or chars == 'n' or chars == 'a' or chars == 'k':
			count = count+1
	return count

def is_interpolant_v2(A,B,Interpolant):
	Final_A, Final_B, Implication = translate2(A,B)
	res1 = correct_number_v2('c('+Final_A+','+Interpolant+')')
	res2 = correct_number_v2('c('+Interpolant+','+Final_B+')')
	#final0 = is_tautology(correct_number_v2(Implication))
	final1 = is_tautology(res1)
	
	final2 = is_tautology(res2)
	if final1 and final2:
		return True

	return False

def interpolant_check(List):
	New_List = [[]]*len(List)
	for l in range(len(List)):
		t0 = time.time()
		result = interpolant(List[l][0],List[l][1])
		t1 = time.time()
		total = t1-t0
		connectives = con_count(result)
		length = len(result)
		
		if is_interpolant_v2(List[l][0],List[l][1], result):
			New_List[l] = List[l]+[[total,connectives,length,1]]
		else:
			New_List[l] = List[l]+[[total,connectives,length,0]]
	return New_List 

#print interpolant_check(results50000)
			

