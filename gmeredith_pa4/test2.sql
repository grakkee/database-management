-- On P2:
USE CS457_PA4;
select * from Flights;
begin transaction;
update Flights set status = 1 where seat = 22;
commit;
select * from Flights;
select * from Flights;