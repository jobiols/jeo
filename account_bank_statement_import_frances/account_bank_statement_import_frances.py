# -*- coding: utf-8 -*-

import dateutil.parser
import StringIO
import csv
from openerp.tools.translate import _
from openerp import api, models
from openerp.exceptions import Warning as UserError
from datetime import datetime

class AccountBankStatementImport(models.TransientModel):
    _inherit = "account.bank.statement.import"

    @api.model
    def _get_hide_journal_field(self):
        return self.env.context.get('journal_id') and True

    @api.model
    def _check_frances(self, data_file):
        return data_file.strip().startswith('Fecha,Descripcion,Sucursal,Monto,')

    @api.model
    def _get_monto(self,value):
        value = value.replace('.','')
        value = value.replace(',','.')
        return float(value)

    @api.model
    def _parse_file(self, data_file):
        if not self._check_frances(data_file):
            return super(AccountBankStatementImport, self)._parse_file(
                data_file)

        try:
            file_data = ""
            for line in StringIO.StringIO(data_file).readlines():
                file_data += line

            # check if endline is \r \n or both
            if '\r' in file_data:
                if '\n' in file_data:
                    file_data = file_data.replace('\n','')
            # split file according to endline
            if '\r' in file_data:
                data_list = file_data.split('\r')
            else:
                data_list = file_data.split('\n')

            aaa = csv.DictReader(data_list)
            print '------------- csv'
            for iii in aaa:
                print iii['Fecha']
                print iii['Descripcion']
                print iii['Sucursal']
                print self._get_monto(iii['Monto'])
            print '------------- csv'

        except:
            raise #UserError(_('Could not decipher the Frances file.'))

        transactions = []
        vals_line = {}
        total = 0
        vals_bank_statement = {}
        for line in csv.DictReader(data_list):
            # date of transaction
            vals_line['date'] = datetime.strptime(line['Fecha'],"%d/%m/%Y")
            # Total amount
            total += self._get_monto(line['Monto'])
            vals_line['amount'] = self._get_monto(line['Monto'])
            # Name
            vals_line['name'] = line['Descripcion']+' / '+line['Sucursal']
            # Since QIF doesn't provide account numbers, we'll have to
            #  find res.partner and res.partner.bank here
            # (normal behavious is to provide 'account_number', which
            # the generic module uses to find partner/bank)
            banks = self.env['res.partner.bank'].search(
                [('owner_name', '=', 'Frances')], limit=1)
            if banks:
                bank_account = banks[0]
                vals_line['bank_account_id'] = bank_account.id
                vals_line['partner_id'] = bank_account.partner_id.id

            transactions.append(vals_line)
            vals_line = {}

        vals_bank_statement.update({
            'balance_end_real': total,
            'transactions': transactions
        })

        return None, None, [vals_bank_statement]
