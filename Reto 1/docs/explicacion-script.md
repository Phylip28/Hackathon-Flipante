# Explicación del script de solución

Este documento explica el procesamiento aplicado al CSV de conexiones obtenido del endpoint follows del reto: ¿Cuáles y cuántos usuarios colocar en la zona VIP para alcanzar a la mayor cantidad de gente distinta?

## Condiciones del ejercicio

Elegir **de 5 a 10 figuras** con dos condiciones:

1. Que **se sigan todas entre sí**, en ambos sentidos. Un seguimiento unidireccional no cuenta.
2. Que juntas lleguen al **mayor número de fans diferentes**. Si un fan sigue a varios del grupo,
   se cuenta una sola vez.

Las dos condiciones se condicionan entre sí: la primera define con quién se puede formar grupo; la
segunda, cuál de esos grupos alcanza a más gente. El script resuelve las dos a la vez.

## Carga de los datos

Leemos `follows.csv`, que es una lista de "A sigue a B". Lo recorremos una vez y guardamos dos
cosas: a quién sigue cada usuario y quién sigue a cada figura.

Los seguidores de cada figura se guardan como *bitsets*: la audiencia es un número donde cada bit
indica si un usuario concreto la sigue. Lo usamos porque después hay que **unir audiencias muchas
veces** para contar fans únicos, y con bitsets esa unión y el recuento son operaciones directas y
rápidas. Esto es lo que mantiene el tiempo de ejecución en minutos.

## Grafo de seguimiento mutuo

De todas las conexiones nos quedamos solo con las recíprocas: ponemos una línea entre dos figuras
**solo si cada una sigue a la otra**. Con eso construimos el mapa de relaciones mutuas entre las
600 figuras.

Usamos este grafo porque el reto exige reciprocidad, no popularidad. Trabajar sobre el total de
seguidores no sirve; hay que trabajar sobre las relaciones mutuas.

## Los círculos son *cliques*

Un **clique** es un grupo donde todos están conectados con todos, sin faltar ninguna conexión. Es
exactamente lo que pide el enunciado: un círculo donde nadie queda fuera. Por eso el problema de
"encontrar círculos válidos" se reduce a "encontrar cliques".

Para obtenerlos todos usamos **Bron–Kerbosch** con selección de pivote, que es el algoritmo
estándar para esto y evita explorar ramas inútiles. Devuelve todos los grupos mutuos posibles:
más de cien mil, el mayor de 14 integrantes. Cualquier círculo válido está contenido en ese
conjunto.

## Medir los fans únicos

Falta decidir cuál de esos grupos es el mejor. La condición clave es que un fan compartido por
varias figuras no se cuenta más de una vez. Por eso no sumamos seguidores: calculamos la **unión**
de las audiencias del grupo (la gente distinta a la que llega en total) y descontamos a los
propios miembros, porque una figura no es fan de sí misma.

Esto es el problema de **cobertura máxima**: elegir pocos conjuntos cuya unión abarque a la mayor
cantidad de gente. Coincide con la advertencia del enunciado de no guiarse por las cifras más
altas: no importa quién tiene más seguidores, sino qué combinación aprovecha mejor al conjunto de
la comunidad.

## Encontrar el óptimo sin probarlo todo

Probar todas las combinaciones era inviable por el número de casos. Para obtener la mejor solución
sin ese coste usamos dos ideas.

La primera: **añadir un miembro nunca reduce el alcance**. Por tanto el grupo óptimo tiende a usar
el máximo de 10, y eso orienta el orden de búsqueda.

La segunda: **ramificación y poda**. Antes de analizar los subgrupos de un clique, calculamos el
alcance del clique completo, que es el máximo que podría dar cualquiera de sus subgrupos. Si ese
máximo no supera al mejor círculo ya encontrado, descartamos toda la rama. Recorriendo los
candidatos de mayor a menor alcance, esto elimina casi todo el trabajo y deja solo los que pueden
ganar. El resultado es el **óptimo exacto**, no una aproximación, en un par de minutos.

## Resultado

El círculo ganador es:

```
[80015, 80074, 80149, 80170, 80245, 80288, 80320, 80390, 80443, 80492]
```

Reúne **18.624 fans distintos**. Comparado con la opción directa: las 10 figuras más populares
suman muchos más seguidores sobre el papel, pero sin repetir gente se quedan en unos 13.854
reales, porque comparten buena parte de su audiencia. El círculo óptimo está formado por figuras
con públicos casi sin solapamiento: menos fama individual, más gente distinta en total.

La conclusión del reto: la mejor combinación no es la de los nombres más grandes, sino la que
mejor aprovecha la estructura de conexiones de toda la comunidad.
