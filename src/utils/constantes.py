# Función 2.c
COLUMNAS_RELEVANTES = {
    "iadiza": [
    "scientificName",
    "recordedBy",
    "eventDate",
    "stateProvince",
    "countryCode",
    "decimalLatitude",
    "decimalLongitude",
    "species",             
    "family",              
    "basisOfRecord",
    ],
    "inaturalist": [
    "scientificName",
    "inaturalistLogin", 
    "eventDate",
    "stateProvince",
    "countryCode",
    "decimalLatitude",
    "decimalLongitude",
    "taxonRank",
    "family",
    "captive", 
    ],
    "xenocanto": [
    "scientificName",
    "vernacularName",
    "recordedBy",
    "eventDate",
    "country",
    "locality",
    "latitudeDecimal",
    "longitudeDecimal",
    "behavior", 
    "sex",
    ]
}

REGISTROS_POR_PAGINA = 10 # Por convención

# Función 6.c
TRADUCCION_COLUMNAS = {
    "scientificName":   "Nombre científico",
    "recordedBy":       "Observador",
    "eventDate":        "Fecha",
    "stateProvince":    "Provincia",
    "countryCode":      "País",
    "country":          "País",
    "decimalLatitude":  "Latitud",
    "decimalLongitude": "Longitud",
    "latitudeDecimal":  "Latitud",
    "longitudeDecimal": "Longitud",
    "species":          "Especie",
    "family":           "Familia",
    "basisOfRecord":    "Tipo de registro",
    "inaturalistLogin": "Usuario iNaturalist",
    "taxonRank":        "Rango taxonómico",
    "captive":          "¿Cautivo?",
    "vernacularName":   "Nombre común",
    "locality":         "Localidad",
    "behavior":         "Comportamiento",
    "sex":              "Sexo",
}

# función 5.a
DATASETS = {
    "iadiza": "occurrence.txt",
    "inaturalist": "observations.csv",
    "xenocanto": "Occurrence.txt",
}