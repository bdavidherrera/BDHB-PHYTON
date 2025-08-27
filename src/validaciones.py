# src/validaciones.py
import re
from datetime import datetime
from typing import List

def validar_correo(correo: str) -> bool:
    """Valida que el correo tenga formato válido"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None

def validar_documento(documento: str) -> bool:
    """Valida que el documento solo contenga números y tenga longitud apropiada"""
    return documento.isdigit() and 6 <= len(documento) <= 15

def validar_fecha(fecha_str: str) -> bool:
    """Valida que la fecha esté en formato YYYY-MM-DD y sea válida"""
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validar_creditos(creditos: int) -> bool:
    """Valida que los créditos estén en un rango válido"""
    return 1 <= creditos <= 10

def validar_nota(nota: float) -> bool:
    """Valida que la nota esté entre 0.0 y 5.0"""
    return 0.0 <= nota <= 5.0

class ValidacionError(Exception):
    """Excepción personalizada para errores de validación"""
    pass

def validar_estudiante_completo(estudiante_data: dict) -> List[str]:
    """Valida todos los campos de un estudiante y retorna lista de errores"""
    errores = []
    
    if not estudiante_data.get('documento'):
        errores.append("El documento es obligatorio")
    elif not validar_documento(estudiante_data['documento']):
        errores.append("El documento debe contener solo números y tener entre 6-15 dígitos")
    
    if not estudiante_data.get('nombres'):
        errores.append("Los nombres son obligatorios")
    
    if not estudiante_data.get('apellidos'):
        errores.append("Los apellidos son obligatorios")
    
    if not estudiante_data.get('correo'):
        errores.append("El correo es obligatorio")
    elif not validar_correo(estudiante_data['correo']):
        errores.append("El formato del correo no es válido")
    
    if not estudiante_data.get('fecha_nacimiento'):
        errores.append("La fecha de nacimiento es obligatoria")
    elif not validar_fecha(estudiante_data['fecha_nacimiento']):
        errores.append("La fecha debe estar en formato YYYY-MM-DD")
    
    return errores

