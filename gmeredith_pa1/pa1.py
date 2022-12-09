#Author: Grace Meredith
#Class: CS 457
#Programming Assignment 1
#Due: 10 October 2022

#parse file if file given otherwise read commands from user input
#send commands to correct functions
#print success status of each command

import os
import sys

#check if the database already exists
#then create the database as a directory
def createDatabase(name):
	if os.path.isdir(name):
		print("!Failed to create database " + name + " because it already exists.")
	else:
		os.mkdir(name)
		print("Database " + name + " created.")

#check if the database exists
#then remove the database from the system
def deleteDatabase(name):
	try:
		os.rmdir(name)
		print("Database " + name + " deleted.")
	except OSError as e:
		print("!Failed to delete " + name + " because it does not exist.")

#check if the table exists
#then create the table as a file, child of its database directory
def createTable(database, name):
	newFile = name + ".txt"
	newPath = os.path.join(database, newFile)
	if os.path.isfile(newPath):
		print("!Failed to create table " + name + " because it already exists.")
	else:
		file1 = open(newPath, "w")
		file1.close()
		print("Table " + name + " created.")

#check if the table exists
#then remove the table from the system
def deleteTable(database, name):
	file = name + ".txt"
	path = os.path.join(database, file)
	try:
		os.remove(path)
		print("Table " + name + " deleted.")
	except OSError as e:
		print("!Failed to delete " + name + " because it does not exist.")

#check if the table exists
#then select the column attributes
#display them to the user
def selectFrom(database, table):
	file = table + ".txt"
	path = os.path.join(database, file)
	if os.path.isfile(path):
		outfile = open(path, "r")
		print(outfile.read())
		outfile.close()
	else:
		print("!Failed to query table " + table + " because it does not exist.")

#read commands from test script
#parse lines and pass each one into sendCommands()
def readCommands(script):
	db = "none"
	with open(script,"r") as outfile:
		data = outfile.readlines()

	for line in data:
		cmnds = line.split(" ")
		if "USE" in line:
			db = removeSymbol(cmnds[1], ';\n') #set current working database for any table commands
			print("Using database " + db)

		sendCommands(line, cmnds, db)

#read commands from user input until user chooses to exit
#pass each command into sendCommands()
def takeCommands():
	#no script was given, entering user input mode
	line = 'hello'
	db = "none"
	while line != '.EXIT':
		line = input()
		cmnds = line.split(" ")
		if "USE" in line:
			db = removeSymbol(cmnds[1], ';\n') #set current working database for any table commands
			print("Using database " + db)

		sendCommands(line, cmnds, db)

#reads command and determines which function to pass data into
def sendCommands(line, cmnd, db = "none"):
	if 'CREATE DATABASE' in line:
		name = removeSymbol(cmnd[2], ';\n')
		createDatabase(name)

	elif "DROP DATABASE" in line:
		name = removeSymbol(cmnd[2], ';\n')
		deleteDatabase(name)

	elif "CREATE TABLE" in line:
		name = removeSymbol(cmnd[2], ';\n')
		createTable(db, name)
		l = removeSymbol(line, ';\n')
		addColumns(db, name, l)

	elif "DROP TABLE" in line:
		name = removeSymbol(cmnd[2], ';\n')
		deleteTable(db, name)

	elif "SELECT" in line:
		name = removeSymbol(cmnd[3], ';\n')
		selectFrom(db, name)

	elif "ALTER" in line:
		name = removeSymbol(cmnd[2], ';\n')
		if "ADD" in line:
			l = removeSymbol(line, ';\n')
			addColumns(db, name, l)
		print("Table " + name + " modified.")

	elif ".EXIT" in line:
		print("All done.")

	elif "--" not in line and line != "\n" and "USE" not in line:
		print(line, "not a command")

#check if table exists
#then modify it by adding a new column attribute
def addColumns(database, table, line):
	lines = line.split(" ")
	file = table + ".txt"
	path = os.path.join(database, file)
	if os.path.isfile(path):
		with open(path, "a") as outfile:
			for l in range(3, len(lines)):
				if "ADD" not in lines[l]:
					lines[l] = removeSymbol(lines[l], "(") #clean up lines before writing it into the table
					lines[l] = removeSymbol(lines[l], ")")
					lines[l] = lines[l].replace(",", " |")
					outfile.write(lines[l] + " ")
			outfile.write(" | ")

	else:
		print("!Failed to alter table " + table + " because it does not exist.")

#trivial function to remove things like semicolons & parenthesis from string data
def removeSymbol(str, sym):
	return str.replace(sym, "")

#check if there was a test file given
#then either pass it into readCommands()
#or enter user input mode in takeCommands()
def main():
	if len(sys.argv) > 1:
		readCommands(sys.argv[1])
	else:
		takeCommands()

if __name__ == "__main__":
	main()