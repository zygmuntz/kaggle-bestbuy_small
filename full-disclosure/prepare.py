import re

def prepare( query ):
	query = re.sub( r'[\W]', '', query )
	query = query.lower()
	return query