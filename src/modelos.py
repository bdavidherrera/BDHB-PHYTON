# src/modelos.py - Versión actualizada con modelo de Inscripción
from dataclasses import dataclass
from typing import  Optional

@dataclass
class Estudiante:
    """Modelo para representar un estudiante"""
    id: str
    documento: str
    nombres: str
    apellidos: str
    correo: str
    fecha_nacimiento: str
    
    def __post_init__(self):
        # Validaciones automáticas al crear el objeto
        if not self.id or not self.documento or not self.nombres or not self.apellidos or not self.correo:
            raise ValueError("Todos los campos son obligatorios")
    
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}"

@dataclass
class Curso:
    """Modelo para representar un curso"""
    codigo: str
    nombre: str
    creditos: int
    docente: str
    
    def __post_init__(self):
        if not self.codigo or not self.nombre or not self.docente:
            raise ValueError("Código, nombre y docente son obligatorios")
        if self.creditos <= 0:
            raise ValueError("Los créditos deben ser un número positivo")

@dataclass
class Inscripcion:
    """Modelo para representar una inscripción (estudiante se inscribe a un curso)"""
    id: str
    estudiante_id: str
    curso_codigo: str
    fecha_inscripcion: str
    
    def __post_init__(self):
        if not self.id or not self.estudiante_id or not self.curso_codigo:
            raise ValueError("ID, estudiante_id y curso_codigo son obligatorios")

@dataclass
class Matricula:
    """Modelo para representar una matrícula (inscripción + nota asignada)"""
    id: str
    inscripcion_id: str
    estudiante_id: str
    curso_codigo: str
    fecha_matricula: str
    nota: Optional[float] = None
    
    def __post_init__(self):
        if not self.id or not self.inscripcion_id or not self.estudiante_id or not self.curso_codigo:
            raise ValueError("ID, inscripcion_id, estudiante_id y curso_codigo son obligatorios")
    
    @classmethod
    def from_inscripcion(cls, inscripcion: Inscripcion, matricula_id: str = None):
        """Crea una matrícula a partir de una inscripción"""
        import uuid
        if matricula_id is None:
            matricula_id = str(uuid.uuid4())[:8]
        
        return cls(
            id=matricula_id,
            inscripcion_id=inscripcion.id,
            estudiante_id=inscripcion.estudiante_id,
            curso_codigo=inscripcion.curso_codigo,
            fecha_matricula=inscripcion.fecha_inscripcion,
            nota=None
        )