from db.connection import get_connection

class Role:
    
    @staticmethod
    def get_all():
        sql = "SELECT id, name FROM roles ORDER BY id ASC;"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            print(f"Error fetching roles: {e}")
            return []
        finally:
            if cur: cur.close()
            if conn: conn.close()
            
    @staticmethod
    def get_name_by_id(role_id):
        """Retorna el nombre del rol (str) dado su ID."""
        if not role_id: return "Invitado"
        
        sql = "SELECT name FROM roles WHERE id = %s;"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (role_id,))
            row = cur.fetchone()
            return row[0] if row else "Desconocido"
        except Exception as e:
            print(f"Error Role.get_name_by_id: {e}")
            return "Error"
        finally:
            if cur: cur.close()
            if conn: conn.close()