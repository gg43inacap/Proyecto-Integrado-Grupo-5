Módulo Auditoría
================

Este módulo registra y controla las acciones realizadas en el sistema, garantizando trazabilidad y seguridad.

Modelos
-------

La clase `Auditoria` representa un registro de acción realizada por un usuario.

Campos principales:
- `usuario`: usuario que realizó la acción.
- `accion`: descripción de la acción.
- `fecha`: fecha y hora de la acción.

Vistas
------

Las vistas permiten:
- Listar registros de auditoría.
- Filtrar acciones por usuario o fecha.
- Exportar registros.

URLs
----

- `/auditoria/`: listado de registros.
- `/auditoria/filtrar/`: filtrado de registros.
- `/auditoria/exportar/`: exportación de registros.