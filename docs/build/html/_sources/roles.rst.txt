Módulo Roles
============

Este módulo define y administra los roles de usuario dentro del sistema, garantizando seguridad y control de acceso.

Modelos
-------

La clase `Rol` representa un rol de usuario con permisos específicos.

Campos principales:
- `nombre`: nombre del rol.
- `permisos`: lista de permisos asociados.

Vistas
------

Las vistas permiten:
- Crear nuevos roles.
- Asignar roles a usuarios.
- Editar permisos de un rol existente.

URLs
----

- `/roles/`: listado de roles.
- `/roles/nuevo/`: creación de un rol.
- `/roles/<id>/editar/`: edición de un rol existente.