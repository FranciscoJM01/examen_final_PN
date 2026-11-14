from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    convenio_unicah_id = fields.Many2one(
        'tienda.convenio',
        string='Convenio',
        domain=[('activo', '=', True)],
    )
    descuento_convenio = fields.Float(
        string='Descuento Convenio (%)',
        related='convenio_unicah_id.porcentaje_descuento',
        readonly=True,
    )
    ahorro_convenio = fields.Monetary(
        string='Ahorro por convenio',
        compute='_compute_ahorro_convenio',
        store=True,
        currency_field='currency_id',
    )

    @api.depends('order_line.price_unit', 'order_line.product_uom_qty', 'order_line.discount', 'order_line.display_type', 'convenio_unicah_id')
    def _compute_ahorro_convenio(self):
        for order in self:
            ahorro = 0.0
            if order.convenio_unicah_id:
                for line in order.order_line:
                    if not line.display_type and line.discount > 0:
                        subtotal_sin_desc = line.price_unit * line.product_uom_qty
                        ahorro += subtotal_sin_desc * (line.discount / 100.0)
            order.ahorro_convenio = ahorro

    @api.onchange('partner_id')
    def _onchange_partner_id_convenio_unicah(self):
        if self.partner_id and self.partner_id.convenio_unicah_id:
            self.convenio_unicah_id = self.partner_id.convenio_unicah_id
        else:
            self.convenio_unicah_id = False

    def action_aplicar_convenio(self):
        for order in self:
            if not order.convenio_unicah_id:
                continue
            descuento = order.convenio_unicah_id.porcentaje_descuento
            for line in order.order_line:
                if not line.display_type:
                    line.discount = descuento
            order.message_post(
                body=f"Se aplicó el convenio '{order.convenio_unicah_id.name}' con un {descuento:.2f}% de descuento a los productos del pedido."
            )

    def action_confirm(self):
        for order in self:
            if order.partner_id.tipo_unicah == 'estudiante':
                total_unidades = sum(line.product_uom_qty for line in order.order_line if not line.display_type)
                if total_unidades > 10:
                    raise ValidationError('Los pedidos de estudiantes no pueden superar las 10 unidades en total.')
        return super().action_confirm()