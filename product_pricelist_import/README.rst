.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
:target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Importar listas de precios
==========================

Este módulo permite importar una lista de precios desde un archivo que puede ser csv
o xls. Una lista de precios corresponde a un proveedor, no está soportado tener varios
proveedores en la misma lista.

Formato del archivo de importación
----------------------------------
**Columnas:** product_code, product_name, list_price, [product_description,] [package_qty,]
[package_uom,] categ, sub_categ, dp, dc1, dc2, ds1, ds2, ds3

Nota:las que estan entre corchetes son opcionales las seis últimas columnas definen su
comportamiento con los dos primeros caracteres del nombre.

**product_code** Es el código del producto, debe ser único y si no lo es odoo generará una
excepción, Esto lo maneja el módulo product_unique_default_code que esta como dependencia.

**product_name** Es el nombre del producto

**list_price** Es el precio de lista del proveedor, el precio al que el proveedor nos sugiere
vender al público, sobre este precio el proveedor nos hace una serie de descuentos.

**product_description** Es la descripción del producto, en este caso el texto no se muestra
en la vista de importación de precios porque ocuparía demasiado espacio.

**package_qty** *Opcional* Indica la cantidad de producto que hay en una caja sirve para aclarar en
la factura la cantidad total de producto que se vende dada la cantida de cajas vendidas.

**package_uom** *Opcional* Indica la unidad de medida del producto que está en la caja.

**categ** Nombre de la categoria de producto puede estar en blanco si la sub_cat esta en blanco

**sub_categ** Nombre de la subcategoria de producto, puede estar en blanco

Las últimas seis columnas son los descuentos, los dos primeros caracteres del nombre de estas
columnas indican donde va a aplicarse el descuento. Los descuentos se pueden aplicar en tres
lugares. La categoría que representa al proveedor, la categoria de producto y la subcategoría
de producto, puede haber mas de un descuento aplicado en el mismo lugar. Los descuentos tienen
signo negativo es un descuento positivo es un incremento.

- dp = se aplica en la categoría que representa al proveedor
- dc = se aplica en la categoria de producto
- ds = se aplica en la subcategoria de producto

En el ejemplo se pusieron dos descuentos para la categoría y tres para la sub categoría
pero se puede cambiar por ejemplo: dc1, ds1, ds2, ds3, ds4 en este caso tendríamos un
descuento para la categoría y cuatro para la sub categoría. El resto del nombre puede ser
cualquier cosa, se estila poner un número que sería el orden de las columnas.

Configuración
-------------
**Proveedores** Cada proveedor que va a enviar una lista de precios debe tener cargada
una categoría, esa categoría representa todos los productos del proveedor. Se estila ponerle
un nombre que tenga que ver con el nombre del proveedor en cuestion.
Hay ejemplos de planillas de importación en tests/test_calc*.xls

Forma de Uso
------------
- Ir a Compras / Listas de precio
- Oprimir *Crear*
- Definir el modo "Agregar productos nuevos" (si el producto existe lo agrega y si no existe lo crea) o "No agregar productos nuevos" (solo actualiza los productos existentes).
- Seleccionar el proveedor (debe tener una categoria asociada).
- Oprimir *Cargar archivo*
- Seleccionar el archivo xls o csv a cargar
- Notar la linea "Descuentos sobre precio de lista" que indica donde van a parar los descuentos de cada columna.
- Oprimir *Procesar*
- Notar la cantidad de errores y revisarlos

Listas de precio
----------------
Para configurar las listas de precio basadas en costo al crear una lista de precios se
debe seleccionar "Precio de costo" que es el precio que calcula este sistema basado en
las planillas importadas.
