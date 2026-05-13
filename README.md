# Dispatch Management API

Aplicación backend en FastAPI para gestionar productos, puntos de entrega y despachos con control de roles y estados.

## 🧩 Resumen

Esta API administra:
- Usuarios con autenticación JWT
- Productos con stock y estado activo/inactivo
- Puntos de entrega con información de dirección y receptor
- Despachos con detalles de productos y transición de estados

Está diseñada para ser consumida por un frontend o integraciones que requieran gestionar un flujo de despacho logístico.

## 🛠️ Tecnologías principales

- Python 3.x
- FastAPI
- SQLAlchemy
- PostgreSQL (vía `psycopg2-binary`)
- JWT con `python-jose`
- `bcrypt` para hashing de contraseñas
- `python-dotenv` para variables de entorno

## 📁 Estructura del proyecto

- `app/main.py` - arranque de la aplicación y registro de routers
- `app/database.py` - configuración de base de datos con SQLAlchemy
- `app/models/` - modelos ORM para `users`, `products`, `delivery_points`, `dispatches`, `dispatch_details`
- `app/schemas/` - esquemas Pydantic para validación de datos
- `app/services/` - lógica de negocio para autenticación, productos y despachos
- `app/routers/` - endpoints organizados por recurso
- `app/utils/security.py` - helpers de autenticación y autorización

## ⚙️ Configuración inicial

1. Crea y activa el entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instala dependencias:

```powershell
pip install -r requirements.txt
```

3. Configura las variables de entorno en un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/mi_base_de_datos
SECRET_KEY=una_clave_secreta_muy_larga
ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:5173
```

> Si estás usando SQLite u otra base de datos, actualiza `DATABASE_URL` según la conexión deseada.

4. Crea las tablas ejecutando la app, ya que `Base.metadata.create_all(bind=engine)` crea el esquema automáticamente.

## 🚀 Ejecución

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Accede a la documentación interactiva de Swagger:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## 🔐 Autenticación y roles

La API usa JWT con bearer token. Los endpoints de creación y actualización requieren roles específicos.

Roles usados:
- `ADMIN`
- `OPERADOR`
- `SUPERVISOR`

### Roles y permisos

- `ADMIN`:
  - crear productos
  - editar productos
  - eliminar productos
  - crear puntos de entrega
  - editar puntos de entrega
  - eliminar puntos de entrega
  - crear despachos
  - cambiar estado de despacho
- `OPERADOR`:
  - crear productos
  - editar productos
  - crear puntos de entrega
  - editar puntos de entrega
  - crear despachos
  - cambiar estado de despacho
- `SUPERVISOR`:
  - consultar productos, puntos de entrega y despachos
  - cambiar estado de despacho

## 📌 Endpoints principales

### Auth

- `POST /auth/register`
  - Datos: `email`, `password`, `role`
  - Crea usuario

- `POST /auth/login`
  - Datos: `email`, `password`
  - Responde con `access_token`

- `POST /auth/forgot-password`
  - Datos: `email`, `new_password`, `confirm_password`
  - Actualiza contraseña

### Products

- `POST /products/`
  - Crear producto
  - Requiere rol `ADMIN` o `OPERADOR`
  - Datos: `sku`, `name`, `stock`, `unit`

- `GET /products/`
  - Listar productos activos
  - Requiere autenticación

- `GET /products/{product_id}`
  - Obtener producto por ID
  - Requiere autenticación

- `PUT /products/{product_id}`
  - Actualizar producto
  - Requiere rol `ADMIN` o `OPERADOR`

- `DELETE /products/{product_id}`
  - Desactivar producto (`status = INACTIVE`)
  - Requiere rol `ADMIN`

### Delivery Points

- `POST /delivery-points/`
  - Crear punto de entrega
  - Requiere rol `ADMIN` o `OPERADOR`

- `GET /delivery-points/`
  - Listar puntos de entrega
  - Requiere autenticación

- `GET /delivery-points/{point_id}`
  - Obtener punto de entrega por ID
  - Requiere autenticación

- `PUT /delivery-points/{point_id}`
  - Actualizar punto de entrega
  - Requiere rol `ADMIN` o `OPERADOR`

- `DELETE /delivery-points/{point_id}`
  - Eliminar punto de entrega
  - Requiere rol `ADMIN`

### Dispatches

- `POST /dispatches/`
  - Crear despacho con detalles de productos
  - Requiere rol `ADMIN` o `OPERADOR`
  - Datos: `delivery_point_id`, lista `details` con `product_id` y `quantity`

- `GET /dispatches/`
  - Listar despachos
  - Permite filtro opcional `status`
  - Requiere autenticación

- `GET /dispatches/{dispatch_id}`
  - Obtener despacho por ID
  - Requiere autenticación

- `PATCH /dispatches/{dispatch_id}/status`
  - Actualizar estado del despacho
  - Requiere rol `ADMIN`, `OPERADOR` o `SUPERVISOR`

## 🔄 Flujo de trabajo de la aplicación

### 1. Registro e inicio de sesión

1. El usuario se registra con `POST /auth/register`.
2. Inicia sesión con `POST /auth/login`.
3. Recibe un JWT para usar en las siguientes llamadas.

### 2. Gestión de productos

1. Crear producto con `POST /products/`.
2. Consultar inventario con `GET /products/`.
3. Actualizar stock o información del producto con `PUT /products/{product_id}`.
4. Desactivar producto con `DELETE /products/{product_id}`.

### 3. Gestión de puntos de entrega

1. Crear punto de entrega con `POST /delivery-points/`.
2. Consultar puntos con `GET /delivery-points/`.
3. Actualizar datos con `PUT /delivery-points/{point_id}`.
4. Eliminar con `DELETE /delivery-points/{point_id}`.

### 4. Creación de despacho

1. Crear despacho vinculando un punto de entrega y productos.
2. El sistema valida stock disponible y resta las cantidades.
3. Se crea un registro en `dispatches` y `dispatch_details`.

### 5. Gestión de estados de despacho

El flujo de estados actual es:

- `PENDIENTE` → `ENVIADO` o `CANCELADO`
- `ENVIADO` → `ENTREGADO` o `CANCELADO`
- `ENTREGADO` → finalizado
- `CANCELADO` → finalizado

Esto asegura que no se puedan hacer transiciones inválidas entre estados.

## 📊 Modelo de datos simplificado

- `User`
  - `id`, `email`, `password_hash`, `role`, `is_active`, `created_at`
- `Product`
  - `id`, `sku`, `name`, `stock`, `unit`, `status`, `created_at`
- `DeliveryPoint`
  - `id`, `name`, `address`, `city`, `zone`, `receiver_name`, `delivery_schedule`, `created_at`
- `Dispatch`
  - `id`, `delivery_point_id`, `created_by`, `dispatch_date`, `status`, `created_at`
- `DispatchDetail`
  - `id`, `dispatch_id`, `product_id`, `quantity`, `created_at`

## ✅ Recomendaciones de uso

- Inicia siempre sesión antes de llamar a endpoints protegidos.
- Usa el token Bearer en `Authorization`.
- Controla el stock al crear despachos para evitar errores.
- Registra usuarios con roles adecuados según la operación.

## 💡 Mejoras posibles

- Añadir manejo de migraciones con Alembic real.
- Incluir paginación en listados.
- Añadir validaciones más estrictas de roles y permisos.
- Implementar control de usuarios activos/inactivos.
- Crear endpoints de reporte y exportación de despachos.

---

Esta documentación cubre la arquitectura, los endpoints, los roles, los flujos de negocio y el arranque de la aplicación.
