 create database stakevision;

 create schema tonusdt;

create table tonusdt.hourly (
	epoch int primary key,
	open  int not null,
	high int not null,
	low int not null,
	close int not null,
	volume int not null
);



insert into stakevision.tonusdt.hourly values (1,2,3,4,5,6);



select "open", "close" from stakevision.tonusdt.hourly;

delete from stakevision.tonusdt.hourly
where epoch = 1 ;
