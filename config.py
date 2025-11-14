# =========================================================
#                   CONFIG.PY
# =========================================================

# --- CONFIGURACIÓN DE PANTALLA ---
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 60

# --- COLORES ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# --- FUENTE ---
FONT_NAME = "Arial" # Puedes cambiar esto si tienes una fuente específica

# --- PERSONAJES DEL JUGADOR (EL ORDEN QUE PEDISTE) ---
# Marco es el inicial [0], Levi es el último [9]
PERSONAJES_104 = [
    "Marco", 
    "Armin",
    "Connie",
    "Jean",
    "Sasha",
    "Historia",
    "Annie",
    "Mikasa",
    "Eren",
    "Levi"  
] 

# --- TITANES ---
# El sprite del titán puro que subiste
TITAN_PURO_SPRITE_NAME = "titan_puro" 

# Aunque no tienes sprites de cambiantes, se deja la lista para evitar errores
TITANES_CAMBIANTES = [
    "titan_acorazado", 
    "titan_bestia", 
    "titan_colosal"
]

# --- ESTADÍSTICAS DEL JUGADOR ---
PLAYER_SPEED = 5
PLAYER_BASE_HEALTH = 100
PLAYER_BASE_DAMAGE = 10
XP_PER_LEVEL = 100

# --- ESTADÍSTICAS DE TITANES ---
TITAN_BASE_SPEED = 0.5
TITAN_BASE_HEALTH = 20
TITAN_BASE_DAMAGE = 5