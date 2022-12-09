Grace Meredith
CS457 PA1
Due 10 October 2022

Hi, welcome to my project. To start, let's see how to run the program. Then we'll review the algorithm put into the program.

### Running the Program

My program is written in **Python3**. Supplied is a test file **PA1_test.sql**.

If you want to run the program with the test script, run:
`python3 pa1.py PA1_test.sql` in the shell. The program should run through the commands and close when complete.

if you want to run the program without the test script and input commands one at a time, run:
`python3 pa1.py` and you should be allowed to enter commands. The program will close once you input `.EXIT`.

*The output data may include a warning about checking for endlines, but removing them was necassary in the parsing process*

### Algorithm

The purpose of this assignment is to organize and access databases and tables. I represented databases as directories and tables as their files. To access the attributes, simply open the table file and read the data. To add attributes, open the table file and append the document with the given data. You can also create or delete databases and tables, and select attributes from the existing tables.