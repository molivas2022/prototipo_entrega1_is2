from typing import Optional
from modelos import Usuario, Caso, Accion, Antecedente, Estudiante
from repositorios import RepositorioCasos, RepositorioAcciones, GestorAntecedentes
from utils import print_arq # Importamos la herramienta visual

class ServicioGestionCasos:
    def __init__(self, repo_casos: RepositorioCasos, gestor_antecedentes: GestorAntecedentes):
        self.repo_casos = repo_casos
        self.gestor_antecedentes = gestor_antecedentes
        self._contador_casos = 1

    def abrir_caso(self, nombre_caso: str, creador: Usuario) -> Caso:
        id_caso = f"CASO-{self._contador_casos:03d}"
        self._contador_casos += 1
        nuevo_caso = Caso(id_caso, nombre_caso, creador)
        self.repo_casos.guardar(nuevo_caso)
        return nuevo_caso

    def asociar_estudiante(self, id_caso: str, estudiante: Estudiante) -> bool:
        caso = self.repo_casos.obtener(id_caso)
        if caso and caso.estado == "Abierto":
            caso.vincular_estudiante(estudiante)
            return True
        return False

    def asociar_antecedente(self, id_caso: str, antecedente: Antecedente) -> bool:
        print_arq("Gestor de Casos", f"Solicitando cruce de datos al Cliente de Antecedentes para vincular ID {antecedente.id_antecedente}...")
        caso = self.repo_casos.obtener(id_caso)
        if caso and caso.estado == "Abierto":
            caso.agregar_antecedente(antecedente)
            return True
        return False

    def cerrar_caso(self, id_caso: str) -> bool:
        caso = self.repo_casos.obtener(id_caso)
        if caso and caso.estado == "Abierto":
            caso.cerrar()
            print_arq("Notificaciones", "Gatillando alertas a los involucrados de que la investigación ha concluido.")
            print_arq("Servicio de Correos (Externo)", "Enviando correos electrónicos de resumen de resolución.")
            return True
        return False

class ServicioGestionAcciones:
    def __init__(self, repo_acciones: RepositorioAcciones, repo_casos: RepositorioCasos):
        self.repo_acciones = repo_acciones
        self.repo_casos = repo_casos
        self._contador_acciones = 1

    def derivar_accion(self, id_caso: str, descripcion: str, encargado_asignado: Usuario, creador: Usuario) -> Optional[Accion]:
        caso = self.repo_casos.obtener(id_caso)
        if not caso or caso.estado != "Abierto":
            return None
        
        id_accion = f"ACC-{self._contador_acciones:03d}"
        self._contador_acciones += 1
        
        nueva_accion = Accion(id_accion, descripcion, encargado_asignado, creador)
        self.repo_acciones.guardar(nueva_accion)
        caso.agregar_accion(nueva_accion)
        
        print_arq("Notificaciones", f"Construyendo evento de alerta de derivación para el usuario {encargado_asignado.id_usuario}.")
        print_arq("Servicio de Correos (Externo)", f"Enviando correo automatizado a {encargado_asignado.correo}.")
        return nueva_accion

    def completar_accion(self, id_accion: str, resultado: str) -> bool:
        accion = self.repo_acciones.obtener(id_accion)
        if accion and accion.estado != "Completada":
            accion.completar(resultado)
            print_arq("Notificaciones", f"Alertando al encargado de convivencia {accion.creador.nombre_completo} sobre nueva evidencia recolectada.")
            return True
        return False