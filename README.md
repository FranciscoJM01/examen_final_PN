# Módulo Odoo 20.0: Tienda UNICAH (`tienda_unicah`)

Módulo personalizado para la gestión de convenios de descuento universitarios y aplicación automática de porcentajes en cotizaciones y pedidos de venta (`sale.order`).

## Características Principales
- **Modelo `tienda.convenio`:** Administración de convenios institucionales (`EST-UNICAH`, `DOC-UNICAH`, `BEC-UNICAH`) con porcentaje de descuento configurable.
- **Herencia en Contactos (`res.partner`):** Asignación de número de cuenta/empleado y convenio universitario activo.
- **Automatización en Ventas (`sale.order`):** Propagación automática del porcentaje de descuento hacia las líneas del pedido mediante `@api.onchange`.
- **Seguridad Odoo 20.0:** Reglas configuradas en `security/ir.access.csv` para lectura (`r`) y administración (`crud`).

## Autor
Francisco Javier Martínez