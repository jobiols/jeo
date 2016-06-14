/*  account account
    descripción de las cuentas contables
*/

/*  account_invoice | facturas ------------------------------------------------------- */
/*  Cambiar los números de factura del PV 0006 al PV 0005 renumerando
    según está en el campo referencia. Sin tocar las que tienen Z: en referencia.

    Journal Document Class id
          VEN06     VEN02     VEN05
    FA    24        43        34
    FB    26        45        36
    NDA   25        44        35
    NDB    -
    NCA    30       49        40
    NCB    31       50        41

    Account Journal
        RVE04 VEN04 VEN06 RVE06 VEN05 RVE05 VEN02 RVE02
    id    5     4     9     10    18    19    20    21
*/

/* para seleccionar facturas */
select
  number,
  'VEN05/2016/' || substring(number, 12, 4)          AS number_new
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
, internal_number,
  'VEN05/2016/' || substring(internal_number, 12, 4) AS internal_number_new
, afip_document_number
, reference as afip_document_number_new
, ai.move_name,
  'VEN05/2016/' || substring(number, 12, 4)          AS move_name_new
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


/* para seleccionar notas de crédito */
SELECT
  number,
  'VEN05/2016/' || substring(reference, 10, 4) AS number_new,
  ai.journal_id,
  (SELECT id
   FROM account_journal
   WHERE code = 'VEN05')                       AS journal_id_new,
  journal_document_class_id,
  (SELECT ajadc.id
   FROM account_journal_afip_document_class ajadc
     JOIN afip_document_class adc
       ON adc.id = ajadc.afip_document_class_id
   WHERE journal_id = (SELECT id
                       FROM account_journal
                       WHERE code = 'VEN05')
         AND doc_code_prefix LIKE 'ND-A%'
  )                                            AS journal_document_class_id_new,
  internal_number,
  'VEN05/2016/' || substring(reference, 10, 4) AS internal_number_new,
  afip_document_number,
  reference                                    AS afip_document_number_new,
  ai.move_name,
  'VEN05/2016/' || substring(reference, 10, 4) AS move_name_new,
  adc.doc_code_prefix,
  reference,
  move_id,
  ai.type
FROM account_invoice ai
  JOIN account_journal_afip_document_class ajadc
    ON ai.journal_document_class_id = ajadc.id
  JOIN afip_document_class adc
    ON ajadc.afip_document_class_id = adc.id
WHERE
  ai.type LIKE 'out_r%'
  AND reference LIKE '0005%'
  AND ai.journal_id = (SELECT id
                       FROM account_journal
                       WHERE code = 'RVE06')
  AND doc_code_prefix LIKE 'NC-A%';


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
ORDER BY ref;

/*  account_move_line
    linea de movimiento contable
*/

SELECT
  ai.reference,
  am.ref
FROM
  account_invoice ai
  INNER JOIN account_move am
    ON ai.move_id = am.id
WHERE reference LIKE '0005%' AND reference <> ref

SELECT
  am.ref,
  aml.ref
FROM
  account_move am
  INNER JOIN account_move_line aml
    ON am.id = aml.move_id
WHERE am.ref <> aml.ref


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
  number          = 'VEN05/2016/' || substring(number, 12, 4),
  journal_id = (select id from account_journal where code = 'VEN05'),
  journal_document_class_id = 34,
  internal_number = 'VEN05/2016/' || substring(internal_number, 12, 4),
  afip_document_number = reference,
  move_name       = 'VEN05/2016/' || substring(number, 12, 4)
where
      type like 'out_i%'
  and reference LIKE '0005%'
  and journal_id = (select id from account_journal where code = 'VEN06')
  and journal_document_class_id = 24;

/* Facturas B*/
update account_invoice
SET
  number          = 'VEN05/2016/' || substring(number, 12, 4),
  journal_id = (select id from account_journal where code = 'VEN05'),
  journal_document_class_id = 36,
  internal_number = 'VEN05/2016/' || substring(internal_number, 12, 4),
  afip_document_number = reference,
  move_name       = 'VEN05/2016/' || substring(number, 12, 4)
where
      type like 'out_i%'
  and reference LIKE '0005%'
  and journal_id = (select id from account_journal where code = 'VEN06')
  and journal_document_class_id = 26;

/* Nota de débito A*/
update account_invoice
SET
  number          = 'VEN05/2016/' || substring(number, 12, 4),
  journal_id = (select id from account_journal where code = 'VEN05'),
  journal_document_class_id = 35,
  internal_number = 'VEN05/2016/' || substring(internal_number, 12, 4),
  afip_document_number = reference,
  move_name       = 'VEN05/2016/' || substring(number, 12, 4)
where
      type like 'out_i%'
  and reference LIKE '0005%'
  and journal_id = (select id from account_journal where code = 'VEN06')
  and journal_document_class_id = 25;

/* Nota de débito B  NO HAY*/

/* Nota de crédito A*/
UPDATE account_invoice
SET
  number                    = 'RVE05/2016/' || substring(number, 12, 4),
  journal_id                = (SELECT id
                               FROM account_journal
                               WHERE code = 'RVE05'),
  journal_document_class_id = 40,
  internal_number           = 'RVE05/2016/' || substring(internal_number, 12, 4),
  afip_document_number      = reference,
  move_name                 = 'RVE05/2016/' || substring(number, 12, 4)
WHERE
  type LIKE 'out_r%'
  AND reference LIKE '0005%'
  AND journal_id = (SELECT id
                    FROM account_journal
                    WHERE code = 'RVE06')
  AND journal_document_class_id = 30;


/* Nota de crédito B*/
UPDATE account_invoice
SET
  number                    = 'RVE05/2016/' || substring(number, 12, 4),
  journal_id                = (SELECT id
                               FROM account_journal
                               WHERE code = 'RVE05'),
  journal_document_class_id = 41,
  internal_number           = 'RVE05/2016/' || substring(internal_number, 12, 4),
  afip_document_number      = reference,
  move_name                 = 'RVE05/2016/' || substring(number, 12, 4)
WHERE
  type LIKE 'out_r%'
  AND reference LIKE '0005%'
  AND journal_id = (SELECT id
                    FROM account_journal
                    WHERE code = 'RVE06')
  AND journal_document_class_id = 31;

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
  number          = 'VEN02/2016/' || substring(number, 12, 4),
  journal_id = (select id from account_journal where code = 'VEN02'),
  journal_document_class_id = 45,
  internal_number = 'VEN02/2016/' || substring(internal_number, 12, 4),
  afip_document_number = '0002-' || LPAD((cast(substring(reference, 3 ,4) as int)-1516)::text, 8, '0'),
  move_name       = 'VEN02/2016/' || substring(number, 12, 4)
WHERE
      reference LIKE 'Z%'
  and type like 'out_i%'
  and journal_id = 9;


/* ponerle a las move la referencia de las facturas */
UPDATE account_move am
SET
  ref = ai.reference
FROM account_invoice ai
WHERE
  am.id = ai.move_id;

/* ponerle a las move line la referencia de las move */
UPDATE account_move_line aml
SET
  ref = am.ref
FROM account_move am
WHERE
  am.id = aml.move_id;


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

/* -------------------------------------------------------------------------------
  Termina el patch
*/

/*
**********************************************************************************
ajustar nros de secuencia
***********************************************************************************/

/* obtener los numeros de secuencia para los cuatro PV
PV2 FA-A:1    FA-B:25 NC-A:1  NC-B:1 ND-A:1 ND-B:1
PV4 FA-A:88   FA-B:34 NC-A:4  NC-B:6 ND-A:1 ND-B:1
PV5 FA-A:418  FA-B:41 NC-A:16 NC-B:4 ND-A:2 ND-B:1
PV6 FA-A:1    FA-B:1  NC-A:1  NC-B:1 ND-A:1 ND-B:1
*/
SELECT
  reference,
  afip_document_number,
  adc.doc_code_prefix
FROM account_invoice ai
  JOIN account_journal_afip_document_class ajadc
    ON ai.journal_document_class_id = ajadc.id
  JOIN afip_document_class adc
    ON ajadc.afip_document_class_id = adc.id
WHERE
  afip_document_number LIKE '0002-%'
  AND adc.doc_code_prefix LIKE 'ND-B%'
  AND type LIKE 'out%'
ORDER
BY afip_document_number DESC
LIMIT 3;


/* secuencias internas
    VEN   RVE
PV2 239   1
PV4 118   9
PV5 250   10
PV6 1     1
*/

SELECT
  number,
  internal_number
FROM account_invoice
WHERE state <> 'draft'
      AND number LIKE 'VEN05%'
ORDER BY number DESC;

/* Verificaciones */
/* verificar la denormalización de journal_id tiene que dar cero*/
select sum(am.journal_id- aml.journal_id)
from account_move am
join account_move_line aml
on am.id = aml.move_id


/* Cambiar punto de venta 2 factura B por TIQUE */
UPDATE account_invoice
SET
  journal_document_class_id = 52,
  afip_document_class_id    = 58,
  responsability_id         = 5
WHERE journal_id = 20


/* corregir numeros de factura Tiket */
UPDATE account_invoice
SET
  afip_document_number = '0002-' ||
                         LPAD((cast(substring(reference, 3, 4) AS INT)) :: TEXT, 8, '0')
WHERE
  reference LIKE 'Z%'
  AND type LIKE 'out_i%'
  AND journal_id = (SELECT id
                    FROM account_journal
                    WHERE code = 'VEN02');

UPDATE account_move
SET
  document_number      = 'TIKE ' || '0002-' ||
                         LPAD((cast(substring(ref, 3, 4) AS INT)) :: TEXT, 8, '0'),
  afip_document_number = '0002-' ||
                         LPAD((cast(substring(ref, 3, 4) AS INT)) :: TEXT, 8, '0')
WHERE
  ref LIKE 'Z%';

UPDATE account_move_line
SET
  journal_id      = (SELECT journal_id
                     FROM account_move
                     WHERE id = move_id),
  document_number = (SELECT document_number
                     FROM account_move
                     WHERE id = move_id)
WHERE
  move_id IN (SELECT move_id
              FROM account_move
              WHERE ref LIKE 'Z%');
