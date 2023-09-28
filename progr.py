import json
import os
from datetime import datetime, timedelta

# Nombre de los archivos de datos
TAREAS_PENDIENTES_FILE = "tareas_pendientes.json"
TAREAS_COMPLETADAS_FILE = "tareas_completadas.json"

# Función para cargar las tareas desde un archivo JSON
def cargar_tareas(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as archivo:
            return json.load(archivo)
    else:
        return []

# Función para guardar las tareas en un archivo JSON
def guardar_tareas(tareas, nombre_archivo):
    with open(nombre_archivo, "w") as archivo:
        json.dump(tareas, archivo, indent=4)

# Función para agregar una tarea a la lista de tareas pendientes
def agregar_tarea(tareas_pendientes):
    titulo = input("Ingrese el título de la tarea: ")
    descripcion = input("Ingrese la descripción de la tarea: ")
    fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD, dejar en blanco si no hay fecha): ")

    tarea = {"titulo": titulo, "descripcion": descripcion, "completada": False}

    if fecha_vencimiento:
        tarea["fecha_vencimiento"] = fecha_vencimiento

    tareas_pendientes.append(tarea)
    print("Tarea agregada con éxito.")

# Función para listar las tareas pendientes o completadas
def listar_tareas(tareas, completadas=False):
    if completadas:
        print("Lista de tareas completadas:")
    else:
        print("Lista de tareas pendientes:")

    for idx, tarea in enumerate(tareas, start=1):
        estado = "Completada" if tarea["completada"] else "Pendiente"
        print(f"{idx}. {tarea['titulo']} - {estado}")

# Función para marcar una tarea como completada
def marcar_completada(tareas_pendientes, tareas_completadas):
    listar_tareas(tareas_pendientes)
    try:
        opcion = int(input("Ingrese el número de la tarea que desea marcar como completada: ")) - 1
        if 0 <= opcion < len(tareas_pendientes):
            tarea_completada = tareas_pendientes.pop(opcion)
            tarea_completada["completada"] = True
            tareas_completadas.append(tarea_completada)
            print("Tarea marcada como completada.")
            guardar_tareas(tareas_pendientes, TAREAS_PENDIENTES_FILE)  # Guardar tareas pendientes actualizadas
            guardar_tareas(tareas_completadas, TAREAS_COMPLETADAS_FILE)  # Guardar tareas completadas actualizadas
        else:
            print("Número de tarea inválido.")
    except ValueError:
        print("Entrada inválida. Debe ingresar un número.")

# Función para verificar y mostrar tareas vencidas
def mostrar_tareas_vencidas(tareas_pendientes):
    hoy = datetime.now()
    print("Tareas vencidas o próximas a vencerse:")
    for tarea in tareas_pendientes:
        if "fecha_vencimiento" in tarea:
            fecha_vencimiento = datetime.strptime(tarea["fecha_vencimiento"], "%Y-%m-%d")
            if fecha_vencimiento < hoy:
                print(f"{tarea['titulo']} - Vencida")
            elif fecha_vencimiento <= hoy + timedelta(days=7):
                print(f"{tarea['titulo']} - Próxima a vencerse")

def main():
    # Cargar tareas pendientes y completadas desde los archivos
    tareas_pendientes = cargar_tareas(TAREAS_PENDIENTES_FILE)
    tareas_completadas = cargar_tareas(TAREAS_COMPLETADAS_FILE)

    while True:
        print("\n===== Gestor de Tareas =====")
        print("1. Agregar tarea")
        print("2. Listar tareas pendientes")
        print("3. Listar tareas completadas")
        print("4. Marcar tarea como completada")
        print("5. Mostrar tareas vencidas o próximas a vencerse")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_tarea(tareas_pendientes)
        elif opcion == "2":
            listar_tareas(tareas_pendientes)
        elif opcion == "3":
            listar_tareas(tareas_completadas, completadas=True)
        elif opcion == "4":
            marcar_completada(tareas_pendientes, tareas_completadas)
        elif opcion == "5":
            mostrar_tareas_vencidas(tareas_pendientes)
        elif opcion == "6":
            # Guardar tareas en archivos antes de salir
            guardar_tareas(tareas_pendientes, TAREAS_PENDIENTES_FILE)
            guardar_tareas(tareas_completadas, TAREAS_COMPLETADAS_FILE)
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()