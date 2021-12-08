#!/usr/bin/env python
# coding: utf-8

## A validity-checker used in Rozko, Trybus, Skura, 'A new method for finding interpolants: theoretical and practical considerations'

import random

# check if falsum is left to be F() anywhere (it should be N())

## Syntax for formulas is as follows:
## 
## LaTeX | This version
##
## A \to B | c(A,B)
## \lnot A | n(A)

## set up for propositional variables' valuations used in evaluating formulas


p = [[1,0],[1,1,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]]
q = [[],[1,0,1,0],[1,1,0,0,1,1,0,0],[1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0]]
r = [[],[],[1,0,1,0,1,0,1,0],[1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0]]
s = [[],[],[],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]]

#support for p_1...

def P(V_number, Total_variables):

	rows = 2**Total_variables
	divide = 2**(V_number-1)
	result = [0]*rows
	skip = rows / divide
	last_step = 0
	while last_step < rows:
		for i in range(last_step,last_step+(skip/2)):
			result[i] = 1
		last_step = last_step+skip
	return result

#uncomment for testing
#print P(1,3)
#print P(2,3)
#print P(3,3)	
		

## definitions of variables and connectives as in CL (implication and negation as primitives)

# Verum

def V(Number):
	result = [1]*(2**Number)
	return result

# Falsum

def N(Number):
	#print 'number ', Number
	result = [0]*(2**Number)
	return result

#variable+number of variables in a formula

def v(name, no):
	if name == p:
		return p[no-1]
	elif name == q and len(q[no-1]) != 0:
		return q[no-1]
	elif name == r and len(r[no-1]) != 0:
		return r[no-1]
	elif name == s and len(s[no-1]) != 0:
		return s[no-1]
	else:
		return name

#print v(p,2)
#print v(P(2,2),2)

def n(A):
	result = []
	for i in range(len(A)):
		if A[i] == 1:
			result.append(0)
		elif A[i] == 0:
			result.append(1)	
	return result

def c(A, B):
	result = [0]*len(A)
	for i in range(len(A)):
		if A[i] == 1 and B[i] == 1:
			result[i] = 1
		elif A[i] == 1 and B[i] == 0:
			result[i] = 0
		elif A[i] == 0 and B[i] == 1:
			result[i] = 1
		elif A[i] == 0 and B[i] == 0:
			result[i] = 1

	return result

def a(A,B):
	return c(n(A),B)	# should there be the parentheses around the thing? see if it gives problems		


def k(A,B):
	return n(a(n(A),n(B)))

def e(A,B):
	return k(c(A,B),c(B,A))


## uncomment first two for testing. These all should evaluate to 1:

#print c(V(2),v(p,2))
#print c(v(p,2),c(v(q,2),v(p,2)))
#print c(c(v(p,3),c(v(q,3),v(r,3))),c(c(v(p,3),v(q,3)),c(v(p,3),v(r,3))))
#ax3 = c(con,c(con,vble(a,2),vble(b,2)),c(con,n(con,vble(b,2)),n(con,vble(a,2))))
#ax4 = c(con,n(con,n(con,vble(a,2))),vble(a,2))
#ax5 = c(con,vble(a,2),n(con,n(con,vble(a,2))))
#ax6 = c(con,pand(con,vble(a,2),vble(b,2)),vble(a,2))
#ax7 = c(con,pand(con,vble(a,2),vble(b,2)),vble(b,2))
#ax8 = c(con,c(con,vble(a,3),vble(b,3)),c(con,c(con,vble(a,3),vble(d,3)),c(con,vble(a,3),pand(con,vble(b,3),vble(d,3)))))
#ax9 = c(con,vble(a,2),por(con,vble(a,2),vble(b,2)))
#ax10 = c(con,vble(b,2),por(con,vble(a,2),vble(b,2)))
#ax11 = c(con,c(con,vble(a,3),vble(d,3)),c(con,c(con,vble(b,3),vble(d,3)),c(con,por(con,vble(a,3),vble(b,3)),vble(d,3))))
#ax12 = c(con,peq(con, vble(a,2),vble(b,2)),c(con, vble(a,2),vble(b,2)))
#ax13 = c(con,peq(con, vble(a,2),vble(b,2)),c(con, vble(b,2),vble(a,2)))
#ax14 = c(con,c(con, vble(a,2),vble(b,2)),c(con,c(con, vble(b,2),vble(a,2)),peq(con, vble(a,2),vble(b,2))))



## a parser (in general, it does not check whether the string entered is of the correct form, it might simply not work tho). When parsing a formula it builds its truth-table for further processing:

def parser(F):

	rev = F[::-1]
	stack = []
	final = []
	subflas = []
	number = 0
	table = []	
		
	for i in range(len(rev)):

		if str(rev[i]).isdigit() and str(rev[i+2]).isdigit():
			# support for p_1 ... p_n notation
			if not rev[i+2] <= rev[i]:
				print 'ERROR. Badly defined variable arities.'
			else:
				if number == 0 or number == rev[i]:
					number = rev[i]
					add = rev[i]
					stack = [add]+stack
				else:
					print 'ERROR: The arities of variables do not match!'
					print ''

		elif str(rev[i]).isdigit() and rev[i+1] == '(':
			add = rev[i]
			stack = [add]+stack
		elif str(rev[i]).isdigit():
			if number == 0 or number == rev[i]:
				number = rev[i]
				add = rev[i]
				stack = [add]+stack
			else:
				print 'ERROR: The arities of variables do not match!'
				print ''
		# support for p_{1} ... p_{n} notation
		if rev[i] == 'P':
			add = ')'+stack[1]+','+stack[0]+'('+rev[i]
			stack = stack[2:]
			stack = [add]+stack
		elif rev[i] == 'p' or rev[i] == 'q' or rev[i] == 'r' or rev[i] == 's':
			#if rev[i] == 's':
			#	print 'here' 
			add = rev[i]
			stack = [add]+stack
		elif rev[i] == 'n':
			add = ')'+stack[0]+'('+rev[i]
			#print add[::-1]
			goahead = 1
			for t in table:
				if t[0] == add[::-1]:
					goahead = 0
			if goahead == 1:
				table = table + [[add[::-1],eval(rev[i])(eval(stack[0][::-1]))]]			
			stack = stack[1:]
			stack = [add]+stack
			if add not in final:
				final = [add]+final				

		elif rev[i] == 'v' or rev[i] == 'k' or rev[i] == 'a' or rev[i] == 'c' or rev[i] == 'e':
			add = ')'+stack[1]+','+stack[0]+'('+rev[i]
			goahead = 1
			#if rev[i] == 'k' or rev[i] == 'a':
			#	if stack[1] == '0':
					
			for t in table:
				if t[0] == add[::-1]:
					goahead = 0
			if goahead == 1:
				table = table + [[add[::-1],eval(rev[i])(eval(stack[0][::-1]),eval(stack[1][::-1]))]]
			stack = stack[2:]
			stack = [add]+stack
			if add not in final:
				final = [add]+final
		elif rev[i] == 'N' or rev[i] == 'V':
			add = ')'+stack[0]+'('+rev[i]
			goahead = 1			
			for t in table:
				if t[0] == add[::-1]:
					goahead = 0
			if goahead == 1:
				#print rev[i][::-1]
				#print 'stack', stack[0][::-1]
				table = table + [[add[::-1],eval(rev[i])(eval(stack[0][::-1]))]]
			stack = stack[1:]
			stack = [add]+stack
			if add not in final:
				final = [add]+final
	# gives a list of subflas, if I ever need one here
	for f in final:
		a = f[::-1]
		subflas = subflas + [a]
	#final prepocessing of table. Need all the variables up front in the following order p, q ,r (if exist).

	vbles = []
	for j in table:

		if j[0][0] == 'v':
			vbles.append(j)
	for v in vbles:
		table.remove(v)
	vbles.sort(key=lambda x: x[0])
	table = vbles+table

	return number, table, subflas
	#return subflas

## uncomment the following for testing. The result should be the truth-table for a given formula

#print parser('c(v(P(1,2),2),c(v(P(2,2),2),v(P(1,2),2)))')
#print parser('c(v(p,2),c(v(q,2),v(p,2)))')
#print parser('c(V(2),c(v(q,2),v(p,2)))')
#print parser('v(p(2),2)')
#print parser('c(c(v(p,3),c(v(q,3),v(r,3))),c(c(v(p,3),v(q,3)),c(v(p,3),v(r,3))))')
#print parser('k(k(k(k(a(v(p,4),n(v(s,4))),a(v(q,4),v(r,4))),a(v(q,4),v(r,4))),a(n(v(p,4)),n(v(q,4)))),a(n(v(r,4)),v(s,4)))')
#print parser('a(a(k(n(v(p,4)),v(q,4)),k(v(p,4),n(v(q,4)))),k(v(p,4),n(v(q,4))))')
#print parser('a(a(k(n(v(p,4)),v(q,4)),k(v(p,4),n(v(q,4)))),k(v(p,4),n(v(q,4))))')
#print parser('k(a(v(p,2),a(v(q,2),F(2)),a(n(v(p,2),n(v(q,2))))')
#print eval('N')(eval('2'))
#print parser('N(2)')
#print F(2)
#print parser('k(a(v(p,2),a(v(q,2),F(2)),a(n(v(p,2),n(v(q,2))))')
#print parser('k(a(v(p,2),a(v(q,2),F(2)),a(n(v(p,2),n(v(q,2))))')
#print parser('c(k(k(k(k(a(v(p,4),n(v(s,4))),a(v(q,4),v(r,4))),a(v(q,4),v(r,4))),a(n(v(p,4)),n(v(q,4)))),a(n(v(r,4)),v(s,4))),k(a(v(p,4),a(v(q,4),F(4)),a(n(v(p,4),n(v(q,4)))))')
## checks whether a given formula is a tautology, returns True if so, False otherwise

def is_tautology(Formula):

	tautology  = 'yes'
	number, parsed, subflas = parser(Formula)
	#print parsed
	for i in parsed[-1][1]:
		if i == 0:
			tautology = 'no'
	if tautology == 'yes':
		return True
	#print parsed[-1][1]
	return False

## random formula generator. Gives formulas with up to 4 variables, up to 4 connectives, when variables and connectives are chosen at random (i.e. are set to 0) This can be overrun apart from the lower limit for variable number. Negation default is set to 0, can be any number.

def generate(variables=0,connectives=0,negation=0):
	subflas = []
	vbles = []
	symbols = ['c','k','e','a']
	
	if variables == 0:
		variables = random.choice([1,2,3,4])
	if connectives == 0:
		if variables != 4:
			connectives = random.choice(range(variables,4))
		else:
			connectives = 4
	
	
	if variables == 1:
		vbles = ['v(p,1)']
	elif variables == 2:
		vbles = ['v(p,2)','v(q,2)']
	elif variables == 3:
		vbles = ['v(p,3)','v(q,3)','v(r,3)']
	elif variables == 4:
		vbles = ['v(p,4)','v(q,4)','v(r,4)','v(s,4)']
	elif variables > 4:
		for v in range(variables):
			vbles = vbles+['P('+str(v+1)+','+str(variables)+')']
		
	
	used_symbols = []
	count = connectives
	while count > 0:
		used_symbols.append(random.choice(symbols))
		count = count - 1
	
	count = negation
	while count > 0:
		used_symbols.append('n')
		count = count - 1	
	random.shuffle(used_symbols)
	random.shuffle(vbles)
	subflas = vbles+subflas
	
	#gives simple formulas - the method can be easily changed to give something more interesting
	if len(used_symbols) < len(vbles):
		print 'ERROR. Number of connectives must be at least to equal the number of variables'
		return False
	else:
		count = 0
		for u in used_symbols:
			
			if count > len(vbles)-1:
	
				count = random.choice(range(len(vbles)))
			if u == 'c' or u == 'a' or u == 'k' or u == 'e':
				vble = random.choice([1,0])
				if vble == 1:
					one = vbles[count]
					two = subflas[-1]
				else:
					two = vbles[count]
					one = subflas[-1]			
  	
				add = u+'('+one+','+two+')'
				subflas = subflas+[add]
				count = count+1
			elif u == 'n':
				one = subflas[-1]
				add = u+'('+one+')'
				subflas = subflas+[add]
			
		

	return subflas[-1]

#uncomment for testing

#print generate(2,3,1)
#print generate()
#print generate(5,6,1)
# Either generates a random formula or selects one from a list, and asks for filling in the missing values for a randomly chosen subformula (that is not a variable) and asks whether the entire formula is a tautology. Could be easily extended to ask for filling in random spots (not entire columns) or to print the truth-table (with the missing spots) in a human-readable form (also the formula itself can be presented in a more standard way). It can be passed on to create a LaTeX file and used to calculate points.

def question_one(flas, variables=0, connectives=0, negation=0):

	if len(flas) == 0:
		Formula = generate(variables,connectives,negation)
	else:
		Formula = random.choice(flas)
	tautology  = 'yes'
	number, parsed, subflas = parser(Formula)
	#print parsed
	for i in parsed[-1][1]:
		if i == 0:
			tautology = 'no'
	column = random.choice(parsed[int(number):-1])
		
	print ''
	print 'Consider the following formula:'
	print ''
	print parsed[-1][0]
	print ''
	tautology_answer = raw_input("Is this formula a tautology (yes/no):\n")
	print ''
		
	if tautology_answer == tautology:
		print 'Correct!'
	else:
		print 'Wrong!'
	print ''
	print ''
	print 'What are the values for '+column[0]+'?'
	print ''
	column_answer = raw_input("Enter them from top to bottom in the following format el_1 el_2 el_3 ... el_n:\n")
	print ''
	list_answer = column_answer.split()
	#print list_answer
	correct = 1
	if len(list_answer) == len(column[1]):
		for r in range(len(list_answer)):
			if int(list_answer[r]) != column[1][r]:
				correct = 0 
		if correct == 1:
			print 'Correct!'
		else:
			print 'Wrong!'
			print 'This is how it should have looked like:'
			print ''
			print column[1]
		print ''
	else:
		print 'You have entered a wrong number of values.'

# uncomment for testing
#print c(k(k(k(k(a(v(p,4),n(v(s,4))),a(v(q,4),v(r,4))),a(v(q,4),v(r,4))),a(n(v(p,4)),n(v(q,4)))),a(n(v(r,4)),v(s,4))),k(a(v(q,4),a(k(a(v(r,4),N(4)),a(n(v(r,4)),N(4))),k(a(v(p,4),V(4)),V(4)))),a(n(v(q,4)),a(k(a(v(p,4),V(4)),a(n(v(p,4)),k(a(v(r,4),N(4)),a(n(v(r,4)),V(4))))),k(a(v(p,4),N(4)),a(n(v(p,4)),N(4)))))))

#print c(k(a(v(q,3),a(k(a(v(r,3),N(3)),a(n(v(r,3)),N(3))),k(a(v(p,3),V(3)),V(3)))),a(n(v(q,3)),a(k(a(v(p,3),V(3)),a(n(v(p,3)),k(a(v(r,3),N(3)),a(n(v(r,3)),V(3))))),k(a(v(p,3),N(3)),a(n(v(p,3)),N(3)))))),a(a(a(k(v(p,3),n(v(r,3))),k(n(v(p,3)),v(q,3))),k(n(v(p,3)),v(q,3))),k(v(p,3),n(v(q,3)))))
#question_one([])
#question_one([],2,3,1)
#question_one(['c(v(p,2),c(v(q,2),v(p,2)))'])
#question_one(['c(c(v(p,3),c(v(q,3),v(r,3))),c(c(v(p,3),v(q,3)),c(v(p,3),v(r,3))))'])
#print k(a(n(v(r,2)),N(2)),V(2))
#print v(s,1)
#print n(v(s,1))
#print a(n(v(p,1)),N(1))
#print  c(k(k(k(a(n(v(s,4)),N(4)),a(v(q,4),v(r,4))),a(v(q,4),v(r,4))),a(n(v(r,4)),v(s,4))),a(k(a(v(p,4),N(4)),V(4)),N(4)))
#print c(V(1),a(a(n(v(p,1)),N(1)),N(1)))
#print k(a(v(p,1),k(a(v(p,1),V(1)),V(1))),a(n(v(p,1)),a(k(N(1),k(v(p,1),N(1))),k(N(1),k(v(p,1),N(1))))))
#print c(k(k(k(k(a(v(p,4),n(v(s,4))),a(v(q,4),v(r,4))),a(v(q,4),v(r,4))),a(n(v(p,4)),n(v(q,4)))),a(n(v(r,4)),v(s,4))),k(a(v(p,4),a(a(k(a(v(q,4),N(4)),V(4)),N(4)),k(a(v(q,4),N(4)),N(4)))),a(n(v(p,4)),k(V(4),k(v(q,4),N(4))))))
#print k(k(k(k(a(v(q,2),v(r,2)),n(v(q,1))),n(v(q,1))),a(n(v(r,2)),v(s,2))),a(v(q,1),N(1)))

