#crear aplicacion tienda nube

Las entidades expuestas para interactuar vía API son las siguientes: 

-Tienda 
-Producto 
-Variantes de producto 
-Imágenes de producto 
-Categoría 
-Orden 
-Cliente 
-Cupones

Si ya tienen experiencia trabajando con este tipo de integraciones, te 
dejo la documentación completa para que puedas analizarla:
https://github.com/TiendaNube/api-docs

¿Tengo otra opción?
También podrás hacer una carga masiva de tus imágenes vía Dropbox, una 
plataforma que te permite almacenar y sincronizar archivos en línea, al 
igual que compartir archivos y carpetas con otros usuarios.  

Esta funcionalidad les permitirá cargar de manera conjunta y rápida todos 
las fotos de tus productos de tu tienda, como alternativa a la integración vía API.

Te invito a ver el siguiente tutorial, ¿Cómo utilizo la carga masiva de 
imágenes vía Dropbox?, que explica paso a paso cómo hacer la sincronización 
de imágenes y ver si es lo que estás buscando.

#Soporte Tienda Nube
api@tiendanube.com

Flujo de autenticación:

Crear la app desde el perfil de socios comerciales. En la url de redirección le pongo http://makeoverlab.com.ar/nube.php

Luego el cliente accede o mediante link o mediante la tienda de aplicaciones 
al link de instalación, que es siempre de la forma {url_tienda}/admin/apps/{app_id}/authorize
 
en mi caso sería:

https://jeoshops.mitiendanube.com/admin/apps/473/authorize 

Aca te pide la password de administrador de la tienda

Eso redirige al cliente a una pagina donde debe aceptar los permisos que tu app tenga configurada.

Una vez que acepta ese permiso, lo redirigimos a la url que tenés configurada en el perfil de socios comerciales, como url de redirección.
Esto es http://makeoverlab.com.ar/nube.php
Cuando lo redirigimos ahi, se lo envia con un codigo generado por nosotros

http://makeoverlab.com.ar/nube.php?code=240e94c071c95ac665c1c54d29fc5381ca13b7fd

Con ese code, lo que vos debés hacer (que lo hace el php) es hacer un post http a 

curl https://www.tiendanube.com/apps/authorize/token --data 'client_id=473&client_secret=6yMptv2zbiNxCC3BlpnppoxjpUUZ6bCYoMCeC8zSHakrCCki&grant_type=authorization_code&code=240e94c071c95ac665c1c54d29fc5381ca13b7fd'

donde client_id y client_secret ya son datos conocidos desde el perfil, 
y el code es el que recibiste en ese request.

Ese post http te retorna esto, que se muestra en la página (no me anduvo con chrome, lo hice con firefox)

{   "access_token":"d9960ed98ccb85dc290a1919d52f48af2e4e2130",
    "token_type":"bearer",
    "scope":"read_content,write_content,read_products,write_products,read_coupons,write_coupons,read_customers,write_customers,read_orders,write_orders,write_scripts",
    "user_id":424577}" 
}

donde el access_token es el token OAUTH que debés utilizar en los 
request subsiguientes y el user_id es el ID de la tienda

