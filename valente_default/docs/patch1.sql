/* borrar factura 40 y su nota de crédito*/
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


DELETE FROM account_invoice_line
WHERE invoice_id = 402;
DELETE FROM account_invoice
WHERE afip_document_number = '0005-00000040';
DELETE FROM account_invoice
WHERE afip_document_number = '0005-00000003';
DELETE FROM account_invoice_line
WHERE invoice_id = 403;
DELETE FROM account_move
WHERE afip_document_number = '0005-00000040';
DELETE FROM account_move_line
WHERE move_id = 648;
DELETE FROM account_move
WHERE afip_document_number = '0005-00000003';
DELETE FROM account_move_line
WHERE move_id = 649;


/* Borrar factura 417 y su nota de crédito */
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

DELETE FROM account_invoice
WHERE afip_document_number = '0005-00000417';
DELETE FROM account_invoice_line
WHERE invoice_id = 400;
DELETE FROM account_move
WHERE afip_document_number = '0005-00000417';
DELETE FROM account_move_line
WHERE move_id = 646;
DELETE FROM account_invoice
WHERE afip_document_number = '0005-00000015';
DELETE FROM account_invoice_line
WHERE invoice_id = 401;
DELETE FROM account_move
WHERE afip_document_number = '0005-00000015';
DELETE FROM account_move_line
WHERE move_id = 647;

