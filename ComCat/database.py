import sqlite3

class Database(object):

	def __init__(self, database):
		self.database = database
		
		c = self.cursor()
		c.execute('CREATE TABLE IF NOT EXISTS publishers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);')
		c.execute('CREATE TABLE IF NOT EXISTS comics (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, publisher_id INTEGER NOT NULL CONSTRAINT publisher REFERENCES publishers (id) ON DELETE CASCADE);')
		c.execute('CREATE TABLE IF NOT EXISTS volumes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, comic_id INTEGER NOT NULL CONSTRAINT comic REFERENCES comics (id) ON DELETE CASCADE);')
		c.execute('CREATE TABLE IF NOT EXISTS issues (id INTEGER PRIMARY KEY AUTOINCREMENT, number INTEGER NOT NULL, variant TEXT NOT NULL, volume_id INTEGER NOT NULL CONSTRAINT volume REFERENCES volumes (id) ON DELETE CASCADE);')
		c.execute('CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);')
		c.execute('CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);')
		c.execute('CREATE TABLE IF NOT EXISTS issues_people (issue_id INTEGER NOT NULL CONSTRAINT issue REFERENCES issues (id), relationship_id INTEGER NOT NULL CONSTRAINT relationship REFERENCES relationships (id), person_id INTEGER NOT NULL CONSTRAINT person REFERENCES people (id));')
		self.commit()
	
	def cursor(self):
		self.connection = sqlite3.connect(self.database)
		self.connection.row_factory = sqlite3.Row
		return self.connection.cursor()
		
	def commit(self):
		self.connection.commit()
		self.connection.close()
	
	# publishers
	
	def get_publishers(self):
		c = self.cursor()
		c.execute('SELECT * FROM publishers ORDER BY name;')
		return c.fetchall()
	
	def get_publisher(self, publisher_id):
		c = self.cursor()
		c.execute('SELECT * FROM publishers WHERE id=?;', (publisher_id,))
		return c.fetchone()
	
	def add_publisher(self, name):
		c = self.cursor()
		c.execute('INSERT INTO publishers (name) VALUES (?);', (name,))
		self.commit()
	
	def del_publisher(self, publisher_id):
		c = self.cursor()
		c.execute('DELETE FROM publishers WHERE id=?;', (publisher_id,))
		self.commit()
	
	def mod_publisher(self, publisher_id, name):
		c = self.cursor()
		c.execute('UPDATE publishers SET name=? WHERE publisher_id=?;', (name, publisher_id))
		self.commit()
	
	# comics
	
	def get_comics(self, publisher_id):
		c = self.cursor()
		c.execute('SELECT * FROM comics WHERE publisher_id=? ORDER BY name;', (publisher_id,))
		return c.fetchall()
	
	def get_comic(self, comic_id):
		c = self.cursor()
		c.execute('SELECT * FROM comics WHERE id=?;', (comic_id,))
		return c.fetchone()
	
	def add_comic(self, name, publisher_id):
		c = self.cursor()
		c.execute('INSERT INTO comics (name, publisher_id) VALUES (?, ?);', (name, publisher_id))
		self.commit()

	def del_comic(self, comic_id):
		c = self.cursor()
		c.execute('DELETE FROM comics WHERE id=?;', (comic_id,))
		self.commit()
	
	def mod_comic(self, comic_id, name, publisher_id):
		c = self.cursor()
		c.execute('UPDATE comics SET name=?, publisher_id=? WHERE comic_id=?', (name, publisher_id, comic_id))
		self.commit()
	
	# volumes
	
	def get_volumes(self, comic_id):
		c = self.cursor()
		c.execute('SELECT * FROM volumes WHERE comic_id=? ORDER BY name;', (comic_id,))
		return c.fetchall()
	
	def get_volume(self, volume_id):
		c = self.cursor()
		c.execute('SELECT * FROM volumes WHERE id=?', (volume_id,))
		return c.fetchone()
	
	def add_volume(self, name, comic_id):
		c = self.cursor()
		c.execute('INSERT INTO volumes (name, comic_id) VALUES (?, ?)', (name, comic_id))
		self.commit()

	def del_volume(self, volume_id):
		c = self.cursor()
		c.execute('DELETE FROM volumes WHERE id=?;', (volume_id,))
		self.commit()
	
	def mod_volume(self, volume_id, name, comic_id):
		c = self.cursor()
		c.execute('UPDATE volumes SET name=?, comic_id=? WHERE id=?', (name, comic_id, volume_id))
		self.commit()
	
	# issues
	
	def get_issues(self):
		c = self.cursor()
		c.execute('SELECT p.id AS pid, p.name AS pname, c.id AS cid, c.name AS cname, v.id AS vid, v.name AS vname, i.id, i.number, i.variant, i.volume_id FROM issues AS i JOIN volumes AS v ON i.volume_id=v.id JOIN comics AS c ON v.comic_id=c.id JOIN publishers AS p ON c.publisher_id=p.id ORDER BY p.name, c.name, v.name, i.number, i.variant;')
		return c.fetchall()
	
	def get_issue(self, issue_id):
		c = self.cursor()
		c.execute('SELECT p.id AS pid, p.name AS pname, c.id AS cid, c.name AS cname, v.id AS vid, v.name AS vname, i.id, i.number, i.variant, i.volume_id FROM issues AS i JOIN volumes AS v ON i.volume_id=v.id JOIN comics AS c ON v.comic_id=c.id JOIN publishers AS p ON c.publisher_id=p.id WHERE i.id=? ORDER BY p.name, c.name, v.name, i.number, i.variant;', (issue_id,))
		return c.fetchone()
	
	def add_issue(self, number, variant, volume_id):
		c = self.cursor()
		c.execute('INSERT INTO issues (number, variant, volume_id) VALUES (?, ?, ?);', (number, variant, volume_id))
		self.commit()
	
	def del_issue(self, issue_id):
		c = self.cursor()
		c.execute('DELETE FROM issues WHERE id=?;', (issue_id,))
		self.commit()
	
	def mod_issue(self, issue_id, number, variant, volume_id):
		c = self.cursor()
		c.execute('UPDATE issues SET number=?, variant=?, volume_id=? WHERE id=?;', (number, variant, volume_id, issue_id))
		self.commit()

	# people
	
	def get_people(self):
		c = self.cursor()
		c.execute('SELECT * FROM people ORDER BY name;')
		return c.fetchall()
	
	def add_person(self, name):
		c = self.cursor()
		c.execute('INSERT INTO people (name) VALUES (?)', (name,))
		self.commit()
		
	# relationships
	
	def get_relationships(self):
		c = self.cursor()
		c.execute('SELECT * FROM relationships ORDER BY name;')
		return c.fetchall()
	
	def add_relationship(self, name):
		c = self.cursor()
		c.execute('INSERT INTO relationships (name) VALUES (?)', (name,))
		self.commit()
	
	# related people
	
	def get_related_people(self, issue_id):
		c = self.cursor()
		c.execute('SELECT i.issue_id, p.id AS pid, p.name AS pname, r.id AS rid, r.name AS rname FROM issues_people AS i JOIN people AS p ON i.person_id=p.id JOIN relationships AS r ON i.relationship_id=r.id WHERE i.issue_id=?;', (issue_id,)) # TODO: order
		return c.fetchall()
	
	def add_related_person(self, issue_id, person_id, relationship_id):
		c = self.cursor()
		c.execute('INSERT INTO issues_people (issue_id, person_id, relationship_id) VALUES (?, ?, ?);', (issue_id, person_id, relationship_id))
		self.commit()
		
	def del_related_people(self, issue_id):
		c = self.cursor()
		c.execute('DELETE FROM issues_people WHERE issue_id=?', (issue_id,))
		self.commit()
