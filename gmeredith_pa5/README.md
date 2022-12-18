Grace Meredith
CS457 PA4
Due 15 December 2022

Hi, welcome to my project. To start, let's see how to run the program. Then we'll review the algorithm put into the program.

### Running the Program

My program is written in **Python3**. Supplied is a test file **PA5_test.sql**.

To run the given program copy: `python3 pa5.py PA5_test.sql` in the terminal.

### Algorithm

10/10/22
The purpose of this assignment is to organize and access databases and tables. I represented databases as directories and tables as their files. To access the attributes, simply open the table file and read the data. To add attributes, open the table file and append the document with the given data. You can also create or delete databases and tables, and select attributes from the existing tables.

10/31/22
For the second iteration of this project, I added functionality to insert records into tables, select records, delete records and update records from a given table. To insert a record, simply check for the table's existence, then append the table file with the new record given. To delete a record, check the tables existence, check the where clause for conditionals and remove the appropriate record. Finally, to update a record, check the table's existence, check the where clause for conditionals and update the record's attribute based on the set clause of the command.

11/21/22
Funtionality was added to accomodate inner joins, left outer joins and values selected from conditions of two tables. Essentially, we check the given condition of the values from each table, if it's true we output the data from the table. If it's false, and not a left outer join, we don't output anything. Finally, if the condition returns false and it is a left outer join, then we print values only from the first table given.

12/15/22 p4
Add file locking feature so a table isn't written to at the same time by multiple processes. If the file is locked, the transaction is aborted and the table won't be written to. Otherwise, the process is free to modify the table.

12/15/22 p5
In selectFrom, the program checks which operated the user wants to perform, and which attribute to perform operations. It returns the desired calculation from the table's data. 