# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from openerp import models, fields, exceptions, api, _


class ProductPricelistLoad(models.Model):
    _name = 'product.pricelist.load'
    _description = 'Product Price List Load'
    _order = 'id desc'

    def _discount_modes(self):
        if not self.keys:
            return

        keys = self.keys.split(',')

        supplier_discounts = []
        for i, disc in enumerate(keys):
            if disc[0:2] == 'dp':
                supplier_discounts.append('D' + str(i - 4) + '%')

        categ_discounts = []
        for i, disc in enumerate(keys):
            if disc[0:2] == 'dc':
                categ_discounts.append('D' + str(i - 4) + '%')

        subcateg_discounts = []
        for i, disc in enumerate(keys):
            if disc[0:2] == 'ds':
                subcateg_discounts.append('D' + str(i - 4) + '%')

        self.description = 'Descuentos sobre precio de lista: (Producto {})   (Categoria {})   (Sub categoria {})'. \
            format(', '.join(supplier_discounts),
                   ', '.join(categ_discounts),
                   ', '.join(subcateg_discounts))

    name = fields.Char('Load')
    date = fields.Date('Date:', readonly=True, help='Fecha del archivo')
    file_name = fields.Char('File Name', readonly=True, help='nombre del archivo')
    file_lines = fields.One2many('product.pricelist.load.line', 'file_load',
                                 'Product Pricelist Lines')
    fails = fields.Integer('Fail Lines:', readonly=True, help='Lineas sin procesar')
    process = fields.Integer('Lines to Process:', readonly=True,
                             help='Lineas pendientes de proceso')
    supplier = fields.Many2one('res.partner', 'Supplier', required=True)
    mode = fields.Selection([('no_append', 'No agregar productos nuevos'),
                             ('append', 'Agregar productos nuevos')
                             ], help='define el modo en el que se procesa la lista de \
                             precios, si el modo es "No agregar productos nuevos", el \
                             proceso solo actualizará los precios y descuentos de los\
                             productos existentes. Si el modo es "Agregar productos nuevos"\
                             entonces si no encuentra un producto lo agrega y si lo \
                             encuentra, lo actualiza',
                            required=True,
                            default='no_append')
    keys = fields.Char('keys')
    description = fields.Char(compute="_discount_modes")

    @api.multi
    def check_category(self, line):
        # obtener la categoria que identifica al proveedor, es la root del arbol
        supp_categ = self.supplier.categ_id
        if not supp_categ:
            raise exceptions.Warning(_("Supplier without category"))

        # cargar los descuentos para el proveedor
        supp_categ.update_discounts(line.get_discounts('dp'))
        # preparar el return
        res = supp_categ

        # si hay una categoria en la linea procesar esto
        if line.categ:
            # ver si existe la categoria bajo el root
            cat = supp_categ.search_child(line.categ)
            # si la categoria no existe, la creo
            if not cat:
                cat = supp_categ.create_child(line.categ)
            # cargo los descuentos para esta categoria
            cat.update_discounts(line.get_discounts('dc'))
            # preparo el return
            res = cat
            # veo si hay una subcategoria en la linea
            if line.sub_categ:
                # verifico si existe en los hijos de la categoria
                sub = cat.search_child(line.sub_categ)
                # si no existe la agrego
                if not sub:
                    sub = cat.create_child(line.sub_categ)
                # aplico los descuentos de la subcategoria
                sub.update_discounts(line.get_discounts('ds'))
                # preparo el return
                res = sub

        # devuelvo la ultima categoria que procesé
        return res

    @api.multi
    def process_line(self, line):
        # buscar en suppinfo proveedor y codigo
        suppinfo = self.psupplinfo_obj.search(
            [('product_code', '=', line.product_code),
             ('name', '=', self.supplier.id)])

        if not suppinfo and self.mode == 'append':
            # crear o actualizar categorias
            cat = self.check_category(line)

            # crear el producto, si tenemos prod in box agregarlo al values
            values = {
                'default_code': line.product_code,
                'name': line.product_name,
                'type': 'product',
                'categ_id': cat.id
            }
            if line.prod_in_box:
                values['prod_in_box'] = line.prod_in_box
                values['prod_in_box_uom'] = line.prod_in_box_uom
            prod = self.product_template_obj.create(values)

            # crear información del proveedor
            suppinfo = self.psupplinfo_obj.create({
                'product_code': line.product_code,
                'product_name': line.product_name,
                'name': self.supplier.id,
                'product_tmpl_id': prod.id
            })
            # actualizar precio de lista
            suppinfo.list_price = line.list_price
            line.write({'fail': False, 'fail_reason': 'Importado'})

            return

        if suppinfo:
            # crear o actualizar categorias
            cat = self.check_category(line)

            # actualizar precio de lista del producto
            suppinfo.list_price = line.list_price
            line.write({'fail': False, 'fail_reason': 'Actualizado'})
        else:
            line.fail_reaseon = 'No actualizado'

    @api.multi
    def process_lines(self):
        # si no le puse proveedor abortar
        if not self.supplier:
            raise exceptions.Warning(_("You must select a Supplier"))

        self.product_template_obj = self.env['product.template']
        self.psupplinfo_obj = self.env['product.supplierinfo']
        self.pricepinfo_obj = self.env['pricelist.partnerinfo']
        self.category_obj = self.env['product.category']

        if not self.file_lines:
            raise exceptions.Warning(_("There must be one line at least to process"))

        # procesar cada linea
        for line in self.file_lines:
            # procesar las lineas que estan en fail
            if line.fail and line.check():
                self.process_line(line)

        count = 0
        for line in self.file_lines:
            if line.fail:
                count += 1
        self.fails = count

        return True


class ProductPricelistLoadLine(models.Model):
    _name = 'product.pricelist.load.line'
    _description = 'Product Price List Load Line'

    product_code = fields.Char('Product Code', required=True)
    product_name = fields.Char('Product Name')
    list_price = fields.Float('List Price', required=True)
    prod_in_box = fields.Float('Cant. producto por caja')
    prod_in_box_uom = fields.Char()
    categ = fields.Char('Category')
    sub_categ = fields.Char('Sub Category')
    d1 = fields.Float('D1%')
    d2 = fields.Float('D2%')
    d3 = fields.Float('D3%')
    d4 = fields.Float('D4%')
    d5 = fields.Float('D5%')
    d6 = fields.Float('D6%')
    fail = fields.Boolean('Fail')
    fail_reason = fields.Char('Fail Reason')
    file_load = fields.Many2one('product.pricelist.load', 'Load', required=True)
    keys = fields.Char(related='file_load.keys')
    supplier = fields.Char(related='file_load.supplier.name')

    @api.multi
    def debug(self):
        for rec in self:
            res = '({:5})({:5})({:10})({:10})[{:5}][{:5}]({:5})({:5})({:5})({:5})({:5})({:5}) -- {}'.format(
                rec.product_code, rec.list_price, rec.categ, rec.sub_categ, \
                rec.prod_in_box, rec.prod_in_box_uom, \
                rec.d1, rec.d2, rec.d3, rec.d4, rec.d5, rec.d6, rec.keys
            )
            return res

    @api.multi
    def check(self):
        for rec in self:
            # check product, must exist code and name
            if rec.product_code and not rec.product_name:
                rec.fail_reason = _('Missing product name')
                return False
            if not rec.product_code and rec.product_name:
                rec.fail_reason = _('Missing product code')
                return False
            if rec.product_code and not rec.list_price:
                rec.fail_reason = _('Missing list price')
                return False
            if not rec.product_code and rec.list_price:
                rec.fail_reason = _('Missing product')
                return False
            if not rec.categ and rec.sub_categ:
                rec.fail_reason = _('Missing category')
                return False
            return True

    def get_discounts(self, categ):
        # dado un categ, que es un nombre que puede ser 'dp' 'dc' o 'ds'
        # devolver una lista de los descuentos que corresponden
        keys = self.keys.split(',')
        ret = []
        if self.d1 <> 0 and keys[0][:2] == categ:
            ret.append(self.d1)
        if self.d2 <> 0 and keys[1][:2] == categ:
            ret.append(self.d2)
        if self.d3 <> 0 and keys[2][:2] == categ:
            ret.append(self.d3)
        if self.d4 <> 0 and keys[3][:2] == categ:
            ret.append(self.d4)
        if self.d5 <> 0 and keys[4][:2] == categ:
            ret.append(self.d5)
        if self.d6 <> 0 and keys[5][:2] == categ:
            ret.append(self.d6)

        return ret

        # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
