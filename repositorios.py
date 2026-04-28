from typing import List, Dict, Optional, Type
from modelos import Usuario, Estudiante, Antecedente, Caso, Accion, ReporteIncidente, Diagnostico, Observacion
from utils import print_arq # Importamos nuestra herramienta de trazabilidad

class RepositorioUsuarios:
    def __init__(self):
        self._usuarios: Dict[str, Usuario] = {}

    def guardar(self, usuario: Usuario):
        self._usuarios[usuario.id_usuario] = usuario

    def obtener(self, id_usuario: str) -> Optional[Usuario]:
        print_arq("Gestión de Identidad", f"Validando credenciales y rol de {id_usuario} en Sistema Propietario Externo...")
        return self._usuarios.get(id_usuario)

    def obtener_todos(self) -> List[Usuario]:
        return list(self._usuarios.values())
        
    def obtener_por_rol(self, tipo_rol: Type[Usuario]) -> List[Usuario]:
        return [u for u in self._usuarios.values() if isinstance(u, tipo_rol)]

class RepositorioEstudiantes:
    def __init__(self):
        self._estudiantes: Dict[str, Estudiante] = {}

    def guardar(self, estudiante: Estudiante):
        self._estudiantes[estudiante.id_estudiante] = estudiante

    def obtener(self, id_estudiante: str) -> Optional[Estudiante]:
        print_arq("Herramienta de Consultas", f"Obteniendo registro del estudiante {id_estudiante} desde Sistema Propietario Externo...")
        return self._estudiantes.get(id_estudiante)

    def obtener_todos(self) -> List[Estudiante]:
        return list(self._estudiantes.values())

class GestorAntecedentes:
    def __init__(self):
        self._antecedentes: Dict[str, Antecedente] = {}

    def guardar(self, antecedente: Antecedente):
        print_arq("Gestor de Reportes y Antecedentes", f"Persistiendo {type(antecedente).__name__} en Almacenamiento de Antecedentes...")
        self._antecedentes[antecedente.id_antecedente] = antecedente

    def obtener_todos(self) -> List[Antecedente]:
        return list(self._antecedentes.values())

    def obtener(self, id_antecedente: str) -> Optional[Antecedente]:
        return self._antecedentes.get(id_antecedente)

    def obtener_por_creador(self, id_usuario: str) -> List[Antecedente]:
        print_arq("API Gateway -> Gestor de Reportes", f"Consultando historial generado por el usuario {id_usuario}...")
        return [ant for ant in self._antecedentes.values() if ant.creador.id_usuario == id_usuario]

class RepositorioCasos:
    def __init__(self):
        self._casos: Dict[str, Caso] = {}

    def guardar(self, caso: Caso):
        print_arq("Gestor de Casos y Acciones", f"Abstrayendo transacción hacia Almacenamiento de Casos...")
        self._casos[caso.id_caso] = caso

    def obtener(self, id_caso: str) -> Optional[Caso]:
        return self._casos.get(id_caso)

    def obtener_todos(self) -> List[Caso]:
        return list(self._casos.values())

class RepositorioAcciones:
    def __init__(self):
        self._acciones: Dict[str, Accion] = {}

    def guardar(self, accion: Accion):
        print_arq("Gestor de Casos y Acciones", f"Persistiendo nueva acción vinculada a un caso...")
        self._acciones[accion.id_accion] = accion

    def obtener(self, id_accion: str) -> Optional[Accion]:
        return self._acciones.get(id_accion)

    def obtener_por_encargado(self, id_usuario: str) -> List[Accion]:
        print_arq("API Gateway -> Gestor de Casos", f"Recuperando bandeja de acciones para {id_usuario}...")
        return [acc for acc in self._acciones.values() if acc.encargado_asignado.id_usuario == id_usuario]