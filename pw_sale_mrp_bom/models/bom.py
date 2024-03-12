from odoo import fields, models, api


class Location(models.Model):
    _name = "roller.location"

    name = fields.Char()


class OtherLocation(models.Model):
    _name = "other.location"

    name = fields.Char()


class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    location = fields.Many2one('roller.location')
    other_location = fields.Many2many('other.location')
    length = fields.Float(string="Height(m)")
    width = fields.Float(string="Width(m)")
    type = fields.Selection([
        ('normal', 'Manufacture this product'),
        ('phantom', 'Kit')], 'BoM Type',
        default='phantom', required=True)
    style = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double')],
        'Style'
    )
    control_blind = fields.Selection([
        ('manual', 'Manual'),
        ('motorized', 'Motorized')],
        'Control Blind'
    )
    control_side = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')],
        'Control Side'
    )
    roll_direction = fields.Selection([
        ('standard', 'Standard'),
        ('reverse', 'Reverse')],
        'Roll Direction'
    )
    fitting_method = fields.Selection([
        ('wall_mount', 'Wall Mount'),
        ('ceiling_mount', 'Ceiling Mount'),
        ('existing_mount', 'Existing Mount')],
        'Fitting Method'
    )
    check_measure = fields.Selection([
        ('not_required', 'Not Required'),
        ('required', 'Required')],
        'Check Measure'
    )
    remove_product = fields.Selection([
        ('not_required', 'Not Required'),
        ('required', 'Required')],
        'Remove Product'
    )
