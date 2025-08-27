# src/ui.py
from typing import List, Optional
from datetime import datetime
import uuid
from src.modelos import Estudiante, Curso, Matricula
from src.validaciones import validar_estudiante_completo, validar_correo, validar_documento, validar_fecha, validar_creditos, validar_nota
from src.consultas import ConsultasAcademicas

class InterfazUsuario:
    """Interfaz de usuario para el sistema MiniSIGA"""
    
    def __init__(self, estudiantes: List[Estudiante], cursos: List[Curso], matriculas: List[Matricula]):
        self.estudiantes = estudiantes
        self.cursos = cursos
        self.matriculas = matriculas
        self.consultas = ConsultasAcademicas(estudiantes, cursos, matriculas)
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del sistema"""
        print("\n" + "="*50)
        print("           MINISIGA - SISTEMA ACADÉMICO")
        print("="*50)
        print("1. Estudiantes")
        print("2. Cursos") 
        print("3. Matrículas")
        print("4. Consultas/Reportes")
        print("5. Exportar JSON")
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
    
    def mostrar_menu_matriculas(self):
        """Muestra el menú de gestión de matrículas"""
        print("\n--- GESTIÓN DE MATRÍCULAS ---")
        print("1. Crear matrícula")
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
        nuevo_id = str(uuid.uuid4())[:8]
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
    
    def listar_estudiantes(self):
        """Lista todos los estudiantes"""
        if not self.estudiantes:
            print("No hay estudiantes registrados.")
            return
        
        print(f"\n--- LISTA DE ESTUDIANTES ({len(self.estudiantes)}) ---")
        print(f"{'ID':<10} {'Documento':<12} {'Nombres':<20} {'Apellidos':<20} {'Correo':<25}")
        print("-" * 87)
        
        for estudiante in self.estudiantes:
            print(f"{estudiante.id:<10} {estudiante.documento:<12} {estudiante.nombres:<20} {estudiante.apellidos:<20} {estudiante.correo:<25}")
    
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
    
    def crear_matricula(self):
        """Interfaz para crear una nueva matrícula"""
        print("\n--- CREAR NUEVA MATRÍCULA ---")
        
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
        
        # Verificar que no esté ya matriculado
        for matricula in self.matriculas:
            if (matricula.estudiante_id == estudiante_seleccionado.id and 
                matricula.curso_codigo == curso_seleccionado.codigo):
                print(f"❌ Error: El estudiante ya está matriculado en el curso {curso_seleccionado.codigo}")
                return False
        
        # Crear matrícula
        nueva_matricula = Matricula(
            id=str(uuid.uuid4())[:8],
            estudiante_id=estudiante_seleccionado.id,
            curso_codigo=curso_seleccionado.codigo,
            fecha_matricula=datetime.now().strftime('%Y-%m-%d')
        )
        
        self.matriculas.append(nueva_matricula)
        print(f"✅ Matrícula creada exitosamente. ID: {nueva_matricula.id}")
        print(f"   Estudiante: {estudiante_seleccionado.nombre_completo()}")
        print(f"   Curso: {curso_seleccionado.nombre}")
        return True
    
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
    
    def listar_matriculas(self):
        """Lista todas las matrículas"""
        if not self.matriculas:
            print("No hay matrículas registradas.")
            return
        
        print(f"\n--- LISTA DE MATRÍCULAS ({len(self.matriculas)}) ---")
        print(f"{'ID':<10} {'Estudiante':<25} {'Curso':<15} {'Fecha':<12} {'Nota':<6}")
        print("-" * 68)
        
        for matricula in self.matriculas:
            estudiante = self.consultas.buscar_estudiante_por_id(matricula.estudiante_id)
            curso = self.consultas.buscar_curso_por_codigo(matricula.curso_codigo)
            
            nombre_estudiante = estudiante.nombre_completo() if estudiante else "N/A"
            codigo_curso = curso.codigo if curso else "N/A"
            nota_str = f"{matricula.nota:.1f}" if matricula.nota is not None else "---"
            
            print(f"{matricula.id:<10} {nombre_estudiante:<25} {codigo_curso:<15} {matricula.fecha_matricula:<12} {nota_str:<6}")
    
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