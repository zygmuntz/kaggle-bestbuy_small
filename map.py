'''
Compute MAP score for given test and prediction files
Usage: map.py test_with_answers.csv predictions.txt

Test file is supposed to have headers in first line
Predictions file is supposed to NOT have headers
'''

import sys, csv

test_file = sys.argv[1]
predictions_file = sys.argv[2]

t = open( test_file )
p = open( predictions_file )

t_reader = csv.reader( t )
headers = t_reader.next()

p_reader = csv.reader( p, delimiter = " " )

n = 0
m = 0
aps = []

for line in t_reader:
	n += 1
	predictions = p_reader.next()
	sku = line[1]
	if sku not in predictions:
		aps.append( 0 )
		continue
		
	m += 1
	i = predictions.index( sku )
	ap = 1.0 / ( i + 1 )
	#print ap
	aps.append( ap )

map_score = sum( aps ) / n
	
print predictions_file
print "Found clicked SKU in %s / %s cases (%s)" % ( m, n, 1.0 * m / n )
print "MAP: %s" % ( map_score )
