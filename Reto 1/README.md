# Hackathon-Flipante

## RETO 1 (Puerto Rico - La Chocita)

### Reconocimiento inicial
Este reto consiste en analizar la red de datos de la plataforma social **Eidolon** para seleccionar al grupo ideal de invitados VIP para el concierto de J.P. Miracorta en San Juan, Puerto Rico.

Para resolver el desafío y presentar la solución correcta, se debe analizar lo siguiente:

* **Identificar conexiones de confianza entre personas:** Analizar el core de datos de Eidolon para encontrar grupos de entre **5 y 10 personajes públicos** en los que exista **seguimiento mutuo entre todos** sus integrantes, es decir que cada miembro debe seguir y ser seguido por todos los demás del grupo.


* **Maximizar el alcance único:** Evaluar qué combinación válida de invitados atrae a la mayor cantidad de seguidores distintos en total, teniendo en cuenta que si un fan sigue a varios invitados del grupo, solo debe contabilizarse una vez.

Para ello nos disponen de una página con los datos core de Eidolon, con el fin de acceder a ellos en mediante direcciones en la URL:

Dirección: http://hpecds.comnetconsultores.cloud:7373/

[inserte imagen]

El primer reto que se puede divisar es que no nos dan el endpoint para acceder a los datos de followers, y aparece el mensaje "solo personal autorizado". En cuanto al contenido de los otros 2 endpoints, encontramos que la primera (/api/users) nos da un listado en formato json de los usuarios. Sin embargo solo lista a 500 usuarios, lo cual difiere a la cantidad de usuarios que dice tener Eidolon. La pista de que no son todos los usuarios no las da primeramente el segundo endpoint (/api/users/{id}) en el aparecían más usuarios al colocar un id mayor a 500.

### Inspección de los encabezados HTTP
Para esta segunda fase, gracias a la pista número dos: 

"Cuando un servidor devuelve 'datos restringidos', la información útil a veces viaja por vías distintas al cuerpo del mensaje... aprende a decodificarlo" 

Se dedujo que había que buscar algo en los encabezados al inspeccionar los distintos endpoints. En el endpoint raiz no encontramos nada, tampoco en el endpoint de /api/users. Ya para el endpoint /api/users/{id} concluímos que para darle una inspección completa necesitaríamos una automatización para leer cada uno de los 80600 usuarios y buscar alguna anomalía en sus cabeceras HTTP.

Tambien debido a que al acceder a la ruta raiz (http://hpecds.comnetconsultores.cloud:7373/) no devolvía una página web sino un json, se tenía la teoría de que la comunicación cliente servidor se hacía mediante una API REST, lo cual fue confirmado al acceder a la ruta /openapi.json que es el esquema estandar de OpenApi:

[Inserte imagen]

De aquí observamos cosas interezantes:

* El nombre de la aplicación es "La chocita" y está en su version 1.0.0
* Solo aparecen 3 rutas que tienen habilitado solo el método GET los cuales son: "/", "/api/users" y "/api/users/{user_id}". Esto es importante porque acá no se menciona de otro endpoint relacionado con followers, como se indica en la raíz.
* Tambien estan las reglas y limites en la paginación, lo cual explica el porque solo cargan 500 usuarios cuando se utiliza el endpoint /api/users.

### extracción de datos y detección de anomalías
Como se dijo en la fase anterior, para poder darle una inspeccion completa a todos los usuarios, necesitariamos de una automatización,