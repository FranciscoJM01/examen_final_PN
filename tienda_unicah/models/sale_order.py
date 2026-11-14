from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    convenio_unicah_id = fields.Many2one(
        'tienda.convenio',
        string='Convenio UNICAH',
        domain=[('activo', '=', True)],
    )
    descuento_convenio = fields.Float(
        string='Descuento Convenio (%)',
        related='convenio_unicah_id.porcentaje_descuento',
        readonly=True,
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_convenio_unicah(self):
        if self.partner_id and self.partner_id.convenio_unicah_id:
            self.convenio_unicah_id = self.partner_id.convenio_unicah_id
        else:
            self.convenio_unicah_id = False

    @api.onchange('convenio_unicah_id', 'order_line')
    def _onchange_convenio_unicah_descuento(self):
        descuento = self.convenio_unicah_id.porcentaje_descuento if self.convenio_unicah_id else 0.0
        for line in self.order_line:
            if not line.display_type:
                line.discount = descuento