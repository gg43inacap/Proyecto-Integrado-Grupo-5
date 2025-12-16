Módulo Partos
=============

Este módulo gestiona la información relacionada con los partos y recién nacidos en el sistema.

Modelos
-------

La clase `Parto` representa un parto registrado en el sistema.  
Incluye datos clínicos, fecha, tipo de parto y estado del recién nacido.

Campos principales:
- `fecha_parto`: Fecha en que ocurrió el parto.
- `tipo_parto`: Tipo de parto (vaginal, cesárea, instrumental).
- `estado_recien_nacido`: Estado clínico del recién nacido.

Vistas
------

Las vistas permiten:
- Listar partos registrados.
- Registrar un nuevo parto.
- Editar información de un parto existente.

Formularios
-----------

Los formularios validan la información clínica y garantizan consistencia en los datos ingresados.

URLs
----

- `/partos/`: listado de partos.
- `/partos/nuevo/`: formulario de registro.
- `/partos/<id>/editar/`: edición de un parto existente.