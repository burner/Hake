import xml.dom.minidom
import subprocess
import os.path
from collections import defaultdict

def hake():
	if os.path.exists("Hakefile"):
		parseHakeFile()
		checkForUpdatesAndHake()
	else:
		print("No Hakefile present")
		return
	
	if os.path.exists(".hake"):
		parseHakeInfo()

def parseHakeInfo():
	return

def checkForUpdatesAndHake():
	notPresent = checkForUpdates()

	if notPresent:
		hakeAll()

def hakeAll():
	impl = xml.dom.getDOMImplementation()
	doc = impl.createDocument(None, "hake", None)
	file = doc.createElement("Files")
	doc.documentElement.appendChild(file)
	for i in indirs.keys():
		files = []
		for j in indirs[i]: 
			call = "find " + "./" + i + " -name \*" + j[0]
			f = subprocess.Popen(call, shell=True, stdout=subprocess.PIPE,)
			tmp = str(f.communicate()[0])
			tmp = tmp[2:]
			tmp = tmp.split("\\n")
			for u in tmp:
				files.append(u)
		
		del files[-1]

		for k in files:
			print(k)
			dumpMeIntoFile = doc.createElement("File")
			dumpMeIntoFile.setAttribute("File", k)
			dumpMeIntoFile.setAttribute("LastFileCompile", str(int(os.path.getctime(k))))
			file.appendChild(dumpMeIntoFile)

#	print(doc.toprettyxml())
	toWrite = open(".hake", "w")
	doc.writexml(toWrite, "\n", " ")
	toWrite.close()


def checkForUpdates():
	if os.path.exists(".haked"):
		parseHaked()
	else:
		return True;

def parseHaked():
	haked = open(".haked")
	dom = xml.dom.minidom.parse(haked)
	haked.close()

def parseHakeFile():
	hakefile = open("Hakefile", "r")
	dom = xml.dom.minidom.parse(hakefile)
	hakefile.close()
	global name
	name = dom.getElementsByTagName("Programname")[0].getAttribute("Name")
	
	#compiler
	setCompilerFiletypeDefaults(dom.getElementsByTagName("Typedefaults")[0])

	#oudirs
	setOutdir(dom.getElementsByTagName("Outdir"))

	#indirs	
	setIndirs(dom.getElementsByTagName("Inputdir"))

	#exceptions
	setExceptFiles(dom.getElementsByTagName("Exceptions"))

	#linker
	setLinker(dom.getElementsByTagName("Linker"))

def setLinker(link):
	global linker, linkOps
	linker = link[0].getAttribute("Linker")
	linkOps = link[0].getAttribute("LinkerOptions")

def setExceptFiles(ex):
	global excepFiles
	for i in ex:
		excepFiles[i.getAttribute("File")] = i.getAttribute("Options")

def setOutdir(outdirtmp):
	global outdir
	outdir = outdirtmp[0].getAttribute("OutDir")
	return

def setCompilerFiletypeDefaults(types):
	for de in types.getElementsByTagName("Filetype_Default"):
		compiler[de.getAttribute("filetype")] = de.getAttribute("options")
	return

def setIndirs(dir):
	global indirs
	for i in dir:
		for j in i.getElementsByTagName("Compile_Options"):
			indirs[i.getAttribute("Name")].append((j.getAttribute("Filetyp"), j.getAttribute("Options")))

#program name
name = ""

#outdir
outdir = ""

#file exceptions
excepFiles = {}

#linker command in outdir
linker = ""
linkOps = ""

#compiler command dict for indirs
compiler = {}

#input directory optionsa
indirs = defaultdict(list) 
