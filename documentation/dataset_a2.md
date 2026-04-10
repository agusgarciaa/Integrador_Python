## occurrenceID - index = 1
    Descripción: An identifier for the dwc:Occurrence. In the absence of a persistent global unique identifier, construct one from a combination of identifiers in the record that will most closely make the dwc:occurrenceID globally unique.

    Ejemplo de valores: 
    http://arctos.database.museum/guid/MSB:Mamm:233627
    000866d2-c177-4648-a200-ead4007051b9
    urn:catalog:UWBM:Bird:89776

## catalogNumber - index = 2
    Descripción: An identifier (preferably unique) for the record within the data set or collection.

    Ejemplo de valores: 
    145732
    145732a
    2008.1334

## basisOfRecord - index = 3
    Descripción: The specific nature of the data record.

    Ejemplo de valores: MaterialEntity
    PreservedSpecimen
    FossilSpecimen

## collectionCode - index = 4
    Descripción: The name, acronym, coden, or initialism identifying the collection or data set from which the record was derived.

    Ejemplo de valores: 
    Mammals
    Hildebrandt
    EBIRD

## dynamicProperties - index = 5
    Descripción: A list of additional measurements, facts, characteristics, or assertions about the record. Meant to provide a mechanism for structured content.

    Ejemplo de valores: 
    {"heightInMeters":1.5}
    {"targusLengthInMeters":0.014, "weightInGrams":120}
    {"natureOfID":"expert identification", "identificationEvidence":"cytochrome B sequence"}

## otherCatalogNumbers - index = 6
    Descripción: A list (concatenated and separated) of previous or alternate fully qualified catalog numbers or other human-used identifiers for the same dwc:Occurrence, whether in the current or any other data set or collection.

    Ejemplo de valores: 
    FMNH:Mammal:1234
    NPS YELLO6778 | MBG 33424

## genus - index = 7
    Descripción: The full scientific name of the genus in which the dwc:Taxon is classified.

    Ejemplo de valores: 
    Puma
    Monoclea

## specificEpithet - index = 8
    Descripción: The name of the first or species epithet of the dwc:scientificName.

    Ejemplo de valores: 
    concolor
    gottschei

## infraspecificEpithet - index = 9
    Descripción: The name of the lowest or terminal infraspecific epithet of the dwc:scientificName, excluding any rank designation.

    Ejemplo de valores: 
    concolor (for scientificName Puma concolor concolor (Linnaeus, 1771))
    oxyadenia (for scientificName Quercus agrifolia var. oxyadenia (Torr.) J.T. Howell)
    laxa (for scientificName Cheilanthes hirta f. laxa (Kunze) W.Jacobsen & N.Jacobsen)

## scientificName - index = 10
    Descripción: The full scientific name, with authorship and date information if known. When forming part of a dwc:Identification, this should be the name in lowest level taxonomic rank that can be determined. This term should not contain identification qualifications, which should instead be supplied in the dwc:identificationQualifier term.

    Ejemplo de valores: 
    Coleoptera (order)
    Manis (genus)
    Ctenomys sociabilis (genus + specificEpithet)

## taxonRank - index = 11
    Descripción: The taxonomic rank of the most specific name in the dwc:scientificName.

    Ejemplo de valores: 
    subspecies
    varietas
    forma

## kingdom - index = 12
    Descripción: The full scientific name of the kingdom in which the dwc:Taxon is classified.

    Ejemplo de valores: 
    Animalia
    Archaea
    Bacteria

## family - index = 13
    Descripción: The full scientific name of the family in which the dwc:Taxon is classified.

    Ejemplo de valores: 
    Felidae
    Monocleaceae

## higherClassification - index = 14
    Descripción: A list (concatenated and separated) of taxa names terminating at the rank immediately superior to the referenced dwc:Taxon.

    Ejemplo de valores: 
    Plantae | Tracheophyta | Magnoliopsida | Ranunculales | Ranunculaceae | Ranunculus
    Animalia
    Animalia | Chordata | Vertebrata | Mammalia | Theria | Eutheria | Rodentia | Hystricognatha | Hystricognathi | Ctenomyidae | Ctenomyini | Ctenomys

## nomenclaturalCode - index = 15
    Descripción: The nomenclatural code (or codes in the case of an ambiregnal name) under which the dwc:scientificName is constructed.

    Ejemplo de valores: 
    ICN
    ICZN
    BC

## identificationRemarks - index = 16
    Descripción: Comments or notes about the dwc:Identification.

    Ejemplo de valores: 
    Distinguished between Anthus correndera and Anthus hellmayri based on the comparative lengths of the uñas.

## vernacularName - index = 17
    Descripción: A common or vernacular name.

    Ejemplo de valores: 
    Andean Condor
    Condor Andino
    Gänsegeier

## decimalLongitude - index = 18
    Descripción: The geographic longitude (in decimal degrees, using the spatial reference system given in dwc:geodeticDatum) of the geographic center of a dcterms:Location. Positive values are east of the Greenwich Meridian, negative values are west of it. Legal values lie between -180 and 180, inclusive.

    Ejemplo de valores: 
    -121.1761111

## decimalLatitude - index = 19
    Descripción: The geographic latitude (in decimal degrees, using the spatial reference system given in dwc:geodeticDatum) of the geographic center of a dcterms:Location. Positive values are north of the Equator, negative values are south of it. Legal values lie between -90 and 90, inclusive.

    Ejemplo de valores: 
    -41.0983423

## geodeticDatum - index = 20
    Descripción: The ellipsoid, geodetic datum, or spatial reference system (SRS) upon which the geographic coordinates given in dwc:decimalLatitude and dwc:decimalLongitude are based.

    Ejemplo de valores: 
    EPSG:4326
    WGS84
    NAD27


### country
__Descripción:__ Nombre del país en el que se registró la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ Denmark, Colombia, España.

### locality
__Descripción:__ Descripción del lugar donde se realizó la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ Bariloche, 25 km NNE via Ruta Nacional 40 (=Ruta 237), Queets Rainforest, Olympic National Park

### verbatimElevation
__Descripción:__ Representación textual de la elevación del lugar de la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ 100m, 200 m

### recordedBy
__Descripción:__ Lista de personas, grupos o agrupaciones que registraron la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ José E. Crespo, Oliver P. Pearson

### eventDate
__Descripción:__ Fecha en la que se registró la observación.
__Tipo de dato:__ fecha (datetime)
__Ejemplo de valores:__ 2009-02-20T08:40Z, 1809-02-12

### eventTime
__Descripción:__ Horario en la que se registró la observación.
__Tipo de dato:__ hora (datetime) 
__Ejemplo de valores:__ 08:40:21Z 

### verbatimEventDate
__Descripción:__ Representación textual de la fecha y/o hora de la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ spring 1910, Marzo 2002

### fieldNotes
__Descripción:__ Notas o comentarios adicionales registrados durante la observación.
__Tipo de dato:__ string
__Ejemplo de valores:__ Notes available in the Grinnell-Miller Library.

### behavior
__Descripción:__  Comportamiento observado del organismo en el momento del registro.
__Tipo de dato:__ string
__Ejemplo de valores:__ roosting, running

### sex
__Descripción:__ Sexo al que pertenece la especie.
__Tipo de dato:__ string
__Ejemplo de valores:__ female, male


### lifeStage
__Descripción:__ Edad o etapa en la que se encuentra la especie al momento de la identificación.
__Tipo de dato:__ string
__Ejemplo de valores:__ adult, juvenile

### preparations
__Descripción:__ Lista de métodos de preparación y conservación.
__Tipo de dato:__ string
__Ejemplo de valores:__ fossil, skin | skull | skeleton.

### references
__Descripción:__ Referencias del dato.
__Tipo de dato:__ string (link)
__Ejemplo de valores:__ https://www.iso.org/standard/71341.html

### associatedTaxa
__Descripción:__ Lista de taxones asociados y el tipo de relación con el organismo observado.
__Tipo de dato:__ string
__Ejemplo de valores:__ "host":"Quercus alba", "parasitoid of":"Cyclocephala signaticollis" | "predator of":"Apis mellifera"

### rightsHolder
__Descripción:__ Persona u organización que posee los derechos sobre el recurso.
__Tipo de dato:__ string
__Ejemplo de valores:__ Bernabe Lopez-Lanus, Franco Vushurovich

### license
__Descripción:__ Un documento legal que otorga permiso oficial para hacer algo con el recurso.
__Tipo de dato:__ string (link o código de licencia)
__Ejemplo de valores:__ CC BY-NC