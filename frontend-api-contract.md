# Contrato para Frontend

Base URL sugerida en desarrollo: `http://localhost:8000`

Los endpoints protegidos usan JWT Bearer:

```http
Authorization: Bearer <access_token>
```

## Auth

| Metodo | Endpoint | Body | Respuesta |
| --- | --- | --- | --- |
| POST | `/auth/login` | `LoginRequest` | `TokenResponse` |
| POST | `/auth/register` | `RegisterRequest` | `RegisterResponse` |
| POST | `/auth/forgot-password` | `ForgotPasswordRequest` | `MessageResponse` |

## Products

| Metodo | Endpoint | Body | Respuesta | Roles |
| --- | --- | --- | --- | --- |
| GET | `/products/` | - | `ProductResponse[]` | autenticado |
| GET | `/products/{product_id}` | - | `ProductResponse` | autenticado |
| POST | `/products/` | `ProductCreate` | `ProductResponse` | `ADMIN`, `OPERADOR` |
| PUT | `/products/{product_id}` | `ProductUpdate` | `ProductResponse` | `ADMIN`, `OPERADOR` |
| DELETE | `/products/{product_id}` | - | `MessageResponse` | `ADMIN` |

## Delivery Points

| Metodo | Endpoint | Body | Respuesta | Roles |
| --- | --- | --- | --- | --- |
| GET | `/delivery-points/` | - | `DeliveryPointResponse[]` | autenticado |
| GET | `/delivery-points/{point_id}` | - | `DeliveryPointResponse` | autenticado |
| POST | `/delivery-points/` | `DeliveryPointCreate` | `DeliveryPointResponse` | `ADMIN`, `OPERADOR` |
| PUT | `/delivery-points/{point_id}` | `DeliveryPointUpdate` | `DeliveryPointResponse` | `ADMIN`, `OPERADOR` |
| DELETE | `/delivery-points/{point_id}` | - | `MessageResponse` | `ADMIN` |

## Dispatches

| Metodo | Endpoint | Body | Respuesta | Roles |
| --- | --- | --- | --- | --- |
| GET | `/dispatches/` | - | `DispatchResponse[]` | autenticado |
| GET | `/dispatches/?status=PENDIENTE` | - | `DispatchResponse[]` | autenticado |
| GET | `/dispatches/{dispatch_id}` | - | `DispatchResponse` | autenticado |
| POST | `/dispatches/` | `DispatchCreate` | `DispatchResponse` | `ADMIN`, `OPERADOR` |
| PATCH | `/dispatches/{dispatch_id}/status` | `DispatchStatusUpdate` | `DispatchResponse` | `ADMIN`, `OPERADOR`, `SUPERVISOR` |

## Estados validos

`DispatchStatus`: `PENDIENTE`, `ENVIADO`, `ENTREGADO`, `CANCELADO`

Transiciones permitidas:

| Desde | Hacia |
| --- | --- |
| `PENDIENTE` | `ENVIADO`, `CANCELADO` |
| `ENVIADO` | `ENTREGADO`, `CANCELADO` |
| `ENTREGADO` | sin transiciones |
| `CANCELADO` | sin transiciones |

`ProductStatus`: `ACTIVE`, `INACTIVE`

`UserRole`: `ADMIN`, `OPERADOR`, `SUPERVISOR`

## Nota tecnica

En el backend, `User.id` esta definido como UUID en SQLAlchemy, pero `UserResponse.id` esta tipado como `int` en `app/schemas/user_schema.py`. Para el frontend lo deje como `UUID`, porque es lo que realmente devuelve el servicio de login.
