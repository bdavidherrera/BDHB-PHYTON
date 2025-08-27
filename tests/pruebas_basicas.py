
# tests/pruebas_basicas.py
import unittest
import tempfile
import shutil
from datetime import datetime
import os
import sys

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modelos import Estudiante, Curso, Matricula
from src.validaciones import validar_correo, validar_documento, validar_fecha, validar_creditos, validar_nota
from src.persistencia import PersistenciaCSV
from src.consultas import ConsultasAcademicas

class TestModelos(unittest.TestCase):
    """Pruebas para los modelos de datos"""
    
    def test_crear_estudiante_valido(self):
        """Prueba creación de estudiante válido"""
        estudiante = Estudiante(
            id="est001",
            documento="12345678",
            nombres="Juan Carlos",
            apellidos="Pérez García",
            correo="juan.perez@email.com",
            fecha_nacimiento="1995-06-15"
        )
        
        self.assertEqual(estudiante.id, "est001")
        self.assertEqual(estudiante.documento, "12345678")
        self.assertEqual(estudiante.nombre_completo(), "Juan Carlos Pérez García")
    
    def test_crear_curso_valido(self):
        """Prueba creación de curso válido"""
        curso = Curso(
            codigo="MAT101",
            nombre="Matemáticas Básicas",
            creditos=3,
            docente="Dr. Ana López"
        )
        
        self.assertEqual(curso.codigo, "MAT101")
        self.assertEqual(curso.creditos, 3)
    
    def test_crear_matricula_valida(self):
        """Prueba creación de matrícula válida"""
        matricula = Matricula(
            id="mat001",
            estudiante_id="est001",
            curso_codigo="MAT101",
            fecha_matricula="2024-02-15"
        )
        
        self.assertEqual(matricula.estudiante_id, "est001")
        self.assertEqual(matricula.curso_codigo, "MAT101")
        self.assertIsNone(matricula.nota)

class TestValidaciones(unittest.TestCase):
    """Pruebas para las funciones de validación"""
    
    def test_validar_correo_valido(self):
        """Prueba validación de correos válidos"""
        self.assertTrue(validar_correo("test@email.com"))
        self.assertTrue(validar_correo("usuario.nombre@universidad.edu.co"))
        self.assertTrue(validar_correo("123@test.org"))
    
    def test_validar_correo_invalido(self):
        """Prueba validación de correos inválidos"""
        self.assertFalse(validar_correo("correo_sin_arroba"))
        self.assertFalse(validar_correo("@dominio.com"))
        self.assertFalse(validar_correo("usuario@"))
        self.assertFalse(validar_correo("usuario@dominio"))
    
    def test_validar_documento_valido(self):
        """Prueba validación de documentos válidos"""
        self.assertTrue(validar_documento("123456"))
        self.assertTrue(validar_documento("12345678901"))
        self.assertTrue(validar_documento("1234567890123"))
    
    def test_validar_documento_invalido(self):
        """Prueba validación de documentos inválidos"""
        self.assertFalse(validar_documento("12345"))  # Muy corto
        self.assertFalse(validar_documento("1234567890123456"))  # Muy largo
        self.assertFalse(validar_documento("12345abc"))  # Contiene letras
        self.assertFalse(validar_documento(""))  # Vacío
    
    def test_validar_fecha_valida(self):
        """Prueba validación de fechas válidas"""
        self.assertTrue(validar_fecha("2024-02-15"))
        self.assertTrue(validar_fecha("1995-12-31"))
        self.assertTrue(validar_fecha("2000-01-01"))
    
    def test_validar_fecha_invalida(self):
        """Prueba validación de fechas inválidas"""
        self.assertFalse(validar_fecha("2024-13-15"))  # Mes inválido
        self.assertFalse(validar_fecha("2024-02-30"))  # Día inválido
        self.assertFalse(validar_fecha("15-02-2024"))  # Formato incorrecto
        self.assertFalse(validar_fecha("2024/02/15"))  # Separador incorrecto
    
    def test_validar_creditos_valido(self):
        """Prueba validación de créditos válidos"""
        self.assertTrue(validar_creditos(1))
        self.assertTrue(validar_creditos(5))
        self.assertTrue(validar_creditos(10))
    
    def test_validar_creditos_invalido(self):
        """Prueba validación de créditos inválidos"""
        self.assertFalse(validar_creditos(0))
        self.assertFalse(validar_creditos(-1))
        self.assertFalse(validar_creditos(11))
    
    def test_validar_nota_valida(self):
        """Prueba validación de notas válidas"""
        self.assertTrue(validar_nota(0.0))
        self.assertTrue(validar_nota(2.5))
        self.assertTrue(validar_nota(5.0))
    
    def test_validar_nota_invalida(self):
        """Prueba validación de notas inválidas"""
        self.assertFalse(validar_nota(-0.1))
        self.assertFalse(validar_nota(5.1))

class TestPersistencia(unittest.TestCase):
    """Pruebas para la persistencia de datos"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.temp_dir = tempfile.mkdtemp()
        self.persistencia = PersistenciaCSV(self.temp_dir)
        
        # Datos de prueba
        self.estudiantes_prueba = [
            Estudiante("1", "12345678", "Juan", "Pérez", "juan@test.com", "1995-01-01"),
            Estudiante("2", "87654321", "María", "González", "maria@test.com", "1996-02-02")
        ]
        
        self.cursos_prueba = [
            Curso("MAT101", "Matemáticas", 3, "Dr. López"),
            Curso("FIS101", "Física", 4, "Dr. García")
        ]
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        shutil.rmtree(self.temp_dir)
    
    def test_guardar_y_cargar_estudiantes(self):
        """Prueba guardar y cargar estudiantes"""
        # Guardar
        self.persistencia.guardar_estudiantes(self.estudiantes_prueba)
        
        # Cargar
        estudiantes_cargados = self.persistencia.cargar_estudiantes()
        
        # Verificar
        self.assertEqual(len(estudiantes_cargados), 2)
        self.assertEqual(estudiantes_cargados[0].documento, "12345678")
        self.assertEqual(estudiantes_cargados[1].correo, "maria@test.com")
    
    def test_guardar_y_cargar_cursos(self):
        """Prueba guardar y cargar cursos"""
        # Guardar
        self.persistencia.guardar_cursos(self.cursos_prueba)
        
        # Cargar
        cursos_cargados = self.persistencia.cargar_cursos()
        
        # Verificar
        self.assertEqual(len(cursos_cargados), 2)
        self.assertEqual(cursos_cargados[0].codigo, "MAT101")
        self.assertEqual(cursos_cargados[1].creditos, 4)

class TestConsultas(unittest.TestCase):
    """Pruebas para las consultas académicas"""
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.estudiantes = [
            Estudiante("1", "12345678", "Juan", "Pérez", "juan@test.com", "1995-01-01"),
            Estudiante("2", "87654321", "María", "González", "maria@test.com", "1996-02-02"),
            Estudiante("3", "11111111", "Ana", "López", "ana@test.com", "1997-03-03")
        ]
        
        self.cursos = [
            Curso("MAT101", "Matemáticas", 3, "Dr. López"),
            Curso("FIS101", "Física", 4, "Dr. García")
        ]
        
        self.matriculas = [
            Matricula("m1", "1", "MAT101", "2024-02-01", 4.5),
            Matricula("m2", "2", "MAT101", "2024-02-01", 3.8),
            Matricula("m3", "3", "MAT101", "2024-02-01", 2.1),
            Matricula("m4", "1", "FIS101", "2024-02-01", None)
        ]
        
        self.consultas = ConsultasAcademicas(self.estudiantes, self.cursos, self.matriculas)
    
    def test_buscar_estudiante_por_documento(self):
        """Prueba búsqueda de estudiante por documento"""
        estudiante = self.consultas.buscar_estudiante_por_documento("12345678")
        self.assertIsNotNone(estudiante)
        self.assertEqual(estudiante.nombres, "Juan")
        
        estudiante_inexistente = self.consultas.buscar_estudiante_por_documento("99999999")
        self.assertIsNone(estudiante_inexistente)
    
    def test_buscar_estudiante_por_correo(self):
        """Prueba búsqueda de estudiante por correo"""
        estudiante = self.consultas.buscar_estudiante_por_correo("maria@test.com")
        self.assertIsNotNone(estudiante)
        self.assertEqual(estudiante.apellidos, "González")
        
        # Prueba case insensitive
        estudiante = self.consultas.buscar_estudiante_por_correo("MARIA@TEST.COM")
        self.assertIsNotNone(estudiante)
    
    def test_listar_estudiantes_ordenados_por_apellido(self):
        """Prueba listado ordenado por apellido"""
        ordenados = self.consultas.listar_estudiantes_ordenados_por_apellido()
        
        self.assertEqual(len(ordenados), 3)
        self.assertEqual(ordenados[0].apellidos, "González")  # Primero alfabéticamente
        self.assertEqual(ordenados[1].apellidos, "López")
        self.assertEqual(ordenados[2].apellidos, "Pérez")
    
    def test_obtener_top_promedios_por_curso(self):
        """Prueba obtención de top promedios"""
        top = self.consultas.obtener_top_promedios_por_curso("MAT101", 3)
        
        self.assertEqual(len(top), 3)
        # Verificar que está ordenado descendente por nota
        self.assertEqual(top[0][1], 4.5)  # Juan - nota más alta
        self.assertEqual(top[1][1], 3.8)  # María
        self.assertEqual(top[2][1], 2.1)  # Ana - nota más baja
    
    def test_obtener_reprobados(self):
        """Prueba obtención de reprobados"""
        reprobados = self.consultas.obtener_reprobados(3.0)
        
        self.assertEqual(len(reprobados), 1)
        self.assertEqual(reprobados[0][2], 2.1)  # Ana con nota 2.1
    
    def test_obtener_creditos_inscritos_por_estudiante(self):
        """Prueba cálculo de créditos inscritos"""
        creditos = self.consultas.obtener_creditos_inscritos_por_estudiante("1")
        self.assertEqual(creditos, 7)  # MAT101 (3) + FIS101 (4)
        
        creditos = self.consultas.obtener_creditos_inscritos_por_estudiante("2")
        self.assertEqual(creditos, 3)  # Solo MAT101 (3)
    
    def test_obtener_dominios_correo_unicos(self):
        """Prueba obtención de dominios únicos"""
        dominios = self.consultas.obtener_dominios_correo_unicos()
        
        self.assertEqual(len(dominios), 1)
        self.assertEqual(dominios[0], "test.com")
    
    def test_buscar_binario_estudiante(self):
        """Prueba búsqueda binaria por apellido"""
        estudiante = self.consultas.buscar_binario_estudiante("López")
        self.assertIsNotNone(estudiante)
        self.assertEqual(estudiante.nombres, "Ana")
        
        estudiante_inexistente = self.consultas.buscar_binario_estudiante("Inexistente")
        self.assertIsNone(estudiante_inexistente)

if __name__ == '__main__':
    print("Ejecutando pruebas básicas de MiniSIGA...")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    unittest.main(verbosity=2)