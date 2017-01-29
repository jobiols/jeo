# -*- coding: utf-8 -*-

from openerp.tests.common import TransactionCase
from openerp.modules.module import get_module_resource


class TestFrancesFile(TransactionCase):
    """Tests for import bank statement for frances file format
    (account.bank.statement.import)
    """

    def setUp(self):
        super(TestFrancesFile, self).setUp()
        self.statement_import_model = self.env['account.bank.statement.import']
        self.statement_line_model = self.env['account.bank.statement.line']

    def test_frances_file_import(self):
        from openerp.tools import float_compare
        frances_file_path = get_module_resource(
            'account_bank_statement_import_frances',
            'test_qif_file', 'test_frances.csv')
        frances_file = open(frances_file_path, 'rb').read().encode('base64')
        bank_statement_import = self.statement_import_model.with_context(
            journal_id=self.ref('account.bank_journal')).create(
            dict(data_file=frances_file))
        bank_statement_import.import_file()
        bank_statement = self.statement_line_model.search(
            [('name', '=', 'TRANSFERENCIA XX0000001266940 / 100 - FRANCES NET')], limit=1)[0].statement_id
        assert float_compare(bank_statement.balance_end_real, -1484.81, 2) == 0
