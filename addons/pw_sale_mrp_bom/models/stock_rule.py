# -*- coding: utf-8 -*-
from odoo import fields, models, api


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_matching_bom(self, product_id, company_id, values):
        sale_line_id = values.get('move_dest_ids').mapped('sale_line_id')
        if sale_line_id and sale_line_id[0].pw_bom_id:
            return sale_line_id[0].pw_bom_id
        if values.get('bom_id', False):
            return values['bom_id']
        return self.env['mrp.bom']._bom_find(product_id, picking_type=self.picking_type_id, bom_type='normal', company_id=company_id.id)[product_id]
