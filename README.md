Este es un pequeño programa que esta destiando para la caraga de grandes cantidades de datos.
Actualmente solo puede leer archivos .xlsx y muestra su contenido a traves de una tabla en una base de datos.
El programa permite la creacion, actualizacion y eliminacion de elementos de la tabla.

Instalacion:

Pasos para correr el programa de manera local:

1. Asegurese de tener instalado Python. El programa fue creado y probado en Python 3.9.5
2. Descargue el codigo de GitHub a su carpeta preferida
3. Asegurese que los contenidos de la descarga esten todos en una misma carpeta
4. Abra una terminal, viaje hasta la carpeta donde descargo el codigo y cree un ambiente virtual de python (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
5. Active su ambiente virtual he instale los modulos de: flask, pandas y openpyxl
6. Ejecute el comando 
   > export FLASK_APP=API   (BASH)


   > set FLASK_APP=API      (CMD)


   > $env:FLASK_APP = "API" (PowerShell)
7. Corra el programa usando 
   > flask run
8. Abra una pestaña en su navegador favorito y escriba localhost:5000. Presione enter.
9. Una vez ahi sera recibido por el programa. Siga las indicaciones en pantalla para saber que hacer
10. Una vez terminado el uso del programa cierre su navegador y vuelva a la terminal y cierre la sesion activa del programa (CTRL + cpara windows)

Tenga en cuenta que el programa creara una carpeta llamada 'instance' donde se encuentra para guardar la base de datos que usa durante su ejecucion.
