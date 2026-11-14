from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tipo_unicah = fields.Selection(
        [
            ('estudiante', 'Estudiante'),
            ('docente', 'Docente'),
        ],
        string='Tipo de Miembro UNICAH',
    )
    numero_cuenta_unicah = fields.Char(string='Número de Cuenta')
    carrera_unicah = fields.Char(string='Carrera')
    convenio_unicah_id = fields.Many2one(
        'tienda.convenio',
        string='Convenio UNICAH',
        domain=[('activo', '=', True)],
    )

    @api.constrains('tipo_unicah', 'numero_cuenta_unicah')
    def _check_numero_cuenta_unicah(self):
        for rec in self:
            if rec.tipo_unicah == 'estudiante':
                cuenta = (rec.numero_cuenta_unicah or '').strip()
                if len(cuenta) != 10 or not cuenta.isdigit():
                    raise ValidationError('El número de cuenta del estudiante debe contener exactamente 10 dígitos numéricos.')