# Práctica de Gestión de Proyectos de Base Tecnológica

## 1. Objetivo
Esta práctica tiene como objetivo aprender a programar una API REST en Flask y aprender a documentar correctamente un programa Python.

## 2. API REST
Se ha programado una API REST (fichero server.py), utilizando la librería **Flask** de Python.

Cuenta con los siguientes endpoints:

- GET /options/: muestra los métodos más comunes que pueden utilizarse en una API REST. Además, especifica los errores que puede devovler esta API REST en concreto.
- GET /sayhello/: devuelve el saludo 'hola'
- GET /calculate/\<num\>: calcula el cuadrado del número que se ha pasado en la URL
- GET /calculate/: acepta el parámetro 'num' (ha de ser un número). Calcula el cuadrado del número pasado como parámetro.
- GET /concatenate/: acepta los parámetros 'cad1' y 'cad2'. Estos parámetros han de ser de tipo string. Concatena ambos parámetros.
- GET /users/\<id\>: dado un 'id' (en la url) obtiene y devuelve el usuario con ese id.


## 3. Cliente
También se ha programado un cliente (fichero client.py), utilizando la librería **requests** de Python.
Comprueba e imprime la salida de cada uno de los endpoints de la API REST.

A continuación se muestra la salida del cliente:
```
When
         -Method: GET
         -Url: /sayhello/
         -Params: None
         -Data: None
         -Result: {'greeting': 'hola'}






When
         -Method: GET
         -Url: /calculate/5
         -Params: None
         -Data: None
         -Result: {'result': 25}






When
         -Method: GET
         -Url: /calculate/prueba
         -Params: None
         -Data: None
         -Error: {'message': '400 Bad Request: You have not enter a valid number'}






When
         -Method: GET
         -Url: /calculate/
         -Params: {'num': '5'}
         -Data: None
         -Result: {'result': 25}






When
         -Method: GET
         -Url: /calculate/
         -Params: {'num': 'prueba'}
         -Data: None
         -Error: {'message': '400 Bad Request: You have not enter a valid number'}






When
         -Method: GET
         -Url: /concatenate/
         -Params: {'cad1': 'Me llamo Marcos ', 'cad2': ' Rivera Martínez'}
         -Data: None
         -Result: {'concatenation': 'Me llamo Marcos  Rivera Martínez'}






When
         -Method: GET
         -Url: /concatenate/
         -Params: {'cad1': '', 'cad2': 'Rivera Martínez'}
         -Data: None
         -Result: {'concatenation': 'Rivera Martínez'}






When
         -Method: GET
         -Url: /concatenate/
         -Params: {'cad1': 'Me llamo Marcos ', 'cad2': ''}
         -Data: None
         -Result: {'concatenation': 'Me llamo Marcos '}






When
         -Method: GET
         -Url: /concatenate/
         -Params: {'cad1': '', 'cad2': ''}
         -Data: None
         -Result: {'concatenation': ''}






When
         -Method: GET
         -Url: /users/1
         -Params: None
         -Data: None
         -Result: {'user': 'Marcos'}






When
         -Method: GET
         -Url: /users/100
         -Params: None
         -Data: None
         -Error: {'message': '404 Not Found: This user does not exist'}






When
         -Method: GET
         -Url: /users/prueba
         -Params: None
         -Data: None
         -Error: {'message': '400 Bad Request: You have not enter a valid number'}






When
         -Method: POST
         -Url: /options/
         -Params: None
         -Data: None
         -Error: {'message': '405 Method Not Allowed: The method is not allowed for the requested URL.'}






When
         -Method: POST
         -Url: /sayhello/
         -Params: None
         -Data: None
         -Error: {'message': '405 Method Not Allowed: The method is not allowed for the requested URL.'}






When
         -Method: POST
         -Url: /calculate/5
         -Params: None
         -Data: None
         -Error: {'message': '405 Method Not Allowed: The method is not allowed for the requested URL.'}






When
         -Method: POST
         -Url: /calculate/
         -Params: None
         -Data: None
         -Error: {'message': '405 Method Not Allowed: The method is not allowed for the requested URL.'}






When
         -Method: POST
         -Url: /concatenate/
         -Params: None
         -Data: None
         -Error: {'message': '405 Method Not Allowed: The method is not allowed for the requested URL.'}






When
         -Method: POST
         -Url: /users/1
         -Params: None
         -Data: None
         -Error: {'message': '405 Method Not Allowed: The method is not allowed for the requested URL.'}
```

## 4. Documentación
Para documentar la práctica se ha seguido el enlace proporcionado en la asignatura: https://realpython.com/documenting-python-code/ 

## 5. Ejecución
1. Instalar los requirements:
```
pip install -r requirements.txt
```

2. Ejecución de la API REST:
```
python server.py
```

3. Ejecución del cliente:
```
python client.py
```

**Realizado por: Marcos Rivera Martínez.**