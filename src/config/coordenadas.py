"""
Coordenadas geográficas de los municipios de Yucatán
Diccionario con latitud y longitud para el mapa
"""

COORDENADAS_MUNICIPIOS = {
    'MERIDA': (20.9674, -89.5926),
    'TIZIMIN': (21.1442, -88.1538),
    'TZUCACAB': (20.0833, -89.0500),
    'PETO': (20.1333, -88.9167),
    'TEMAX': (21.1833, -89.0167),
    'BUCTZOZ': (21.1167, -89.0500),
    'OXKUTZCAB': (20.3017, -89.4189),
    'IZAMAL': (20.9308, -89.0181),
    'UMAN': (20.8833, -89.7500),
    'TEKAX': (20.2069, -89.2911),
    'SUCILA': (21.0833, -88.4000),
    'VALLADOLID': (20.6897, -88.2011),
    'MOTUL': (21.0931, -89.2911),
    'TICUL': (20.4008, -89.5364),
    'MAXCANU': (20.5833, -90.0167),
    'CELESTUN': (20.8581, -90.3997),
    'CONKAL': (21.0819, -89.5164),
    'KANASIN': (20.9439, -89.5600),
    'PROGRESO': (21.2808, -89.6647),
    'CHICXULUB': (21.2500, -89.5833),
    'CUZAMA': (20.8500, -89.3500),
    'DZILAM': (21.3833, -88.9000),
    'HOCTUN': (20.8667, -89.2000),
    'MAMA': (20.4500, -89.4833),
    'MUNA': (20.4833, -89.7167),
    'PANABA': (21.2833, -88.2667),
    'SEYE': (20.7000, -89.6833),
    'TEPAKAN': (20.2333, -90.0333),
    'TIXKOKOB': (21.0167, -89.4000),
    'TIXMEHUAC': (20.6333, -88.9500),
    'TIXPEHUAL': (21.1000, -89.5333),
    'TUNKAS': (21.0833, -88.8333),
    'CHICHIMILA': (20.6333, -88.2833),
    'CHOCHOLA': (20.9167, -89.8667),
    'ACAKAH': (20.2833, -90.0667),
    'MAYAPAN': (20.3333, -89.4667),
    'MOCEL': (21.2333, -89.4667),
    'CULUCUM': (20.8667, -88.4333),
    'DZINDZANTUN': (21.2333, -89.7833),
    'TEMOZON': (21.2167, -88.0333),
    'TEKANTO': (21.0500, -88.7333),
    'TINUM': (20.6500, -88.6000),
    'UXMAL': (20.3583, -89.7667),
    'YAXCABA': (20.6500, -89.0500),
    'YAXKUKUL': (21.1000, -89.6333)
}


def obtener_coordenadas(municipio):
    """
    Obtiene las coordenadas (lat, lon) de un municipio.
    Si no existe, devuelve coordenadas del centro de Yucatán.

    Args:
        municipio (str): Nombre del municipio

    Returns:
        tuple: (latitud, longitud)
    """
    return COORDENADAS_MUNICIPIOS.get(
        str(municipio).upper().strip(),
        (20.7, -89.0)  # Coordenadas por defecto (centro de Yucatán)
    )
