/*  account account
    descripción de las cuentas contables
*/
select * from account_account;

/*  account_invoice | facturas ------------------------------------------------------- */
/*  Cambiar los números de factura del PV 0006 al PV 0005 renumerando
    según está en el campo referencia. Sin tocar las que tienen Z: en referencia.

    Journal Document Class id
          VEN06     VEN02     VEN05
    FA    24        43        34
    FB    26        45        36
    NDA   25        44        35

    Account Journal
        RVE04 VEN04 VEN06 RVE06 VEN05 RVE05 VEN02 RVE02
    id    5     4     9     10    18    19    20    21
*/

select
  number
, 'VEN05/2016/'||substring(reference,10,4) as number_new
, ai.journal_id
, (select id from account_journal where code = 'VEN05') as journal_id_new
, journal_document_class_id
, ( select ajadc.id
    from account_journal_afip_document_class ajadc
      join afip_document_class adc
      on adc.id = ajadc.afip_document_class_id
    where journal_id = (select id from account_journal
                        where code = 'VEN05')
                        and doc_code_prefix like 'ND-A%'
  ) as journal_document_class_id_new
, internal_number
, 'VEN05/2016/'||substring(reference,10,4) as internal_number_new
, afip_document_number
, reference as afip_document_number_new
, ai.move_name
, 'VEN05/2016/'||substring(reference,10,4) as move_name_new
, adc.doc_code_prefix
, reference
, move_id
, ai.type
from account_invoice ai
  join account_journal_afip_document_class ajadc
    on ai.journal_document_class_id = ajadc.id
  join afip_document_class adc
      on ajadc.afip_document_class_id = adc.id
where
      ai.type like 'out_i%'
  and reference LIKE '0005%'
  and ai.journal_id = (select id from account_journal where code = 'VEN06')
  and doc_code_prefix like 'ND-A%';

/* para facturas z */
select
  number
, 'VEN02/2016/'||LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text,4,'0') as number_new
, ai.journal_id
, (select id from account_journal where code = 'VEN02') as journal_id_new
, journal_document_class_id
, ( select ajadc.id
    from account_journal_afip_document_class ajadc
      join afip_document_class adc
      on adc.id = ajadc.afip_document_class_id
    where journal_id = (select id from account_journal
                        where code = 'VEN02')
                        and doc_code_prefix like 'FA-B%'
  ) as journal_document_class_id_new
, internal_number
, 'VEN02/2016/'||LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text,4,'0') as internal_number_new
, afip_document_number
, '0002-' || LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text, 8, '0') as afip_document_number_new
, ai.move_name
, 'VEN02/2016/'||LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text,4,'0') as move_name_new
, adc.doc_code_prefix
, reference
, move_id
, ai.type
from account_invoice ai
  join account_journal_afip_document_class ajadc
    on ai.journal_document_class_id = ajadc.id
  join afip_document_class adc
      on ajadc.afip_document_class_id = adc.id
where
      reference LIKE 'Z%'
  and ai.type like 'out_i%'
  and ai.journal_id = (select id from account_journal where code = 'VEN06')
  and doc_code_prefix like 'FA-B%'
order by reference;


/*  account_move movimiento contable está relacionada con la factura -------------------*/
select
    journal_id
,    ((select 18 where journal_id = 9) UNION (select 19 where journal_id = 10)) as new_journal_id
,   document_number
,    substring(document_number,1,5) || ref as new_document_number
,   afip_document_number
,   ref as new_afip_document_number
,   ref
from
  account_move
where
  ref like '0005%';

select
    journal_id
,    ((select 18 where journal_id = 9) UNION (select 19 where journal_id = 10)) as new_journal_id
,   document_number
,    substring(document_number,1,5) || '0002-'||LPAD((cast(substring(ref, 3 ,4) as int)-1516)::text,8,'0') as new_document_number
,   afip_document_number
,   '0002-'||LPAD((cast(substring(ref, 3 ,4) as int)-1516)::text,8,'0') as new_afip_document_number
,   ref
from
  account_move
where
  ref LIKE 'Z%'
order by ref

/*  account_move_line
    linea de movimiento contable
*/

select
    journal_id
  ,  (select journal_id from account_move where id=move_id) as new_journal_id
  , document_number
  , (select document_number from account_move where id=move_id) as new_document_number
  , ref
from account_move_line
where move_id in (select move_id from account_move where ref LIKE 'z%' or ref LIKE '0005%')

select
    aml.journal_id
  ,  (select journal_id from account_move where id=move_id) as new_journal_id
  , aml.ref
  , aml.document_number
  , (select document_number from account_move where id=move_id) as new_document_number
from
  account_move_line aml
join account_move am
ON am.id = aml.move_id;


/*-----------------------------------------------------------------------------------*/
/* Comienza el patch ----------------------------------------------------------------*/
/*-----------------------------------------------------------------------------------*/

/* account_invoice ------------
  campos a corregir
    number
    journal_id
    journal_document_class_id
    afip_document_number
    internal_number
    move_name
*/

/*  Cambiar los números de factura del PV 0006 al PV 0005 renumerando
    según está en el campo referencia. Sin tocar las que tienen Z: en referencia.
*/

/* Facturas A*/
update account_invoice
SET
  number = 'VEN05/2016/'||substring(reference,10,4),
  journal_id = (select id from account_journal where code = 'VEN05'),
  journal_document_class_id = 34,
  internal_number = 'VEN05/2016/'||substring(reference,10,4),
  afip_document_number = reference,
  move_name = 'VEN05/2016/'||substring(reference,10,4)
where
      type like 'out_i%'
  and reference LIKE '0005%'
  and journal_id = (select id from account_journal where code = 'VEN06')
  and journal_document_class_id = 24;

/* Facturas B*/
update account_invoice
SET
  number = 'VEN05/2016/'||substring(reference,10,4),
  journal_id = (select id from account_journal where code = 'VEN05'),
  journal_document_class_id = 36,
  internal_number = 'VEN05/2016/'||substring(reference,10,4),
  afip_document_number = reference,
  move_name = 'VEN05/2016/'||substring(reference,10,4)
where
      type like 'out_i%'
  and reference LIKE '0005%'
  and journal_id = (select id from account_journal where code = 'VEN06')
  and journal_document_class_id = 26;

/* Nota de débito A*/
update account_invoice
SET
  number = 'VEN05/2016/'||substring(reference,10,4),
  journal_id = (select id from account_journal where code = 'VEN05'),
  journal_document_class_id = 35,
  internal_number = 'VEN05/2016/'||substring(reference,10,4),
  afip_document_number = reference,
  move_name = 'VEN05/2016/'||substring(reference,10,4)
where
      type like 'out_i%'
  and reference LIKE '0005%'
  and journal_id = (select id from account_journal where code = 'VEN06')
  and journal_document_class_id = 25;

/*  Cambiar los numeros de factura del PV 0006 al PV 0002 de las facturas Z:
    renumerando desde el número 1.

    account invoice
    campos a corregir

    number
    journal_id
    journal_document_class_id
    afip_document_number
    move_name
*/

UPDATE account_invoice
SET
  number = 'VEN02/2016/'||LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text,4,'0'),
  journal_id = (select id from account_journal where code = 'VEN02'),
  journal_document_class_id = 45,
  internal_number = 'VEN02/2016/'||LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text,4,'0'),
  afip_document_number = '0002-' || LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text, 8, '0'),
  move_name = 'VEN02/2016/'||LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text,4,'0')
WHERE
      reference LIKE 'Z%'
  and type like 'out_i%'
  and journal_id = 9;


/*  account_move ------------
    campos a corregir
    journal_id
    document_number
    afip_document_number
*/

update account_move
set
  journal_id = ((select 18 where journal_id = 9) UNION (select 19 where journal_id = 10)),
  document_number = substring(document_number,1,5) || ref,
  afip_document_number = ref
where ref like '0005-%';

update account_move
set
  journal_id = 20,
	document_number = substring(document_number,1,5) || '0002-'||LPAD((cast(substring(ref, 3 ,4) as int)-1516)::text,8,'0'),
  afip_document_number = '0002-'||LPAD((cast(substring(ref, 3 ,4) as int)-1516)::text,8,'0')
where
ref like 'Z%';

/* account_move_line ------------
  campos a corregir
  journal_id
  Document_number
  se copian del padre, no deberían estar en esta tabla, está denormalizado!!!
*/

update account_move_line
set
    journal_id = (select journal_id from account_move where id=move_id),
    document_number = (select document_number from account_move where id=move_id)
where
  move_id in (select move_id from account_move where ref LIKE 'z%' or ref LIKE '0005%');



hasta aca llegue ---
/* account_journal_period ------------*/

update account_journal_period
set name = 'VEN05:05/2016'
where name like 'VEN06%';

update account_journal_period
set name = 'RVE05:05/2016'
where name like 'RVE06%';

/* account_journal ------------*/

update account_journal
set
	code = 'VEN05',
	name = 'Ventas (0005 - Manual)'
where code = 'VEN06';

update account_journal
set
	code = 'RVE05',
	name = 'Reembolso Ventas (0005 - Manual)'
where code = 'RVE06';

/*
**********************************************************************************
ajustar nros de secuencia
***********************************************************************************/

select reference,afip_document_number,type from account_invoice
where afip_document_number like '0002-%'
and type like 'out%'
order by afip_document_number desc;


/* Verificaciones */
/* verificar la denormalización de journal_id*/
select sum(am.journal_id- aml.journal_id)
from account_move am
join account_move_line aml
on am.id = aml.move_id
