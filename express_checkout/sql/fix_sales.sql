alter table sale_order add column journal_id integer;
update sale_order set journal_id = 1;
alter table sale_order alter column journal_id set not null;
