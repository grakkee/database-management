#Author: Grace Meredith
#Class: CS 457
#Programming Assignment 2
#Due: 31 October 2022

#parse file if file given otherwise read commands from user input
#send commands to correct functions
#print success status of each command

#10/31/22
#added functionality to 
#delete items from tables, 
#select items from tables, 
#update items in tables and 
#insert items into tables

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
	with open(script,"r") as outfile:
		data = outfile.readlines()

	cmnds = [""] * len(data)
	for line in data:
		if "--" not in line:
			cmnds[i] += removeSymbol(line, '\n')
			if ";" in line:
				i +=1

	for line in cmnds:
		cmnd = line.split(" ")
		if "USE" in line:
			db = removeSymbol(cmnd[1], ';') #set current working database for any table commands
			print("Using database " + db)

		sendCommands(line, cmnd, db)

#read commands from user input until user chooses to exit
#pass each command into sendCommands()
def takeCommands():
	#no script was given, entering user input mode
	line = 'hello'
	db = "none"
	while line != '.exit':
		line = input()
		cmnds = line.split(" ")
		if "USE" in line:
			db = removeSymbol(cmnds[1], ';') #set current working database for any table commands
			print("Using database " + db)

		sendCommands(line, cmnds, db)

#reads command and determines which function to pass data into
def sendCommands(line, cmnd, db = "none"):
	if 'CREATE DATABASE' in line:
		name = removeSymbol(cmnd[2], ';')
		createDatabase(name)

	elif "DROP DATABASE" in line:
		name = removeSymbol(cmnd[2], ';')
		deleteDatabase(name)

	elif "CREATE TABLE" in line:
		name = removeSymbol(cmnd[2], ';')
		createTable(db, name)
		l = removeSymbol(line, ';')
		addColumns(db, name, l)

	elif "DROP TABLE" in line:
		name = removeSymbol(cmnd[2], ';')
		deleteTable(db, name)

	elif "select" in line:
		name = "none"
		if "*" in cmnd[1]:
			name = removeSymbol(cmnd[3], ';')
		else:
			name = removeSymbol(cmnd[cmnd.index("from") + 1], ';')
		l = removeSymbol(line, ';')
		selectFrom(db, name, l)

	elif "ALTER" in line:
		name = removeSymbol(cmnd[2], ';')
		if "ADD" in line:
			l = removeSymbol(line, ';')
			addColumns(db, name, l)
		print("Table " + name + " modified.")

	elif "insert" in line:
		name = removeSymbol(cmnd[2], ';')
		l = removeSymbol(line, ';')
		insertInto(db, name, l)
		print("1 new record inserted.")

	elif "update" in line:
		name = removeSymbol(cmnd[1], '')
		l = removeSymbol(line, ';')
		num = updateTable(db, name, l)
		if num > 1:
			print(str(num) + " records modified")
		else:
			print("1 record modified")

	elif "delete" in line:
		name = removeSymbol(cmnd[2], '\n')
		l = removeSymbol(line, ';')
		num = deleteFrom(db, name, l)
		if num > 1:
			print(str(num) + " records deleted")
		else:
			print("1 record deleted")

	elif ".exit" in line:
		print("All done.")

	elif "--" not in line and line != '\n' and "USE" not in line and line != "":
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
				lines[l] = removeSymbol(lines[l], "\t")
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
		with open(path, "w") as newfile:
			for d in newData:
				newfile.write(d)

	else:
		print("Failed to update table " + table + " because it does not exist.")

	return count

#Check if table exists
#then delete approriate records
#by overwriting the table file 
#with 'good data'
#return number of records deleted
def deleteFrom(db, table, line):
	lines = line.split(" ")
	sym = lines[5]
	where = lines[4]
	val = lines[6]
	file = table + ".txt"
	path = os.path.join(db, file)
	i=0
	if os.path.isfile(path):
		outfile = open(path, "r")
		data = outfile.readlines()
		outfile.close()

		cols = data[0].split("|")
		goodData = [""] * len(data)
		goodData[0] = data[0]
		for c in cols:
			if where in c:
				i = cols.index(c)

		for d in range(1, len(data)):
			cmnd = data[d].split("|")
			if sym == ">" and float(cmnd[i]) <= float(val):
				goodData[d] = data[d]

			elif sym == "<" and float(cmnd[i]) >= float(val):
				goodData[d] = data[d]
				
			elif sym == "=" and cmnd[i] != val:
				goodData[d] = data[d]

			elif sym == "!=" and cmnd[i] == val:
				goodData[d] = data[d]

		with open(path, "w") as newfile:
			for d in goodData:
				newfile.write(d)
	else:
		print("Failed to delete from table " + table + " because it does not exist.")

	return len(data) - len(goodData)

#check if the table exists
#then select the column attributes
#display them to the user
def selectFrom(database, table, line):
	file = table + ".txt"
	path = os.path.join(database, file)
	lines = line.split(" ")

	if os.path.isfile(path):
		outfile = open(path, "r")
		data = outfile.readlines()
		outfile.close()

		infile = open(path, "r")
		fullData = infile.read()
		infile.close()

		if lines[1] == "*":
			print(fullData)
		else:
			f = lines.index("from")
			sym = lines[f+ 4]
			where = lines[f + 3]
			val = lines[f + 5]
			showVals = [""] * f
			i=0
			cols = data[0].split("|")
			goodData = [""] * len(data)
			goodData[0] = data[0]
			for c in cols:
				if where in c:
					i = cols.index(c)

			for d in range(1, len(data)):
				cmnd = data[d].split("|")
				if sym == ">" and float(cmnd[i]) > float(val):
					goodData[d] = data[d]

				elif sym == "<" and float(cmnd[i]) < float(val):
					goodData[d] = data[d]
				
				elif sym == "=" and cmnd[i] == val:
					goodData[d] = data[d]

				elif sym == "!=" and cmnd[i] != val:
					goodData[d] = data[d]
			with open(path, "w") as newfile:
				for d in goodData:
					print(d)	
	else:
		print("!Failed to query table " + table + " because it does not exist.")

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