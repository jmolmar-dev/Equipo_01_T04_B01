-- #############################################
-- # Archivo: src\models\inicializacion_db.sql #
-- #############################################

-- Crear la tabla 'roles' para definir los permisos de los usuarios
CREATE TABLE IF NOT EXISTS roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) UNIQUE NOT NULL
);

-- Insertar datos iniciales en la tabla 'roles'
-- Se utilizan los valores 'admin', 'desarrollador' y 'jugador' como roles de ejemplo
INSERT INTO roles (nombre_rol)
VALUES 
    ('admin'),
    ('desarrollador'),
    ('jugador')
ON CONFLICT DO NOTHING;

-- Crear la tabla 'usuarios' con referencia a 'roles'
-- Cada usuario está asociado a un rol específico mediante la columna 'id_rol'
CREATE TABLE IF NOT EXISTS usuarios (
    email VARCHAR(255) PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    id_rol INT REFERENCES roles(id_rol) DEFAULT 3  -- Rol de jugador por defecto
);

-- Insertar datos iniciales en la tabla 'usuarios'
-- Añadimos tres usuarios de ejemplo con diferentes roles
INSERT INTO usuarios (email, nombre_usuario, password, id_rol)
VALUES 
    ('admin@example.com', 'admin', 'adminpass', 1),
    ('dev1@example.com', 'dev1', 'devpass1', 2),
    ('jugador1@example.com', 'jugador1', 'jugadorpass1', 3)
ON CONFLICT (email) DO NOTHING;

-- Crear la tabla 'generos' para clasificar videojuegos, con unicidad en 'nombre_genero'
-- Se utiliza un índice insensible a mayúsculas para evitar duplicados (ej. 'Acción' y 'acción' serán tratados como iguales)
CREATE TABLE IF NOT EXISTS generos (
    id_genero SERIAL PRIMARY KEY,
    nombre_genero VARCHAR(255) NOT NULL UNIQUE
);

-- Añadir un índice único en 'nombre_genero' en minúsculas para evitar duplicados insensibles a mayúsculas
CREATE UNIQUE INDEX IF NOT EXISTS idx_nombre_genero_lower
ON generos (LOWER(nombre_genero));

-- Insertar datos de ejemplo en la tabla 'generos'
-- Se insertan cuatro géneros de videojuegos
INSERT INTO generos (nombre_genero)
VALUES 
    ('Acción'),
    ('Aventura'),
    ('RPG'),
    ('Deportes')
ON CONFLICT (nombre_genero) DO NOTHING;

-- Crear la tabla 'videojuegos' para almacenar información sobre los videojuegos
-- Cada videojuego se relaciona con un género mediante 'id_genero'
CREATE TABLE IF NOT EXISTS videojuegos (
    codigo VARCHAR(10) PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255),
    precio DECIMAL(10, 2) NOT NULL,
    plataforma VARCHAR(50) NOT NULL,
    stock INT NOT NULL,
    ventas INT NOT NULL DEFAULT 0,
    id_genero INT REFERENCES generos(id_genero),
    fecha_lanzamiento DATE DEFAULT CURRENT_DATE
);

-- Insertar datos de ejemplo en la tabla 'videojuegos'
-- Añadimos videojuegos de ejemplo para los géneros de 'Acción', 'Aventura', 'RPG' y 'Deportes'
INSERT INTO videojuegos (codigo, titulo, descripcion, precio, plataforma, stock, ventas, id_genero)
VALUES 
    -- Acción
    ('001', 'Shooter Extremo', 'Juego de disparos intensos', 60, 'PC', 20, 150, 1),
    ('002', 'Pelea Urbana', 'Juego de lucha en las calles', 50, 'Xbox', 30, 120, 1),
    ('003', 'Super Ninja', 'Aventuras y acción ninja', 70, 'PlayStation', 25, 90, 1),

    -- Aventura
    ('004', 'Isla Perdida', 'Exploración en una isla misteriosa', 50, 'PC', 15, 75, 2),
    ('005', 'Aventuras Épicas', 'Viaje por mundos fantásticos', 65, 'Nintendo Switch', 10, 80, 2),
    ('006', 'Cazador de Tesoros', 'Busca el tesoro perdido', 55, 'PlayStation', 20, 60, 2),

    -- RPG
    ('007', 'Reinos Mágicos', 'Conquista tierras mágicas', 70, 'PC', 12, 50, 3),
    ('008', 'Guerreros del Alba', 'RPG épico con batallas tácticas', 60, 'Xbox', 15, 45, 3),
    ('009', 'Leyendas Antiguas', 'Historia épica de héroes', 80, 'PC', 8, 30, 3),

    -- Deportes
    ('010', 'Fútbol Pro', 'Simulación de fútbol realista', 40, 'PC', 50, 200, 4),
    ('011', 'Básquet Estelar', 'Juego de baloncesto arcade', 30, 'PlayStation', 30, 150, 4),
    ('012', 'Tenis Master', 'Juego de tenis competitivo', 50, 'Nintendo Switch', 20, 100, 4)
ON CONFLICT (codigo) DO NOTHING;

-- Crear la tabla 'ventas' para registrar ventas individuales, con relación a 'usuarios' y 'videojuegos'
-- Cada venta registra el videojuego vendido, el usuario que realiza la compra, y la cantidad
CREATE TABLE IF NOT EXISTS ventas (
    id_venta SERIAL PRIMARY KEY,
    codigo_videojuego VARCHAR(10) REFERENCES videojuegos(codigo),
    email_usuario VARCHAR(255) REFERENCES usuarios(email),
    cantidad_vendida INT NOT NULL,
    fecha_venta DATE DEFAULT CURRENT_DATE
);

-- Insertar datos de ejemplo en la tabla 'ventas'
-- Añadimos ventas de ejemplo para relacionar videojuegos y usuarios
INSERT INTO ventas (codigo_videojuego, email_usuario, cantidad_vendida, fecha_venta)
VALUES 
    ('001', 'jugador1@example.com', 2, '2024-11-13'),
    ('004', 'jugador1@example.com', 1, '2024-11-14'),
    ('007', 'dev1@example.com', 1, '2024-11-15'),
    ('010', 'jugador1@example.com', 3, '2024-11-15'),
    ('012', 'jugador1@example.com', 1, '2024-11-16');

-- ########################################################################
-- # Consultas de verificación de datos en las tablas                     #
-- ########################################################################

-- Consultar todos los datos de la tabla 'roles'
SELECT * FROM roles;

-- Consultar todos los datos de la tabla 'usuarios'
SELECT * FROM usuarios;

-- Consultar todos los datos de la tabla 'generos'
SELECT * FROM generos;

-- Consultar todos los datos de la tabla 'videojuegos'
SELECT * FROM videojuegos;

-- Consultar todos los datos de la tabla 'ventas'
SELECT * FROM ventas;

-- Consultar todos los usuarios y sus roles
-- Esta consulta une las tablas 'usuarios' y 'roles' para mostrar el rol de cada usuario
SELECT u.email, u.nombre_usuario, r.nombre_rol
FROM usuarios u
JOIN roles r ON u.id_rol = r.id_rol;

-- Consultar todos los videojuegos con su género
-- Esta consulta une las tablas 'videojuegos' y 'generos' para mostrar el género de cada videojuego
SELECT v.codigo, v.titulo, v.descripcion, v.precio, v.plataforma, v.stock, v.ventas, g.nombre_genero
FROM videojuegos v
JOIN generos g ON v.id_genero = g.id_genero;

-- Consultar todas las ventas con detalles de usuario y videojuego
-- Esta consulta une las tablas 'ventas', 'usuarios', y 'videojuegos' para mostrar quién compró qué videojuego
SELECT v.id_venta, u.email AS usuario, vg.titulo, v.cantidad_vendida, v.fecha_venta
FROM ventas v
JOIN usuarios u ON v.email_usuario = u.email
JOIN videojuegos vg ON v.codigo_videojuego = vg.codigo;

-- Consultar el stock total de videojuegos
-- Esta consulta muestra el título del videojuego, el stock disponible y el total vendido.
SELECT titulo, stock, ventas FROM videojuegos;

-- Fin del archivo 'inicializacion_db.sql'
