from odoo import api, fields, models
from odoo.exceptions import ValidationError


class UnicahReserva(models.Model):
    _name = 'unicah.reserva'
    _description = 'Reserva de Aula o Laboratorio UNICAH'

    name = fields.Char(string='Código / Motivo', required=True)
    aula = fields.Selection([
        ('lab1', 'Laboratorio de Cómputo 1'),
        ('lab2', 'Laboratorio de Redes'),
        ('aula101', 'Aula Magna 101'),
    ], string='Aula / Laboratorio', required=True)
    solicitante_id = fields.Many2one('res.partner', string='Docente / Solicitante', required=True)
    fecha_inicio = fields.Datetime(string='Hora Inicio', required=True)
    fecha_fin = fields.Datetime(string='Hora Fin', required=True)
    duracion_horas = fields.Float(string='Duración (Horas)', compute='_compute_duracion', store=True)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
    ], string='Estado', default='borrador')

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_duracion(self):
        for rec in self:
            if rec.fecha_inicio and rec.fecha_fin and rec.fecha_fin > rec.fecha_inicio:
                diff = rec.fecha_fin - rec.fecha_inicio
                rec.duracion_horas = diff.total_seconds() / 3600.0
            else:
                rec.duracion_horas = 0.0

    @api.constrains('fecha_inicio', 'fecha_fin', 'aula', 'estado')
    def _check_disponibilidad_y_fechas(self):
        for rec in self:
            if rec.fecha_inicio and rec.fecha_fin and rec.fecha_fin <= rec.fecha_inicio:
                raise ValidationError('La hora de fin debe ser posterior a la hora de inicio.')
            traslape = self.search([
                ('id', '!=', rec.id),
                ('aula', '=', rec.aula),
                ('estado', '=', 'confirmada'),
                ('fecha_inicio', '<', rec.fecha_fin),
                ('fecha_fin', '>', rec.fecha_inicio),
            ])
            if traslape:
                raise ValidationError('El aula ya tiene una reserva confirmada en ese horario.')

    def action_confirmar(self):
        for rec in self:
            rec.estado = 'confirmada'