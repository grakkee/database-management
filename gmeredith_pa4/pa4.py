#Author: Grace Meredith
#Class: CS 457
#Programming Assignment 4
#Due: 15 December 2022

#parse file if file given otherwise read commands from user input
#send commands to correct functions
#print success status of each command

#10/31/22
#added functionality to 
#delete items from tables, 
#select items from tables, 
#update items in tables and 
#insert items into tables

#11/21/22
#add functionality for
#innerjoins of two tables,
#left outer joins of two tables

#12/15/22
#add file locking feature
#to accomodate multiple processes
#wanting to write to the same table at the same time.

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

#read commands from test script
#parse lines and pass each one into sendCommands()
def readCommands(script):
	db = "none"
	i = 0
	p = 0
	with open(script,"r") as outfile:
		data = outfile.readlines()

	cmnds = [""] * len(data)
	for line in data:
		if "P1" in line:
			p = 1
			print("\nOn Process 1")
		if "P2" in line:
			p = 2
			print("\nOn Process 2")
		if "--" not in line:
			cmnds[i] += removeSymbol(line, '\n')
			if ";" in line:
				i +=1

	for line in cmnds:
		cmnd = line.split(" ")
		if "USE" in line:
			db = removeSymbol(cmnd[1], ';') #set current working database for any table commands
			print("Using database " + db)

		sendCommands(line, cmnd, p, db)

#reads command and determines which function to pass data into
def sendCommands(line, cmnd, p, db = "none"):
	if 'CREATE DATABASE' in line:
		name = removeSymbol(cmnd[2], ';')
		createDatabase(name)

	elif "DROP DATABASE" in line:
		name = removeSymbol(cmnd[2], ';')
		deleteDatabase(name)

	elif "create table" in line:
		name = removeSymbol(cmnd[2], ';')
		createTable(db, name)
		l = removeSymbol(line, ';')
		addColumns(db, name, l)

	elif "DROP TABLE" in line:
		name = removeSymbol(cmnd[2], ';')
		deleteTable(db, name)

	elif "select" in line:
		name = removeSymbol(cmnd[3], ';\n')
		selectFrom(db, name)

	elif "insert" in line:
		name = removeSymbol(cmnd[2], ';')
		l = removeSymbol(line, ';')
		insertInto(db, name, l)
		print("1 new record inserted.")

	elif "update" in line:
		name = removeSymbol(cmnd[1], '')
		l = removeSymbol(line, ';')
		num, changes = updateTable(db, name, l)
		commitChanges(db, name, changes, p, num)

	elif "begin transaction" in line:
		print("Transaction starts.")

	elif ".exit" in line:
		print("All done.")

	elif "--" not in line and "commit;" not in line and line != '\n' and "USE" not in line and line != "":
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
					lines[l] = lines[l].replace(",", "|")
					outfile.write(lines[l])
			outfile.write("|")

	else:
		print("!Failed to insert into table " + table + " because it does not exist.")

#check if table exists
#then instert new record in to table file
def insertInto(database, table, line):
	lines = line.split(" ")
	file = table + ".txt"
	path = os.path.join(database, file)
	if os.path.isfile(path):
		with open(path, "a") as outfile:
			outfile.write("\n")
			for l in range(3, len(lines)):
				lines[l] = removeSymbol(lines[l], "values")
				#lines[l] = removeSymbol(lines[l], " ")
				#lines[l] = removeSymbol(lines[l], "\t")
				lines[l] = removeSymbol(lines[l], "(") #clean up lines before writing it into the table
				lines[l] = removeSymbol(lines[l], ")")
				lines[l] = lines[l].replace(",", "|")
				outfile.write(lines[l])
			outfile.write("|")

	else:
		print("!Failed to alter table " + table + " because it does not exist.")

#check if table exists
#then update appropriate record line(s)
#with new col value
#return number of records modified
def updateTable(db, table, line):
	lines = line.split(" ")
	setType = lines[3]
	setVal = lines[5]
	whereType = lines[7]
	whereSym = lines[8]
	whereVal = lines[9]
	file = table + ".txt"
	path = os.path.join(db, file)
	count = 0
	wi=0
	si=0
	if os.path.isfile(path):
		outfile = open(path, "r")
		data = outfile.readlines()
		outfile.close()

		cols = data[0].split("|")
		newData = [""] * len(data)
		newData[0] = data[0]

		for c in cols:
			if whereType in c:
				wi = cols.index(c)
			if setType in c:
				si = cols.index(c)

		for d in range(1, len(data)):
			cmnd = data[d].split("|")
			if whereSym == ">" and float(cmnd[wi]) >= float(whereVal):
				newData[d] = data[d].replace(cmnd[si], setVal)
				count +=1

			elif whereSym == "<" and float(cmnd[wi]) <= float(whereVal):
				newData[d] = data[d].replace(cmnd[si], setVal)
				count +=1
				
			elif whereSym == "=" and cmnd[wi] == whereVal:
				newData[d] = data[d].replace(cmnd[si], setVal)
				count +=1

			elif whereSym == "!=" and cmnd[wi] != whereVal:
				newData[d] = data[d].replace(cmnd[si], setVal)
				count +=1
			else:
				newData[d] = data[d]
		return count, newData

	else:
		print("Failed to update table " + table + " because it does not exist.")
		return 0, 0


#check if the table exists
#then select the column attributes
#display them to the user
def selectFrom(database, table):
	file = removeSymbol(table, ";") + ".txt"
	path = os.path.join(database, file)
	if os.path.isfile(path):
		outfile = open(path, "r")
		print(outfile.read())
		outfile.close()
	else:
		print("!Failed to query table " + table + " because it does not exist.")

#trivial function to remove things like semicolons & parenthesis from string data
def removeSymbol(str, sym):
	return str.replace(sym, "")

def commitChanges(database, table, newData, p, num):
	file = table + ".txt"
	path = os.path.join(database, file)

	if p == 1:
		with open(path, "w") as f:
			for d in newData:
				f.write(d)
			if num > 1:
				print(str(num) + " records modified")
			else:
				print("1 record modified")

			print("Transaction committed.")

	else:
		print("Error table " + table + " is locked!")
		print("Transaction abort.")	

#check if there was a test file given
#then either pass it into readCommands()
#or enter user input mode in takeCommands()
#enter user input mode in takeCommands()
def main():
	#takeCommands()
	if len(sys.argv) > 2:
		readCommands(sys.argv[1])
		readCommands(sys.argv[2])
	else:
		print("Not enough arguments")

if __name__ == "__main__":
	main()