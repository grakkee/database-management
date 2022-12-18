-- On P1:
CREATE DATABASE CS457_PA4;
USE CS457_PA4;
create table Flights (seat int, status int);
insert into Flights values(22,0);
insert into Flights values(23,1);
begin transaction;
update Flights set status = 1 where seat = 22;
commit;
select * from Flights;