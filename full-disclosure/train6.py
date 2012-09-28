'http://fastml.com/best-buy-mobile-contest-full-disclosure/'

import sys, csv, re
from prepare import prepare
from correct import *

def get_matches( names, query ):
	matches = [names[n] for n in names if query in n]
	
	if matches:
		name_matches = [n for n in names if query in n]
		print "matches: %s ---> %s\n" % ( query, name_matches )	
	
	return matches	

popular_skus = [9854804, 2107458, 2541184, 2670133, 2173065]

names_file = 'sku_name_prepared.tsv'
input_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]

###

n = open( names_file )
names_reader = csv.reader( n, delimiter = "\t" )

names = {}
for line in names_reader:
	sku = line[0]
	name = line[1]	# names should be prepared
	names[name] = sku
	
# for spelling correction
nwords = {}
for n in names:
	nwords[n] = 1
	
###

i = open( input_file )
reader = csv.reader( i )

t = open( test_file )

headers = reader.next()
mapping = {}

for line in reader:
	query = line[3]
	sku = line[1]
	# print "%s -> %s" % ( query, sku )
	
	query = prepare( query )
	
	try:
		mapping[query][sku] += 1
	except KeyError:
		try:
			mapping[query][sku] = 1
		except KeyError:
			mapping[query] = {}
			mapping[query][sku] = 1

queries = mapping.keys()
nqueries = {}
for n in queries:
	nqueries[n] = 1

#print mapping
#sys.exit( 0 )

reader = csv.reader( t )
headers = reader.next()

o = open( output_file, 'wb' )
writer = csv.writer( o, delimiter = " " )

n = 0	# all test cases
m = 0	# the ones we have mapping for
c = 0 	# found corrected query in mapping

s = 0	# name search
f = 0	# found in search
b = 0	# from benchmark


print "predicting..."

for line in reader:
	n += 1
	if n % 1000 == 0:
		print n
	
	
	skus = []
	query = line[2]
	query = prepare( query )
	
	if query in mapping:

		m += 1
		
		for sku in sorted( mapping[query], key=mapping[query].get, reverse = True ):
			skus.append( sku )
		#print skus

		skus = skus[0:5]
	
	# query spelling correction
	if len( skus ) < 5:
		if len( query ) < 6:
			corrected_queries = edits1( query )
		else:
			corrected_queries = correct( nqueries, query )
		
		corrected_found = [x for x in corrected_queries if x in mapping and x != query]
		
		if corrected_found:
			#print len( corrected_found )
			c += 1
		
			print "%s ---> %s\n" % ( query, corrected_found )

			skus_counts = {}
			for c_query in corrected_found:
				skus_counts.update( mapping[c_query] )

			additional_skus = sorted( skus_counts, key=skus_counts.get, reverse = True )

			skus.extend( additional_skus )
			skus = skus[0:5]
		
	# search in names
	if len( skus ) < 5:
	
		s += 1
		matches = get_matches( names, query )
		if matches:
		
			f += 1
			additional_skus = [x for x in matches if x not in skus]
			#print additional_skus
			skus.extend( additional_skus )
			skus = skus[0:5]
			
	if len( skus ) < 5:
		b += 1
		skus.extend( popular_skus )
		skus = skus[0:5]
		
	writer.writerow( skus )
		
print "Found mapping in %s / %s (%s)" % ( m, n, 1.0 * m / n )
print "Found corrected in %s / %s (%s)" % ( c, n, 1.0 * c / n )
print "Used search in %s / %s (%s)" % ( s, n, 1.0 * s / n )
print "Found search in %s / %s (%s)" % ( f, n, 1.0 * f / n )
print "Used benchmark in %s / %s (%s)" % ( b, n, 1.0 * b / n )
