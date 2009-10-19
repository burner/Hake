#!/usr/bin/python3
#hakefile maker
import os.path
import sys
import xml.dom
from collections import defaultdict
import haker

def main():
	for opt in sys.argv:
		if opt == "-h" or opt == "--help":
			help()
			return
		if opt == "-c" or opt == "--create":
			createHakeFileMenu()
			return
		if opt == "-e" or opt == "--example":
			printexample()
			return
	
	haker.hake()

def help():
	print("No arguments passed will start the hake prozess")
	print("-c or --create to start interactive Halefile creater")
	print("-e or --example to print an example Hakefile")
	print("-h or --help to print this help")

def printexample():
	print("<?xml version=\"1.0\" ?>\n<Hakeexampleprog>\n\t<Typedefaults>\n\t\t<Filetype_Default filetype=\".s\" options=\"yasm\"/>\n\t\t<Filetype_Default filetype=\".d\" options=\"ldc\"/>\n\t\t </Typedefaults>\n\t<Outdir OutDir=\"outdir\"/>\n\t<Exceptions File=\"indir2/kernel/runtime.d\" Options=\"-c -g -I. -nodefaultlib -noruntime\"/>\n\t<Inputdir Name=\"indir1\">\n\t\t<Compile_Options .d=\"-nodefaultlib -c\"/>\n\t\t<Compile_Options .s=\"-nodefaultlib -no-link\"/>\n\t</Inputdir>\t<Inputdir Name=\"indir2\">\n\t\t<Compile_Options .d=\"-c -I../kernel -nodefaultlib\"/>\n\t</Inputdir>\n\t<Linker Linker=\"ld\" LinkerOptions=\"-tkernel/linker.ld\"/>\n</Hakeexampleprog>")

def createHakeFileMenu():
	while True:
		print("\nHake Create Menu")
		print("\nExit without write:                 -1")
		print("Exit with wirte:                     0")
		print("Output dir:                          1")
		print("InputDirectory options:              2")
		print("File Exceptions:                     3")
		print("Program name:                        4")
		print("Default type Compiler and options:   5")
		print("Linker config                        6")
		selection = input("Make selection: ")

		if selection == "-1":
			break
		elif selection == "0":
			writeFile()
			break
		elif selection == "1":
			setOutDir()
		elif selection == "2":
			setDOptions()
		elif selection == "3":
			setFException()
		elif selection == "4":
			setProgramName()
		elif selection == "5":
			setDefaultOps()
		elif selection == "6":
			setLinker()

def setLinker():
	global linker
	global linkops
	print("\nSet Linker and options ")
	p = input("Input linker name: ")
	o = input("Input linker options: ")
	if(p == "" or o == ""):
		print("No linker or  no options set")
		return
	linker = p
	linkops = o

def setDefaultOps():
	print("\nDefault flags for filetype")
	t = input("Filetype :")
	f = input("Compiler and Flags for filetype: ")
	if t in typeDefault:
		if "Y" == input("Type has flags allready assigned, overright (Y/N): "):
			typeDefault[t] = f
	else:
		typeDefault[t] = f


def setProgramName():
	global proName
	print("\nSetting program name")
	proName = input("Name of the program: ")


def setOutDir():
	global outDir
	print("\nSet output directory")
	if outDir != "":
		print("Output directory allready set to ", outDir)
		if input("Want to overright (Y/N): ") == "Y":
			outDir = input("Output directory: ")
			return
		else:
			return
	outDir = input("Output Directory: ")

def setInDir():
	print("\nSet input directory")
	indir = input("Input Directory: ")
	if indir == "":
		print("Not a valid input Option")
		return
	i = inputDir.count(indir)
	if i == 0:
		inputDir.append(indir)
		print(inputDir)
	print(indir, "allready in input directory list")

def setDOptions():
	print("\nSet compile flags for filetype in directory")
	indir = input("Directory: ")
	fileType = input("To what filetype should the options be applied to: ")
	flags = input("Flags to apply to: ")
	if indir == "":
		print("No input made, not allowed")
		return
	if indir in inputDir:
		inputDir[indir].append( (fileType, flags) )
	else:
		if "Y" == input("Input directory not yet present, append it? (Y/N): "):
			inputDir[indir].append( (fileType, flags) )
		else:
			return

def setFException():
	print("\nSet special compile options for file")
	dir = input("Input directory of file: ")
	file = input("Filename: ")
	ops = input("Options for this file: ")
	if dir[-1] == '/':
		fileComOps[dir + file] = ops
	else:
		fileComOps[dir + '/' + file] = ops

def writeFile():
	print("\nWriting File\n")
	if os.path.exists("Hakefile"):
		n = input("Hakefile exists, want to overwrite (Y/N): ")
		if n == "Y":
			writeXml()
		else:
			return
	else:
		writeXml()

def writeXml():
	global proName
	global outDir
	impl = xml.dom.getDOMImplementation()
	doc = impl.createDocument(None, "Hakefile", None)

	#programname
	name = doc.createElement("Programname")
	name.setAttribute("Name", proName)

	doc.documentElement.appendChild(name)

	#default type ops
	tyd = doc.createElement("Typedefaults")
	for i in typeDefault.keys():
		tmp = doc.createElement("Filetype_Default")
		tmp.setAttribute("filetype", i)
		tmp.setAttribute("options", typeDefault[i])
		tyd.appendChild(tmp)

	doc.documentElement.appendChild(tyd)

	#outdir
	outDirEl = doc.createElement("Outdir")
	outDirEl.setAttribute("OutDir", outDir)
	doc.documentElement.appendChild(outDirEl)

	#exceptions
	for i in fileComOps.keys():
		tmp = doc.createElement("Exceptions")
		tmp.setAttribute("File", i)
		tmp.setAttribute("Options", fileComOps[i])
		doc.documentElement.appendChild(tmp)

	#inputDir
	for i in inputDir.keys():
		ind = doc.createElement("Inputdir")
		ind.setAttribute("Name", i)
		for j in inputDir[i]:
			tmp = doc.createElement("Compile_Options")
			tmp.setAttribute("Filetyp", str(j[0]))
			tmp.setAttribute("Options", str(j[1]))
			ind.appendChild(tmp)
		doc.documentElement.appendChild(ind)

	#linker
	link = doc.createElement("Linker")
	link.setAttribute("Linker", linker)
	link.setAttribute("LinkerOptions", linkops)
	doc.documentElement.appendChild(link)

	file = open("Hakefile", "w")
	doc.writexml(file, "\n", " ")
	file.close()

linker = ""
linkops = ""
outDir = ""
proName = ""
typeDefault = {}
inputDir = defaultdict(list)
dirComOps = {}
fileComOps = {}
main()
