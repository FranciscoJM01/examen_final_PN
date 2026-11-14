from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TiendaConvenio(models.Model):
    _name = 'tienda.convenio'
    _description = 'Convenio de Descuento Tienda UNICAH'

    name = fields.Char(string='Nombre del Convenio', required=True)
    codigo = fields.Char(string='Código', required=True)
    porcentaje_descuento = fields.Float(string='Porcentaje de Descuento (%)', required=True, default=0.0)
    fecha_inicio = fields.Date(string='Fecha de Inicio')
    fecha_fin = fields.Date(string='Fecha de Fin')
    activo = fields.Boolean(string='Activo', default=True)
    descripcion = fields.Text(string='Descripción')

    @api.constrains('porcentaje_descuento')
    def _check_porcentaje_descuento(self):
        for rec in self:
            if rec.porcentaje_descuento < 0 or rec.porcentaje_descuento > 30:
                raise ValidationError('El porcentaje de descuento debe estar entre 0% y 30%.')

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for rec in self:
            if rec.fecha_inicio and rec.fecha_fin and rec.fecha_fin < rec.fecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')