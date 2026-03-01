## **Stock Flow**

**Professional desktop application for inventory control, movements, auditing, user management, and graphical reporting.** Built with **Python + PySide6**, connected to **PostgreSQL**, and featuring a comprehensive **Roles and Permissions** system.

### **Core Technologies**

- **Python 3.10+**
- **PySide6 + QtAwesome + QDarkTheme** (Modern UI with dark mode support)
- **PostgreSQL 16** (Deployed via Docker)
- **bcrypt** for secure password hashing
- **Matplotlib** for interactive dashboards and analytics

---

### **Key Features**

### **Authentication & Security**

- Secure login using **bcrypt** (`security/hashing.py`).
- Session management.
- Robust **RBAC (Role-Based Access Control)** and permissions model (`entities.Role`, `entities.Permission`).

### **Modern Interface**

- Dark theme with animated transitions.
- Dynamic side menu (toggles based on user permissions).
- Smooth UI animations powered by **PySide6 (Qt Widgets)**.

### **Dashboard & Analytics**

- Categorized distribution charts.
- Critical stock alerts.
- Top users by activity level.
- Ready-to-use **seed data** for demos.

### **Comprehensive Inventory Management**

- **CRUD** operations for items, categories, brands, and locations.
- Inventory views filtered by location.
- Stock validation and "no-negative" logic.

### **Smart Inventory Movements**

- Movement types: **IN / OUT / ADJUST**.
- Item auto-complete functionality.
- Source/Destination validation.
- PostgreSQL **triggers and views** for real-time data integrity.

### **User Management**

- Create and edit user profiles.
- Assign specific roles and permissions.
- Dedicated administrative view (`ui/forms/user_hub.py`).

---

### **Advanced Database Implementation**

- **Enums** for movement types.
- **Triggers** for automatic stock updates.
- **Database Views** for reporting real-time availability.
- Automatic recalculation in `item_locations`.
- Server-side logic to prevent negative stock.

---

### **Setting Up the Database with Docker**

The project includes a `docker-compose.yml` file to deploy:

1. **PostgreSQL**
2. **Adminer** (Web-based DB Management UI) → `http://localhost:8080`

---

### **How to Run (Development Mode)**

1. **Create a Virtual Environment**
    
    `python -m venv venv`
    # Windows:
    `.\venv\Scripts\activate`
    # Linux/Mac:
    `source venv/bin/activate`
    
    > 
2. **Configure Environment Variables** Copy `.env.example` to `.env` and adjust the following:
    - `PGUSER` / `PGPASSWORD`
    - `PGSUPERUSER` / `PGSUPERPASSWORD`
3. **Install Dependencies**
    
    `pip install -r requirements.txt`
    
4. **Launch Docker Containers**
    
    `docker-compose up -d`
    
    > 
5. **Initialize Database (Migrations + Seeds)**
    
    `python -m db.setup_db`
    
    *This creates the roles, database, tables, views, triggers, and demo data.*
    
6. **Run the Application**
    
    `python main.py`
   
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


### **Downloads**

Download the latest version: [Stock Flow Releases](https://github.com/Andres-Santanaszk/Stock-Flow/releases/latest)

**Available files:**

- `StockFlow.exe` (Standalone executable)
- `StockFlow.zip`
- Source Code
