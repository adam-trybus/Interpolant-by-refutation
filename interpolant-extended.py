#!/usr/bin/env python
# coding: utf-8

## Programs used in Rozko, Trybus, Skura 'A new method for finding interpolants: theoretical and practical considerations'
## the main program extended to cover any number of variables

import re
import itertools
import random

# gives simple random formula generator, parser and validity checker

from truthtable import *

# given a CNF/DNF formula in the truthtable.py notation, translates it into the list notation used here (aka the 'dot' notation)

def translate_to(Formula):
	rev = Formula[::-1]
	stack = []
	for i in range(len(rev)):
		if rev[i] == 'P':
			add = '.'+rev[i-4]+rev[i-2]+rev[i]+'.'
			stack = [add]+stack
		elif rev[i] == 'k':
			add = stack[1]+stack[0]+'C'
			stack = stack[2:]
			stack = [add]+stack	
		elif rev[i] == 'a':
			add = stack[1]+stack[0]+'D'
			stack = stack[2:]
			stack = [add]+stack
		elif rev[i] == 'n':
			add = stack[0]+'N'
			stack = stack[1:]
			stack = [add]+stack
	if stack[0][-1] == 'C' or stack[0][-1] == 'C':
		clean = stack[0]
		new_clean = clean.replace("C", "")
		clean = new_clean.replace("D", "")
		final = stack[0][-1]+clean[::-1]
	else:
		final = stack[0][::-1]	 
	return final

#print translate_to('k(P(1,2),P(2,2))')

# given a CNF/DNF formula used here, translate it into truthtable.py notation

def translate_from(Formula):
	rev = Formula[::-1]
	stack = []
	count = 1
	i = 0
	j = 0
	while i < len(rev) and j == 0:
		if rev[i] == 'P':
			count = rev[i-2]
			j = 1
		i = i+1
	

	for i in range(len(rev)):

		if rev[i] == 'P':
			add = ')'+rev[i-2]+','+rev[i-1]+'('+rev[i]
			stack = [add]+stack
		elif rev[i] == '1' and rev[i-1] == '.' and rev[i+1] == '.':
			add = ')'+str(count)+'(V'
			stack = [add]+stack
		elif rev[i] == '0' and rev[i-1] == '.' and rev[i+1] == '.':
			add = ')'+str(count)+'(N'
			stack = [add]+stack
		elif rev[i] == 'C':
			conjuncts = len(stack)
			if conjuncts == 1:
				add = '))'+str(count)+'(V,'+stack[0]+'(k'
				stack = stack[1:]
				stack = [add]+stack
			s = 1
			while s < conjuncts:
				add = ')'+stack[1]+','+stack[0]+'(k'
				stack = stack[2:]
				stack = [add]+stack
				s = s+1
		elif rev[i] == 'D':
			
			disjuncts = len(stack)
			if disjuncts == 1:
				
				add = '))'+str(count)+'(N,'+stack[0]+'(a'
				stack = stack[1:]
				stack = [add]+stack
			s = 1
			while s < disjuncts:
				
				add = ')'+stack[1]+','+stack[0]+'(a'
				stack = stack[2:]
				stack = [add]+stack
				s = s+1
		elif rev[i] == 'N':
			add = ')'+stack[0]+'(n'
			stack = stack[1:]
			stack = [add]+stack
	 
	return stack[0][::-1]

# input: a formula of the form X: CNF -> DNF in truthtable.py notation
# output: two sets of formulas in the 'dot' notation, to be treated as an input to interpolant(A,B) (provided X is a tautology)

def translate1(Formula):
	Formula = Formula[2:-1]
	#rev = Formula[::-1]
	two = []
	con = 0
	dis = 0
	for i in range(len(Formula)):
		
		if Formula[i] == 'k' and con == 0:
			con = 1
			count = 0
			fragment = Formula[i:]
			#print fragment
			for j in range(len(fragment)):
				if fragment[j] == '(':
					count = count+1
				elif fragment[j] == ')':
					count = count-1
				elif fragment[j] == ',' and count == 0:
					add1 = Formula[i:i+j]
					add2 = Formula[i+j+1:]
					two = two+[add1]+[add2]
	#print two
	count = 0
	remember = ['',0,0]
	flas0 = []
	for i in range(len(two[0])):
		if two[0][i] == '(':
			count = count+1
		elif two[0][i] == ')':
			if count == remember[2]:
				add = two[0][remember[1]:i]
				if add not in flas0:
					flas0 = flas0+[add]
				remember = [')',0,0]
			count = count-1
		elif two[0][i] == 'a':
			remember = ['a',i,count]
		elif two[0][i] == 'P' and remember[0] == '':
			remember = ['P',i,count]
		elif two[0][i] == 'n' and remember[0] == '':
			remember = ['n',i,count]
		elif two[0][i] == ',':
			if count == remember[2] and remember[0] != '':
				add = two[0][remember[1]:i]
				if add not in flas0:
					flas0 = flas0+[add]
				remember = ['',0,0]
	add = ''
	count = 0
	remember = ['',0,0]
	flas1 = []
	for i in range(len(two[1])):
		if two[1][i] == '(':
			count = count+1
		elif two[1][i] == ')':

			if count == remember[2]:
				add = two[1][remember[1]:i]
				if add not in flas1:
					flas1 = flas1+[add]
				remember = [')',0,0]
			count = count-1
		elif two[1][i] == 'k':
			remember = ['k',i,count]
		elif two[1][i] == 'P' and remember[0] == '':
			remember = ['P',i,count]
		elif two[1][i] == 'n' and remember[0] == '':
			remember = ['n',i,count]
		elif two[1][i] == ',':
			if count == remember[2] and remember[0] != '':
				add = two[1][remember[1]:i]
				if add not in flas1:
					flas1 = flas1+[add]
				remember = ['',0,0]

	
	# final step: translating the above into the 'dot' notation

	for f in range(len(flas0)):
		flas0[f] = translate_to(flas0[f])
	for f in range(len(flas1)):
		flas1[f] = translate_to(flas1[f])	
	return flas0, flas1



## given two sets of formulas (disjunctions and conjunctions) translate it to the truthtable.py notation in the form of A -> B (A is CNF, B is DNF) outputs three values A, B, and A->B

#print translate_from('.0.')
#print translate_from('C.P14.')

def translate2(A,B):

	New_A = ['']*len(A)
	New_B = ['']*len(B)


	for a in range(len(A)):
		New_A[a] = translate_from(A[a])

	for b in range(len(B)):
		New_B[b] = translate_from(B[b])

	items = len(A)
	final0 = []
	s = 0
	while s < items:
		if s == 0:
			if items == 1:
				add = New_A[s]
				final0 = [add]+final0
			elif items > 1:
				add = 'k('+New_A[s]+','+New_A[s+1]+')'
			final0 = [add]+final0
			s = s+2
		else:
			#if items > 2:
			add = 'k('+final0[0]+','+New_A[s]+')'
			final0 = [add]+final0
			s = s+1
	items = len(B)
	
	final1 = []
	s = 0
	while s < items:
		if s == 0:
			if items == 1:
				add = New_B[s]

				final1 = [add]+final1
			elif items > 1:
				add = 'a('+New_B[s]+','+New_B[s+1]+')'
			final1 = [add]+final1
			s = s+2
		else:
			#if items > 2:
			add = 'a('+final1[0]+','+New_B[s]+')'
			final1 = [add]+final1
			s = s+1
	return final0[0], final1[0], 'c('+final0[0]+','+final1[0]+')'




## checks whether given two formulas A,B, the third one (Interpolant) is their interpolant. Yields True if so, False otherwise.

def is_tautology_int(F1,F2):
	translation = translate2(F1,F2)
	return is_tautology(translation)

# checks whether a given formula is a part of any formula in a given list

def check_membership(y,X):
	for x in X:
		if y in x:
			return True
	return False



def preprocess(X):
	new_X = []
	for x in X:
		new_x = x.split('.')
		new_x = [value for value in new_x if value != '']
		checked = []
   		for e in new_x:
       			if e == 'D' or e == 'C':
           			checked.append(e)
			else:
				if '.'+e+'.' not in checked:
					checked.append('.'+e+'.')
   			
		new_X.append(checked)
	joined_X = []
	for x in new_X:
		joined_x = ''.join(x)
		joined_X.append(joined_x)
	return joined_X


# leaves only one copy of a given formula in a set

def preprocess_set(X):
	new_X = []
	for x in X:
		if x not in new_X:
			new_X.append(x)
	return new_X

# X conjunction of disjunctions
# Y disjunction of conjunctions
# changes Y into Y' which is of the same form as X
# Y' conjunction of disjunctions

def oneside_normal_form(Y):
	#print Y
	Y_prime = []
	for i in Y:
		if len(i) > 2 and i != '.1.' and i != '.0.':
			all_elements = re.findall(r'\.[A-Za-z0-9]+\.',i[1:])
		
			i_prime = 'D'
			for a in all_elements:
				a = a[1:-1]
				a_prime = ''
			
				if a[0] == 'N':
				
					a_prime = '.'+a[1:]+'.'
				elif a == '0':
					a_prime = '.1.'
				elif a == '1':
					a_prime = '.0.'
			
				else:
				
					a_prime = '.N'+a+'.'
			
				i_prime = i_prime+a_prime
			Y_prime.append(i_prime)
		elif len(i) == 1 and i == 'C':
			Y_prime.append('.0.')
		elif i == '.1.':
			Y_prime.append('.0.')
		elif i == '.0.':
			Y_prime.append('.1.')
		else:
			print 'Exception caught in oneside_normal_form'
	return Y_prime
#print oneside_normal_form(['C.P12..NP22.','C.P12.'])

def rev_oneside_normal_form(Y_Prime):
	Y = []
	for i in Y_Prime:
		if len(i) > 2 and i != '.1.' and i != '.0.':		
			all_elements = re.findall(r'\.[A-Za-z0-9]+\.',i[1:])
		
			i_rev = 'C'
			for a in all_elements:
				a = a[1:-1]
				a_rev = ''
				
				if a[0] == 'N':
				
					a_rev = '.'+a[1:]+'.'
				elif a == '0':
					a_rev = '.1.'
				elif a == '1':
					a_rev = '.0.'		
				else:
					
					a_rev = '.N'+a+'.'
			
				i_rev = i_rev+a_rev
			Y.append(i_rev)

		elif len(i) == 1 and i == 'D':
			Y.append('.1.')
		elif i == '.0.':
			Y.append('.1.')	
		elif i == '.1.':
			Y.append('.0.')		
		else:
			print 'Exception caught in rev_oneside_normal_form'
	return Y
#print rev_oneside_normal_form(['D.NP12..P22.', 'D.NP12.'])

def correct_number(X):
	count = '1'
	new_X = ''
	i = 0
	j = 0
	while i < len(X) and j == 0:
		if X[i] == 'P':
			count = X[i+4]
			j = 1
		i = i+1
	for i in range(len(X)):
		if X[i].isdigit() and X[i-2] == 'V' or X[i-2] == 'N':
			new_X = new_X+count
		else:
			new_X = new_X+X[i]
	return new_X

def correct_number_v2(X):
	count = '1'
	new_X = ''
	i = 0
	j = 0
	while i < len(X) and j == 0:
		if X[i] == 'P':
			count = X[i+4]
			j = 1
		i = i+1
	for i in range(len(X)):
		if X[i].isdigit() and X[i-2] == 'V' or X[i-2] == 'N':
			new_X = new_X+count
		else:
			new_X = new_X+X[i]
	return new_X

#checks if formulas are the same disregarding the order of the elements

def equal_formulas(a,b):
	all_lit_a = re.findall(r'\.[A-Za-z]+\.',a[1:])
	all_lit_b = re.findall(r'\.[A-Za-z]+\.',b[1:])
	if a[0] == b[0]:
		for alla in all_lit_a:
			for allb in all_lit_b:
				if alla not in all_lit_b or allb not in all_lit_a:
				 	return False
		return True
	else: return False

#gathers literals of size 1 (negates them or gets rid of negation) and cuts of the leading connective for further processing			

def gather_singles(A):
	singles = []
	for a in A:
		if len(a) < 6:
			singles.append(a[1:])
	return singles
	
#takes all the singles and produces all possible combinations of these


def sum_up(A):
	singles = gather_singles(A)
	combinations = []
	i = 2
	while i < len(singles)+1:
		value = [list(x) for x in itertools.product(singles,repeat=i)]
		for v in value:	
			va = ''.join(v)
			combinations.append(va)
		i = i+1
	final = preprocess(combinations)
	return final



def same_formulas(new_X,new_Y):
	X_lit = sum_up(new_X)
	Y_lit = sum_up(new_Y)
	Y_prime = oneside_normal_form(new_Y)
	for i in range(0,len(X_lit)):
		X_lit[i] = 'C'+X_lit[i]

	for i in range(0,len(Y_lit)):
		Y_lit[i] = 'D'+Y_lit[i]

	for x in new_X:
		for y in Y_prime + Y_lit:
			if equal_formulas(x,y):
				return x
	for y in gather_singles(new_Y):
		for x in gather_singles(new_X):
			if y == x:
				return y
	return False

#given a set of formulas, it extracts all the variables used

def variable_search(LitSet):
	var = []
	for i in LitSet:
		all_lit_i = re.findall(r'\.[A-Za-z0-9]+\.',i[1:])
		#print 'here', all_lit_i
		for l in all_lit_i:
			#print 'here', l
			if l[1] == 'N':
				if l[2:-1] not in var:
					var.append(l[2:-1])
			else:
				#print 'error'
				if l[1:-1] not in var:
					var.append(l[1:-1])
				#if 'D' in l or 'C' in l:
				#	print 'error'
	
	return var	

#print variable_search(['D.NP12..P22.', 'D.NP12.'])		

# produces all the formulas containing given literal
def literal_search(var,LitSet):
	lits = {}
	for v in var:
		lits[v] = []
		lits['N'+v] = []
		for i in LitSet:
			if 'N'+v+'.' in i:
				lits['N'+v].append(i)
			if '.'+v+'.' in i:
				lits[v].append(i)
	#for key in lits:
    	#	for k in lits[key]:
	#		print 'hello'
	return lits
#splits a clause into two: one is a single variable or its negation and the other is the rest 

def take_out(x,clause):
	new_clause = [clause[0]]
	result = ''
	all_lit = re.findall(r'\.[A-Za-z0-9]+\.',clause[1:])
	news = [value for value in all_lit if value != '.'+x+'.']
	new_clause = new_clause+news
	result = ''.join(new_clause)
	return result


# removes all occurences of a formula from a given set of formulas

def take_out_fla(fla, flas):
	news = [value for value in flas if value != fla]
	return news

# checks whether two formulas share at least one variable:

def vars_in_common(X,Y):
	var1 = variable_search(X)
	var2 = variable_search(Y)
	for x in var1:
		for y in var2:
			if x == y:
				return True
	
	return False
	#return any(x in set_v1 for x in var2)

# a helper function to simplify interpolants

def simplify(X):
	rev = X[::-1]
	print X
	#count = 0
	stack = []
	add = ''
	for x in range(len(X)):
		#print rev[x][::-1]
		if rev[x] == 'k':
			if stack[0][-1] == 'N':
				add = stack[0]
			elif stack[1][-1] == 'N':
				add = stack[1]
			elif stack[0][-1] == 'V':
				add = stack[1]
			elif stack[1][-1] == 'V':
				add = stack[0]
			else:
				add = ')'+stack[1]+','+stack[0]+'('+rev[x]
			stack = stack[2:]
			stack = [add]+stack
		elif rev[x] == 'a':
			if stack[0][-1] == 'N':
				add = stack[1]
			elif stack[1][-1] == 'N':
				add = stack[0]
			elif stack[0][-1] == 'V':
				add = stack[0]
			elif stack[1][-1] == 'V':
				add = stack[1]
			else:
				add = ')'+stack[1]+','+stack[0]+'('+rev[x]
			stack = stack[2:]
			stack = [add]+stack
		elif rev[x] == 'n':
			add = ')'+stack[0]+'('+rev[x]
			stack = stack[1:]
			stack = [add]+stack

		elif rev[x] == 'P':
			add = ')'+stack[1]+','+stack[0]+'('+rev[x]
			stack = stack[2:]
			stack = [add]+stack
		elif rev[x] == 'N':
			add = ')'+stack[0]+'('+rev[x]
			stack = stack[1:]
			stack = [add]+stack
		elif rev[x] == 'V':
			add = ')'+stack[0]+'('+rev[x]
			stack = stack[1:]
			stack = [add]+stack
		elif str(rev[x]).isdigit():
			add = rev[x]
			stack = [add]+stack
		#print 's: ',stack
	return stack[0][::-1]

#print simplify('k(N(1),P(1,1))')
#print simplify('k(a(P(1,4),k(a(P(2,4),N(4)),a(n(P(2,4)),V(4)))),a(n(P(1,4)),k(a(P(3,4),k(a(P(2,4),N(4)),a(n(P(2,4)),N(4)))),a(n(P(3,4)),k(a(P(2,4),V(4)),a(n(P(2,4)),N(4)))))))')
print simplify('k(a(P(2,2),k(a(P(1,2),V(2)),a(n(P(1,2)),N(2)))),a(n(P(2,2)),k(a(P(1,2),N(2)),a(n(P(1,2)),N(2)))))')

## not necessary?			
#def simplify_final(X):
#	formula = ''
#	sim = X
#	while len(sim) != len(formula):
#		formula = sim
#		sim = simplify(formula)
		
#	return sim
#print simplify_final('k(N(1),k(N(1),P(1,1)))')
#print simplify_final('k(a(P(1,4),k(a(P(2,4),N(4)),a(n(P(2,4)),V(4)))),a(n(P(1,4)),k(a(P(3,4),k(a(P(2,4),N(4)),a(n(P(2,4)),N(4)))),a(n(P(3,4)),k(a(P(2,4),V(4)),a(n(P(2,4)),N(4)))))))')	

#print simplify('k(a(P(2,4),N(4)),a(n(P(2,4)),k(a(P(3,4),V(4)),a(n(P(3,4)),N(4)))))')
#print simplify('k(a(P(1,1),N(1)),a(n(P(1,1)),V(1)))')
## the main function, given two formulas one a conjunction of DNFs and the other a disjunction of CNFs, it produces an interpolant of these, if it exists (pseudo-randomly selecting the literals to be eliminated)

def interpolant(X,Y):
	# the following two lines,uncommented, help build a search tree:
	print 'X: ',X
	print 'Y: ',Y
	
	
	if vars_in_common(X,Y):
		new_X = X
		new_Y = Y
		Y_Prime = oneside_normal_form(new_Y)
		var = variable_search(new_X+Y_Prime)
		Remainder_x = []
		Remainder_y = []
		selected = []
		literals_X = literal_search(var,new_X)
		literals_Y_Prime = literal_search(var,Y_Prime)
		total_literals = {}
		if len(literals_X) != 0:
			for key in literals_X:	
				if key in literals_Y_Prime:
	
					total_literals[key] = literals_X[key]+literals_Y_Prime[key]
				else:
					total_literals[key] = literals_X[key]
			if len(literals_Y_Prime) != 0:
				for key in literals_Y_Prime:
					if key not in total_literals:
						total_literals[key] = literals_Y_Prime[key]
			for key in total_literals:
				if 'N' not in key:
					if len(total_literals[key]) != 0 and len(total_literals['N'+key]) != 0:
						selected.append(key)




		if len(selected) != 0:
			chosen_literal = random.choice(selected)

			Remainder_x = new_X
			Remainder_y = Y_Prime
			for i in literals_X[chosen_literal]:	
				Remainder_x = take_out_fla(i, Remainder_x)

			for i in literals_Y_Prime[chosen_literal]:
				Remainder_y = take_out_fla(i, Remainder_y)
 
			for i in literals_X['N'+chosen_literal]:	
				Remainder_x = take_out_fla(i, Remainder_x)

			for i in literals_Y_Prime['N'+chosen_literal]:		
				Remainder_y = take_out_fla(i, Remainder_y)

			X_f1 = literals_X[chosen_literal]

			XF1 = []
			for xf1 in X_f1:
				xf1_new = take_out(chosen_literal,xf1)
				if xf1_new != 'D':
					XF1.append(xf1_new)
				else:
					XF1.append('.0.')

			Y_Prime_f1 = literals_Y_Prime[chosen_literal]
			YPF1 = []
			for ypf1 in Y_Prime_f1:
				ypf1_new = take_out(chosen_literal,ypf1)
				if ypf1_new != 'D':
					YPF1.append(ypf1_new)
				else:
					YPF1.append('.0.')

			X_f2 = literals_X['N'+chosen_literal]
			XF2 = []
			for xf2 in X_f2:
				xf2_new = take_out('N'+chosen_literal,xf2)
				if xf2_new != 'D':
					XF2.append(xf2_new)
				else:
					XF2.append('.0.')		
			Y_Prime_f2 = literals_Y_Prime['N'+chosen_literal]
			YPF2 = []
			for ypf2 in Y_Prime_f2:
				ypf2_new = take_out('N'+chosen_literal,ypf2)
				if ypf2_new != 'D':
					YPF2.append(ypf2_new)
				else:
					YPF2.append('.0.')

			YF1 = rev_oneside_normal_form(YPF1 + Remainder_y)
			YF2 = rev_oneside_normal_form(YPF2 + Remainder_y)
			XF1 = XF1 + Remainder_x
			XF2 = XF2 + Remainder_x
			F1 = (XF1, YF1)
			F2 = (XF2, YF2)
			print 'literal', chosen_literal	

	# l,l* in X
			if check_membership(chosen_literal,new_X) and check_membership('N'+chosen_literal,new_X) and not check_membership(chosen_literal,Y_Prime) and not check_membership('N'+chosen_literal,Y_Prime):
				#print 'doing alt',chosen_literal

				return correct_number('a('+interpolant(F1[0],F1[1])+','+interpolant(F2[0],F2[1])+')')
	# l,l* in Y
			elif not check_membership(chosen_literal,new_X) and not check_membership('N'+chosen_literal,new_X) and check_membership(chosen_literal,Y_Prime) and check_membership('N'+chosen_literal,Y_Prime):
				#print 'doing con',chosen_literal

				return correct_number('k('+interpolant(F1[0],F1[1])+','+interpolant(F2[0],F2[1])+')')

			else:
				#print 'doing the main form', chosen_literal
				return correct_number('k(a('+translate_from(chosen_literal)+','+interpolant(F1[0],F1[1])+'),a(n('+translate_from(chosen_literal)+'),'+interpolant(F2[0],F2[1])+'))')


			



		elif len(selected) == 0:
			#print 'to be translated', X, Y
			translatedX, translatedY, implication = translate2(X,Y)
			cor_X = correct_number_v2('n('+translatedX+')')
			cor_Y = correct_number_v2(translatedY)
			if is_tautology(cor_X):
				
				return 'N(1)'
			elif is_tautology(cor_Y):
				
				return 'V(1)'
			
	else:

		if len(X) != 0:
			if len(Y) != 0:
				#print 'to be translated', X, Y
				translatedX, translatedY, implication = translate2(X,Y)
				cor_X = correct_number_v2('n('+translatedX+')')
				cor_Y = correct_number_v2(translatedY)
			
				if is_tautology(cor_X):
			
					return 'N(1)'
				elif is_tautology(cor_Y):
			
					return 'V(1)'
			
			elif len(Y) == 0:
			#THIS CHECK IS SUPERFLUOUS - WE KNOW X HAS TO BE TAUT
				#new_Y = ['.1.']
				#translatedX, translatedY, implication = translate2(X,new_Y)

				#cor_X = correct_number_v2('n('+translatedX+')')
				#if is_tautology(cor_X):
				return 'N(1)'
				#	return 'N(1)'				
		elif len(X) == 0:
			#if len(Y) != 0: 
			#THIS CHECK IS SUPERFLUOUS - WE KNOW Y HAS TO BE TAUT
			#	X_new = ['.0.']
			#	translatedX, translatedY, implication = translate2(X_new,Y)
			#	cor_Y = correct_number_v2(translatedY)
			#	if is_tautology(cor_Y):
			return 'V(1)'
			#		return 'V(1)'



## a selection of functions used in stringing together and pretty-printing the results

def is_interpolant(A,B,Interpolant):
	#print 'Left side: ', A
	#print 'Right side: ', B
	#print 'Interpolant: ', Interpolant
	#print ''
	Final_A, Final_B, Implication = translate2(A,B)
	res1 = correct_number_v2('c('+Final_A+','+Interpolant+')')
	res2 = correct_number_v2('c('+Interpolant+','+Final_B+')')
	#print 'Implication: ',Implication
	#print 'final a ',Final_A
	#print 'final b ',Final_B
	#print 'imp1 ', res1 
	#print 'imp2 ', res2
	#print ''
	#imp_corrected = correct_number('c('+Final_A+','+Final_B')')
	final0 = is_tautology(correct_number_v2(Implication))
	if not final0:
		print 'The implication A -> B is not True! Searching for interpolant makes no sense!'
		return False
	#print 'Implication A -> B: ', final0
	final1 = is_tautology(res1)
	
	##print res1, final1
	
	final2 = is_tautology(res2)
	##print res2, final2
	#print final2
	if final0 and final1 and final2:
		return True
	#print res1, res2
	return False

def interpolant_final(X,Y):
	#print 'X1: ', X
	#print 'Y1: ', Y
	Final_X, Final_Y, Implication = translate2(X,Y)
	final0 = is_tautology(correct_number_v2(Implication))
	if not final0:
		print ''
		print 'The implication A -> B is not True! Searching for interpolant makes no sense!'
		print ''
		return False		
	result = interpolant(X,Y)
	#print 'interpolant to be checked: ', result
	#print 'X: ', X
	#print 'Y: ', Y
	#print 'result of is interpolant: ',is_interpolant(X,Y, result)
	if is_interpolant(X,Y, result):

		print ''
		print 'Good news everyone!'
		print ''
		print 'The formula'
		print ''
		print result
		print ''
		print 'is an interpolant of'
		print ''
		print X
		print ''
		print 'and'
		print ''
		print Y
		print ''
		print ''
		print '-------------------------------------------------------------------'
		print '-------------------------------------------------------------------'
		#return True
	else:
		print 'Bad news. We could not find an interpolant despite the right set-up.'
		print result
		#return False

# generates formulas A -> B in the dot notation. Default settings: pseudo-randomly choosing the number of variables (up to 4), conjuncts and disjuncts (10), 50% chance of getting negation. 

def generate_interpolant_formulas(vble,conjuncts=0,disjuncts=0):
	leftside = []
	rightside = []
	#vbles = []
	flagc = 0
	flagd = 0
	if conjuncts == 0:
		conjuncts = random.choice([1,2,3,4,5,6,7,8,9,10])
	variables = random.choice(range(1,vble))				
	for c in range(conjuncts):
		if flagc == 0:
			vc = variables
			flagc = 1
		else:
			vc = random.choice(range(variables))
		if vc == 0:
			vc = variables			
		vbles = []
		i = 1
		while i <= vc:
			vbles.append('.P'+str(i)+str(variables)+'.')
			i = i+1
		vbles_neg = []
		#negated = 0
		for v in vbles:
			neg = random.choice([0,1])
			if neg == 0:
		#		negated = negated+1
				vbles_neg.append('.N'+v[1:])

			else:
				vbles_neg.append(v)
		#ver = 0
		##vr = random.choice(range(10))
		##if vr == 1:
		##	vbles_neg = vbles_neg+['.1.']
		#	ver=ver+1
			#print ver
		##fl = random.choice(range(10))
		#fal = 0
		##if fl == 0:
		##	vbles_neg = vbles_neg+['.0.']
			#fal = fal+1
		random.shuffle(vbles_neg)
		conjunct = 'D'
		#negated = 0
		for v in vbles_neg:
			#if v[1] == 'N':
				#print v
		#		negated = negated+1
			conjunct = conjunct+v
		if conjunct not in leftside:
			leftside = leftside+[conjunct]	
	#variables_left = len(vbles)
	#print 'neg1',negated
	
	if disjuncts == 0:
		disjuncts = random.choice([1,2,3,4,5,6,7,8,9,10])
	
	for c in range(disjuncts):
		if flagd == 0:
			vd = variables
			flagd = 1
		else:
			vd = random.choice(range(variables))
		if vd == 0:
			vd = variables	
		vbles = []
		i = 1
		while i <= vd:
			vbles.append('.P'+str(i)+str(variables)+'.')
			i = i+1
		vbles_neg = []
		for v in vbles:
			neg = random.choice([0,1])
			if neg == 0:

				vbles_neg.append('.N'+v[1:])
			#	negated = negated+1
			else:
				vbles_neg.append(v)
		#ver = 0
		##vr = random.choice(range(10))
		##if vr == 1:
		##	vbles_neg = vbles_neg+['.1.']
		#	ver = ver+1
		#fal = 0
		##fl = random.choice(range(10))
		##if fl == 0:
		##	vbles_neg = vbles_neg+['.0.']
		#	fal=fal+1
		random.shuffle(vbles_neg)
		disjunct = 'C'
		for v in vbles_neg:
		#	if v[1] == 'N':
		#		negated  = negated+1
			disjunct = disjunct+v
		if disjunct not in rightside:
			rightside = rightside+[disjunct]
	#variables_right = len(vbles)
	formula_length_left = 0
	formula_length_right = 0
	negated_left = 0
	negated_right = 0
	#fal = 0
	#ver = 0

	for l in leftside:
		for i in l:
			#if i == '0':
			#	fal = fal+1
			#if i == '1':
			#	ver = ver+1
			if i == 'N':
				negated_left = negated_left+1

			
		formula_length_left = formula_length_left+len(l)

	for r in rightside:
		for i in r:
			#if i == '0':
			#	fal = fal+1
			#if i == '1':
			#	ver = ver+1
			if i == 'N':
				negated_right = negated_right+1

		formula_length_right = formula_length_right+len(r)	
	
	#return leftside, rightside
	return [leftside, rightside, len(leftside),len(rightside), variables, negated_left, negated_right, formula_length_left,formula_length_right, len(leftside)+len(rightside), negated_left+negated_right,formula_length_left+formula_length_right]


#print generate_interpolant_formulas(5)


# generates a set of CNF->DNF tautologies 

def generate_formulas_final(size,vble,conjuncts=0,disjuncts=0):
	formulas = []
	#if size == 0:
	#	size = 10
	while len(formulas) < size:
		result = generate_interpolant_formulas(vble,conjuncts,disjuncts)
		#print result
		Final_X, Final_Y, Implication = translate2(result[0],result[1])
		#print correct_number_v2(Implication)
		final0 = is_tautology(correct_number_v2(Implication))
		if final0 and ([result] not in formulas):
			formulas = formulas+[result]
		#formulas = formulas+[result]		
	return formulas
	
## a procedure generating formulas and checking their interpolants
	
#check = generate_formulas_final(1000,10,20,20)
#print check
#for i in check:
#	interpolant_final(i[0],i[1])

#print translate_from('D.P11.')#, 'D.NP11.')#, ['C.P11.', 'C.NP11.'])
#print c(k(a(P(1,1),V(1)),a(n(P(1,1)),V(1))),a(k(P(1,1),V(1)),k(n(P(1,1)),V(1))))
#print c(k(a(P(1,1),N(1)),a(n(P(1,1)),N(1))),a(k(P(1,1),V(1)),k(n(P(1,1)),V(1))))
#print c(k(a(P(1,1),V(1)),a(n(P(1,1)),V(1))),a(k(P(1,1),V(1)),k(n(P(1,1)),V(1))))
#print c(k(a(P(1,1),V(1)),a(n(P(1,1)),V(1))),k(a(P(1,1),N(1)),a(n(P(1,1)),N(1))))
#print c(k(a(P(1,1),V(1)),a(n(P(1,1)),V(1))),k(a(P(1,1),N(1)),a(n(P(1,1)),N(1))))
#print is_interpolant(['D.P11.', 'D.NP11.'], ['C.P11.', 'C.NP11.'],'k(a(P(1,1),N(1)),a(n(P(1,1)),N(1)))')

#EXAMPLES
#print translate2(['.0.'], ['C.P14.'])
#interpolant_final(['D.P14..NP44.', 'D.P24..P34.', 'D.NP14..NP24.','D.NP34..P44.'],['C.NP14..P24.','C.P14..NP24.'])
#print k(a(P(2,4),a(N(4),k(a(P(1,4),N(4)),a(n(P(1,4)),V(4))))),a(n(P(2,4)),k(a(P(1,4),V(4)),a(n(P(1,4)),N(4)))))
#interpolant_final(['D.p..Ns.', 'D.q..r.', 'D.Np..Nq.','D.Nr..s.'],['C.Np..q.','C.p..Nq.']) 
#interpolant_final(['D.Np..Nq..r.'],['C.p..Nq.','C.Np.','C.r.']) 
#c = 0
#while c < 100:
	
#	interpolant_final(['D.P14..NP44.', 'D.P24..P34.', 'D.NP14..NP24.','D.NP34..P44.'],['C.P14..NP34.','C.NP14..P24.','C.P14..NP24.']) #from article
#	c = c+1
interpolant_final(['D.P14..NP44.', 'D.P24..P34.', 'D.NP14..NP24.','D.NP34..P44.'],['C.P14..NP34.','C.NP14..P24.','C.P14..NP24.']) #from article
#interpolant_final(['D.P11..NP11.', 'D.P11..P11.'],['C.P11.']) #from article
#interpolant_final(['D.P11.'],['C.P11.']) #from article

#interpolant_final(['D.q..r.','D.Nq.','D.Nr..s.','D.q.'],['.0.'])
#interpolant_final(['D.P14..NP24.','D.NP14..NP34.','D.P24.'],['C.P24..NP34.','C.NP24..NP44.','C.P44.']) #from D'Silva
#interpolant_final(['D.P12.','D.P22.'],['C.NP12.','C.P22.'])# Szymon's example
#interpolant_final(['D.NP12.','D.P12..NP22.'],['D.NP12.','D.P12..NP22.']) # from D'Silva 2



