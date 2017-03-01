create user usr with password 'pwd';
--\set ON_ERROR_ROLLBACK
GRANT ALL ON pricing TO usr;
GRANT ALL ON portfolio TO usr;
GRANT ALL ON universe TO usr;


create database yah;
\connect yah

create schema yah;

\encoding UTF8
\set ON_ERROR_ROLLBACK on

-- drop table twitt.tweet;
create table pricing
(
	symbol varchar(10),
	tradeDate timestamp, -- both of those form the primary key
	open_ float,
	high_ float,
	low_ float,
	close_ float,
	adjClose float,
	volume float,
	primary key (symbol, tradeDate)
);

-- creating and dropping pkeys and indexes
ALTER TABLE pricing ADD PRIMARY KEY (symbol, tradeDate);
create index idx_date on pricing(tradeDate);
create index idx_symbol on pricing using hash (symbol);

ALTER TABLE pricing DROP CONSTRAINT pricing_pkey;
DROP INDEX idx_date;
DROP INDEX idx_symbol;

create table portfolio
(
	portfolio varchar(10),
	symbol varchar(10),
	quantity integer
);

ALTER TABLE portfolio ADD PRIMARY KEY (portfolio, symbol);

create table universe
(
	symbol varchar(10),
	name varchar(100)
);

ALTER TABLE universe ADD PRIMARY KEY (symbol);