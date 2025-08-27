# src/ui.py - Versión completa con editar y eliminar
from typing import List 
from datetime import datetime
from src.modelos import Estudiante, Curso, Inscripcion, Matricula
from src.validaciones import validar_estudiante_completo, validar_fecha, validar_creditos, validar_nota
from src.consultas import ConsultasAcademicas

class InterfazUsuario:
    """Interfaz de usuario para el sistema MiniSIGA"""
    
    def __init__(self, estudiantes: List[Estudiante], cursos: List[Curso], 
                 inscripciones: List[Inscripcion], matriculas: List[Matricula]):
        self.estudiantes = estudiantes
        self.cursos = cursos
        self.inscripciones = inscripciones
        self.matriculas = matriculas
        self.consultas = ConsultasAcademicas(estudiantes, cursos, inscripciones, matriculas)
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del sistema"""
        print("\n" + "="*50)
        print("           MINISIGA - SISTEMA ACADÉMICO")
        print("="*50)
        print("1. Estudiantes")
        print("2. Cursos") 
        print("3. Inscripciones")
        print("4. Matrículas")
        print("5. Consultas/Reportes")
        print("6. Exportar JSON")
        print("0. Salir")
        print("="*50)
    
    def mostrar_menu_estudiantes(self):
        """Muestra el menú de gestión de estudiantes"""
        print("\n--- GESTIÓN DE ESTUDIANTES ---")
        print("1. Crear estudiante")
        print("2. Editar estudiante")
        print("3. Eliminar estudiante")
        print("4. Listar estudiantes")
        print("0. Volver al menú principal")
    
    def mostrar_menu_cursos(self):
        """Muestra el menú de gestión de cursos"""
        print("\n--- GESTIÓN DE CURSOS ---")
        print("1. Crear curso")
        print("2. Editar curso")
        print("3. Eliminar curso")
        print("4. Listar cursos")
        print("0. Volver al menú principal")
    
    def mostrar_menu_inscripciones(self):
        """Muestra el menú de gestión de inscripciones"""
        print("\n--- GESTIÓN DE INSCRIPCIONES ---")
        print("1. Crear inscripción")
        print("2. Editar inscripción")
        print("3. Eliminar inscripción")
        print("4. Listar inscripciones")
        print("5. Ver inscripciones pendientes de matrícula")
        print("0. Volver al menú principal")
    
    def mostrar_menu_matriculas(self):
        """Muestra el menú de gestión de matrículas"""
        print("\n--- GESTIÓN DE MATRÍCULAS ---")
        print("1. Crear matrícula (desde inscripción)")
        print("2. Asignar nota")
        print("3. Eliminar matrícula")
        print("4. Listar matrículas")
        print("0. Volver al menú principal")
    
    def mostrar_menu_consultas(self):
        """Muestra el menú de consultas y reportes"""
        print("\n--- CONSULTAS Y REPORTES ---")
        print("1. Buscar estudiante por documento")
        print("2. Buscar estudiante por correo")
        print("3. Listar estudiantes ordenados por apellido")
        print("4. Top 3 promedios por curso")
        print("5. Estudiantes reprobados")
        print("6. Créditos inscritos por estudiante")
        print("7. Dominios de correo únicos")
        print("8. Búsqueda binaria por apellido")
        print("0. Volver al menú principal")
    
    def crear_estudiante(self):
        """Interfaz para crear un nuevo estudiante"""
        print("\n--- CREAR NUEVO ESTUDIANTE ---")
        
        datos = {}
        datos['documento'] = input("Documento: ").strip()
        datos['nombres'] = input("Nombres: ").strip()
        datos['apellidos'] = input("Apellidos: ").strip()
        datos['correo'] = input("Correo electrónico: ").strip()
        datos['fecha_nacimiento'] = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
        
        # Validar datos
        errores = validar_estudiante_completo(datos)
        if errores:
            print("\n❌ ERRORES DE VALIDACIÓN:")
            for error in errores:
                print(f"  • {error}")
            return False
        
        # Verificar que el documento no esté duplicado
        for estudiante in self.estudiantes:
            if estudiante.documento == datos['documento']:
                print(f"❌ Error: Ya existe un estudiante con documento {datos['documento']}")
                return False
        
        # Verificar que el correo no esté duplicado
        for estudiante in self.estudiantes:
            if estudiante.correo.lower() == datos['correo'].lower():
                print(f"❌ Error: Ya existe un estudiante con correo {datos['correo']}")
                return False
        
        # Crear estudiante
        nuevo_id = f"est{len(self.estudiantes)+1:03d}"
        nuevo_estudiante = Estudiante(
            id=nuevo_id,
            documento=datos['documento'],
            nombres=datos['nombres'],
            apellidos=datos['apellidos'],
            correo=datos['correo'],
            fecha_nacimiento=datos['fecha_nacimiento']
        )
        
        self.estudiantes.append(nuevo_estudiante)
        print(f"✅ Estudiante creado exitosamente con ID: {nuevo_id}")
        return True
    
    def editar_estudiante(self):
        """Interfaz para editar un estudiante existente"""
        print("\n--- EDITAR ESTUDIANTE ---")
        
        if not self.estudiantes:
            print("❌ No hay estudiantes registrados.")
            return False
        
        # Mostrar estudiantes disponibles
        print("\nEstudiantes disponibles:")
        for i, estudiante in enumerate(self.estudiantes, 1):
            print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()}")
        
        try:
            indice = int(input("\nSeleccione estudiante a editar (número): ")) - 1
            if indice < 0 or indice >= len(self.estudiantes):
                print("❌ Error: Selección inválida")
                return False
            
            estudiante_a_editar = self.estudiantes[indice]
            
            print(f"\n--- EDITANDO: {estudiante_a_editar.nombre_completo()} ---")
            print("Ingrese los nuevos datos (presione Enter para mantener el valor actual):")
            
            # Recopilar nuevos datos
            print(f"Documento actual: {estudiante_a_editar.documento}")
            nuevo_documento = input("Nuevo documento: ").strip()
            if not nuevo_documento:
                nuevo_documento = estudiante_a_editar.documento
            
            print(f"Nombres actuales: {estudiante_a_editar.nombres}")
            nuevos_nombres = input("Nuevos nombres: ").strip()
            if not nuevos_nombres:
                nuevos_nombres = estudiante_a_editar.nombres
            
            print(f"Apellidos actuales: {estudiante_a_editar.apellidos}")
            nuevos_apellidos = input("Nuevos apellidos: ").strip()
            if not nuevos_apellidos:
                nuevos_apellidos = estudiante_a_editar.apellidos
            
            print(f"Correo actual: {estudiante_a_editar.correo}")
            nuevo_correo = input("Nuevo correo: ").strip()
            if not nuevo_correo:
                nuevo_correo = estudiante_a_editar.correo
            
            print(f"Fecha de nacimiento actual: {estudiante_a_editar.fecha_nacimiento}")
            nueva_fecha = input("Nueva fecha de nacimiento (YYYY-MM-DD): ").strip()
            if not nueva_fecha:
                nueva_fecha = estudiante_a_editar.fecha_nacimiento
            
            # Validar nuevos datos
            datos_nuevos = {
                'documento': nuevo_documento,
                'nombres': nuevos_nombres,
                'apellidos': nuevos_apellidos,
                'correo': nuevo_correo,
                'fecha_nacimiento': nueva_fecha
            }
            
            errores = validar_estudiante_completo(datos_nuevos)
            if errores:
                print("\n❌ ERRORES DE VALIDACIÓN:")
                for error in errores:
                    print(f"  • {error}")
                return False
            
            # Verificar duplicados (excluyendo el estudiante actual)
            for estudiante in self.estudiantes:
                if estudiante.id != estudiante_a_editar.id:
                    if estudiante.documento == nuevo_documento:
                        print(f"❌ Error: Ya existe otro estudiante con documento {nuevo_documento}")
                        return False
                    if estudiante.correo.lower() == nuevo_correo.lower():
                        print(f"❌ Error: Ya existe otro estudiante con correo {nuevo_correo}")
                        return False
            
            # Actualizar estudiante
            estudiante_a_editar.documento = nuevo_documento
            estudiante_a_editar.nombres = nuevos_nombres
            estudiante_a_editar.apellidos = nuevos_apellidos
            estudiante_a_editar.correo = nuevo_correo
            estudiante_a_editar.fecha_nacimiento = nueva_fecha
            
            print("✅ Estudiante actualizado exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def eliminar_estudiante(self):
        """Interfaz para eliminar un estudiante"""
        print("\n--- ELIMINAR ESTUDIANTE ---")
        
        if not self.estudiantes:
            print("❌ No hay estudiantes registrados.")
            return False
        
        # Mostrar estudiantes disponibles
        print("\nEstudiantes disponibles:")
        for i, estudiante in enumerate(self.estudiantes, 1):
            print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()}")
        
        try:
            indice = int(input("\nSeleccione estudiante a eliminar (número): ")) - 1
            if indice < 0 or indice >= len(self.estudiantes):
                print("❌ Error: Selección inválida")
                return False
            
            estudiante_a_eliminar = self.estudiantes[indice]
            
            # Verificar si tiene inscripciones o matrículas
            tiene_inscripciones = any(i.estudiante_id == estudiante_a_eliminar.id for i in self.inscripciones)
            tiene_matriculas = any(m.estudiante_id == estudiante_a_eliminar.id for m in self.matriculas)
            
            if tiene_inscripciones or tiene_matriculas:
                print(f"⚠️  ADVERTENCIA: El estudiante {estudiante_a_eliminar.nombre_completo()} tiene registros asociados:")
                if tiene_inscripciones:
                    print("  • Inscripciones activas")
                if tiene_matriculas:
                    print("  • Matrículas registradas")
                
                confirmar = input("¿Desea eliminarlo junto con todos sus registros? (s/N): ").strip().lower()
                if confirmar != 's':
                    print("Eliminación cancelada")
                    return False
                
                # Eliminar inscripciones asociadas
                self.inscripciones = [i for i in self.inscripciones if i.estudiante_id != estudiante_a_eliminar.id]
                
                # Eliminar matrículas asociadas
                self.matriculas = [m for m in self.matriculas if m.estudiante_id != estudiante_a_eliminar.id]
            
            # Eliminar estudiante
            self.estudiantes.remove(estudiante_a_eliminar)
            print(f"✅ Estudiante {estudiante_a_eliminar.nombre_completo()} eliminado exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def listar_estudiantes(self):
        """Lista todos los estudiantes"""
        if not self.estudiantes:
            print("No hay estudiantes registrados.")
            return
        
        print(f"\n--- LISTA DE ESTUDIANTES ({len(self.estudiantes)}) ---")
        print(f"{'ID':<10} {'Documento':<12} {'Nombres':<20} {'Apellidos':<20} {'Correo':<25} {'fecha_nacimiento':<40}")
        print("-" * 140)
        
        for estudiante in self.estudiantes:
            print(f"{estudiante.id:<10} {estudiante.documento:<12} {estudiante.nombres:<20} {estudiante.apellidos:<20} {estudiante.correo:<25} {estudiante.fecha_nacimiento:<1}")
    
    def crear_curso(self):
        """Interfaz para crear un nuevo curso"""
        print("\n--- CREAR NUEVO CURSO ---")
        
        codigo = input("Código del curso: ").strip().upper()
        nombre = input("Nombre del curso: ").strip()
        creditos_str = input("Número de créditos: ").strip()
        docente = input("Nombre del docente: ").strip()
        
        # Validaciones básicas
        if not codigo or not nombre or not docente:
            print("❌ Error: Todos los campos son obligatorios")
            return False
        
        try:
            creditos = int(creditos_str)
        except ValueError:
            print("❌ Error: Los créditos deben ser un número entero")
            return False
        
        if not validar_creditos(creditos):
            print("❌ Error: Los créditos deben estar entre 1 y 10")
            return False
        
        # Verificar que el código no esté duplicado
        for curso in self.cursos:
            if curso.codigo == codigo:
                print(f"❌ Error: Ya existe un curso con código {codigo}")
                return False
        
        # Crear curso
        nuevo_curso = Curso(
            codigo=codigo,
            nombre=nombre,
            creditos=creditos,
            docente=docente
        )
        
        self.cursos.append(nuevo_curso)
        print(f"✅ Curso creado exitosamente con código: {codigo}")
        return True
    
    def editar_curso(self):
        """Interfaz para editar un curso existente"""
        print("\n--- EDITAR CURSO ---")
        
        if not self.cursos:
            print("❌ No hay cursos registrados.")
            return False
        
        # Mostrar cursos disponibles
        print("\nCursos disponibles:")
        for i, curso in enumerate(self.cursos, 1):
            print(f"{i}. {curso.codigo} - {curso.nombre}")
        
        try:
            indice = int(input("\nSeleccione curso a editar (número): ")) - 1
            if indice < 0 or indice >= len(self.cursos):
                print("❌ Error: Selección inválida")
                return False
            
            curso_a_editar = self.cursos[indice]
            
            print(f"\n--- EDITANDO: {curso_a_editar.nombre} ---")
            print("Ingrese los nuevos datos (presione Enter para mantener el valor actual):")
            
            # Recopilar nuevos datos
            print(f"Código actual: {curso_a_editar.codigo}")
            nuevo_codigo = input("Nuevo código: ").strip().upper()
            if not nuevo_codigo:
                nuevo_codigo = curso_a_editar.codigo
            
            print(f"Nombre actual: {curso_a_editar.nombre}")
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if not nuevo_nombre:
                nuevo_nombre = curso_a_editar.nombre
            
            print(f"Créditos actuales: {curso_a_editar.creditos}")
            nuevos_creditos_str = input("Nuevos créditos: ").strip()
            if nuevos_creditos_str:
                try:
                    nuevos_creditos = int(nuevos_creditos_str)
                except ValueError:
                    print("❌ Error: Los créditos deben ser un número entero")
                    return False
                
                if not validar_creditos(nuevos_creditos):
                    print("❌ Error: Los créditos deben estar entre 1 y 10")
                    return False
            else:
                nuevos_creditos = curso_a_editar.creditos
            
            print(f"Docente actual: {curso_a_editar.docente}")
            nuevo_docente = input("Nuevo docente: ").strip()
            if not nuevo_docente:
                nuevo_docente = curso_a_editar.docente
            
            # Verificar duplicado de código (excluyendo el curso actual)
            for curso in self.cursos:
                if curso.codigo != curso_a_editar.codigo and curso.codigo == nuevo_codigo:
                    print(f"❌ Error: Ya existe otro curso con código {nuevo_codigo}")
                    return False
            
            # Actualizar curso
            # Si cambia el código, también actualizar referencias en inscripciones y matrículas
            if nuevo_codigo != curso_a_editar.codigo:
                for inscripcion in self.inscripciones:
                    if inscripcion.curso_codigo == curso_a_editar.codigo:
                        inscripcion.curso_codigo = nuevo_codigo
                
                for matricula in self.matriculas:
                    if matricula.curso_codigo == curso_a_editar.codigo:
                        matricula.curso_codigo = nuevo_codigo
            
            curso_a_editar.codigo = nuevo_codigo
            curso_a_editar.nombre = nuevo_nombre
            curso_a_editar.creditos = nuevos_creditos
            curso_a_editar.docente = nuevo_docente
            
            print("✅ Curso actualizado exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def eliminar_curso(self):
        """Interfaz para eliminar un curso"""
        print("\n--- ELIMINAR CURSO ---")
        
        if not self.cursos:
            print("❌ No hay cursos registrados.")
            return False
        
        # Mostrar cursos disponibles
        print("\nCursos disponibles:")
        for i, curso in enumerate(self.cursos, 1):
            print(f"{i}. {curso.codigo} - {curso.nombre}")
        
        try:
            indice = int(input("\nSeleccione curso a eliminar (número): ")) - 1
            if indice < 0 or indice >= len(self.cursos):
                print("❌ Error: Selección inválida")
                return False
            
            curso_a_eliminar = self.cursos[indice]
            
            # Verificar si tiene inscripciones o matrículas
            tiene_inscripciones = any(i.curso_codigo == curso_a_eliminar.codigo for i in self.inscripciones)
            tiene_matriculas = any(m.curso_codigo == curso_a_eliminar.codigo for m in self.matriculas)
            
            if tiene_inscripciones or tiene_matriculas:
                print(f"⚠️  ADVERTENCIA: El curso {curso_a_eliminar.nombre} tiene registros asociados:")
                if tiene_inscripciones:
                    print("  • Inscripciones activas")
                if tiene_matriculas:
                    print("  • Matrículas registradas")
                
                confirmar = input("¿Desea eliminarlo junto con todos sus registros? (s/N): ").strip().lower()
                if confirmar != 's':
                    print("Eliminación cancelada")
                    return False
                
                # Eliminar inscripciones asociadas
                self.inscripciones = [i for i in self.inscripciones if i.curso_codigo != curso_a_eliminar.codigo]
                
                # Eliminar matrículas asociadas
                self.matriculas = [m for m in self.matriculas if m.curso_codigo != curso_a_eliminar.codigo]
            
            # Eliminar curso
            self.cursos.remove(curso_a_eliminar)
            print(f"✅ Curso {curso_a_eliminar.nombre} eliminado exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def listar_cursos(self):
        """Lista todos los cursos"""
        if not self.cursos:
            print("No hay cursos registrados.")
            return
        
        print(f"\n--- LISTA DE CURSOS ({len(self.cursos)}) ---")
        print(f"{'Código':<10} {'Nombre':<30} {'Créditos':<10} {'Docente':<25}")
        print("-" * 75)
        
        for curso in self.cursos:
            print(f"{curso.codigo:<10} {curso.nombre:<30} {curso.creditos:<10} {curso.docente:<25}")
    
    def crear_inscripcion(self):
        """Interfaz para crear una nueva inscripción"""
        print("\n--- CREAR NUEVA INSCRIPCIÓN ---")
        
        if not self.estudiantes:
            print("❌ Error: No hay estudiantes registrados")
            return False
        
        if not self.cursos:
            print("❌ Error: No hay cursos registrados")
            return False
        
        # Mostrar estudiantes disponibles
        print("\nEstudiantes disponibles:")
        for i, estudiante in enumerate(self.estudiantes, 1):
            print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()}")
        
        try:
            indice_estudiante = int(input("\nSeleccione estudiante (número): ")) - 1
            if indice_estudiante < 0 or indice_estudiante >= len(self.estudiantes):
                print("❌ Error: Selección inválida")
                return False
            estudiante_seleccionado = self.estudiantes[indice_estudiante]
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
        
        # Mostrar cursos disponibles
        print("\nCursos disponibles:")
        for i, curso in enumerate(self.cursos, 1):
            print(f"{i}. {curso.codigo} - {curso.nombre} ({curso.creditos} créditos)")
        
        try:
            indice_curso = int(input("\nSeleccione curso (número): ")) - 1
            if indice_curso < 0 or indice_curso >= len(self.cursos):
                print("❌ Error: Selección inválida")
                return False
            curso_seleccionado = self.cursos[indice_curso]
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
        
        # Verificar que no esté ya inscrito
        for inscripcion in self.inscripciones:
            if (inscripcion.estudiante_id == estudiante_seleccionado.id and 
                inscripcion.curso_codigo == curso_seleccionado.codigo):
                print(f"❌ Error: El estudiante ya está inscrito en el curso {curso_seleccionado.codigo}")
                return False
        
        # Crear inscripción
        nueva_inscripcion = Inscripcion(
            id=f"ins{len(self.inscripciones)+1:03d}",
            estudiante_id=estudiante_seleccionado.id,
            curso_codigo=curso_seleccionado.codigo,
            fecha_inscripcion=datetime.now().strftime('%Y-%m-%d')
        )
        
        self.inscripciones.append(nueva_inscripcion)
        print(f"✅ Inscripción creada exitosamente. ID: {nueva_inscripcion.id}")
        print(f"   Estudiante: {estudiante_seleccionado.nombre_completo()}")
        print(f"   Curso: {curso_seleccionado.nombre}")
        return True
    
    def editar_inscripcion(self):
        """Interfaz para editar una inscripción existente"""
        print("\n--- EDITAR INSCRIPCIÓN ---")
        
        if not self.inscripciones:
            print("❌ No hay inscripciones registradas.")
            return False
        
        # Mostrar inscripciones disponibles
        print("\nInscripciones disponibles:")
        for i, inscripcion in enumerate(self.inscripciones, 1):
            estudiante = self.consultas.buscar_estudiante_por_id(inscripcion.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(inscripcion.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            
            print(f"{i}. {inscripcion.id} - {nombre_estudiante} en {nombre_curso}")
        
        try:
            indice = int(input("\nSeleccione inscripción a editar (número): ")) - 1
            if indice < 0 or indice >= len(self.inscripciones):
                print("❌ Error: Selección inválida")
                return False
            
            inscripcion_a_editar = self.inscripciones[indice]
            
            # Verificar si ya tiene matrícula asociada
            tiene_matricula = any(m.inscripcion_id == inscripcion_a_editar.id for m in self.matriculas)
            if tiene_matricula:
                print("⚠️  Esta inscripción ya tiene una matrícula asociada.")
                print("Solo se puede modificar la fecha de inscripción.")
                
                print(f"Fecha actual: {inscripcion_a_editar.fecha_inscripcion}")
                nueva_fecha = input("Nueva fecha (YYYY-MM-DD) o Enter para mantener: ").strip()
                
                if nueva_fecha and not validar_fecha(nueva_fecha):
                    print("❌ Error: Formato de fecha inválido")
                    return False
                
                if nueva_fecha:
                    inscripcion_a_editar.fecha_inscripcion = nueva_fecha
                    print("✅ Fecha de inscripción actualizada")
                else:
                    print("No se realizaron cambios")
                return True
            
            print(f"\n--- EDITANDO INSCRIPCIÓN: {inscripcion_a_editar.id} ---")
            
            # Cambiar estudiante
            print("\n1. Cambiar estudiante:")
            print(f"   Estudiante actual: {self.consultas.buscar_estudiante_por_id(inscripcion_a_editar.estudiante_id).nombre_completo()}")
            cambiar_estudiante = input("¿Cambiar estudiante? (s/N): ").strip().lower()
            
            nuevo_estudiante_id = inscripcion_a_editar.estudiante_id
            if cambiar_estudiante == 's':
                print("\nEstudiantes disponibles:")
                for i, estudiante in enumerate(self.estudiantes, 1):
                    print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()}")
                
                try:
                    indice_est = int(input("Seleccione nuevo estudiante (número): ")) - 1
                    if 0 <= indice_est < len(self.estudiantes):
                        nuevo_estudiante_id = self.estudiantes[indice_est].id
                    else:
                        print("❌ Selección inválida, manteniendo estudiante actual")
                except ValueError:
                    print("❌ Entrada inválida, manteniendo estudiante actual")
            
            # Cambiar curso
            print("\n2. Cambiar curso:")
            print(f"   Curso actual: {self.consultas.buscar_curso_por_codigo(inscripcion_a_editar.curso_codigo).nombre}")
            cambiar_curso = input("¿Cambiar curso? (s/N): ").strip().lower()
            
            nuevo_curso_codigo = inscripcion_a_editar.curso_codigo
            if cambiar_curso == 's':
                print("\nCursos disponibles:")
                for i, curso in enumerate(self.cursos, 1):
                    print(f"{i}. {curso.codigo} - {curso.nombre}")
                
                try:
                    indice_curso = int(input("Seleccione nuevo curso (número): ")) - 1
                    if 0 <= indice_curso < len(self.cursos):
                        nuevo_curso_codigo = self.cursos[indice_curso].codigo
                    else:
                        print("❌ Selección inválida, manteniendo curso actual")
                except ValueError:
                    print("❌ Entrada inválida, manteniendo curso actual")
            
            # Verificar que no exista duplicado
            if (nuevo_estudiante_id != inscripcion_a_editar.estudiante_id or 
                nuevo_curso_codigo != inscripcion_a_editar.curso_codigo):
                
                for inscripcion in self.inscripciones:
                    if (inscripcion.id != inscripcion_a_editar.id and
                        inscripcion.estudiante_id == nuevo_estudiante_id and 
                        inscripcion.curso_codigo == nuevo_curso_codigo):
                        print("❌ Error: Ya existe una inscripción con esta combinación")
                        return False
            
            # Cambiar fecha
            print(f"\n3. Fecha actual: {inscripcion_a_editar.fecha_inscripcion}")
            nueva_fecha = input("Nueva fecha (YYYY-MM-DD) o Enter para mantener: ").strip()
            if nueva_fecha and not validar_fecha(nueva_fecha):
                print("❌ Error: Formato de fecha inválido")
                return False
            
            # Aplicar cambios
            inscripcion_a_editar.estudiante_id = nuevo_estudiante_id
            inscripcion_a_editar.curso_codigo = nuevo_curso_codigo
            if nueva_fecha:
                inscripcion_a_editar.fecha_inscripcion = nueva_fecha
            
            print("✅ Inscripción actualizada exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def eliminar_inscripcion(self):
        """Interfaz para eliminar una inscripción"""
        print("\n--- ELIMINAR INSCRIPCIÓN ---")
        
        if not self.inscripciones:
            print("❌ No hay inscripciones registradas.")
            return False
        
        # Mostrar inscripciones disponibles
        print("\nInscripciones disponibles:")
        for i, inscripcion in enumerate(self.inscripciones, 1):
            estudiante = self.consultas.buscar_estudiante_por_id(inscripcion.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(inscripcion.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            
            # Verificar si tiene matrícula
            tiene_matricula = any(m.inscripcion_id == inscripcion.id for m in self.matriculas)
            estado = " [CON MATRÍCULA]" if tiene_matricula else ""
            
            print(f"{i}. {inscripcion.id} - {nombre_estudiante} en {nombre_curso}{estado}")
        
        try:
            indice = int(input("\nSeleccione inscripción a eliminar (número): ")) - 1
            if indice < 0 or indice >= len(self.inscripciones):
                print("❌ Error: Selección inválida")
                return False
            
            inscripcion_a_eliminar = self.inscripciones[indice]
            
            # Verificar si tiene matrícula asociada
            matriculas_asociadas = [m for m in self.matriculas if m.inscripcion_id == inscripcion_a_eliminar.id]
            
            if matriculas_asociadas:
                print(f"⚠️  ADVERTENCIA: Esta inscripción tiene {len(matriculas_asociadas)} matrícula(s) asociada(s)")
                confirmar = input("¿Desea eliminarla junto con sus matrículas? (s/N): ").strip().lower()
                if confirmar != 's':
                    print("Eliminación cancelada")
                    return False
                
                # Eliminar matrículas asociadas
                self.matriculas = [m for m in self.matriculas if m.inscripcion_id != inscripcion_a_eliminar.id]
                print(f"  • {len(matriculas_asociadas)} matrícula(s) eliminada(s)")
            
            # Eliminar inscripción
            self.inscripciones.remove(inscripcion_a_eliminar)
            
            estudiante = self.consultas.buscar_estudiante_por_id(inscripcion_a_eliminar.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(inscripcion_a_eliminar.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            
            print(f"✅ Inscripción eliminada exitosamente")
            print(f"   {nombre_estudiante} - {nombre_curso}")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def listar_inscripciones(self):
        """Lista todas las inscripciones"""
        if not self.inscripciones:
            print("No hay inscripciones registradas.")
            return
        
        print(f"\n--- LISTA DE INSCRIPCIONES ({len(self.inscripciones)}) ---")
        print(f"{'ID':<10} {'Estudiante':<25} {'Curso':<15} {'Fecha':<12} {'Estado':<12}")
        print("-" * 74)
        
        for inscripcion in self.inscripciones:
            estudiante = self.consultas.buscar_estudiante_por_id(inscripcion.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(inscripcion.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            codigo_curso = curso.codigo if curso else "N/A"
            
            # Verificar si ya tiene matrícula
            tiene_matricula = any(m.inscripcion_id == inscripcion.id for m in self.matriculas)
            estado = "Matriculado" if tiene_matricula else "Pendiente"
            
            print(f"{inscripcion.id:<10} {nombre_estudiante:<25} {codigo_curso:<15} {inscripcion.fecha_inscripcion:<12} {estado:<12}")
    
    def ver_inscripciones_pendientes(self):
        """Muestra inscripciones pendientes de convertir en matrícula"""
        pendientes = self.consultas.obtener_inscripciones_sin_matricular()
        
        if not pendientes:
            print("✅ No hay inscripciones pendientes de matrícula.")
            return
        
        print(f"\n--- INSCRIPCIONES PENDIENTES DE MATRÍCULA ({len(pendientes)}) ---")
        print(f"{'ID':<10} {'Estudiante':<25} {'Curso':<15} {'Fecha':<12}")
        print("-" * 62)
        
        for inscripcion, estudiante, curso in pendientes:
            print(f"{inscripcion.id:<10} {estudiante.nombre_completo():<25} {curso.codigo:<15} {inscripcion.fecha_inscripcion:<12}")
    
    def crear_matricula(self):
        """Interfaz para crear matrícula desde inscripción"""
        print("\n--- CREAR MATRÍCULA DESDE INSCRIPCIÓN ---")
        
        # Obtener inscripciones pendientes
        pendientes = self.consultas.obtener_inscripciones_sin_matricular()
        
        if not pendientes:
            print("❌ No hay inscripciones pendientes de matrícula.")
            return False
        
        print("\nInscripciones disponibles para matrícula:")
        for i, (inscripcion, estudiante, curso) in enumerate(pendientes, 1):
            print(f"{i}. {inscripcion.id} - {estudiante.nombre_completo()} en {curso.nombre}")
        
        try:
            indice = int(input("\nSeleccione inscripción (número): ")) - 1
            if indice < 0 or indice >= len(pendientes):
                print("❌ Error: Selección inválida")
                return False
            
            inscripcion_seleccionada, estudiante, curso = pendientes[indice]
            
            # Crear matrícula desde inscripción
            nueva_matricula = Matricula.from_inscripcion(
                inscripcion_seleccionada, 
                f"mat{len(self.matriculas)+1:03d}"
            )
            
            self.matriculas.append(nueva_matricula)
            print(f"✅ Matrícula creada exitosamente. ID: {nueva_matricula.id}")
            print(f"   Estudiante: {estudiante.nombre_completo()}")
            print(f"   Curso: {curso.nombre}")
            print(f"   Basada en inscripción: {inscripcion_seleccionada.id}")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def asignar_nota(self):
        """Interfaz para asignar nota a una matrícula"""
        print("\n--- ASIGNAR NOTA ---")
        
        # Mostrar matrículas sin nota
        matriculas_sin_nota = [m for m in self.matriculas if m.nota is None]
        
        if not matriculas_sin_nota:
            print("No hay matrículas pendientes de calificación.")
            return False
        
        print("\nMatrículas pendientes de calificación:")
        for i, matricula in enumerate(matriculas_sin_nota, 1):
            estudiante = self.consultas.buscar_estudiante_por_id(matricula.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula.curso_codigo)
            
            if estudiante and curso:
                print(f"{i}. {estudiante.nombre_completo()} - {curso.nombre} (ID: {matricula.id})")
        
        try:
            indice = int(input("\nSeleccione matrícula (número): ")) - 1
            if indice < 0 or indice >= len(matriculas_sin_nota):
                print("❌ Error: Selección inválida")
                return False
            
            matricula_seleccionada = matriculas_sin_nota[indice]
            
            nota_str = input("Ingrese la nota (0.0 - 5.0): ").strip()
            nota = float(nota_str)
            
            if not validar_nota(nota):
                print("❌ Error: La nota debe estar entre 0.0 y 5.0")
                return False
            
            matricula_seleccionada.nota = nota
            print(f"✅ Nota asignada exitosamente: {nota}")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def eliminar_matricula(self):
        """Interfaz para eliminar una matrícula"""
        print("\n--- ELIMINAR MATRÍCULA ---")
        
        if not self.matriculas:
            print("❌ No hay matrículas registradas.")
            return False
        
        # Mostrar matrículas disponibles
        print("\nMatrículas disponibles:")
        for i, matricula in enumerate(self.matriculas, 1):
            estudiante = self.consultas.buscar_estudiante_por_id(matricula.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            nota_str = f"{matricula.nota:.1f}" if matricula.nota is not None else "Sin nota"
            
            print(f"{i}. {matricula.id} - {nombre_estudiante} en {nombre_curso} ({nota_str})")
        
        try:
            indice = int(input("\nSeleccione matrícula a eliminar (número): ")) - 1
            if indice < 0 or indice >= len(self.matriculas):
                print("❌ Error: Selección inválida")
                return False
            
            matricula_a_eliminar = self.matriculas[indice]
            
            # Mostrar información de la matrícula
            estudiante = self.consultas.buscar_estudiante_por_id(matricula_a_eliminar.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula_a_eliminar.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            nombre_curso = curso.nombre if curso else "N/A"
            nota_str = f"{matricula_a_eliminar.nota:.1f}" if matricula_a_eliminar.nota is not None else "Sin nota"
            
            print(f"\n⚠️  Matrícula a eliminar:")
            print(f"   ID: {matricula_a_eliminar.id}")
            print(f"   Estudiante: {nombre_estudiante}")
            print(f"   Curso: {nombre_curso}")
            print(f"   Nota: {nota_str}")
            print(f"   Fecha: {matricula_a_eliminar.fecha_matricula}")
            
            confirmar = input("\n¿Está seguro de eliminar esta matrícula? (s/N): ").strip().lower()
            if confirmar != 's':
                print("Eliminación cancelada")
                return False
            
            # Eliminar matrícula
            self.matriculas.remove(matricula_a_eliminar)
            print(f"✅ Matrícula {matricula_a_eliminar.id} eliminada exitosamente")
            return True
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
            return False
    
    def listar_matriculas(self):
        """Lista todas las matrículas con información completa"""
        if not self.matriculas:
            print("No hay matrículas registradas.")
            return
        
        print(f"\n--- LISTA DE MATRÍCULAS ({len(self.matriculas)}) ---")
        print(f"{'ID':<10} {'Inscr.ID':<10} {'Estudiante':<25} {'Curso':<15} {'Fecha':<12} {'Nota':<6}")
        print("-" * 88)
        
        for matricula in self.matriculas:
            estudiante = self.consultas.buscar_estudiante_por_id(matricula.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            codigo_curso = curso.codigo if curso else "N/A"
            nota_str = f"{matricula.nota:.1f}" if matricula.nota is not None else "---"
            
            print(f"{matricula.id:<10} {matricula.inscripcion_id:<10} {nombre_estudiante:<25} {codigo_curso:<15} {matricula.fecha_matricula:<12} {nota_str:<6}")
    
    # Métodos de consultas (mantienen la misma funcionalidad)
    def ejecutar_consulta_buscar_documento(self):
        """Ejecuta consulta de búsqueda por documento"""
        documento = input("Ingrese documento a buscar: ").strip()
        estudiante = self.consultas.buscar_estudiante_por_documento(documento)
        
        if estudiante:
            print(f"\n✅ Estudiante encontrado:")
            print(f"   ID: {estudiante.id}")
            print(f"   Documento: {estudiante.documento}")
            print(f"   Nombre: {estudiante.nombre_completo()}")
            print(f"   Correo: {estudiante.correo}")
            print(f"   Fecha nacimiento: {estudiante.fecha_nacimiento}")
        else:
            print(f"❌ No se encontró estudiante con documento {documento}")
    
    def ejecutar_consulta_buscar_correo(self):
        """Ejecuta consulta de búsqueda por correo"""
        correo = input("Ingrese correo a buscar: ").strip()
        estudiante = self.consultas.buscar_estudiante_por_correo(correo)
        
        if estudiante:
            print(f"\n✅ Estudiante encontrado:")
            print(f"   ID: {estudiante.id}")
            print(f"   Documento: {estudiante.documento}")
            print(f"   Nombre: {estudiante.nombre_completo()}")
            print(f"   Correo: {estudiante.correo}")
            print(f"   Fecha nacimiento: {estudiante.fecha_nacimiento}")
        else:
            print(f"❌ No se encontró estudiante con correo {correo}")
    
    def ejecutar_consulta_ordenados_apellido(self):
        """Ejecuta consulta de estudiantes ordenados por apellido"""
        estudiantes_ordenados = self.consultas.listar_estudiantes_ordenados_por_apellido()
        
        if not estudiantes_ordenados:
            print("No hay estudiantes registrados.")
            return
        
        print(f"\n--- ESTUDIANTES ORDENADOS POR APELLIDO ({len(estudiantes_ordenados)}) ---")
        print(f"{'Apellidos':<20} {'Nombres':<20} {'Documento':<12} {'Correo':<25}")
        print("-" * 77)
        
        for estudiante in estudiantes_ordenados:
            print(f"{estudiante.apellidos:<20} {estudiante.nombres:<20} {estudiante.documento:<12} {estudiante.correo:<25}")
    
    def ejecutar_consulta_top_promedios(self):
        """Ejecuta consulta de top 3 promedios por curso"""
        if not self.cursos:
            print("No hay cursos registrados.")
            return
        
        print("\nCursos disponibles:")
        for i, curso in enumerate(self.cursos, 1):
            print(f"{i}. {curso.codigo} - {curso.nombre}")
        
        try:
            indice = int(input("\nSeleccione curso (número): ")) - 1
            if indice < 0 or indice >= len(self.cursos):
                print("❌ Error: Selección inválida")
                return
            
            curso_seleccionado = self.cursos[indice]
            top_estudiantes = self.consultas.obtener_top_promedios_por_curso(curso_seleccionado.codigo)
            
            if not top_estudiantes:
                print(f"No hay notas registradas para el curso {curso_seleccionado.codigo}")
                return
            
            print(f"\n--- TOP 3 PROMEDIOS - {curso_seleccionado.nombre} ---")
            print(f"{'Posición':<10} {'Estudiante':<25} {'Nota':<6}")
            print("-" * 41)
            
            for i, (estudiante, nota) in enumerate(top_estudiantes, 1):
                print(f"{i}°{'':<8} {estudiante.nombre_completo():<25} {nota:.1f}")
                
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
    
    def ejecutar_consulta_reprobados(self):
        """Ejecuta consulta de estudiantes reprobados"""
        reprobados = self.consultas.obtener_reprobados()
        
        if not reprobados:
            print("No hay estudiantes reprobados (nota < 3.0)")
            return
        
        print(f"\n--- ESTUDIANTES REPROBADOS ({len(reprobados)}) ---")
        print(f"{'Estudiante':<25} {'Curso':<15} {'Nota':<6}")
        print("-" * 46)
        
        for estudiante, curso, nota in reprobados:
            print(f"{estudiante.nombre_completo():<25} {curso.codigo:<15} {nota:.1f}")
    
    def ejecutar_consulta_creditos_estudiante(self):
        """Ejecuta consulta de créditos inscritos por estudiante"""
        if not self.estudiantes:
            print("No hay estudiantes registrados.")
            return
        
        print("\nEstudiantes disponibles:")
        for i, estudiante in enumerate(self.estudiantes, 1):
            print(f"{i}. {estudiante.documento} - {estudiante.nombre_completo()}")
        
        try:
            indice = int(input("\nSeleccione estudiante (número): ")) - 1
            if indice < 0 or indice >= len(self.estudiantes):
                print("❌ Error: Selección inválida")
                return
            
            estudiante_seleccionado = self.estudiantes[indice]
            creditos = self.consultas.obtener_creditos_inscritos_por_estudiante(estudiante_seleccionado.id)
            
            print(f"\n--- CRÉDITOS INSCRITOS ---")
            print(f"Estudiante: {estudiante_seleccionado.nombre_completo()}")
            print(f"Total créditos inscritos: {creditos}")
            
        except ValueError:
            print("❌ Error: Debe ingresar un número válido")
    
    def ejecutar_consulta_dominios_correo(self):
        """Ejecuta consulta de dominios de correo únicos"""
        dominios = self.consultas.obtener_dominios_correo_unicos()
        
        if not dominios:
            print("No hay dominios de correo registrados.")
            return
        
        print(f"\n--- DOMINIOS DE CORREO ÚNICOS ({len(dominios)}) ---")
        for i, dominio in enumerate(dominios, 1):
            print(f"{i}. {dominio}")
    
    def ejecutar_busqueda_binaria_apellido(self):
        """Ejecuta búsqueda binaria por apellido"""
        apellido = input("Ingrese apellido a buscar: ").strip()
        estudiante = self.consultas.buscar_binario_estudiante(apellido)
        
        if estudiante:
            print(f"\n✅ Estudiante encontrado (búsqueda binaria):")
            print(f"   ID: {estudiante.id}")
            print(f"   Documento: {estudiante.documento}")
            print(f"   Nombre: {estudiante.nombre_completo()}")
            print(f"   Correo: {estudiante.correo}")
            print(f"   Fecha nacimiento: {estudiante.fecha_nacimiento}")
        else:
            print(f"❌ No se encontró estudiante con apellido {apellido}")