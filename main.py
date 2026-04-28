import sys
from modelos import Reportador, EncargadoConvivencia, Orientador, Estudiante, ReporteIncidente, Diagnostico, Observacion
from repositorios import RepositorioUsuarios, RepositorioEstudiantes, GestorAntecedentes, RepositorioCasos, RepositorioAcciones
from servicios import ServicioGestionCasos, ServicioGestionAcciones
from utils import print_ui, input_ui, print_accion, print_error, print_arq, Colores

# ==========================================
# CONFIGURACIÓN INICIAL
# ==========================================
repo_usuarios = RepositorioUsuarios()
repo_estudiantes = RepositorioEstudiantes()
gestor_antecedentes = GestorAntecedentes()
repo_casos = RepositorioCasos()
repo_acciones = RepositorioAcciones()

servicio_casos = ServicioGestionCasos(repo_casos, gestor_antecedentes)
servicio_acciones = ServicioGestionAcciones(repo_acciones, repo_casos)

def poblar_datos_prueba():
    repo_usuarios.guardar(EncargadoConvivencia("ENC-1", "111", "Ana Directora", "ana@col.cl"))
    repo_usuarios.guardar(EncargadoConvivencia("ENC-2", "222", "Carlos UTP", "carlos@col.cl"))
    
    repo_usuarios.guardar(Reportador("REP-1", "333", "Luis Profesor", "luis@col.cl"))
    repo_usuarios.guardar(Reportador("REP-2", "444", "María Inspectora", "maria@col.cl"))
    
    repo_usuarios.guardar(Orientador("ORI-1", "555", "Marta Psicóloga", "marta@col.cl"))
    repo_usuarios.guardar(Orientador("ORI-2", "666", "José Orientador", "jose@col.cl"))

    repo_estudiantes.guardar(Estudiante("E1", "999-1", "Juan Pérez", "1 Medio A"))
    repo_estudiantes.guardar(Estudiante("E2", "888-2", "Pedro Gómez", "1 Medio A"))
    repo_estudiantes.guardar(Estudiante("E3", "777-3", "Diego López", "2 Medio B"))

# ==========================================
# UTILIDADES DE INTERFAZ
# ==========================================
def seleccionar_estudiantes() -> list:
    print_ui("\n--- Estudiantes Registrados ---")
    for e in repo_estudiantes.obtener_todos():
        print_ui(f"[{e.id_estudiante}] {e.nombre_completo} - {e.curso}")
    
    seleccionados = []
    while True:
        id_est = input_ui("Ingrese ID del estudiante (o presione Enter para terminar selección): ")
        if not id_est:
            if len(seleccionados) > 0: break
            else: print_error("Debe seleccionar al menos un estudiante."); continue
        
        est = repo_estudiantes.obtener(id_est.upper())
        if est and est not in seleccionados:
            seleccionados.append(est)
            print_accion(f"  -> Agregado: {est.nombre_completo}")
        elif est in seleccionados:
            print_error("  -> Ya está en la lista.")
        else:
            print_error("  -> Estudiante no encontrado.")
    return seleccionados

# ==========================================
# MENÚS POR ROL
# ==========================================
def menu_encargado(usuario_actual):
    while True:
        print_ui(f"\n--- MENÚ ENCARGADO: {usuario_actual.nombre_completo} ---")
        print_ui("1. Abrir nuevo caso")
        print_ui("2. Ver e interactuar con casos existentes")
        print_ui("3. Cerrar sesión")
        opcion = input_ui("Seleccione: ")

        if opcion == "1":
            print_arq("Interfaz Web General", "Enviando solicitud POST a API Gateway...")
            nombre = input_ui("Nombre descriptivo para el caso: ")
            caso = servicio_casos.abrir_caso(nombre, usuario_actual)
            print_accion(f"✅ Caso {caso.id_caso} abierto exitosamente.")
        
        elif opcion == "2":
            casos = repo_casos.obtener_todos()
            if not casos:
                print_error("No hay casos en el sistema.")
                continue
            for c in casos:
                print_ui(f"[{c.id_caso}] {c.nombre_caso} (Estado: {c.estado})")
            
            id_caso = input_ui("\nIngrese ID del caso a explorar (o Enter para cancelar): ")
            caso = repo_casos.obtener(id_caso.upper())
            if caso:
                submenu_caso(caso, usuario_actual)
            
        elif opcion == "3":
            break

def submenu_caso(caso, usuario_actual):
    while True:
        print_ui(f"\n=== DETALLE DEL CASO: {caso.id_caso} - {caso.nombre_caso} ===")
        print_ui(f"Estado: {caso.estado} | Creador: {caso.creador.nombre_completo}")
        print_ui("Estudiantes involucrados: " + (", ".join([e.nombre_completo for e in caso.estudiantes_asociados]) or "Ninguno"))
        print_ui(f"Cronología: {len(caso.antecedentes)} Antecedentes | {len(caso.acciones)} Acciones")
        
        print_ui("\nOpciones:")
        print_ui("1. Ver cronología completa (Antecedentes y Acciones)")
        print_ui("2. Vincular estudiante al caso")
        print_ui("3. Vincular antecedente existente al caso")
        print_ui("4. Derivar acción a Orientador")
        print_ui("5. Cerrar caso")
        print_ui("6. Volver atrás")
        
        op = input_ui("Seleccione: ")
        
        if op == "1":
            print_ui("\n-- ANTECEDENTES --")
            for ant in caso.antecedentes:
                tipo = type(ant).__name__
                print_ui(f"[{ant.id_antecedente}] {tipo} - Creado por: {ant.creador.nombre_completo}")
                print_ui(f"   Involucrados: {', '.join([e.nombre_completo for e in ant.estudiantes_involucrados])}")
            print_ui("-- ACCIONES --")
            for acc in caso.acciones:
                print_ui(f"[{acc.id_accion}] {acc.descripcion} | Encargado: {acc.encargado_asignado.nombre_completo} | Estado: {acc.estado}")
                if acc.resultado: print_ui(f"   Resultado: {acc.resultado}")
        
        elif op == "2":
            print_ui("Estudiantes disponibles:")
            for e in repo_estudiantes.obtener_todos(): print_ui(f"[{e.id_estudiante}] {e.nombre_completo}")
            est = repo_estudiantes.obtener(input_ui("ID del estudiante a vincular: ").upper())
            if est and servicio_casos.asociar_estudiante(caso.id_caso, est):
                print_accion("✅ Estudiante vinculado.")
            else:
                print_error("❌ Fallo la vinculación (verifique ID o si el caso está cerrado).")
                
        elif op == "3":
            print_ui("Antecedentes en el sistema:")
            for ant in gestor_antecedentes.obtener_todos():
                print_ui(f"[{ant.id_antecedente}] {type(ant).__name__} (Alumnos: {', '.join([e.nombre_completo for e in ant.estudiantes_involucrados])})")
            ant = gestor_antecedentes.obtener(input_ui("ID del antecedente a vincular: ").upper())
            if ant and servicio_casos.asociar_antecedente(caso.id_caso, ant):
                print_accion("✅ Antecedente vinculado.")
            else:
                print_error("❌ Fallo la vinculación.")
                
        elif op == "4":
            print_arq("Interfaz Web General", "Enviando solicitud para derivar acción a Controlador de Acciones...")
            desc = input_ui("Descripción de la acción: ")
            print_ui("\nOrientadores disponibles:")
            orientadores = repo_usuarios.obtener_por_rol(Orientador)
            for o in orientadores: print_ui(f"[{o.id_usuario}] {o.nombre_completo}")
            
            ori = repo_usuarios.obtener(input_ui("ID del Orientador: ").upper())
            if ori and isinstance(ori, Orientador):
                accion = servicio_acciones.derivar_accion(caso.id_caso, desc, ori, usuario_actual)
                if accion: print_accion(f"✅ Acción derivada a {ori.nombre_completo}.")
                else: print_error("❌ Error al derivar (¿El caso está cerrado?).")
            else: print_error("❌ Orientador inválido.")
            
        elif op == "5":
            if servicio_casos.cerrar_caso(caso.id_caso):
                print_accion("✅ Caso cerrado. Ya no se admiten modificaciones.")
            else: print_error("❌ El caso ya estaba cerrado.")
            
        elif op == "6":
            break

def menu_reportador(usuario_actual):
    while True:
        print_ui(f"\n--- MENÚ REPORTADOR: {usuario_actual.nombre_completo} ---")
        print_ui("1. Registrar nuevo incidente")
        print_ui("2. Ver mis reportes de incidentes")
        print_ui("3. Cerrar sesión")
        opcion = input_ui("Seleccione: ")

        if opcion == "1":
            print_arq("Interfaz Web General", "Iniciando flujo de registro de incidente hacia API Gateway...")
            estudiantes = seleccionar_estudiantes()
            desc = input_ui("Describa el incidente: ")
            resp = input_ui("Respuesta inmediata tomada: ")
            
            import random 
            id_inc = f"INC-{random.randint(100, 999)}"
            incidente = ReporteIncidente(id_inc, estudiantes, desc, resp, ["General"], usuario_actual)
            gestor_antecedentes.guardar(incidente)
            print_accion("✅ Incidente registrado.")
            
        elif opcion == "2":
            mis_reportes = gestor_antecedentes.obtener_por_creador(usuario_actual.id_usuario)
            if not mis_reportes: print_error("No has registrado reportes.")
            for r in mis_reportes:
                print_ui(f"[{r.id_antecedente}] Alumnos: {', '.join([e.nombre_completo for e in r.estudiantes_involucrados])}")
                print_ui(f"  Detalle: {r.descripcion}")
        
        elif opcion == "3":
            break

def menu_orientador(usuario_actual):
    while True:
        print_ui(f"\n--- MENÚ ORIENTADOR: {usuario_actual.nombre_completo} ---")
        print_ui("1. Ver y completar mis acciones derivadas")
        print_ui("2. Registrar Diagnóstico (1 alumno)")
        print_ui("3. Registrar Observación (Contexto)")
        print_ui("4. Ver mis registros")
        print_ui("5. Cerrar sesión")
        opcion = input_ui("Seleccione: ")

        if opcion == "1":
            acciones = repo_acciones.obtener_por_encargado(usuario_actual.id_usuario)
            pendientes = [a for a in acciones if a.estado != "Completada"]
            if not pendientes: print_error("No tienes acciones pendientes.")
            for a in pendientes:
                print_ui(f"[{a.id_accion}] Tarea: {a.descripcion} (Asignada por: {a.creador.nombre_completo})")
                
            id_acc = input_ui("\nID de acción a completar (o Enter para volver): ").upper()
            if id_acc:
                print_arq("API Gateway", f"Derivando petición PATCH a Controlador de Acciones para {id_acc}...")
                resultado = input_ui("Resultado de la intervención: ")
                if servicio_acciones.completar_accion(id_acc, resultado): print_accion("✅ Acción completada.")
                else: print_error("❌ Fallo al completar.")
                
        elif opcion == "2":
            print_ui("Estudiantes disponibles:")
            for e in repo_estudiantes.obtener_todos(): print_ui(f"[{e.id_estudiante}] {e.nombre_completo}")
            est = repo_estudiantes.obtener(input_ui("ID del estudiante diagnosticado: ").upper())
            
            if est:
                cond = input_ui("Condición detectada: ")
                desc = input_ui("Descripción profesional: ")
                import random
                diag = Diagnostico(f"DIAG-{random.randint(100,999)}", est, cond, desc, usuario_actual)
                gestor_antecedentes.guardar(diag)
                print_accion("✅ Diagnóstico guardado.")
            else: print_error("❌ Estudiante no encontrado.")
            
        elif opcion == "3":
            estudiantes = seleccionar_estudiantes()
            cat = input_ui("Categoría (ej. Familiar, Social): ")
            desc = input_ui("Descripción del contexto: ")
            import random
            obs = Observacion(f"OBS-{random.randint(100,999)}", estudiantes, cat, desc, usuario_actual)
            gestor_antecedentes.guardar(obs)
            print_accion("✅ Observación guardada.")
            
        elif opcion == "4":
            mis_registros = gestor_antecedentes.obtener_por_creador(usuario_actual.id_usuario)
            if not mis_registros: print_error("No has realizado registros.")
            for r in mis_registros:
                print_ui(f"[{r.id_antecedente}] {type(r).__name__} | Alumnos: {', '.join([e.nombre_completo for e in r.estudiantes_involucrados])}")
                
        elif opcion == "5":
            break

# ==========================================
# INICIO DE SISTEMA Y LOGIN
# ==========================================
def main():
    print_arq("Sistema Principal", "Inicializando bases de datos en memoria y poblando datos de prueba...")
    poblar_datos_prueba()
    
    while True:
        print_ui("\n=========================================")
        print_ui("  SISTEMA DE CONVIVENCIA ESCOLAR  ")
        print_ui("=========================================")
        print_ui("Seleccione con quién desea iniciar sesión:")
        
        usuarios = repo_usuarios.obtener_todos()
        for u in usuarios:
            print_ui(f"[{u.id_usuario}] {u.nombre_completo} (Rol: {type(u).__name__})")
        print_ui("[0] Salir del programa")
        
        login_id = input_ui("\nIngrese ID del usuario: ").upper()
        if login_id == "0":
            print_ui("Cerrando sistema...")
            sys.exit()
            
        print_arq("Interfaz Web General", "Enviando solicitud de autenticación al API Gateway...")
        usuario_actual = repo_usuarios.obtener(login_id)
        
        if not usuario_actual:
            print_error("❌ Usuario no encontrado. Intente nuevamente.")
            continue

        print_accion(f"🔓 Sesión iniciada como {usuario_actual.nombre_completo}")

        if isinstance(usuario_actual, EncargadoConvivencia):
            menu_encargado(usuario_actual)
        elif isinstance(usuario_actual, Reportador):
            menu_reportador(usuario_actual)
        elif isinstance(usuario_actual, Orientador):
            menu_orientador(usuario_actual)

if __name__ == "__main__":
    main()
