# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    lead_source = fields.Selection([
        ('drive_past', 'Drive Past'),
        ('previous_customer', 'Previous Customer'),
        ('printing', 'Printing'),
        ('own_lead', 'Own Lead'),
        ('recommended', 'Recommended'),
        ('internet', 'Internet'),
        ('other', 'Other'),
    ], string='Lead Source')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pw_bom_id = fields.Many2one('mrp.bom', string="Bill of Material", domain="""[
        '|',
            '&',
                ('company_id', '=', False),
                ('company_id', '=', company_id),
            ('product_tmpl_id','=',product_template_id)]""")

    length = fields.Float(related="pw_bom_id.length", string="Height(m)", readonly=True)
    width = fields.Float(related="pw_bom_id.width", string="Width(m)", readonly=True)
    size = fields.Float(compute="_calculate_size", readonly=True, string="Size(m2)")
    location = fields.Many2one(related="pw_bom_id.location", readonly=True)

    @api.depends('length', 'width')
    def _calculate_size(self):
        for rec in self:
            if rec.length and rec.width:
                rec.size = rec.length * rec.width
            else:
                rec.size = 0.0

    def open_pw_bom_id_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': 'BOM',
            'res_model': 'mrp.bom',
            'view_mode': 'form',
            'target': 'new',
        }

        # If a BOM exists, open it for editing
        if self.pw_bom_id:
            action['res_id'] = self.pw_bom_id.id

        return action

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            product = self.product_id.product_tmpl_id
            sale_order = self.order_id

            # Check if the sale order and product are set
            if product and sale_order:
                # Get the next number in the sequence
                sequence = self.env['ir.sequence'].next_by_code('mrp.bom.code')
                bom_code = f"{sequence}"

                # Define the BOM values
                bom_vals = {
                    'code': bom_code,
                    'product_tmpl_id': product.id,
                    # Add any other required fields for your BOM here
                }

                # Create a new BOM
                new_bom = self.env['mrp.bom'].create(bom_vals)

                # Set the created BOM's ID to the pw_bom_id field
                self.pw_bom_id = new_bom.id
            else:
                # If there's no product or sale order, reset the BOM field
                self.pw_bom_id = False

    # @api.model
    # def create(self, vals):
    #     new_record = super(SaleOrderLine, self).create(vals)
    #     print(vals)
    #
    #     if 'product_id' in vals:
    #         product = new_record.product_template_id
    #         sale_order = new_record.order_id
    #
    #         # Ensure product and sale_order exist and are not empty records
    #         if product and sale_order:
    #             # Create a new BOM
    #             bom_vals = {
    #                 'code': f"{product.name} {sale_order.name}",
    #                 'product_tmpl_id': product.id,
    #                 # 'product_id': product.id,
    #                 # Add any other required fields for your BOM here
    #             }
    #             new_bom = self.env['mrp.bom'].create(bom_vals)
    #
    #             # Link the newly created BOM to this sale order line
    #             new_record.pw_bom_id = new_bom
    #
    #     return new_record


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    delivery_split = fields.Selection([('not_permitted', 'permitted')])
    priority = fields.Selection([('normal', 'Normal'), ('special', 'Special')], 'Priority')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_fabric_product = fields.Boolean(default=False)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_fabric_product = fields.Boolean(
        string='Is Fabric Product',
        related='product_tmpl_id.is_fabric_product',
        store=True,
        readonly=True
    )

