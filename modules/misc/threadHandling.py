import threading
threadLock = threading.Lock()

class a_thread (threading.Thread) :
	def __init__(self):
		threading.Thread.__init__(self)
		self.__fn = None
		self.__args = None
		self.__kwargs = None
	def run(self) :
		self.__fn(*self.__args,**self.__kwargs)
	def create_task(self,fn,*args,**kwargs) :
		self.__fn = fn
		self.__args = args
		self.__kwargs = kwargs
	def run_task(self,fn,*args,**kwargs) : # RUN A TASK IN ONE GO
		self.create_task(fn,*args,**kwargs)
		self.start()

# MODULE USAGE EXAMPLE
if __name__ == "__main__" :
	from time import sleep
	from datetime import datetime
	
	col_list=[(21,'W'),(13,'W'),(1,'R'),(13,'Y'),(13,'G'),(5,'W')]
	
	def prt(loc,col) :
		print("col=%s to loc=%s at %s" % (col,loc,datetime.now()))
		sleep(5)
		print("col=%s to loc=%s at %s" % ('1',loc,datetime.now()))
	
	print("start at %s" % datetime.now())
	for c in col_list :
		x = a_thread()
		x.run_task(prt,c[0],c[1])
		del(x)
	print("end at %s" % datetime.now())
