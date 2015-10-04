## Scoring Personal - TP ISW2

### Correr todos los tests

python -m unittest discover tests/ -p '*.py'


### Configurar app de Django para la demo

1. Instalar virtualenvwrapper con `sudo apt-get install virtualenvwrapper`
2. Crear virtual env para el proyecto con `mkvirtualenv scoring`
3. Activar virtualenv con `workon scoring`
4. Instalar dependencias con `pip install -r requirements.txt`
5. Ir al directorio scoring/demo y correr las migraciones para crear las tablas con `python manage.py migrate`
6. Ir a scoring/demo/calculador_de_scoring y copiar el archivo configuracion_ejemplo.py a un archivo configuracion.py en la misma carpeta
7. En el directorio scoring/demo iniciar el servidor con `python manage.py runserver`
8. Entrar a la app en http://localhost:8000
