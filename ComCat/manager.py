from database import Database
from models import Publisher, Comic, Volume, Issue, Relationship, Person, RelatedPerson

# TODO: use models as inputs to methods, along with model/db abstraction

class Manager(object):

	def __init__(self, database):
		self.database = Database(database)

	# publishers
	
	def get_publishers(self):
		rows = self.database.get_publishers()
		result = []
		for row in rows:
			result.append(Publisher(row))
		return result

	def add_publisher(self, name):
		self.database.add_publisher(name)

	def del_publisher(self, publisher_id):
		self.database.del_publisher(publisher_id)

	# comics
	
	def get_comics(self, publisher_id):
		rows = self.database.get_comics(publisher_id)
		result = []
		for row in rows:
			result.append(Comic(row))
		return result

	def add_comic(self, name, publisher_id):
		self.database.add_comic(name, publisher_id)

	def del_comic(self, comic_id):
		self.database.del_comic(comic_id)
	
	def mod_comic(self, comic_id, name, publisher_id):
		self.database.mod_comic(comic_id, name, publisher_id)
	
	# volumes
	
	def get_volumes(self, comic_id):
		rows = self.database.get_volumes(comic_id)
		result = []
		for row in rows:
			result.append(Volume(row))
		return result

	def get_volume(self, volume_id):
		return Volume(self.database.get_volume(volume_id))
	
	def add_volume(self, name, comic_id):
		self.database.add_volume(name, comic_id)

	def del_volume(self, volume_id):
		self.database.del_volume(volume_id)
	
	def mod_volume(self, volume_id, name, comic_id):
		self.database.mod_volume(volume_id, name, comic_id)
	
	# issues

	def get_issues(self):
		rows = self.database.get_issues()
		result = []
		for row in rows:
			result.append(Issue(row))
		return result
	
	def get_issue(self, issue_id):
		return Issue(self.database.get_issue(issue_id))

	def add_issue(self, number, variant, volume_id):
		self.database.add_issue(number, variant, volume_id)

	def del_issue(self, issue_id):
		self.database.del_issue(issue_id)
	
	def mod_issue(self, issue_id, number, variant, volume_id):
		self.database.mod_issue(issue_id, number, variant, volume_id)
	
	# people
	
	def get_people(self):
		rows = self.database.get_people()
		result = []
		for row in rows:
			result.append(Person(row))
		return result
	
	def add_person(self, name):
		self.database.add_person(name)
	
	def mod_person(self, person_id, name):
		self.database.mod_person(person_id, name)
	
	# relationships
	
	def get_relationships(self):
		rows = self.database.get_relationships()
		result = []
		for row in rows:
			result.append(Relationship(row))
		return result
	
	def add_relationship(self, name):
		self.database.add_relationship(name)

	# related people
	
	def get_related_people(self, issue_id):
		rows = self.database.get_related_people(issue_id)
		result = []
		for row in rows:
			result.append(RelatedPerson(row))
		return result
	
	def add_related_people(self, issue_id, related_people):
		for related_person in related_people:
			self.database.add_related_person(issue_id, related_person.pid, related_person.rid)

	def del_related_people(self, issue_id):
		self.database.del_related_people(issue_id)
