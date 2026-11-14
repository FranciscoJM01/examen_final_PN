from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    reserva_ids = fields.One2many('unicah.reserva', 'solicitante_id', string='Reservas de Aulas')