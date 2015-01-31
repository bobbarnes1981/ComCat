import custom
import tkinter
import tkinter.messagebox

from models import RelatedPerson

# todo: error handling, abstraction for database and models, show/hide volume info

"""This class is the main UI window"""
class Ui(tkinter.Tk):

	def __init__(self, parent, manager):
		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.manager = manager
		self.title('ComCat - Comic Catalogue')
		self.grid()
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		#self.geometry('640x480')
		
		# menu bar
		
		menubar = tkinter.Menu(self, tearoff=0)
		self.config(menu=menubar)
		
		menu_file = tkinter.Menu(menubar, tearoff=0)
		menu_file.add_command(label='Exit', command=self.menu_file_exit)
		
		menu_comic = tkinter.Menu(menubar, tearoff=0)
		menu_comic.add_command(label='Add Issue', command=self.menu_comic_addissue)
		
		menubar.add_cascade(label='File', menu=menu_file)
		menubar.add_cascade(label='Comic', menu=menu_comic)
		
		# tree
		
		self.tree_comics = custom.Treeview(self, show='tree', selectmode='browse')
		sbx = tkinter.ttk.Scrollbar(self, orient='horizontal', command=self.tree_comics.xview)
		sby = tkinter.ttk.Scrollbar(self, orient='vertical', command=self.tree_comics.yview)
		self.tree_comics.configure(xscroll=sbx.set, yscroll=sby.set)
		
		self.tree_comics.grid(row=0, column=0, sticky='NSEW')
		sbx.grid(row=1, column=0, sticky='EW')
		sby.grid(row=0, column=1, sticky='NS')

		self.tree_comics.bind('<<TreeviewSelect>>', self.tree_comics_select)
		self.tree_comics.bind('<Button-3>', self.tree_comics_button3)

		# context menu
		
		self.menu_context = tkinter.Menu(self, tearoff=0)
		
		# update issues
		
		self.update_issues();

	def menu_file_exit(self):
		self.quit()
		
	def menu_comic_addissue(self):
		popup = Ui_Add_Issue(self, self.manager)
		popup.bind('<Destroy>', self.ui_add_issue_destroy)
	
	def tree_comics_clear(self):
		self.publisher_open = {}
		self.comic_open = {}
		self.volume_open = {}
		# remove all children and build dictionary of open items
		for child_p in self.tree_comics.get_children():
			self.publisher_open[self.tree_comics.get_item(child_p).pid] = self.tree_comics.item(child_p)['open']
			for child_c in self.tree_comics.get_children(child_p):
				self.comic_open[self.tree_comics.get_item(child_c).cid] = self.tree_comics.item(child_c)['open']
				for child_v in self.tree_comics.get_children(child_c):
					self.volume_open[self.tree_comics.get_item(child_v).vid] = self.tree_comics.item(child_v)['open']
					self.tree_comics.delete(child_v)
				self.tree_comics.delete(child_c)
			self.tree_comics.delete(child_p)
	
	def tree_comics_populate(self):
		# create tree and open items where necessary
		self.publisher_dict = {}
		self.comic_dict = {}
		self.volume_dict = {}
		for issue in self.manager.get_issues():
			if issue.pid not in self.publisher_dict.keys():
				self.publisher_dict[issue.pid] = self.tree_comics.insert('', 'end', issue, text=issue.pname, tags=('publisher'), open=self.publisher_open[issue.pid] if issue.pid in self.publisher_open.keys() else 0)
			if issue.cid not in self.comic_dict.keys():
				self.comic_dict[issue.cid] = self.tree_comics.insert(self.publisher_dict[issue.pid], 'end', issue, text=issue.cname, tags=('comic'), open=self.comic_open[issue.cid] if issue.cid in self.comic_open.keys() else 0)
			if issue.vid not in self.volume_dict.keys():
				self.volume_dict[issue.vid] = self.tree_comics.insert(self.comic_dict[issue.cid], 'end', issue, text=issue.vname, tags=('volume'), open=self.volume_open[issue.vid] if issue.vid in self.volume_open.keys() else 0)
			self.tree_comics.insert(self.volume_dict[issue.vid], 'end', issue, text='{0} #{1} ({2})'.format(issue.cname, issue.number, issue.variant if issue.variant else 'Standard Variant'), tags=('issue'))
			# TODO: add related people
	
	def update_issues(self):
		self.tree_comics_clear()
		self.tree_comics_populate()
		
	def menu_tree_del_issue(self):
		if tkinter.messagebox.askquestion('Delete', 'Are You Sure?', icon='warning') == 'yes':
			self.manager.del_issue(self.tree_comics.selected_item().id)
			self.update_issues()
	
	def menu_tree_mod_issue(self):
		popup = Ui_Add_Issue(self, self.manager, self.tree_comics.selected_item().id)
		popup.bind('<Destroy>', self.ui_add_issue_destroy)

	def ui_add_issue_destroy(self, event):
		if isinstance(event.widget, Ui_Add_Issue):
			self.update_issues()
	
	def menu_tree_del_comic(self):
		if tkinter.messagebox.askquestion('Delete', 'Are You Sure?', icon='warning') == 'yes':
			self.manager.del_comic(self.tree_comicx.selected_item().cid)
			self.update_issues()
	
	def menu_tree_mod_comic(self):
		popup = Ui_Add_Comic(self, self.manager, self.tree_comics.selected_item().pid, self.tree_comics.selected_item().cid)
		popup.bind('<Destroy>', self.ui_add_comic_destroy)
	
	def ui_add_comic_destroy(self, event):
		if isinstance(event.widget, Ui_Add_Comic):
			self.update_issues()
		
	def ui_add_comic_destroy(self, event):
		self.update_issues()
		
	def menu_tree_del_volume(self):
		if tkinter.messagebox.askquestion('Delete', 'Are You Sure?', icon='warning') == 'yes':
			self.manager.del_volume(self.tree_comics.selected_item().vid)
			self.update_issues()
	
	def menu_tree_mod_volume(self):
		popup = Ui_Add_Volume(self, self.manager, self.tree_comics.selected_item().cid, self.tree_comics.selected_item().vid)
		popup.bind('<Destroy>', self.ui_add_volume_destroy)
	
	def ui_add_volume_destroy(self, event):
		if isinstance(event.widget, Ui_Add_Volume):
			self.update_issues()
	
	def tree_comics_select(self, event):
		self.update_context_menu()
		
	def update_context_menu(self):
		id = self.tree_comics.focus()
		self.menu_context = tkinter.Menu(self, tearoff=0)
		if self.tree_comics.tag_has('volume', id):
			self.menu_context.add_command(label='delete', command=self.menu_tree_del_volume)
			self.menu_context.add_command(label='edit', command=self.menu_tree_mod_volume)
		if self.tree_comics.tag_has('comic', id):
			self.menu_context.add_command(label='delete', command=self.menu_tree_del_comic)
			self.menu_context.add_command(label='edit', command=self.menu_tree_mod_comic)
		if self.tree_comics.tag_has('issue', id):
			self.menu_context.add_command(label='delete', command=self.menu_tree_del_issue)
			self.menu_context.add_command(label='edit', command=self.menu_tree_mod_issue)
			self.menu_context.add_command(label='copy', command=self.menu_tree_cop_issue)
		
	def tree_comics_button3(self, event):
		self.menu_context.post(event.x_root, event.y_root)

"""This class is a popup for handling adding a comic issue"""
class Ui_Add_Issue(tkinter.Toplevel):

	def __init__(self, parent, manager, issue_id = None):
		tkinter.Toplevel.__init__(self, parent)
		self.parent = parent
		self.manager = manager
		self.issue_id = issue_id
		self.title('ComCat - Add Issue')
		self.grid()
		#self.geometry('430x240')
		self.grab_set()
		
		# publisher option
		
		self.label_publisher = tkinter.Label(self, text='Publisher')
		self.label_publisher.grid(column=0, row=0, sticky='NW')
		
		self.publisher = tkinter.StringVar(self)
		self.option_publisher = custom.Combobox(self, textvariable=self.publisher, state='readonly')
		self.option_publisher.grid(column=1, row=0, sticky='NW')
		
		self.button_addpublisher = tkinter.Button(self, text='+', command=self.button_addpublisher_click)
		self.button_addpublisher.grid(column=2, row=0, sticky='NW')
		
		self.button_delpublisher = tkinter.Button(self, text='-', command=self.button_delpublisher_click)
		self.button_delpublisher.grid(column=3, row=0, sticky='NW')

		# comic option
		
		self.label_comic = tkinter.Label(self, text='Comic')
		self.label_comic.grid(column=0, row=1, sticky='NW')
		
		self.comic = tkinter.StringVar(self)
		self.option_comic = custom.Combobox(self, textvariable=self.comic, state='readonly')
		self.option_comic.grid(column=1, row=1, sticky='NW')
		
		self.button_addcomic = tkinter.Button(self, text='+', command=self.button_addcomic_click)
		self.button_addcomic.grid(column=2, row=1, sticky='NW')
		
		self.button_delcomic = tkinter.Button(self, text='-', command=self.button_delcomic_click)
		self.button_delcomic.grid(column=3, row=1, sticky='NW')

		# volume option
		
		self.label_volume = tkinter.Label(self, text='Volume')
		self.label_volume.grid(column=0, row=2, sticky='NW')
		
		self.volume = tkinter.StringVar(self)
		self.option_volume = custom.Combobox(self, textvariable=self.volume, state='readonly')
		self.option_volume.grid(column=1, row=2, sticky='NW')
		
		self.button_addvolume = tkinter.Button(self, text='+', command=self.button_addvolume_click)
		self.button_addvolume.grid(column=2, row=2, sticky='NW')
		
		self.button_delvolume = tkinter.Button(self, text='-', command=self.button_delvolume_click)
		self.button_delvolume.grid(column=3, row=2, sticky='NW')
		
		# issue entry
		
		self.label_issue = tkinter.Label(self, text='Issue')
		self.label_issue.grid(column=0, row=3, sticky='NW')
		
		self.entry_issue = tkinter.Entry(self)
		self.entry_issue.grid(column=1, row=3, sticky='NW')
		
		# variant entry
		
		self.label_variant = tkinter.Label(self, text='Variant')
		self.label_variant.grid(column=0, row=4, sticky='NW')
		
		self.entry_variant = tkinter.Entry(self)
		self.entry_variant.grid(column=1, row=4, sticky='NW')
		
		# related people
		
		self.personcollection_people = PersonCollectionFrame(self, self.manager)
		self.personcollection_people.grid(column=1, row=5, sticky='NW')
		
		# ok
		
		self.button_ok = tkinter.Button(self, text='OK', command=self.button_ok_click)
		self.button_ok.grid(column=1, row=6, sticky='NW')
		
		# cancel
		
		self.button_cancel = tkinter.Button(self, text='Cancel', command=self.button_cancel_click)
		self.button_cancel.grid(column=2, row=6, sticky='NW')
		
		# update the options
		
		self.update_publishers()
		
		# bind to the option events
		
		self.option_publisher.bind('<<ComboboxSelected>>', self.option_publisher_selected)
		self.option_comic.bind('<<ComboboxSelected>>', self.option_comic_selected)
		self.option_volume.bind('<<ComboboxSelected>>', self.option_volume_selected)
		
		# if editing load the data
		
		if self.issue_id:
			issue = self.manager.get_issue(self.issue_id)
			self.option_publisher.set(issue.pname)
			self.update_comics()
			self.option_comic.set(issue.cname)
			self.update_volumes()
			self.option_volume.set(issue.vname)
			self.entry_issue.insert(0, issue.number)
			self.entry_variant.insert(0, issue.variant)
			self.personcollection_people.set_relationships(self.manager.get_related_people(self.issue_id))
	
	# buttons
	
	def button_ok_click(self):
		if self.issue_id == None:
			self.manager.add_issue(self.entry_issue.get(), self.entry_variant.get(), self.option_volume.selected_item().id)
		else:
			self.manager.mod_issue(self.issue_id, self.entry_issue.get(), self.entry_variant.get(), self.option_volume.selected_item().id)
		self.manager.del_related_people(self.issue_id)
		self.manager.add_related_people(self.issue_id, self.personcollection_people.get_relationships()) 
		self.destroy()
		
	def button_cancel_click(self):
		self.destroy()
	
	# publisher option
	
	def option_publisher_selected(self, event):
		self.update_comics()
	
	def button_addpublisher_click(self):
		popup = Ui_Add_Publisher(self, self.manager)
		popup.bind('<Destroy>', self.ui_add_publisher_destroy)
	
	def button_delpublisher_click(self):
		if tkinter.messagebox.askquestion('Delete', 'Are You Sure?', icon='warning') == 'yes':
			self.manager.del_publisher(self.option_publisher.selected_item().id)
			self.update_publishers()
	
	def ui_add_publisher_destroy(self, event):
		self.update_publishers()
	
	def update_publishers(self):
		self.option_publisher.set_data_source(self.manager.get_publishers(), 'id')

	# comic option
	
	def option_comic_selected(self, event):
		self.update_volumes()
		
	def button_addcomic_click(self):
		popup = Ui_Add_Comic(self, self.manager, self.option_publisher.selected_item().id)
		popup.bind('<Destroy>', self.ui_add_comic_destroy)
	
	def button_delcomic_click(self):
		if tkinter.messagebox.askquestion('Delete', 'Are You Sure?', icon='warning') == 'yes':
			self.manager.del_comic(self.option_comic.selected_item().id)
			self.update_comics()
	
	def ui_add_comic_destroy(self, event):
		self.update_comics()
	
	def update_comics(self):
		self.option_comic.set_data_source(self.manager.get_comics(self.option_publisher.selected_item().id), 'id')

	# volume option

	def option_volume_selected(self, event):
		pass
	
	def button_addvolume_click(self):
		popup = Ui_Add_Volume(self, self.manager, self.option_comic.selected_item().id)
		popup.bind('<Destroy>', self.ui_add_volume_destroy)
	
	def button_delvolume_click(self):
		if tkinter.messagebox.askquestion('Delete', 'Are You Sure?', icon='warning') == 'yes':
			self.manager.del_volume(self.option_volume.selected_item().id)
			self.update_volumes()
	
	def ui_add_volume_destroy(self, event):
		self.update_volumes()
	
	def update_volumes(self):
		self.option_volume.set_data_source(self.manager.get_volumes(self.option_comic.selected_item().id), 'id')

"""This class is a popup for handling adding a comic publisher"""
class Ui_Add_Publisher(tkinter.Toplevel):

	def __init__(self, parent, manager, publisher_id = None):
		tkinter.Toplevel.__init__(self, parent)
		self.parent = parent
		self.manager = manager
		self.publisher_id = publisher_id
		self.title('ComCat - Publisher')
		self.grid()
		#self.geometry('430x240')
		self.grab_set()
		
		# name entry
		
		self.label_name = tkinter.Label(self, text='Name')
		self.label_name.grid(column=0, row=0, sticky='NW')
		
		self.entry_name = tkinter.Entry(self)
		self.entry_name.grid(column=1, row=0, sticky='NW')

		# buttons
		
		self.button_ok = tkinter.Button(self, text='OK', command=self.button_ok_click)
		self.button_ok.grid(column=2, row=0, sticky='NW')
		
		self.button_cancel = tkinter.Button(self, text='Cancel', command=self.button_cancel_click)
		self.button_cancel.grid(column=3, row=0, sticky='NW')
		
		# if editing load the data
		
		if self.publisher_id:
			publisher = self.manager.get_publisher(self.publisher_id)
			self.entry_name.insert(0, publisher.name)
	
	def button_ok_click(self):
		if self.publisher_id == None:
			self.manager.add_publisher(self.entry_name.get())
		else:
			self.manager.mod_publisher(self.pubilsher_id, self.entry_name.get())
		self.destroy()
		
	def button_cancel_click(self):
		self.destroy()

"""This class is a popup for handling adding a comic series"""
class Ui_Add_Comic(tkinter.Toplevel):

	def __init__(self, parent, manager, publisher_id, comic_id = None):
		tkinter.Toplevel.__init__(self, parent)
		self.parent = parent
		self.manager = manager
		self.publisher_id = publisher_id
		self.comic_id = comic_id
		self.title('ComCat - Add Comic')
		self.grid()
		#self.geometry('430x240')
		self.grab_set()
		
		# name entry
		
		self.label_name = tkinter.Label(self, text='Name')
		self.label_name.grid(column=0, row=0, sticky='NW')
		
		self.entry_name = tkinter.Entry(self)
		self.entry_name.grid(column=1, row=0, sticky='NW')

		# buttons
		
		self.button_ok = tkinter.Button(self, text='OK', command=self.button_ok_click)
		self.button_ok.grid(column=2, row=0, sticky='NW')
		
		self.button_cancel = tkinter.Button(self, text='Cancel', command=self.button_cancel_click)
		self.button_cancel.grid(column=3, row=0, sticky='NW')
		
		# if editing load the data
		
		if self.comic_id:
			comic = self.manager.get_comic(self.comic_id)
			self.entry_name.insert(0, comic.name)
	
	def button_ok_click(self):
		if self.comic_id == None:
			self.manager.add_comic(self.entry_name.get(), self.publisher_id)
		else:
			self.manager.mod_comic(self.comic_id, self.entry_name.get(), self.publisher_id)
		self.destroy()
		
	def button_cancel_click(self):
		self.destroy()

"""This class is a popup for handling adding a volume"""
class Ui_Add_Volume(tkinter.Toplevel):

	def __init__(self, parent, manager, comic_id, volume_id = None):
		tkinter.Toplevel.__init__(self, parent)
		self.parent = parent
		self.manager = manager
		self.comic_id = comic_id
		self.volume_id = volume_id
		self.title('ComCat - Add Volume')
		self.grid()
		#self.geometry('430x240')
		self.grab_set()
		
		# name entry
		
		self.label_name = tkinter.Label(self, text='Name')
		self.label_name.grid(column=0, row=0, sticky='NW')
		
		self.entry_name = tkinter.Entry(self)
		self.entry_name.grid(column=1, row=0, sticky='NW')

		# buttons
		
		self.button_ok = tkinter.Button(self, text='OK', command=self.button_ok_click)
		self.button_ok.grid(column=2, row=0, sticky='NW')
		
		self.button_cancel = tkinter.Button(self, text='Cancel', command=self.button_cancel_click)
		self.button_cancel.grid(column=3, row=0, sticky='NW')
		
		# if editing load the data
		
		if self.volume_id:
			volume = self.manager.get_volume(self.volume_id)
			self.entry_name.insert(0, volume.name)
	
	def button_ok_click(self):
		if self.volume_id == None:
			self.manager.add_volume(self.entry_name.get(), self.comic_id)
		else:
			self.manager.mod_volume(self.volume_id, self.entry_name.get(), self.comic_id)
		self.destroy()
		
	def button_cancel_click(self):
		self.destroy()

"""This class is a popup for handling adding a related person"""
class Ui_Add_Person(tkinter.Toplevel):

	def __init__(self, parent, manager):
		tkinter.Toplevel.__init__(self, parent)
		self.parent = parent
		self.manager = manager
		self.title('ComCat - Add Person')
		self.grid()
		#self.geometry('430x240')
		self.grab_set()
		
		# name entry
		
		self.label_name = tkinter.Label(self, text='Name')
		self.label_name.grid(column=0, row=0, sticky='NW')
		
		self.entry_name = tkinter.Entry(self)
		self.entry_name.grid(column=1, row=0, sticky='NW')

		# buttons
		
		self.button_ok = tkinter.Button(self, text='OK', command=self.button_ok_click)
		self.button_ok.grid(column=2, row=0, sticky='NW')
		
		self.button_cancel = tkinter.Button(self, text='Cancel', command=self.button_cancel_click)
		self.button_cancel.grid(column=3, row=0, sticky='NW')
	
	def button_ok_click(self):
		self.manager.add_person(self.entry_name.get())
		self.destroy()
		
	def button_cancel_click(self):
		self.destroy()

"""This class is a popup for handling adding a person relationship"""
class Ui_Add_Relationship(tkinter.Toplevel):

	def __init__(self, parent, manager):
		tkinter.Toplevel.__init__(self, parent)
		self.parent = parent
		self.manager = manager
		self.title('ComCat - Add Relationship')
		self.grid()
		#self.geometry('430x240')
		self.grab_set()
		
		# name entry
		
		self.label_name = tkinter.Label(self, text='Name')
		self.label_name.grid(column=0, row=0, sticky='NW')
		
		self.entry_name = tkinter.Entry(self)
		self.entry_name.grid(column=1, row=0, sticky='NW')

		# buttons
		
		self.button_ok = tkinter.Button(self, text='OK', command=self.button_ok_click)
		self.button_ok.grid(column=2, row=0, sticky='NW')
		
		self.button_cancel = tkinter.Button(self, text='Cancel', command=self.button_cancel_click)
		self.button_cancel.grid(column=3, row=0, sticky='NW')
	
	def button_ok_click(self):
		self.manager.add_relationship(self.entry_name.get())
		self.destroy()
		
	def button_cancel_click(self):
		self.destroy()

"""This class is a frame that contains a list of related people"""
class PersonCollectionFrame(tkinter.Frame):

	def __init__(self, parent, manager):
		tkinter.Frame.__init__(self, parent)
		self.manager = manager
		self.personframes = []
		
		# add person button
		
		self.button_add = tkinter.Button(self, text='Add Person', command=self.button_add_click)
		self.button_add.grid(column=0, row=0, sticky='NW')
	
	def button_add_click(self):
		self.add_relationship(None)
	
	def button_remove_click(self, id):
		self.personframes[id].grid_forget()
		delete(self.personframes[id])

	# relationships
	
	def add_relationship(self, relationship):
		personframe = PersonFrame(self, self.manager)
		self.personframes.append(personframe)
		id = self.personframes.index(personframe)
		if relationship:
			personframe.set_relationship(relationship)
		personframe.grid(column=0, row=id+1)
	
	def get_relationships(self):
		relationships = []
		for personframe in self.personframes:
			relationships.append(personframe.get_relationship())
		return relationships

	def set_relationships(self, relationships):
		for relationship in relationships:
			self.add_relationship(relationship)

"""This class is a frame that contains a related person"""
class PersonFrame(tkinter.Frame):

	def __init__(self, parent, manager):
		tkinter.Frame.__init__(self, parent)
		self.manager = manager
		
		# title
		
		self.label_title = tkinter.Label(self, text='Related Person')
		self.label_title.grid(column=0, row=0, sticky='NW')
		
		# person option
		
		self.label_person = tkinter.Label(self, text='Person')
		self.label_person.grid(column=0, row=1, sticky='NW')
		
		self.person = tkinter.StringVar(self)
		self.option_person = custom.Combobox(self, textvariable=self.person, state='readonly')
		self.option_person.grid(column=1, row=1, sticky='NW')
		
		self.button_addperson = tkinter.Button(self, text='+', command=self.button_addperson_click)
		self.button_addperson.grid(column=2, row=1, sticky='NW')
		
		self.button_delperson = tkinter.Button(self, text='-', command=self.button_delperson_click)
		self.button_delperson.grid(column=3, row=1, sticky='NW')

		# relationship option
		
		self.label_relationship = tkinter.Label(self, text='Relationship')
		self.label_relationship.grid(column=0, row=2, sticky='NW')
		
		self.volume = tkinter.StringVar(self)
		self.option_relationship = custom.Combobox(self, textvariable=self.volume, state='readonly')
		self.option_relationship.grid(column=1, row=2, sticky='NW')
		
		self.button_addrelationship = tkinter.Button(self, text='+', command=self.button_addrelationship_click)
		self.button_addrelationship.grid(column=2, row=2, sticky='NW')
		
		self.button_delrelationship = tkinter.Button(self, text='-', command=self.button_delrelationship_click)
		self.button_delrelationship.grid(column=3, row=2, sticky='NW')
		
		# remove person button
		
		button_remove = tkinter.Button(self, text='Remove', command=self.button_remove_click)
		button_remove.grid(column=2, row=3)
		
		# update options
		
		self.update_people()
		self.update_relationships()
	
	# person option
	
	def button_addperson_click(self):
		popup = Ui_Add_Person(self, self.manager)
		popup.bind('<Destroy>', self.ui_add_person_destroy)
	
	def button_delperson_click(self):
		pass
	
	def ui_add_person_destroy(self, event):
		self.update_people()
	
	def update_people(self):
		self.option_person.set_data_source(self.manager.get_people(), 'id')
	
	# relationship option
	
	def button_addrelationship_click(self):
		popup = Ui_Add_Relationship(self, self.manager)
		popup.bind('<Destroy>', self.ui_add_relationship_destroy)
	
	def button_delrelationship_click(self):
		pass
	
	def ui_add_relationship_destroy(self, event):
		self.update_relationships()
	
	def update_relationships(self):
		self.option_relationship.set_data_source(self.manager.get_relationships(), 'id')
	
	# remove person button
	
	def button_remove_click(self):
		self.grid_forget()

	# relationship
	
	def get_relationship(self):
		person = self.option_person.selected_item()
		relationship = self.option_relationship.selected_item()
		return RelatedPerson({'pid':person.id,'pname':person.name,'rid':relationship.id,'rname':relationship.name})
	
	def set_relationship(self, relationship):
		self.option_person.select_key(relationship.pid)
		self.option_relationship.select_key(relationship.rid)
