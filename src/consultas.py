

# src/consultas.py
from typing import List, Tuple, Dict, Optional
from src.modelos import Estudiante, Curso, Matricula

class ConsultasAcademicas:
    """Clase para realizar consultas y reportes del sistema"""
    
    def __init__(self, estudiantes: List[Estudiante], cursos: List[Curso], matriculas: List[Matricula]):
        self.estudiantes = estudiantes
        self.cursos = cursos
        self.matriculas = matriculas
    
    def buscar_estudiante_por_documento(self, documento: str) -> Optional[Estudiante]:
        """Busca estudiante por número de documento"""
        for estudiante in self.estudiantes:
            if estudiante.documento == documento:
                return estudiante
        return None
    
    def buscar_estudiante_por_correo(self, correo: str) -> Optional[Estudiante]:
        """Busca estudiante por correo electrónico"""
        for estudiante in self.estudiantes:
            if estudiante.correo.lower() == correo.lower():
                return estudiante
        return None
    
    def listar_estudiantes_ordenados_por_apellido(self) -> List[Estudiante]:
        """Retorna lista de estudiantes ordenados por apellido"""
        return sorted(self.estudiantes, key=lambda e: e.apellidos.lower())
    
    def obtener_top_promedios_por_curso(self, codigo_curso: str, top: int = 3) -> List[Tuple[Estudiante, float]]:
        """Obtiene los mejores promedios de un curso específico"""
        matriculas_curso = [m for m in self.matriculas 
                           if m.curso_codigo == codigo_curso and m.nota is not None]
        
        # Crear lista de estudiante-nota
        estudiantes_notas = []
        for matricula in matriculas_curso:
            estudiante = self.buscar_estudiante_por_id(matricula.estudiante_id)
            if estudiante:
                estudiantes_notas.append((estudiante, matricula.nota))
        
        # Ordenar por nota descendente y tomar el top
        estudiantes_notas.sort(key=lambda x: x[1], reverse=True)
        return estudiantes_notas[:top]
    
    def obtener_reprobados(self, nota_minima: float = 3.0) -> List[Tuple[Estudiante, Curso, float]]:
        """Obtiene estudiantes reprobados (nota < nota_minima)"""
        reprobados = []
        
        for matricula in self.matriculas:
            if matricula.nota is not None and matricula.nota < nota_minima:
                estudiante = self.buscar_estudiante_por_id(matricula.estudiante_id)
                curso = self.buscar_curso_por_codigo(matricula.curso_codigo)
                
                if estudiante and curso:
                    reprobados.append((estudiante, curso, matricula.nota))
        
        return reprobados
    
    def obtener_creditos_inscritos_por_estudiante(self, estudiante_id: str) -> int:
        """Calcula total de créditos inscritos por un estudiante"""
        creditos_total = 0
        
        matriculas_estudiante = [m for m in self.matriculas if m.estudiante_id == estudiante_id]
        
        for matricula in matriculas_estudiante:
            curso = self.buscar_curso_por_codigo(matricula.curso_codigo)
            if curso:
                creditos_total += curso.creditos
        
        return creditos_total
    
    def buscar_estudiante_por_id(self, estudiante_id: str) -> Optional[Estudiante]:
        """Busca estudiante por ID"""
        for estudiante in self.estudiantes:
            if estudiante.id == estudiante_id:
                return estudiante
        return None
    
    def buscar_curso_por_codigo(self, codigo: str) -> Optional[Curso]:
        """Busca curso por código"""
        for curso in self.cursos:
            if curso.codigo == codigo:
                return curso
        return None
    
    def obtener_dominios_correo_unicos(self) -> List[str]:
        """Obtiene lista de dominios de correo únicos"""
        dominios = set()
        for estudiante in self.estudiantes:
            if '@' in estudiante.correo:
                dominio = estudiante.correo.split('@')[1]
                dominios.add(dominio)
        
        return sorted(list(dominios))
    
    def buscar_binario_estudiante(self, apellido_buscar: str) -> Optional[Estudiante]:
        """Implementa búsqueda binaria por apellido (requiere lista ordenada)"""
        estudiantes_ordenados = self.listar_estudiantes_ordenados_por_apellido()
        
        izq, der = 0, len(estudiantes_ordenados) - 1
        
        while izq <= der:
            medio = (izq + der) // 2
            apellido_medio = estudiantes_ordenados[medio].apellidos.lower()
            apellido_buscar_lower = apellido_buscar.lower()
            
            if apellido_medio == apellido_buscar_lower:
                return estudiantes_ordenados[medio]
            elif apellido_medio < apellido_buscar_lower:
                izq = medio + 1
            else:
                der = medio - 1
        
        return None



