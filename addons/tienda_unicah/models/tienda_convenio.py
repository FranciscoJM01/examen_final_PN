from odoo import fields, models


class TiendaConvenio(models.Model):
    _name = 'tienda.convenio'
    _description = 'Convenio de Descuento Tienda UNICAH'

    name = fields.Char(string='Nombre del Convenio', required=True)
    codigo = fields.Char(string='Código', required=True)
    porcentaje_descuento = fields.Float(string='Porcentaje de Descuento (%)', required=True, default=0.0)
    activo = fields.Boolean(string='Activo', default=True)
    descripcion = fields.Text(string='Descripción')