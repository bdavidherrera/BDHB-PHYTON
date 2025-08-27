# migration_script.py - Script para migrar datos existentes al nuevo formato
import csv


def migrar_matriculas_a_inscripciones():
    """
    Migra las matrículas existentes creando inscripciones correspondientes
    y actualizando el formato de matrículas
    """
    print("Iniciando migración de datos...")
    
    # Leer matrículas existentes
    matriculas_existentes = []
    try:
        with open('datos/matriculas.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                matriculas_existentes.append(row)
    except FileNotFoundError:
        print("No se encontró archivo de matrículas existente")
        return
    
    # Crear inscripciones basadas en matrículas existentes
    inscripciones = []
    matriculas_nuevas = []
    
    for i, matricula in enumerate(matriculas_existentes, 1):
        # Crear inscripción
        inscripcion_id = f"ins{i:03d}"
        inscripcion = {
            'id': inscripcion_id,
            'estudiante_id': matricula['estudiante_id'],
            'curso_codigo': matricula['curso_codigo'],
            'fecha_inscripcion': matricula['fecha_matricula']
        }
        inscripciones.append(inscripcion)
        
        # Crear nueva matrícula con referencia a inscripción
        nueva_matricula = {
            'id': matricula['id'],
            'inscripcion_id': inscripcion_id,
            'estudiante_id': matricula['estudiante_id'],
            'curso_codigo': matricula['curso_codigo'],
            'fecha_matricula': matricula['fecha_matricula'],
            'nota': matricula.get('nota', '')
        }
        matriculas_nuevas.append(nueva_matricula)
    
    # Crear archivo de inscripciones
    with open('datos/inscripciones.csv', 'w', newline='', encoding='utf-8') as f:
        if inscripciones:
            fieldnames = ['id', 'estudiante_id', 'curso_codigo', 'fecha_inscripcion']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inscripciones)
    
    # Actualizar archivo de matrículas
    with open('datos/matriculas.csv', 'w', newline='', encoding='utf-8') as f:
        if matriculas_nuevas:
            fieldnames = ['id', 'inscripcion_id', 'estudiante_id', 'curso_codigo', 'fecha_matricula', 'nota']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matriculas_nuevas)
    
    print("Migración completada con éxito.")
    

if __name__ == "__main__":
    migrar_matriculas_a_inscripciones()
