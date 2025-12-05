#  **Stock Flow**

**Aplicación de escritorio profesional para control de inventario, movimientos, auditoría, usuarios y reportes gráficos.**

Construida con **Python + PySide6**, conectada a **PostgreSQL**, e incluye un sistema completo de **roles y permisos**.

---

## **Tecnologías principales**

- **Python 3.10+**
- **PySide6 + QtAwesome + QDarkTheme** (UI moderna con tema oscuro)
- **PostgreSQL 16** (se levanta vía Docker)
- **bcrypt** para contraseñas seguras
- **Matplotlib** para dashboards y gráficas
---

## **Características principales**

###  **Autenticación y seguridad**

- Login seguro con **bcrypt** (`security/hashing.py`)
- Manejo de sesiones
- Modelo sólido de **roles** y **permisos** (`entities.Role`, `entities.Permission`)

###  **Interfaz moderna**

- Tema oscuro con transiciones animadas
- Menú lateral dinámico (se oculta según permisos)
- Animaciones suaves entre vistas
- UI diseñada con PySide6 (Qt Widgets)

###  **Dashboard con gráficas**

Implementado en `ui/view/dashboard_view.py` + `entities/Dashboard.py`:

- Distribución por categoría
- Alertas de stock crítico
- Top usuarios por actividad
- Datos seed listos para demo

###  **Gestión completa de inventario**

- CRUD de ítems, categorías, marcas y ubicaciones (`ui/forms/register_hub.py`)
- Vistas de inventario por ubicación
- Validación de stock y lógica de “no negativos”

###  **Movimientos de inventario inteligentes**

- Tipos IN / OUT / ADJUST
- Autocompletado de ítems
- Validación de origen/destino
- Modelo de datos soportado con **triggers y vistas Postgres**

###  **Gestión de usuarios**

- Crear / editar usuarios
- Asignar roles y permisos
- Vista especializada para administración (`ui/forms/user_hub.py`)

---

##  **Modelo de datos para Postgres**

Implementación avanzada con:

- **Enums** para tipos de movimiento
- **Triggers** que actualizan stock automáticamente
- **Vistas** para reportar disponibilidad real
- Recalculo en `item_locations`
- Lógica para **evitar stock negativo**

---

## 🐳 **Levantando la base de datos con Docker**

El proyecto incluye un `docker-compose.yml` que levanta:

- PostgreSQL
- Adminer (UI web para DB) → [http://localhost:8080](http://localhost:8080/)

---

##  **Cómo ejecutar el proyecto (modo desarrollo)**

### 1. Crear entorno virtual

```bash
python -m venv venv
.\venv\Scripts\activate

```

### 2. Configurar variables de entorno

Copia `.env.example` → `.env`

Ajusta:

```
PGUSER
PGPASSWORD
PGSUPERUSER
PGSUPERPASSWORD

```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt

```

### 4. Levantar Docker

```bash
docker-compose up -d

```

### 5. Crear base de datos + migraciones + seeds

```bash
python -m db.setup_db

```

(Ejecuta: creación de rol, DB, tablas, vistas, triggers y datos demo)

### 6. Ejecutar la app

```bash
python main.py

```

---

## Screenshots - Stock Flow

<img width="855" height="581" alt="Screenshot 2025-12-01 230530" src="https://github.com/user-attachments/assets/888da39c-6052-4263-a2e2-28032852905a" />
<img width="1385" height="829" alt="image" src="https://github.com/user-attachments/assets/0396b474-b637-40c9-a028-3ea4429e5175" />
<img width="1410" height="827" alt="Screenshot 2025-12-01 230636" src="https://github.com/user-attachments/assets/390a5beb-4daf-479d-a241-281d5cc0b235" />
<img width="1392" height="825" alt="Screenshot 2025-12-01 231514" src="https://github.com/user-attachments/assets/8f0e6e39-0c49-49a2-b7c5-8461f5d8b4b7" />
<img width="1398" height="829" alt="Screenshot 2025-12-01 230754" src="https://github.com/user-attachments/assets/5bb8b848-dce8-49f3-8be2-02f47f3f9e74" />
<img width="1393" height="825" alt="Screenshot 2025-12-01 230748" src="https://github.com/user-attachments/assets/56d1de1c-5aca-411e-9498-4bed06254fa6" />
<img width="1405" height="831" alt="Screenshot 2025-12-01 230802" src="https://github.com/user-attachments/assets/29b32582-8576-47d1-954d-719a2891053a" />
<img width="1403" height="835" alt="Screenshot 2025-12-01 230854" src="https://github.com/user-attachments/assets/bed38d8e-cd2f-4905-870b-2c45d014b9b4" />
<img width="1406" height="829" alt="Screenshot 2025-12-01 230848" src="https://github.com/user-attachments/assets/97ef69e8-3401-4f56-8120-0a1466dd159d" />

---


## **Descargas**

Descarga la última versión:
 **https://github.com/Andres-Santanaszk/Stock-Flow/releases/latest**

Archivos disponibles:

- `StockFlow.exe` (ejecutable)
- `StockFlow.zip`
- Código fuente
