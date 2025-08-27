# src/persistencia.py - Versión actualizada con manejo de inscripciones
import csv
import json
import os
from typing import List
from src.modelos import Estudiante, Curso, Inscripcion, Matricula

class PersistenciaCSV:
    """Maneja la persistencia de datos en archivos CSV"""
    
    def __init__(self, base_path: str = "datos"):
        self.base_path = base_path
        self.crear_directorio()
    
    def crear_directorio(self):
        """Crea el directorio de datos si no existe"""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def cargar_estudiantes(self) -> List[Estudiante]:
        """Carga estudiantes desde CSV"""
        archivo = os.path.join(self.base_path, "estudiantes.csv")
        estudiantes = []
        
        if not os.path.exists(archivo):
            return estudiantes
        
        try:
            with open(archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    estudiante = Estudiante(
                        id=row['id'].strip(),
                        documento=row['documento'].strip(),
                        nombres=row['nombres'].strip(),
                        apellidos=row['apellidos'].strip(),
                        correo=row['correo'].strip(),
                        fecha_nacimiento=row['fecha_nacimiento'].strip()
                    )
                    estudiantes.append(estudiante)
        except Exception as e:
            print(f"Error cargando estudiantes: {e}")
        
        return estudiantes
    
    def guardar_estudiantes(self, estudiantes: List[Estudiante]):
        """Guarda estudiantes en CSV"""
        archivo = os.path.join(self.base_path, "estudiantes.csv")
        
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            if estudiantes:
                fieldnames = ['id', 'documento', 'nombres', 'apellidos', 'correo', 'fecha_nacimiento']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for estudiante in estudiantes:
                    writer.writerow({
                        'id': estudiante.id,
                        'documento': estudiante.documento,
                        'nombres': estudiante.nombres,
                        'apellidos': estudiante.apellidos,
                        'correo': estudiante.correo,
                        'fecha_nacimiento': estudiante.fecha_nacimiento
                    })
    
    def cargar_cursos(self) -> List[Curso]:
        """Carga cursos desde CSV"""
        archivo = os.path.join(self.base_path, "cursos.csv")
        cursos = []
        
        if not os.path.exists(archivo):
            return cursos
        
        try:
            with open(archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    curso = Curso(
                        codigo=row['codigo'].strip(),
                        nombre=row['nombre'].strip(),
                        creditos=int(row['creditos']),
                        docente=row['docente'].strip()
                    )
                    cursos.append(curso)
        except Exception as e:
            print(f"Error cargando cursos: {e}")
        
        return cursos
    
    def guardar_cursos(self, cursos: List[Curso]):
        """Guarda cursos en CSV"""
        archivo = os.path.join(self.base_path, "cursos.csv")
        
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            if cursos:
                fieldnames = ['codigo', 'nombre', 'creditos', 'docente']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for curso in cursos:
                    writer.writerow({
                        'codigo': curso.codigo,
                        'nombre': curso.nombre,
                        'creditos': curso.creditos,
                        'docente': curso.docente
                    })
    
    def cargar_inscripciones(self) -> List[Inscripcion]:
        """Carga inscripciones desde CSV"""
        archivo = os.path.join(self.base_path, "inscripciones.csv")
        inscripciones = []
        
        if not os.path.exists(archivo):
            return inscripciones
        
        try:
            with open(archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    inscripcion = Inscripcion(
                        id=row['id'].strip(),
                        estudiante_id=row['estudiante_id'].strip(),
                        curso_codigo=row['curso_codigo'].strip(),
                        fecha_inscripcion=row['fecha_inscripcion'].strip()
                    )
                    inscripciones.append(inscripcion)
        except Exception as e:
            print(f"Error cargando inscripciones: {e}")
        
        return inscripciones
    
    def guardar_inscripciones(self, inscripciones: List[Inscripcion]):
        """Guarda inscripciones en CSV"""
        archivo = os.path.join(self.base_path, "inscripciones.csv")
        
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            if inscripciones:
                fieldnames = ['id', 'estudiante_id', 'curso_codigo', 'fecha_inscripcion']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for inscripcion in inscripciones:
                    writer.writerow({
                        'id': inscripcion.id,
                        'estudiante_id': inscripcion.estudiante_id,
                        'curso_codigo': inscripcion.curso_codigo,
                        'fecha_inscripcion': inscripcion.fecha_inscripcion
                    })
    
    def cargar_matriculas(self) -> List[Matricula]:
        """Carga matrículas desde CSV - ahora incluye inscripcion_id"""
        archivo = os.path.join(self.base_path, "matriculas.csv")
        matriculas = []
        
        if not os.path.exists(archivo):
            return matriculas
        
        try:
            with open(archivo, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    nota = None
                    if row.get('nota') and row['nota'].strip():
                        try:
                            nota = float(row['nota'])
                        except ValueError:
                            nota = None
                    
                    # Manejar compatibilidad con formato anterior
                    inscripcion_id = row.get('inscripcion_id', '').strip()
                    if not inscripcion_id:
                        # Si no hay inscripcion_id, generar uno temporal
                        inscripcion_id = f"temp_{row['id'].strip()}"
                    
                    matricula = Matricula(
                        id=row['id'].strip(),
                        inscripcion_id=inscripcion_id,
                        estudiante_id=row['estudiante_id'].strip(),
                        curso_codigo=row['curso_codigo'].strip(),
                        fecha_matricula=row['fecha_matricula'].strip(),
                        nota=nota
                    )
                    matriculas.append(matricula)
        except Exception as e:
            print(f"Error cargando matrículas: {e}")
        
        return matriculas
    
    def guardar_matriculas(self, matriculas: List[Matricula]):
        """Guarda matrículas en CSV - ahora incluye inscripcion_id"""
        archivo = os.path.join(self.base_path, "matriculas.csv")
        
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            if matriculas:
                fieldnames = ['id', 'inscripcion_id', 'estudiante_id', 'curso_codigo', 'fecha_matricula', 'nota']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for matricula in matriculas:
                    writer.writerow({
                        'id': matricula.id,
                        'inscripcion_id': matricula.inscripcion_id,
                        'estudiante_id': matricula.estudiante_id,
                        'curso_codigo': matricula.curso_codigo,
                        'fecha_matricula': matricula.fecha_matricula,
                        'nota': matricula.nota if matricula.nota is not None else ''
                    })
    
    def exportar_json(self, estudiantes: List[Estudiante], cursos: List[Curso], 
                     inscripciones: List[Inscripcion], matriculas: List[Matricula]) -> str:
        """Exporta todos los datos a formato JSON"""
        datos = {
            'estudiantes': [
                {
                    'id': e.id,
                    'documento': e.documento,
                    'nombres': e.nombres,
                    'apellidos': e.apellidos,
                    'correo': e.correo,
                    'fecha_nacimiento': e.fecha_nacimiento
                } for e in estudiantes
            ],
            'cursos': [
                {
                    'codigo': c.codigo,
                    'nombre': c.nombre,
                    'creditos': c.creditos,
                    'docente': c.docente
                } for c in cursos
            ],
            'inscripciones': [
                {
                    'id': i.id,
                    'estudiante_id': i.estudiante_id,
                    'curso_codigo': i.curso_codigo,
                    'fecha_inscripcion': i.fecha_inscripcion
                } for i in inscripciones
            ],
            'matriculas': [
                {
                    'id': m.id,
                    'inscripcion_id': m.inscripcion_id,
                    'estudiante_id': m.estudiante_id,
                    'curso_codigo': m.curso_codigo,
                    'fecha_matricula': m.fecha_matricula,
                    'nota': m.nota
                } for m in matriculas
            ]
        }
        
        archivo = os.path.join(self.base_path, "export.json")
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        return archivo