# src/modelos.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import re

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
class Matricula:
    """Modelo para representar una matrícula (inicialmente vacía)"""
    id: str
    estudiante_id: str
    curso_codigo: str
    fecha_matricula: str
    nota: Optional[float] = None
    
    def __post_init__(self):
        if not self.id or not self.estudiante_id or not self.curso_codigo:
            raise ValueError("ID, estudiante_id y curso_codigo son obligatorios")

