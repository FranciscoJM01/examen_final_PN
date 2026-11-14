from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    convenio_unicah_id = fields.Many2one(
        'tienda.convenio',
        string='Convenio UNICAH',
        domain=[('activo', '=', True)],
    )
    numero_cuenta_unicah = fields.Char(string='Número de Cuenta / Empleado UNICAH')