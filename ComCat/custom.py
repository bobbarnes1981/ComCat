import tkinter.ttk

"""A custom combobox that provides key and item methods"""
class Combobox(tkinter.ttk.Combobox):

	def __init__(self, parent, *args, **kwargs):
		tkinter.ttk.Combobox.__init__(self, parent, *args, **kwargs)
		self.__data_source = None
	
	"""set the data source and use the key to re-select the previously selected item if required"""
	def set_data_source(self, data_source, key): # TODO: add val parameter?
		if not isinstance(data_source, list):
			raise Exception('data source is not list')
		# get key of last selected item (or None)
		last_key = self.selected_key() if self.__data_source else None
		self.__key = key
		self.__data_source = data_source
		self['values'] = tuple(data_source)
		# set selected item/key (or None)
		if last_key:
			self.select_key(last_key)
		else:
			self.set('')
	
	def selected_key(self):
		item = self.selected_item()
		return getattr(item, self.__key)
	
	def select_key(self, key):
		for i in range(0, len(self.__data_source)):
			if getattr(self.__data_source[i], self.__key) == key:
				self.set(str(self.__data_source[i]))
				break
		else:
			self.set('')
	
	def selected_item(self):
		index = self.current()
		return self.__data_source[index]
	
	def select_item(self, item):
		key = self.__data_source.index(item)
		self.select_key(key)

"""A custom treeview that provides item methods"""
class Treeview(tkinter.ttk.Treeview):

	def __init__(self, parent, *args, **kwargs):
		tkinter.ttk.Treeview.__init__(self, parent, *args, **kwargs)
		self.__data_dict = {}

	def insert(self, parent, position, item, *args, **kwargs):
		index = tkinter.ttk.Treeview.insert(self, parent, position, *args, **kwargs)
		self.__data_dict[index] = item
		return index
	
	def delete(self, index):
		tkinter.ttk.Treeview.delete(self, index)
		del(self.__data_dict[index])
	
	def selected_item(self):
		return self.__data_dict[self.focus()]
	
	def get_item(self, index):
		return self.__data_dict[index]
	