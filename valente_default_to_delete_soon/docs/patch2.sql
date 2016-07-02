/* borrar tike 1542 */
select afip_document_number from account_invoice
  WHERE id = 624;

select * from account_invoice_line
where invoice_id = 624;

select * from account_move
  WHERE afip_document_number = '0002-00001542';

select * from account_move_line
  WHERE move_id = 1114;



WHERE afip_document_number like '0002-0000154%'


delete FROM account_invoice
where id = 624;
delete FROM account_invoice_line
where invoice_id = 624;
delete FROM account_move
WHERE afip_document_number = '0002-00001542';
delete FROM account_move_line
WHERE move_id = 1114;


