""" Cliente HTTP para consumir la API 
programada en server.py

Comprueba cada uno de los endpoints de la API. Para ello
utiliza un cliente HTTP programado con la librería requests.
Imprime por pantalla los resultados de cada una de las peticiones
realizadas.

Para ejecucatarlo lanzar el comando 'python client.py'

Este fichero cuenta con las siguientes clases:

    * HttpClient - cliente para realizar peticiones a la API
    * APIChecker - consume la API REST e imprime los resultados

Este fichero cuenta con las siguiente funciones:

    * main - programa principal
        Realiza peticiones a la API e imprime por pantalla
        los resultados

Este fichero necesita las siguientes librerías:

    - requests: pip install requests
"""

import requests
from requests.models import Response

from typing import Union, Dict, List

class HttpClient:
    """Cliente HTTP para consumir una API REST
    
    Este cliente HTTP solo permite realizar peticiones
    HTTP con los métodos GET y POST. Solo puede consumir
    APIs REST que devuelvan los datos en formato JSON.

    Attributes
    ----------
    server_url : str
        Nombre de dominio o IP del servidor junto con el puerto.
        Por ejemplo, http://127.0.0.1:5000
    
    Methods
    -------
    get_request(endpoint, params=None, evaluate_request=True)
        Realiza una petición GET al endpoint especificado.
    post_request(endpoint, data=None, evaluate_request=True)
        Realiza una petición POST al endpoint especificado.
    """

    def __init__(self, server_url: str) -> None:
        """
        Parameters
        ----------
        server_url : str
            Nombre de dominio o IP del servidor junto con el puerto.
            Por ejemplo, http://127.0.0.1:5000

        """

        self.server_url = server_url

    def _evaluate_request(self, req: Response) -> Dict[str, str]:
        """
        Comprueba si se ha llevado a cabo correctamente la 
        petición.

        Parameters
        ----------
        req : requests.models.Response
            Respuesta del servidor.

        Returns
        -------
        result : Dict[str, str]
            Devuelve un diccionario con el contenido
            de la respuesta o con el mensaje
            de error.
            El contenido de la respuesta puede ser accedido a 
            través de la clave 'content'.
            El contenido del mensaje de error puede ser accedido
            a través de la clave 'error'.
        """

        result = {}
        content, error = None, None
        try:
            # Comprueba si la respuesta es correcta a través del 
            # código HTTP. De lo contrario lanza una excepción
            req.raise_for_status()
            # Obtiene el contenido de la respuesta
            content = req.json()
        except requests.exceptions.HTTPError as err:
            # Obtiene el mensaje de error
            error = err.response.json()

        result['content'] = content
        result['error'] = error

        return result

    def get_request(self, endpoint: str, params: Dict[str, str]=None, 
        evaluate_request: bool=True) -> Union[Dict[str, str], Response]:
        """
        Realiza una petición GET al endpoint especificado

        Parameters
        ----------
        endpoint : str
            Endpoint al que se realiza la petición. 
            Por ejemplo, /sayhello/
        params : Dict[str, str]
            Parámetros que irán codificados en la URL.
            El primer valor del diccionario será el nombre
            del parámetro y el segundo será el valor
            del parámetro
        evaluate_request : Boolean
            Si es True evalúa la respuesta del servidor para saber
            si la petición se realizó correctamente.
            Si el False devuelve directamente la respuesta

        Returns
        -------
        result : Union[Dict[str, str], requests.models.Response]
            Si evaluate_request=True:
                Devuelve un diccionario con el contenido
                de la respuesta o con el mensaje
                de error.
                El contenido de la petición puede ser accedido a 
                través de la clave 'content'.
                El contenido del mensaje de error puede ser accedido
                a través de la clave 'error'.
            Si no:
                Devuelve la respuesta de la petición realizada.
        """

        # Se realiza la petición GET
        r = requests.get(self.server_url + endpoint, params=params)

        if evaluate_request:
            # Se comprueba si la petición fue correcta
            # Y se obtiene el contenido de la misma
            return self._evaluate_request(r)

        return r

    def post_request(self, endpoint: str, data: Dict[str, str]=None, 
        evaluate_request: bool=True) -> Union[Dict[str, str], Response]:
        """
        Realiza una petición POST al endpoint especificado

        Parameters
        ----------
        endpoint : str
            Endpoint al que se realiza la petición. 
            Por ejemplo, /sayhello/
        data : Dict[str, str]
            Datos a enviar en el cuerpo de la petición
        evaluate_request : Boolean
            Si es True evalúa si la petición se realizó
            correctamente.
            Si el False devuelve directamente la respuesta

        Returns
        -------
        result : Union[Dict[str, str], requests.models.Response]
            Si evaluate_request=True:
                Devuelve un diccionario con el contenido
                de la petición o con el mensaje
                de error.
                El contenido de la petición puede ser accedido a 
                través de la clave 'content'.
                El contenido del mensaje de error puede ser accedido
                a través de la clave 'error'.
            Si no:
                Devuelve la respuesta de la petición realizada.
        """

        # Se realiza la petición POST
        r = requests.post(self.server_url + endpoint, data=data)

        if evaluate_request:
            # Se comprueba si la petición fue correcta
            # Y se obtiene el contenido de la misma
            return self._evaluate_request(r)

        return r

class APIChecker:
    """Consume una API REST e imprime los resultados obtenidos
    
    Solo se puede utilizar para endpoints que acepten los
    métodos HTTP GET y POST. Esta clase solo puede ser utilizada
    para APIs REST que devuelvan los datos en formato JSON.

    Attributes
    ----------
    http_client : HttpClient
        Cliente HTTP para consumir la API
    
    Methods
    -------
    check_get_requests(urls, params)
        Permite hacer varias peticiones con el método GET
        a la lista de urls especificada. Tambien imprime los
        resultados de cada una de las peticiones.
    check_post_requests(urls, data)
        Permite hacer varias peticiones con el método POST
        a la lista de urls especificada. Tambien imprime los
        resultados de cada una de las peticiones.
    """
    
    def __init__(self, http_client: HttpClient) -> None:
        """
        Parameters
        ----------
        http_client : HttpClient
            Cliente HTTP para consumir la API

        """

        self.http_client = http_client

    def _print_results(self, method: str, url: str, result: Dict[str, str],
        param: Dict[str, str]=None, data: Dict[str, str]=None) -> None:
        """
        Imprime los resultados de la petición

        Parameters
        ----------
        method : str
            Método HTTP utilizado en la petición
        url : str
            URL de la petición
        result : Dict[str, str]
            Resultado de la petición. Si la petición fue 
            correctamente el contenido está disponible bajo
            la clave 'content'.
            Si la petición no fue correctamente, el mensaje
            de error está disponible en la clave 'error'
        param : Dict[str, str]
            Parámetros utilizados en la petición
        data : Dict[str, str]
            Datos utilizados en la petición
        """

        if result.get('error') is None:
            # En caso de error
            print("When \n\t -Method: {} \n\t -Url: {} \n\t -Params: {}  \n\t -Data: {} \n\t -Result: {}"
                .format(method, url, param, data, result.get('content')))
        else:
            # En caso de que la petición haya sido exitosa
            print("When \n\t -Method: {} \n\t -Url: {} \n\t -Params: {}  \n\t -Data: {} \n\t -Error: {} "
                .format(method, url, param, data, result.get('error')))

        # Saltos de línea para dar más legibilidad a la salida
        print("\n\n\n\n\n")

    def check_get_requests(self, urls: List[str], params: List[Dict[str, str]]) -> None:
        """
        Realiza las peticiones GET de las URLs especificadas
        e imprime los resultados por pantalla.

        Parameters
        ----------
        urls : list[str]
            Lista de URLs a las que hacer las peticiones
        params : list[Dict[str, str]]
            Lista de parámetros de cada petición

        NOTA: la longitud de las listas urls y params deben
        coincidir. En caso de que una petición web no contenga
        parámetros debe rellenarse esa posición de la lista con
        None.

        EJEMPLO:
            urls : ['/options/', '/sayhello/', '/calculate/']
            params = [None, None, {'num': '5'}]
        """

        for i in range(0, len(urls)):
            url = urls[i]
            param = params[i]
            # Realiza la petición GET
            result = self.http_client.get_request(url, param)
            # Imprime el contenido de la respuesta o el error producido
            self._print_results('GET', url, result, param=param)

    def check_post_requests(self, urls: List[str], data: List[Dict[str, str]]) -> None:
        """
        Realiza las peticiones POST de las URLs especificadas
        e imprime los resultados por pantalla.

        Parameters
        ----------
        urls : list[str]
            Lista de URLs a las que hacer las peticiones
        data : list[Dict[str, str]]
            Lista de datos de cada petición

        NOTA: la longitud de las listas urls y datos deben
        coincidir. En caso de que una petición web no contenga
        datos debe rellenarse esa posición de la lista con
        None. Si se desea añadir parámetros a la petición se
        deberá codficar en la URL.

        EJEMPLO:
            urls : ['/options/', '/sayhello/', '/calculate/']
            params = [None, None, None]
        """

        for i in range(0, len(urls)):
            url = urls[i]
            d = data[i]
            # Realiza la petición POST
            result = self.http_client.post_request(url, d)
            # Imprime el contenido de la respuesta o el error producido
            self._print_results('POST', url, result, data=d)


def main():
    """
    Función principal del programa.
    
    Se encarga de comprobar el correcto funcionamiento de la API
    programada en el fichero server.py

    Imprime el resultado de cada una de las peticiones realizadas 
    a la API
    """

    # URLs a la que hacer una petición GET
    get_urls = ['/options/', '/sayhello/', '/calculate/5', '/calculate/prueba', '/calculate/', '/calculate/',
                '/concatenate/', '/concatenate/', '/concatenate/', '/concatenate/', '/users/1', '/users/100', '/users/prueba']
    # Parámetros de las peticiones GET
    params = [None, None, None, None, {'num': '5'}, {'num': 'prueba'}, {'cad1': 'Me llamo Marcos ', 'cad2': ' Rivera Martínez'},
                {'cad1': '', 'cad2': 'Rivera Martínez'}, {'cad1': 'Me llamo Marcos ', 'cad2': ''}, {'cad1': '', 'cad2': ''},
                None, None, None]

    # URLs a la que hacer una petición POST
    post_urls = ['/options/', '/sayhello/', '/calculate/5', '/calculate/', '/concatenate/', '/users/1']
    # Datos de las peticiones POST
    data = [None, None, None, None, None, None]

    
    http_client = HttpClient('http://127.0.0.1:5000')
    api_checker = APIChecker(http_client)
    api_checker.check_get_requests(get_urls, params)
    api_checker.check_post_requests(post_urls, data)


if __name__ == "__main__":
    main()