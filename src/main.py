# src/main.py
from src.modelos import Estudiante, Curso, Matricula
from src.persistencia import PersistenciaCSV
from src.ui import InterfazUsuario
from src.validaciones import ValidacionError

def main():
    """Función principal del sistema MiniSIGA"""
    
    print("Iniciando MiniSIGA...")
    
    # Inicializar persistencia
    persistencia = PersistenciaCSV()
    
    # Cargar datos desde archivos CSV
    print("Cargando datos...")
    estudiantes = persistencia.cargar_estudiantes()
    cursos = persistencia.cargar_cursos()
    matriculas = persistencia.cargar_matriculas()
    
    print(f"Datos cargados: {len(estudiantes)} estudiantes, {len(cursos)} cursos, {len(matriculas)} matrículas")
    
    # Inicializar interfaz de usuario
    ui = InterfazUsuario(estudiantes, cursos, matriculas)
    
    # Loop principal del programa
    while True:
        try:
            ui.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "0":
                # Guardar datos antes de salir
                print("Guardando datos...")
                persistencia.guardar_estudiantes(estudiantes)
                persistencia.guardar_cursos(cursos)
                persistencia.guardar_matriculas(matriculas)
                print("¡Datos guardados exitosamente!")
                print("¡Gracias por usar MiniSIGA!")
                break
            
            elif opcion == "1":
                # Menú de estudiantes
                while True:
                    ui.mostrar_menu_estudiantes()
                    sub_opcion = input("Seleccione una opción: ").strip()
                    
                    if sub_opcion == "0":
                        break
                    elif sub_opcion == "1":
                        ui.crear_estudiante()
                    elif sub_opcion == "2":
                        print("Función de editar estudiante no implementada en esta versión")
                    elif sub_opcion == "3":
                        print("Función de eliminar estudiante no implementada en esta versión")
                    elif sub_opcion == "4":
                        ui.listar_estudiantes()
                    else:
                        print("❌ Opción no válida")
            
            elif opcion == "2":
                # Menú de cursos
                while True:
                    ui.mostrar_menu_cursos()
                    sub_opcion = input("Seleccione una opción: ").strip()
                    
                    if sub_opcion == "0":
                        break
                    elif sub_opcion == "1":
                        ui.crear_curso()
                    elif sub_opcion == "2":
                        print("Función de editar curso no implementada en esta versión")
                    elif sub_opcion == "3":
                        print("Función de eliminar curso no implementada en esta versión")
                    elif sub_opcion == "4":
                        ui.listar_cursos()
                    else:
                        print("❌ Opción no válida")
            
            elif opcion == "3":
                # Menú de matrículas
                while True:
                    ui.mostrar_menu_matriculas()
                    sub_opcion = input("Seleccione una opción: ").strip()
                    
                    if sub_opcion == "0":
                        break
                    elif sub_opcion == "1":
                        ui.crear_matricula()
                    elif sub_opcion == "2":
                        ui.asignar_nota()
                    elif sub_opcion == "3":
                        print("Función de eliminar matrícula no implementada en esta versión")
                    elif sub_opcion == "4":
                        ui.listar_matriculas()
                    else:
                        print("❌ Opción no válida")
            
            elif opcion == "4":
                # Menú de consultas y reportes
                while True:
                    ui.mostrar_menu_consultas()
                    sub_opcion = input("Seleccione una opción: ").strip()
                    
                    if sub_opcion == "0":
                        break
                    elif sub_opcion == "1":
                        ui.ejecutar_consulta_buscar_documento()
                    elif sub_opcion == "2":
                        ui.ejecutar_consulta_buscar_correo()
                    elif sub_opcion == "3":
                        ui.ejecutar_consulta_ordenados_apellido()
                    elif sub_opcion == "4":
                        ui.ejecutar_consulta_top_promedios()
                    elif sub_opcion == "5":
                        ui.ejecutar_consulta_reprobados()
                    elif sub_opcion == "6":
                        ui.ejecutar_consulta_creditos_estudiante()
                    elif sub_opcion == "7":
                        ui.ejecutar_consulta_dominios_correo()
                    elif sub_opcion == "8":
                        ui.ejecutar_busqueda_binaria_apellido()
                    else:
                        print("❌ Opción no válida")
            
            elif opcion == "5":
                # Exportar a JSON
                try:
                    archivo = persistencia.exportar_json(estudiantes, cursos, matriculas)
                    print(f"✅ Datos exportados exitosamente a: {archivo}")
                except Exception as e:
                    print(f"❌ Error al exportar: {e}")
            
            else:
                print("❌ Opción no válida")
        
        except KeyboardInterrupt:
            print("\n\nInterrumpido por el usuario.")
            # Guardar datos antes de salir
            print("Guardando datos...")
            persistencia.guardar_estudiantes(estudiantes)
            persistencia.guardar_cursos(cursos)
            persistencia.guardar_matriculas(matriculas)
            print("¡Datos guardados exitosamente!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("El programa continuará ejecutándose...")

if __name__ == "__main__":
    main()
