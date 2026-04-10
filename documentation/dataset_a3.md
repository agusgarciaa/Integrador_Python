# Dataset iNaturalist

---

## Información General

- __Nombre del dataset:__ iNaturalist Research-grade Observations.
- __Institución proveedora:__ iNaturalist.
- __Cantidad de registros:__ Más de 1.000.000 (el archivo supera el límite de visualización de Excel).
- __Cobertura geográfica:__ Global.
        Límite oeste: 0.0
        Límite este: -1.676
        Límite norte: 89.99
        Límite sur: -84.41
- __Cobertura temporal:__ Los datos corresponden al período comprendido entre 1768/09/17 y 2026/02/16.
- __Separador de campos:__ Coma (,).
- __Codificación de caracteres (encoding):__ Los datos están codificados en formato UTF-8.
- __Tipo de licencia:__ El nombre de la licencia es Creative Commons Attribution-NonCommercial 4.0 International y el tipo es CC BY-NC 4.0(aunque puede variar por registro).
- __Frecuencia de actualización:__ Semanal
- __Próposito:__ El objetivo de este dataset es recopilar y compartir observaciones de biodiversidad, principalmente documentar la presencia de distintas especies en el mundo y el análisis científico de la distribución de especies.
Las observaciones han sido validadas por la comunidad mediante consenso en la identificación de las especies.

---

## Atributos del dataset

### id
__Descripción:__ Identificador interno del registro dentro del dataset.
__Tipo de dato:__ integer / string
__Ejemplo de valores:__ 42369866, 12345678

### occurrenceID
__Descripción:__ Tipo de registro de la observación.
__Tipo de dato:__ string (link)
__Ejemplo de valores:__ http://arctos.database.museum/guid/MSB:Mamm:233627

### basisOfRecord
__Descripción:__ Tipo de registro de la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ MaterialEntity, HumanObservation, Event

### modified
__Descripción:__ Fecha de última modificación del registro.
__Tipo de dato:__ fecha (datetime)
__Ejemplo de valores:__ 2020-10-27T19:46:33Z, 2026-02-16T15:00:21Z

### institutionCode
__Descripción:__ Institución responsable del registro.
__Tipo de dato:__ string
__Ejemplo de valores:__ iNaturalist, MVZ, CLO

### collectionCode
__Descripción:__ Nombre de la colección a la que pertenece el registro.
__Tipo de dato:__ string
__Ejemplo de valores:__ Observations, Mammals

### datasetName
__Descripción:__ Nombre del dataset al que pertenece la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ iNaturalist Research-grade Observations

### informationWithheld
__Descripción:__ Información adicional que existe, pero que no compartió en el registro.
__Tipo de dato:__ string
__Ejemplo de valores:__ Coordinate uncertainty increased to 29304m at the request of the observer.

### catalogNumber
__Descripción:__ Identificador para el registro dentro de los datos.
__Tipo de dato:__ integer / string
__Ejemplo de valores:__ 42369866, 12345678

### references
__Descripción:__ Referencias del dato.
__Tipo de dato:__ string (link)
__Ejemplo de valores:__ https://www.inaturalist.org/observations/254213950

### ocurrenceRemarks
__Descripción:__ Comentarios o anotaciones acerca de las ocurrencias.
__Tipo de dato:__ string
__Ejemplo de valores:__ Al pie de un tala, found dead on road.

### recordedBy
__Descripción:__ Lista de personas, grupos o agrupaciones que registraron la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ José E. Crespo, Oliver P. Pearson

### recordedByID
__Descripción:__ Lista del identificador de las personas, grupos o agrupaciones que registraron la observación. 
__Tipo de dato:__ integer / string
__Ejemplo de valores:__ 254213950

### identifiedBy
__Descripción:__ Lista de personas, grupos o agrupaciones que registraron la identificación de la especie observada.
__Tipo de dato:__ string
__Ejemplo de valores:__ José E. Crespo, James L. Patton

### identifiedByID
__Descripción:__ Lista del identificador de las personas, grupos o agrupaciones que registraron la identificación de la especie observada.
__Tipo de dato:__ integer / string
__Ejemplo de valores:__ 254213950, 254456219

### captive_cultivated
__Descripción:__ Observación del primer organismo en el momento y lugar en el que se lo esperaria encontrar. 
__Tipo de dato:__ string
__Ejemplo de valores:__ wild

### eventDate
__Descripción:__ Fecha en la que se registró la observación.
__Tipo de dato:__ fecha (datetime)
__Ejemplo de valores:__ 2009-02-20T08:40Z, 1809-02-12

### eventTime
__Descripción:__ Horario en la que se registró la observación.
__Tipo de dato:__ fecha (datetime)
__Ejemplo de valores:__ 08:40:21Z 

### verbatimEventDate
__Descripción:__ Representacion de la fecha y/o hora de la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ spring 1910, Marzo 2002

### verbatimLocality
__Descripción:__ Descripción textual del lugar de la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ 25 km NNE Bariloche por R. Nac. 237

### decimalLatitude
__Descripción:__ Latitud geográfica en grados de la observación.
__Tipo de dato:__ float
__Ejemplo de valores:__ -41.0983423

### decimalLongitude
__Descripción:__ Longitud geográfica en grados de la observación.
__Tipo de dato:__ float
__Ejemplo de valores:__ -58.38, -41.0983423

### coordinateUncertaintyInMeters
__Descripción:__ La distancia horizontal (en metros) desde las coordenadas dadas, que describe el círculo más pequeño que contiene toda la ubicación.
__Tipo de dato:__ integer
__Ejemplo de valores:__ 30, 100, 71

### geodeticDatum
__Descripción:__ Sistema de referencia espacial en el que se basan las coordenadas.
__Tipo de dato:__ string
__Ejemplo de valores:__ EPSG:4326, WGS84

### countryCode
__Descripción:__ El código para el país en el que se registró el evento.
__Tipo de dato:__ string
__Ejemplo de valores:__ AR, XZ, SV

### stateProvince
__Descripción:__ Provincia o Estado en el que se registró el evento.
__Tipo de dato:__ string
__Ejemplo de valores:__ Montana, Minas Gerais, Córdoba

### identificationID
__Descripción:__ Identificador para el sujeto observado (Puede ser nombre científico)
__Tipo de dato:__ string
__Ejemplo de valores:__ 9992, 571126901

### dateIdentified
__Descripción:__ Fecha en la que se identificó el evento.
__Tipo de dato:__ fecha (datetime)
__Ejemplo de valores:__ 2009-02-20T08:40Z, 2015-02-12

### identificationRemarks
__Descripción:__ Comentarios o notas acerca de la identificación.
__Tipo de dato:__ string
__Ejemplo de valores:__ Se distinguen Anthus correndera y Anthus hellmayri en función de la longitud comparativa de las uñas.

### taxonID
__Descripción:__ Identificador para el taxón.
__Tipo de dato:__ integer / string
__Ejemplo de valores:__ 32567, 15764

### scientificName
__Descripción:__ Nombre científico de la especie observada.
__Tipo de dato:__ string
__Ejemplo de valores:__ Ambystoma tigrinum diaboli, Senegalia bonariensis

### taxonRank
__Descripción:__ Nivel taxonómico de la identificación.
__Tipo de dato:__ string
__Ejemplo de valores:__ species, genus

### kingdom
__Descripción:__ Reino biológico al que pertenece la especie.
__Tipo de dato:__ string
__Ejemplo de valores:__ Animalia, Plantae

### phylum
__Descripción:__ Categoría phylum a la que pertenece la especie.
__Tipo de dato:__ string
__Ejemplo de valores:__ Chordata, Bryophyta

### class
__Descripción:__ Nombre científico de la clase a la que pertenece la especie.
__Tipo de dato:__ string
__Ejemplo de valores:__ Mammalia, Hepaticopsida

### order
__Descripción:__ Nombre científico de la orden a la que pertenece la especie.
__Tipo de dato:__ string
__Ejemplo de valores:__ Carnivora, Monocleales

### family
__Descripción:__ Nombre científico de la familia a la que pertenece la especie.
__Tipo de dato:__ string
__Ejemplo de valores:__ Felidae, Monocleaceae

### genus
__Descripción:__ Nombre científico del género al que pertenece la especie.
__Tipo de dato:__ string
__Ejemplo de valores:__ Puma, Monoclea

### license
__Descripción:__ Un documento legal que otorga permiso oficial para hacer algo con el recurso.
__Tipo de dato:__ string (link)
__Ejemplo de valores:__ https://creativecommons.org/licenses/by/4.0/

### rightsHolder
__Descripción:__ Persona u organización que posee los derechos sobre el recurso.
__Tipo de dato:__ string
__Ejemplo de valores:__ Pablo H Capovilla

### nick
__Descripción:__ Apodo por el que se encuentra la persona que posee los derechos sobre el recurso.
__Tipo de dato:__ string
__Ejemplo de valores:__ pablohcapovilla

### publishingCountry
__Descripción:__ El código para el país en el que se publicó el recurso.
__Tipo de dato:__ string
__Ejemplo de valores:__ AR, US

### projectId
__Descripción:__ Identificador para el proyecto en el que se encuentra el recurso.
__Tipo de dato:__ integer / string
__Ejemplo de valores:__ 12345678

### sex
__Descripción:__ Sexo al que pertenece la especie.
__Tipo de dato:__ string
__Ejemplo de valores:__ female, male

### lifeStage
__Descripción:__ Edad o etapa en la que se encuentra la especie al momento de la identificación.
__Tipo de dato:__ string
__Ejemplo de valores:__ adult

### reproductiveCondition
__Descripción:__ Condición reproductiva de la especie al momento de la identificación.
__Tipo de dato:__ string

### vitality
__Descripción:__ Indicador sobre el estado de vida de la especie al momento de la identificación.
__Tipo de dato:__ string
__Ejemplo de valores:__ alive

### dynamicProperties
__Descripción:__ Una lista de mediciones, datos, características o afirmaciones adicionales sobre el registro. 
__Ejemplo de valores:__ {"iucnStatus":"vulnerable", "taxonDistribution":"Neuquén, Argentina"} {"relativeHumidity":28, "airTemperatureInCelsius":22, "sampleSizeInKilograms":10}