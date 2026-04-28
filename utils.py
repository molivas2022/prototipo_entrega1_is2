# utils.py

class Colores:
    """Códigos ANSI para colorear el texto en la terminal."""
    UI = '\033[96m'         # Cyan: Navegación, menús, inputs
    ACCION = '\033[92m'     # Verde: Resultados de acciones exitosas
    ERROR = '\033[91m'      # Rojo: Errores o advertencias
    ARQ = '\033[95m'        # Magenta: Mensajes de arquitectura / C4
    RESET = '\033[0m'       # Reset al color base de la terminal

def print_ui(texto, end='\n'):
    """Imprime texto de la interfaz de usuario."""
    print(f"{Colores.UI}{texto}{Colores.RESET}", end=end)

def input_ui(texto) -> str:
    """Solicita un input con el color de la interfaz."""
    return input(f"{Colores.UI}{texto}{Colores.RESET}")

def print_accion(texto):
    """Imprime el resultado de una operación del usuario."""
    print(f"{Colores.ACCION}{texto}{Colores.RESET}")

def print_error(texto):
    """Imprime mensajes de error."""
    print(f"{Colores.ERROR}{texto}{Colores.RESET}")

def print_arq(contenedor, mensaje):
    """
    Imprime un mensaje simulando la comunicación entre componentes
    arquitectónicos (C4).
    """
    print(f"{Colores.ARQ}⚙️  [ARQUITECTURA | {contenedor}] -> {mensaje}{Colores.RESET}")