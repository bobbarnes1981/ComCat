from manager import Manager
from ui import Ui

if __name__ == '__main__':
	Ui(None, Manager('comcat.db')).mainloop()