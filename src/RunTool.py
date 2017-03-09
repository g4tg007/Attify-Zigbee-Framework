#This file will give access to a thread i suppose,  which will take toolnames, parameters from the main UI and run it,
#and send the output back to the UI, here goes

from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL
import subprocess


class RunTool(QtCore.QThread):
	def __init__(self,tool,parameters):
		super(RunTool,self).__init__()
		self.tool=tool
		self.parameters=parameters


	def __del__(self):
		self.wait()

	def close(self):
		self.terminate()

	def run(self):
		if(self.tool == "zbid"):
			#proc = subprocess.Popen(...)
			try:
				output=subprocess.check_output(["python","killerbee/tools/zbid"])
				output=output.replace("           Dev Product String       Serial Number","")
				device_list=output.strip()
				device_list=device_list.split(" ")
				device_list = filter(None, device_list)
				string="   "
				for x in device_list:
					string=string+x+(" "*27)
			except Exception as e:
				print "[*] Exception : "+str(e)
			self.emit(SIGNAL('update_zbid(QString)'),QtCore.QString(str(string)))
			self.close()

		if(self.tool == "zbdump"):
			try:
				params=self.parameters.split(" ")
				list=["python","killerbee/tools/zbdump"]+params
				print(list)
				output=subprocess.check_output(list)
			except Exception as e:
				output="Error"
				print "[*] Exception : "+str(e)
			self.emit(SIGNAL('zbdump_complete(QString)'),QtCore.QString(str(output)))
			self.close()

