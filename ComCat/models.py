
class Publisher(object):

	def __init__(self, row):
		self.id = row['id']
		self.name = row['name']
	
	def __str__(self):
		return self.name
		
class Comic(object):

	def __init__(self, row):
		self.id = row['id']
		self.name = row['name']
		self.publisher_id = row['publisher_id']
	
	def __str__(self):
		return self.name
		
class Volume(object):

	def __init__(self, row):
		self.id = row['id']
		self.name = row['name']
		self.comic_id = row['comic_id']
	
	def __str__(self):
		return self.name

class Issue(object):

	def __init__(self, row):
		self.id = row['id']
		self.number = row['number']
		self.variant = row['variant']
		self.volume_id = row['volume_id']
		
		self.pid = row['pid']
		self.pname = row['pname']
		self.cid = row['cid']
		self.cname = row['cname']
		self.vid = row['vid']
		self.vname = row['vname']
	
	def __str__(self):
		return self.number

class Person(object):

	def __init__(self, row):
		self.id = row['id']
		self.name = row['name']
	
	def __str__(self):
		return self.name

class Relationship(object):

	def __init__(self, row):
		self.id = row['id']
		self.name = row['name']
	
	def __str__(self):
		return self.name

class RelatedPerson(object):

	def __init__(self, row):
		#self.issue_id = row['issue_id']
		self.pid = row['pid']
		self.pname = row['pname']
		self.rid = row['rid']
		self.rname = row['rname']
