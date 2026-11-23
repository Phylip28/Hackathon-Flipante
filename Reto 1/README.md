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

El primer reto que se puede divisar es que no nos dan la dirección para acceder a los datos de followers, y aparece el mensaje "solo personal autorizado". En cuanto al contenido de las otras dos direcciones, encontramos que la primera (/api/users) nos da un listado en formato json de los usuarios. Sin embargo solo lista a 500 usuarios, lo cual difiere a la cantidad de usuarios que dice tener Eidolon. La pista de que no son todos los usuarios no las da primeramente la segunda dirección (/api/users/{id}) en el aparecían más usuarios al colocar un id mayor a 500. Ahora, gracias a la primera pista entregada, se confirma la cantidad total de usuarios, los cuales son 80,600. 
