from datetime import datetime
from typing import List, Optional

# ==========================================
# 1. USUARIOS Y ROLES
# ==========================================
class Usuario:
    def __init__(self, id_usuario: str, rut: str, nombre_completo: str, correo: str):
        self.id_usuario = id_usuario
        self.rut = rut
        self.nombre_completo = nombre_completo
        self.correo = correo

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.nombre_completo}"

class Reportador(Usuario): pass
class EncargadoConvivencia(Usuario): pass
class Orientador(Usuario): pass

# ==========================================
# 2. ESTUDIANTES
# ==========================================
class Estudiante:
    def __init__(self, id_estudiante: str, rut: str, nombre_completo: str, curso: str):
        self.id_estudiante = id_estudiante
        self.rut = rut
        self.nombre_completo = nombre_completo
        self.curso = curso

    def __str__(self):
        return f"{self.nombre_completo} ({self.curso})"

# ==========================================
# 3. ANTECEDENTES
# ==========================================
class Antecedente:
    def __init__(self, id_antecedente: str, estudiantes_involucrados: List[Estudiante], creador: Usuario):
        self.id_antecedente = id_antecedente
        self.fecha_adicion = datetime.now()
        self.estudiantes_involucrados = estudiantes_involucrados
        self.creador = creador # Nuevo: Quién generó el antecedente (Punto 1.2)

class ReporteIncidente(Antecedente):
    # Soporta múltiples estudiantes por defecto al heredar la lista (Punto 5)
    def __init__(self, id_antecedente: str, estudiantes_involucrados: List[Estudiante], 
                 descripcion: str, respuesta_inmediata: str, categorias: List[str], creador: Usuario):
        super().__init__(id_antecedente, estudiantes_involucrados, creador)
        self.descripcion = descripcion
        self.respuesta_inmediata = respuesta_inmediata
        self.categorias = categorias

class Diagnostico(Antecedente):
    # Un diagnóstico suele ser de un alumno a la vez (Punto 9)
    def __init__(self, id_antecedente: str, estudiante: Estudiante, 
                 condicion: str, descripcion: str, creador: Usuario):
        super().__init__(id_antecedente, [estudiante], creador)
        self.condicion = condicion
        self.descripcion = descripcion

class Observacion(Antecedente):
    def __init__(self, id_antecedente: str, estudiantes_involucrados: List[Estudiante], 
                 categoria: str, descripcion: str, creador: Usuario):
        super().__init__(id_antecedente, estudiantes_involucrados, creador)
        self.categoria = categoria
        self.descripcion = descripcion

# ==========================================
# 4. ACCIONES Y CASOS
# ==========================================
class Accion:
    def __init__(self, id_accion: str, descripcion: str, encargado_asignado: Usuario, creador: Usuario):
        self.id_accion = id_accion
        self.descripcion = descripcion
        self.encargado_asignado = encargado_asignado
        self.creador = creador # Nuevo
        self.estado = "Planificada" 
        self.resultado: Optional[str] = None
        self.fecha_emision = datetime.now()
        self.fecha_completacion: Optional[datetime] = None

    def completar(self, resultado: str):
        self.estado = "Completada"
        self.resultado = resultado
        self.fecha_completacion = datetime.now()

class Caso:
    def __init__(self, id_caso: str, nombre_caso: str, creador: Usuario):
        self.id_caso = id_caso
        self.nombre_caso = nombre_caso
        self.creador = creador # Nuevo (Punto 1.2)
        self.estado = "Abierto" 
        self.fecha_inicio = datetime.now()
        self.fecha_cierre: Optional[datetime] = None
        
        self.estudiantes_asociados: List[Estudiante] = []
        self.antecedentes: List[Antecedente] = []
        self.acciones: List[Accion] = []

    def vincular_estudiante(self, estudiante: Estudiante):
        if estudiante not in self.estudiantes_asociados:
            self.estudiantes_asociados.append(estudiante)

    def agregar_antecedente(self, antecedente: Antecedente):
        if antecedente not in self.antecedentes:
            self.antecedentes.append(antecedente)
            # Autovincular estudiantes del antecedente al caso
            for est in antecedente.estudiantes_involucrados:
                self.vincular_estudiante(est)

    def agregar_accion(self, accion: Accion):
        self.acciones.append(accion)

    def cerrar(self):
        self.estado = "Cerrado"
        self.fecha_cierre = datetime.now()