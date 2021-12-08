#!/usr/bin/env python
# coding: utf-8

## Programs used in Rozko, Trybus, Skura 'A new method for finding interpolants: theoretical and practical considerations'
## This file contains various plotting options to be used on the generated data

import matplotlib.pyplot as plt

# Scientific libraries
from numpy import arange,array,ones
from scipy import stats
from results50000c_final import *
from results100000c_final_changed import *

# x - total number of conjuncts and disjuncts y - execution time

## a routine used for checking whether all interpolants were computed properly

#for r in results100000_final:
#	if r[-1][-1]  == 0:
#		print 'problem: ', r
#for r in results50000_final:
#	if r[-1][-1]  == 0:
#		print 'problem: ', r

def plot_one(results):
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[-3]]
			plot_1y = plot_1y+[r[-1][0]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
	plt.plot(plot_1x, plot_1y,'ro')
	plt.xlabel('Conjuncts+Disjuncts')
	plt.ylabel('Execution time')
	plt.show()
# x - abs(vblesx,vblesy) y - execution time
def plot_two(results):
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[10]]
			plot_1y = plot_1y+[r[-1][0]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
	plt.plot(plot_1x, plot_1y,'ro')
	plt.xlabel('|var(a)-var(b)|')
	plt.ylabel('Execution time')
	plt.show()	

# x - abs(vblesx,vblesy) y - connectives in interpolant
def plot_three(results):
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[10]]
			plot_1y = plot_1y+[r[-1][1]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
	plt.plot(plot_1x, plot_1y,'ro')
	plt.xlabel('|var(a)-var(b)|')
	plt.ylabel('Connectives in interpolant')
	plt.show()

# x - size of entire formula y - connectives in interpolant
def plot_four(results):
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[-2]]
			plot_1y = plot_1y+[r[-1][1]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
	plt.plot(plot_1x, plot_1y,'ro')
	plt.xlabel('Size of entire formula')
	plt.ylabel('Connectives in interpolant')
	plt.show()

# x - size of A y - connectives in interpolant
def plot_five(results):
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[8]]
			plot_1y = plot_1y+[r[-1][1]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
	plt.plot(plot_1x, plot_1y,'ro')
	plt.xlabel('Size of A')
	plt.ylabel('Connectives in interpolant')
	plt.show()

# x - size of B y - connectives in interpolant
def plot_six(results):
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[9]]
			plot_1y = plot_1y+[r[-1][1]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
	plt.plot(plot_1x, plot_1y,'ro')
	plt.xlabel('Size of B')
	plt.ylabel('Connectives in interpolant')
	plt.show()

# x - size of entire formula y - Execution time
def plot_seven(results):
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[-2]]
			plot_1y = plot_1y+[r[-1][0]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
# Generated linear fit
	slope, intercept, r_value, p_value, std_err = stats.linregress(plot_1x, plot_1y)
	#print slope, intercept
	line = [0]*len(plot_1x)
	for x in range(len(plot_1x)):
		line[x] = slope*plot_1x[x]+intercept
	#line = slope*plot_1x+intercept
	#print line
	plt.plot(plot_1x, plot_1y,'ro',plot_1x,line)
	plt.xlabel('Size of entire formula')
	plt.ylabel('Execution time')
	plt.show()

# execution time
def plot_eight(results):
	plot_1x = range(len(results))
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			#plot_1x = plot_1x+[r[9]]
			plot_1y = plot_1y+[r[-1][0]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
	plt.plot(plot_1x, plot_1y)
	plt.xlabel('Formulas')
	plt.ylabel('Execution time')
	plt.show()
# interpolant size
def plot_nine(results):
	plot_1x = range(len(results))
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			#plot_1x = plot_1x+[r[9]]
			plot_1y = plot_1y+[r[-1][1]]
		else:
			print 'problem'
	#x = np.array(plot_1x)
	#y = np.array(plot_1y)
	plt.plot(plot_1x, plot_1y)
	plt.xlabel('Formulas')
	plt.ylabel('Size of interpolant')
	plt.show()
# x - number of connectives y - execution time
def plot_ten(results):
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[11]+r[13]]
			plot_1y = plot_1y+[r[-1][0]]
		else:
			print 'problem'

# Generated linear fit
	slope, intercept, r_value, p_value, std_err = stats.linregress(plot_1x, plot_1y)

	line = [0]*len(plot_1x)
	for x in range(len(plot_1x)):
		line[x] = slope*plot_1x[x]+intercept

	plt.plot(plot_1x, plot_1y,'ro',plot_1x,line)
	plt.xlabel('Number of connectives')
	plt.ylabel('Execution time')
	plt.show()

# x - execution time y - size of interpolant
def plot_eleven(results): # redraw for all!
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1y = plot_1y+[r[-1][0]]
			plot_1x = plot_1x+[r[-1][2]]
		else:
			print 'problem'

# Generated linear fit
	slope, intercept, r_value, p_value, std_err = stats.linregress(plot_1x, plot_1y)

	line = [0]*len(plot_1x)
	for x in range(len(plot_1x)):
		line[x] = slope*plot_1x[x]+intercept

	plt.plot(plot_1x, plot_1y,'ro',plot_1x,line)
	plt.xlabel('Size of interpolant')
	plt.ylabel('Execution time')
	plt.show()

# x - execution time y - connectives in interpolant
def plot_twelve(results): 
	plot_1x = []
	plot_1y = []
	for r in results:
		if r[-1][-1] == 1:
			plot_1x = plot_1x+[r[-1][0]]
			plot_1y = plot_1y+[r[-1][1]]
		else:
			print 'problem'

# Generated linear fit
	slope, intercept, r_value, p_value, std_err = stats.linregress(plot_1x, plot_1y)

	line = [0]*len(plot_1x)
	for x in range(len(plot_1x)):
		line[x] = slope*plot_1x[x]+intercept

	plt.plot(plot_1x, plot_1y,'ro',plot_1x,line)
	plt.xlabel('Execution time')
	plt.ylabel('Connectives in interpolant')
	plt.show()
def avg_plot():
	data = {250: [0.0177167711258, 51.604, 405.728],2500:[0.0178924340248, 51.416, 404.2492],25000:[0.018560828886, 51.6226, 405.78164],500:[0.0111432590485, 42.484, 335.536],5000:[0.0111658424854, 42.1904, 333.3664],50000:[0.0113954098845, 42.40632, 334.99912],1000:[0.00431912994385, 18.784, 152.027],10000:[0.00437281694048, 18.8883776755, 152.797159432],100000:[0.00425030883831, 18.8281765635, 152.360797216]}
	plot_1x = []
	plot_1y = []
	for d in data:
		plot_1x = plot_1x + [data[d][0]]
		plot_1y = plot_1y + [data[d][2]]
	slope, intercept, r_value, p_value, std_err = stats.linregress(plot_1x, plot_1y)

	line = [0]*len(plot_1x)
	for x in range(len(plot_1x)):
		line[x] = slope*plot_1x[x]+intercept

	plt.plot(plot_1x, plot_1y,'ro',plot_1x,line)
	plt.xlabel('Average execution time')
	plt.ylabel('Average size of interpolant')
	plt.show()

## in the paper, only the functions plot_seven and plot_eleven were used

#plot_seven(results50000_final)
#plot_eleven(results50000_final)

