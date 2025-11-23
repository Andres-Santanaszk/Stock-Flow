from db.connection import get_connection

class Permission:
    
    @staticmethod
    def get_codes_by_role_id(role_id):
        """
        Retorna una lista de strings con los codigos de permiso.
        """
        if not role_id: return []

        sql = """
        SELECT p.code 
        FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        WHERE rp.role_id = %s;
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (role_id,))
            rows = cur.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Error Permission.get_codes_by_role_id: {e}")
            return []
        finally:
            if cur: cur.close()
            if conn: conn.close()