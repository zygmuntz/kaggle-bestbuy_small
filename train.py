'http://fastml.com/best-buy-mobile-contest/'

import sys, csv, re

def prepare( query ):
	query = re.sub( r'[\W]', '', query )
	query = query.lower()
	return query

popular_skus = [9854804, 2107458, 2541184, 2670133, 2173065]

input_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]

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

		
#print mapping
#sys.exit( 0 )

reader = csv.reader( t )
headers = reader.next()

o = open( output_file, 'wb' )
writer = csv.writer( o, delimiter = " " )

n = 0	# all test cases
m = 0	# the ones we have mapping for

for line in reader:
	n += 1
	query = line[2]
	query = prepare( query )
	
	if query in mapping:

		m += 1
		skus = []
		
		for sku in sorted( mapping[query], key=mapping[query].get, reverse = True ):
			skus.append( sku )
		#print skus

		'''
		if len( mapping[query] ) > 1:
			print "mapping:"
			print mapping[query]
			print "skus:"
			print skus
		'''
		
		skus.extend( popular_skus )
		skus = skus[0:5]
	else:
		skus = popular_skus
		
	writer.writerow( skus )
		
print "Used mapping in %s / %s (%s)" % ( m, n, 1.0 * m / n )