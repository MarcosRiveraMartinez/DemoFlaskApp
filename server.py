""" API REST para aprender a utilizar Flask y documentar correctamente

Para ejecucatarla lanzar el comando 'python server.py'
Esta API REST escucha en http://127.0.0.1:5000.

Esta API REST cuenta con los siguientes endpoints. Además se 
especifican los métodos permitidos y una pequeña descripción
de lo que devuelve cada endpoint.
    - GET /options/: muestra los métodos más comunes que pueden 
        utilizarse en una API REST. Además, especifica
        los errores que puede devovler esta API REST
        en concreto.
    - GET /sayhello/: devuelve el saludo 'hola'
    - GET /calculate/<num>: calcula el cuadrado del número
        que se ha pasado en la URL
    - GET /calculate/: acepta el parámetro 'num' (ha de ser 
        un número). Calcula el cuadrado del número pasado como
        parámetro.
    - GET /concatenate/: acepta los parámetros 'cad1' y 'cad2'.
        Estos parámetros han de ser de tipo string. Concatena
        ambos parámetros.
    - GET /users/<id>: dado un 'id' (en la url) de tipo entero
        obtiene y devuelve el usuario con ese id.

Este fichero cuenta con las siguientes funciones:

    * http_error_handler - gestiona los errores HTTP
    * options - controlador que gestiona GET /options/
    * say_hello - controlador que gestiona GET /sayhello/
    * convert_to_int - función para pasar un string a int de
        forma segura
    * calculate_square_number - controlador que gestiona 
        GET /calculate/<num>
    * calculate_square_number_param - controlador que gestiona 
        GET /calculate/
    * concatenate - controlador que gestiona GET /concatenate/
    * get_user - controlador que gestiona GET /users/<id>

Este fichero necesita las siguientes librerías:

    - flask: pip install Flask
    - werkzeug: pip install Werkzeug
"""

from flask import Flask, redirect, jsonify, request
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError, NotFound
from typing import Union, Dict, Any, List, Tuple

# Para el type hinting
JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

# Inicialización de la app
app = Flask(__name__)

# Diccionario de usuarios
users = {
    1: 'Marcos',
    2: 'Paula',
    3: 'Alberto R',
    4: 'Alberto F',
    5: 'Isabel'
}

@app.errorhandler(HTTPException)
def http_error_handler(e: HTTPException) -> Tuple[JSONType, int]:
    """ Gestiona los errores HTTP

    Parameters
    ----------
    e : HTTPException
        Puede ser cualquier excepción del módulo werkzeug.exceptions. 
        Por ejemplo, BadRequest, InternalServerError, NotFound, etc

    Returns
    -------
    json 
        Devuelve el mensaje de error, en formato JSON,
        asociado a la excepción que se le ha pasado como parámetro.
        También devuelve el código de error.
        El mensaje de error tiene la esctructura 
        {message: "Mensaje de error"}
    """

    return jsonify(message=str(e)), e.code

@app.route('/options/', methods = ['GET'])
def options() -> JSONType:
    """ Permite recuperar los métodos más comunes de las
    APIs REST y los errores de esta API

    Returns
    -------
    json 
        Devuelve los métodos más comunes de las APIs REST y 
        los errores de esta API en formato JSON. Su estrcutura
        es la siguiente: 
        {
            'api_methods': {
                'method1': 'description',
                'method2': 'description',
                ...
            },
            'errors': {
                'error1': 'description',
                'error2': 'description',
                ...
            }
        }
    """

    # Métodos más comunes utilizados en las APIs REST
    api_methods = {
        'GET': 'return the information',
        'POST': 'create a resource',
        'DELETE': 'delete some information',
        'PUT': 'update some information'
    }

    # Errores devueltos en esta API REST
    errors = {
        'Error 400': 'Bad Request',
        'Error 404': 'Not Found',
        'Error 405': 'Method Not Allowed',
        'Error 500': 'Internal Server Error'
    }

    return jsonify(api_methods=api_methods, errors=errors)

@app.route('/sayhello/', methods=['GET'])
def say_hello() -> JSONType:
    """ Saluda al usuario

    Returns
    -------
    json 
        Devuelve 'hola' como salida en formato JSON.
        El mensaje devuelto es {'greeting': 'hola'}
    """

    greeting = "hola"

    return jsonify(greeting=greeting)

def convert_to_int(num: str) -> int:
    """ Convierte un string en un entero

    Parameters
    ----------
    num : str
        Es el número que se desea convertir a entero

    Returns
    -------
    num : int
        Devuelve el número convertido en entero

    Raises
    ------
    BadRequest
        - Si 'num' no es un número válido
        - Si 'num' es None
    """

    try:
        num = int(num)
    except ValueError:
        # Esta excepción salta cuando 'num' no es un número
        raise BadRequest('You have not enter a valid number')
    except TypeError:
        # Esta excepción salta cuando 'num' es None
        raise BadRequest('You have not entered a number')
    
    return num

@app.route('/calculate/<num>', methods=['GET'])
def calculate_square_number(num: str) -> JSONType:
    """ Calcula y devuelve el cuadrado de un número.
    Este número se obtiene de la URL de la petición HTTP

    Parameters
    ----------
    num : str
        Es el número sobre el que se desea calcular el cuadrado.
        Viene codificado en la URL

    Returns
    -------
    json 
        Devuelve el cuadrado del número en formato JSON.
        El mensaje tiene la estrcutura {'result': '25'}
    """

    num = convert_to_int(num)
    sqr_num = num ** 2
    return jsonify(result=sqr_num)

@app.route('/calculate/', methods=['GET'])
def calculate_square_number_param() -> JSONType:
    """ Calcula y devuelve el cuadrado de un número.
    Este número se obtiene del parámetro 'num' de la 
    petición HTTP recibida.

    Returns
    -------
    json 
        Devuelve el cuadrado del número en formato JSON.
        El mensaje tiene la estrcutura {'result': '25'}
    """

    # Se obtiene el parámetro 'num' de la petición recibida
    num = request.args.get('num')
    num = convert_to_int(num)
    sqr_num = num ** 2

    return jsonify(result=sqr_num)

@app.route('/concatenate/', methods=['GET'])
def concatenate() -> JSONType:
    """ Concatena 2 strings recibidos como parámetros
    de la petición HTTP. El primer parámetro es 'cad1'.
    El segundo parámetro es 'cad2'.

    Returns
    -------
    json 
        Devuelve la concatenación, en formato JSON, de los
        valores, de tipo string, de los parámetros 'cad1' y 'cad2'.
        El mensaje tiene la estructura {'concatenation': cad1+cad2}

    Raises
    ------
    BadRequest
        - Si no se ha proporcionado el parámetro 'cad1'
        - Si no se ha proporcionado el parámetro 'cad2'
    """

    # Se obtienen los parámetros 'cad1' y 'cad2' de
    # la petición recibida
    cad1 = request.args.get('cad1')
    cad2 = request.args.get('cad2')

    # cad1 no puede ser nulo
    if cad1 is None:
        raise BadRequest("You must provide cad1 parameter")

    # cad2 no puede ser nulo
    if cad2 is None:
        raise BadRequest("You must provide cad2 parameter")

    concatenation = cad1 + cad2

    return jsonify(concatenation=concatenation)

@app.route('/users/<id>')
def get_user(id: int) -> JSONType:
    """ Dado el id del usuario, a través de la url,
    devuelve el nombre de usuario

    Returns
    -------
    json 
        Devuelve el nombre de usuario en formato JSON
        El mensaje tiene la estrcutura {'user': 'nombre del usuario'}

    Raises
    ------
    NotFound
        - Si no se encuentra el usuario
    """

    id = convert_to_int(id)
    user = users.get(id)

    # El usuario no puede ser None
    if user is None:
        raise NotFound('This user does not exist')

    return jsonify(user=user)


if __name__ == "__main__":
    # Ejecuta el servidor en el localhost y puerto 5000
    app.run(host="0.0.0.0", port="5000")