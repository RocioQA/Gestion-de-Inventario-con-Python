import sqlite3
from sqlite3 import Error
from colorama import init, Fore, Style

# Inicializa colorama para que funcione en Windows y otros sistemas.
init(autoreset=True)

DB_PATH = "inventario.db"

"""Crea una conexión a la base de datos SQLite."""
def conectar():
    try:
        conexion = sqlite3.connect(DB_PATH)
        return conexion
    except Error as e:
        print(Fore.RED + "Error al conectar con la base de datos:", e)
        return None


def crear_tabla():
    """Crea la tabla Productos."""
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
            """
        )
        conexion.commit()
        conexion.close()


def registrar_producto():
    """Solicita datos al usuario para guardar un producto nuevo en la tabla."""
    print(Fore.CYAN + "\nRegistrar nuevo producto")
    nombre = input("Nombre: ").strip()
    descripcion = input("Descripción: ").strip()
    cantidad_texto = input("Cantidad: ").strip()
    precio_texto = input("Precio: ").strip()
    categoria = input("Categoría: ").strip()

    if not nombre:
        print(Fore.RED + "El nombre no puede estar vacío.")
        return

    try:
        cantidad = int(cantidad_texto)
        precio = float(precio_texto)
    except ValueError:
        print(Fore.RED + "Cantidad y Precio deben ser valores numéricos válidos.")
        return

    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
            (nombre, descripcion, cantidad, precio, categoria)
        )
        conexion.commit()
        conexion.close()
        print(Fore.GREEN + "El producto se  registrado con éxito.")


def mostrar_productos():
    """Muestra todos los productos registrados en la base de datos."""
    print(Fore.CYAN + "\nProductos registrados:")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos")
        filas = cursor.fetchall()
        conexion.close()

        if filas:
            for fila in filas:
                print(Fore.YELLOW + f"ID: {fila[0]}")
                print(f"  Nombre: {fila[1]}")
                print(f"  Descripción: {fila[2]}")
                print(f"  Cantidad: {fila[3]}")
                print(f"  Precio: {fila[4]:.2f}")
                print(f"  Categoría: {fila[5]}")
                print(Style.DIM + "-" * 40)
        else:
            print(Fore.MAGENTA + "No hay ningún producto en el inventario.")


def buscar_producto_id():
    """Busca un producto por su ID y muestra sus datos."""
    print(Fore.CYAN + "\nBuscar producto por ID")
    id_texto = input("ID del producto: ").strip()

    try:
        producto_id = int(id_texto)
    except ValueError:
        print(Fore.RED + "El ID debe ser un número entero.")
        return

    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?",
            (producto_id,)
        )
        fila = cursor.fetchone()
        conexion.close()

        if fila:
            print(Fore.YELLOW + f"ID: {fila[0]}")
            print(f"Nombre: {fila[1]}")
            print(f"Descripción: {fila[2]}")
            print(f"Cantidad: {fila[3]}")
            print(f"Precio: {fila[4]:.2f}")
            print(f"Categoría: {fila[5]}")
        else:
            print(Fore.MAGENTA + "No se encontró un producto con ese ID.")


def buscar_producto_nombre_categoria():
    """Busca productos por su nombre o categoría."""
    print(Fore.CYAN + "\nBuscar por nombre o categoría")
    termino = input("Ingrese nombre o categoría: ").strip()

    if not termino:
        print(Fore.RED + "Debes ingresar un valor para buscar.")
        return

    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT id, nombre, descripcion, cantidad, precio, categoria
            FROM productos
            WHERE nombre LIKE ? OR categoria LIKE ?
            """,
            ("%" + termino + "%", "%" + termino + "%")
        )
        filas = cursor.fetchall()
        conexion.close()

        if filas:
            for fila in filas:
                print(Fore.YELLOW + f"ID: {fila[0]}")
                print(f"  Nombre: {fila[1]}")
                print(f"  Descripción: {fila[2]}")
                print(f"  Cantidad: {fila[3]}")
                print(f"  Precio: {fila[4]:.2f}")
                print(f"  Categoría: {fila[5]}")
                print(Style.DIM + "-" * 40)
        else:
            print(Fore.MAGENTA + "No se encontraron productos con ese término.")


def actualizar_producto():
    """Actualiza los datos de un producto existente usando su ID."""
    print(Fore.CYAN + "\nActualizar producto")
    id_texto = input("ID del producto: ").strip()

    try:
        producto_id = int(id_texto)
    except ValueError:
        print(Fore.RED + "El ID debe ser un número entero y válido.")
        return

    conexion = conectar()
    if not conexion:
        return

    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?", (producto_id,))
    fila = cursor.fetchone()

    if not fila:
        print(Fore.MAGENTA + "No existe un producto con ese ID.")
        conexion.close()
        return

    print(Fore.YELLOW + "Dejar en blanco para mantener el valor actual.")
    nombre = input(f"Nombre [{fila[1]}]: ").strip() or fila[1]
    descripcion = input(f"Descripción [{fila[2]}]: ").strip() or fila[2]
    cantidad_texto = input(f"Cantidad [{fila[3]}]: ").strip()
    precio_texto = input(f"Precio [{fila[4]}]: ").strip()
    categoria = input(f"Categoría [{fila[5]}]: ").strip() or fila[5]

    try:
        cantidad = int(cantidad_texto) if cantidad_texto else fila[3]
        precio = float(precio_texto) if precio_texto else fila[4]
    except ValueError:
        print(Fore.RED + "Cantidad y Precio deben ser valores numéricos válidos.")
        conexion.close()
        return

    cursor.execute(
        """
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
        """,
        (nombre, descripcion, cantidad, precio, categoria, producto_id)
    )
    conexion.commit()
    conexion.close()
    print(Fore.GREEN + "Producto actualizado correctamente.")


def eliminar_producto():
    """Eliminar un producto de la base de datos usando su ID."""
    print(Fore.CYAN + "\nEliminar producto")
    id_texto = input("ID del producto: ").strip()

    try:
        producto_id = int(id_texto)
    except ValueError:
        print(Fore.RED + "El ID debe ser un número entero y válido.")
        return

    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conexion.commit()
        if cursor.rowcount > 0:
            print(Fore.GREEN + "Producto eliminado correctamente.")
        else:
            print(Fore.MAGENTA + "No se encontró un producto con ese ID.")
        conexion.close()


def reporte_stock_bajo():
    """Muestra los productos con cantidad menor o igual al límite ingresado."""
    print(Fore.CYAN + "\nReporte de stock bajo")
    limite_texto = input("Cantidad límite: ").strip()

    try:
        limite = int(limite_texto)
    except ValueError:
        print(Fore.RED + "El límite debe ser un número entero y válido.")
        return

    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT id, nombre, descripcion, cantidad, precio, categoria
            FROM productos
            WHERE cantidad <= ?
            """,
            (limite,)
        )
        filas = cursor.fetchall()
        conexion.close()

        if filas:
            print(Fore.YELLOW + f"Productos con cantidad menor o igual a {limite}:")
            for fila in filas:
                print(f"ID: {fila[0]} - Nombre: {fila[1]} - Cantidad: {fila[3]} - Precio: {fila[4]:.2f}")
        else:
            print(Fore.MAGENTA + "No hay productos con stock bajo en ese rango.")


def mostrar_menu():
    """Muestra el menú principal y devuelve la opción elegida por el usuario."""
    print(Fore.MAGENTA + "\n=== MENÚ PRINCIPAL ===")
    print("1. Registrar producto")
    print("2. Ver todos los productos")
    print("3. Buscar producto por ID")
    print("4. Buscar producto por Nombre o Categoría")
    print("5. Actualizar producto")
    print("6. Eliminar producto")
    print("7. Reporte de stock bajo")
    print("8. Salir")
    return input("Elige una opción: ").strip()


def main():
    """Ejecuta la aplicación."""
    crear_tabla()
    print(Fore.GREEN + "Bienvenido al sistema de inventario")

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            buscar_producto_id()
        elif opcion == "4":
            buscar_producto_nombre_categoria()
        elif opcion == "5":
            actualizar_producto()
        elif opcion == "6":
            eliminar_producto()
        elif opcion == "7":
            reporte_stock_bajo()
        elif opcion == "8":
            print(Fore.GREEN + "Gracias por usar la aplicación de inventario. Hasta luego!")
            break
        else:
            print(Fore.RED + "Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
