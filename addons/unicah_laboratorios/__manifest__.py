{
    'name': 'UNICAH Reserva de Aulas y Laboratorios',
    'version': '20.0.1.0',
    'category': 'Services',
    'summary': 'Control de reservas de aulas y laboratorios universitarios',
    'author': 'Francisco Javier Martinez',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.access.csv',
        'views/unicah_reserva_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}