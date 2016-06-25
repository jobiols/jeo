SELECT *
FROM account_invoice
WHERE afip_document_number = '0005-00000040';
SELECT *
FROM account_invoice_line
WHERE invoice_id = 402;
SELECT *
FROM account_invoice
WHERE afip_document_number = '0005-00000003';
SELECT *
FROM account_invoice_line
WHERE invoice_id = 403;
SELECT *
FROM account_move
WHERE afip_document_number = '0005-00000040';
SELECT *
FROM account_move_line
WHERE move_id = 648;
SELECT *
FROM account_move
WHERE afip_document_number = '0005-00000003';
SELECT *
FROM account_move_line
WHERE move_id = 649;

/* borrar factura 40 y lineas de factura */
DELETE FROM account_invoice_line
WHERE invoice_id = 402;
DELETE FROM account_invoice
WHERE afip_document_number = '0005-00000040';
/* borrar nota de crédito y lineas */
DELETE FROM account_invoice
WHERE afip_document_number = '0005-00000003';
DELETE FROM account_invoice_line
WHERE invoice_id = 403;
/* borrar movimientos contables de factura 40 y lineas */
DELETE FROM account_move
WHERE afip_document_number = '0005-00000040';
DELETE FROM account_move_line
WHERE move_id = 648;
/* borrar movimientos contables de factua 3 y lineas */
DELETE FROM account_move
WHERE afip_document_number = '0005-00000003';
DELETE FROM account_move_line
WHERE move_id = 649;


SELECT *
FROM account_invoice
WHERE afip_document_number = '0005-00000417';
SELECT *
FROM account_invoice_line
WHERE invoice_id = 400;
SELECT *
FROM account_move
WHERE afip_document_number = '0005-00000417';
SELECT *
FROM account_move_line
WHERE move_id = 646;
SELECT *
FROM account_invoice
WHERE afip_document_number = '0005-00000015';
SELECT *
FROM account_invoice_line
WHERE invoice_id = 401;
SELECT *
FROM account_move
WHERE afip_document_number = '0005-00000015';
SELECT *
FROM account_move_line
WHERE move_id = 647;


/* borrar factura 417 y sus lineas */
DELETE FROM account_invoice
WHERE afip_document_number = '0005-00000417';
DELETE FROM account_invoice_line
WHERE invoice_id = 400;
/* borrar nota de crédito 15 y sus lineas */
DELETE FROM account_invoice
WHERE afip_document_number = '0005-00000015';
DELETE FROM account_invoice_line
WHERE invoice_id = 401;
/* borrar movimientos contables de 417 y sus lineas */
DELETE FROM account_move
WHERE afip_document_number = '0005-00000417';
DELETE FROM account_move_line
WHERE move_id = 646;
/* borrar movimientos contables de 15 y sus lineas */
DELETE FROM account_move
WHERE afip_document_number = '0005-00000015';
DELETE FROM account_move_line
WHERE move_id = 647;
