# Dataset Xeno-canto

---

## Información General

- __Nombre del dataset:__ Xeno-canto - Bird sounds from around the world.
- __Institución proveedora:__ Xeno-canto Foundation for Nature Sounds.
- __Cantidad de registros:__ 13471.
- __Cobertura geográfica:__ Global (Aunque se centra en Sudamérica, especialmente Argentina).
        Límite oeste: -180
        Límite este: 180
        Límite norte: 90
        Límite sur: -90
- __Cobertura temporal:__ 1900 - Actualidad.
- __Separador de campos:__ Coma (,).
- __Codificación de caracteres (encoding):__ Los datos están codificados en formato UTF-8.
- __Tipo de licencia:__ No especificado claramente (puede variar según el registro y permisos de los autores).
- __Frecuencia de actualización:__ No especificado.
- __Próposito:__ El objetivo de este dataset es recopilar y compartir grabaciones de sonidos de aves a nivel mundial. Forma parte de la colección de Xeno-canto, una base de datos colaborativa donde participantes de todo el mundo aportan grabaciones de fauna. El proyecto busca representar sonidos de todas las especies posibles, incluyendo variabilidad geográfica y diferentes etapas de desarrollo.

---

## Atributos del dataset.
Los siguientes atributos corresponden al archivo principal del dataset y describen las observaciones registradas.

### occurrenceID
__Descripción:__ Un identificador para dwc:Occurrence. En ausencia de un identificador global único persistente, se construye a partir de una combinación de identificadores del registro que lo hagan lo más cercano posible a ser globalmente único.  
__Ejemplo de valores:__ http://arctos.database.museum/guid/MSB:Mamm:233627, 000866d2-c177-4648-a200-ead4007051b9, urn:catalog:UWBM:Bird:89776.

### catalogNumber
__Descripción:__ Un identificador (preferentemente único) para el registro dentro del conjunto de datos o colección.  
__Ejemplo de valores:__ 145732, 145732a, 2008.1334.

### basisOfRecord
__Descripción:__ La naturaleza específica del registro de datos.  
__Ejemplo de valores:__ MaterialEntity, PreservedSpecimen, FossilSpecimen.

### collectionCode
__Descripción:__ El nombre, acrónimo, código o sigla que identifica la colección o conjunto de datos del cual se derivó el registro.  
__Ejemplo de valores:__ Mammals, Hildebrandt, EBIRD.

### dynamicProperties
__Descripción:__ Una lista de mediciones adicionales, hechos, características o afirmaciones sobre el registro. Diseñado para proporcionar un mecanismo de contenido estructurado.  
__Ejemplo de valores:__ {"heightInMeters":1.5}, {"targusLengthInMeters":0.014, "weightInGrams":120}, {"natureOfID":"expert identification", "identificationEvidence":"cytochrome B sequence"}.

### otherCatalogNumbers
__Descripción:__ Una lista (concatenada y separada) de números de catálogo previos o alternativos completamente calificados u otros identificadores usados por humanos para la misma dwc:Occurrence, ya sea en el conjunto de datos actual o en cualquier otro.  
__Ejemplo de valores:__ FMNH:Mammal:1234, NPS YELLO6778 | MBG 33424.

### genus
__Descripción:__ El nombre científico completo del género en el que se clasifica el dwc:Taxon.  
__Ejemplo de valores:__ Puma, Monoclea.

### specificEpithet
__Descripción:__ El nombre del primer epíteto o epíteto de especie del dwc:scientificName.  
__Ejemplo de valores:__ concolor, gottschei.

### infraspecificEpithet
__Descripción:__ El nombre del epíteto infraespecífico más bajo o terminal del dwc:scientificName, excluyendo cualquier designación de rango.  
__Ejemplo de valores:__ concolor (for scientificName Puma concolor concolor (Linnaeus, 1771)), oxyadenia (for scientificName Quercus agrifolia var. oxyadenia (Torr.) J.T. Howell), laxa (for scientificName Cheilanthes hirta f. laxa (Kunze) W.Jacobsen & N.Jacobsen).

### scientificName
__Descripción:__ El nombre científico completo, con información de autoría y fecha si se conoce. Cuando forma parte de un dwc:Identification, debe ser el nombre del nivel taxonómico más bajo que se pueda determinar. Este término no debe contener calificadores de identificación, que deben proporcionarse en dwc:identificationQualifier.  
__Ejemplo de valores:__ Coleoptera (order), Manis (genus), Ctenomys sociabilis (genus + specificEpithet).

### taxonRank
__Descripción:__ El rango taxonómico del nombre más específico en dwc:scientificName.  
__Ejemplo de valores:__ subspecies, varietas, forma.

### kingdom
__Descripción:__ El nombre científico completo del reino en el que se clasifica el dwc:Taxon.  
__Ejemplo de valores:__ Animalia, Archaea, Bacteria.

### family
__Descripción:__ El nombre científico completo de la familia en la que se clasifica el dwc:Taxon.  
__Ejemplo de valores:__ Felidae, Monocleaceae.

### higherClassification
__Descripción:__ Una lista (concatenada y separada) de nombres de taxones que terminan en el rango inmediatamente superior al dwc:Taxon referenciado.  
__Ejemplo de valores:__ Plantae | Tracheophyta | Magnoliopsida | Ranunculales | Ranunculaceae | Ranunculus, Animalia, Animalia | Chordata | Vertebrata | Mammalia | Theria | Eutheria | Rodentia | Hystricognatha | Hystricognathi | Ctenomyidae | Ctenomyini | Ctenomys.

### nomenclaturalCode
__Descripción:__ El código nomenclatural (o códigos en caso de nombres ambiguos) bajo el cual se construye el dwc:scientificName.  
__Ejemplo de valores:__ ICN, ICZN, BC.

### identificationRemarks
__Descripción:__ Comentarios o notas sobre dwc:Identification.  
__Ejemplo de valores:__ Distinguished between Anthus correndera and Anthus hellmayri based on the comparative lengths of the uñas.

### vernacularName
__Descripción:__ Un nombre común o vernáculo.  
__Ejemplo de valores:__ Andean Condor, Condor Andino, Gänsegeier.

### decimalLongitude
__Descripción:__ La longitud geográfica (en grados decimales, utilizando el sistema de referencia espacial indicado en dwc:geodeticDatum) del centro geográfico de un dcterms:Location. Los valores positivos están al este del meridiano de Greenwich, los negativos al oeste. Los valores válidos están entre -180 y 180, inclusive.  
__Ejemplo de valores:__ -121.1761111.

### decimalLatitude
__Descripción:__ La latitud geográfica (en grados decimales, utilizando el sistema de referencia espacial indicado en dwc:geodeticDatum) del centro geográfico de un dcterms:Location. Los valores positivos están al norte del ecuador, los negativos al sur. Los valores válidos están entre -90 y 90, inclusive.  
__Ejemplo de valores:__ -41.0983423.

### geodeticDatum
__Descripción:__ El elipsoide, datum geodésico o sistema de referencia espacial (SRS) en el que se basan las coordenadas geográficas dadas en dwc:decimalLatitude y dwc:decimalLongitude.  
__Ejemplo de valores:__ EPSG:4326, WGS84, NAD27.

### country
__Descripción:__ Nombre del país en el que se registró la observación.
__Ejemplo de valores:__ Denmark, Colombia, España.

### locality
__Descripción:__ Descripción del lugar donde se realizó la observación.
__Ejemplo de valores:__ Bariloche, 25 km NNE via Ruta Nacional 40 (=Ruta 237), Queets Rainforest, Olympic National Park

### verbatimElevation
__Descripción:__ Representación textual de la elevación del lugar de la observación.
__Ejemplo de valores:__ 100m, 200 m

### recordedBy
__Descripción:__ Lista de personas, grupos o agrupaciones que registraron la observación.
__Ejemplo de valores:__ José E. Crespo, Oliver P. Pearson

### eventDate
__Descripción:__ Fecha en la que se registró la observación.
__Ejemplo de valores:__ 2009-02-20T08:40Z, 1809-02-12

### eventTime
__Descripción:__ Horario en la que se registró la observación.
__Ejemplo de valores:__ 08:40:21Z 

### verbatimEventDate
__Descripción:__ Representación textual de la fecha y/o hora de la observación.
__Ejemplo de valores:__ spring 1910, Marzo 2002

### fieldNotes
__Descripción:__ Notas o comentarios adicionales registrados durante la observación.
__Ejemplo de valores:__ Notes available in the Grinnell-Miller Library.

### behavior
__Descripción:__  Comportamiento observado del organismo en el momento del registro.
__Ejemplo de valores:__ roosting, running

### sex
__Descripción:__ Sexo al que pertenece la especie.
__Ejemplo de valores:__ female, male

### lifeStage
__Descripción:__ Edad o etapa en la que se encuentra la especie al momento de la identificación.
__Ejemplo de valores:__ adult, juvenile

### preparations
__Descripción:__ Lista de métodos de preparación y conservación.
__Ejemplo de valores:__ fossil, skin | skull | skeleton.

### references
__Descripción:__ Referencias del dato. (link)
__Ejemplo de valores:__ https://www.iso.org/standard/71341.html

### associatedTaxa
__Descripción:__ Lista de taxones asociados y el tipo de relación con el organismo observado.
__Ejemplo de valores:__ "host":"Quercus alba", "parasitoid of":"Cyclocephala signaticollis" | "predator of":"Apis mellifera"

### rightsHolder
__Descripción:__ Persona u organización que posee los derechos sobre el recurso.
__Ejemplo de valores:__ Bernabe Lopez-Lanus, Franco Vushurovich

### license
__Descripción:__ Un documento legal que otorga permiso oficial para hacer algo con el recurso.
__Ejemplo de valores:__ CC BY-NC