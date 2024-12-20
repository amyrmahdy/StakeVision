-- create database stakevision;

-- create schema tonusdt;

create table tonusdt.hourly (
	epoch bigint primary key,
	open  real not null,
	high real not null,
	low real not null,
	close real not null,
	volume real not null
);


--insert into stakevision.tonusdt.hourly values (1,2,3,4,5,6);


select "open", "close" from stakevision.tonusdt.hourly;

--delete from stakevision.tonusdt.hourly
--where epoch = 1 ;

insert into stakevision.tonusdt.hourly values (1733950800000, 6.3162, 6.3209, 6.2901, 6.3134, 48581.4471);
