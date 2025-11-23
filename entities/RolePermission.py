from db.connection import get_connection

class RolePermission:
    
    @staticmethod
    def get_roles_with_permissions():
        """
        Obtiene todos los roles junto con sus permisos en un string.
        """
        sql = """
        SELECT 
            r.id,
            r.name,
            COALESCE(r.description, '') as description,
            COALESCE(STRING_AGG(p.code, ', '), 'Sin Permisos') as permissions_list
        FROM roles r
        LEFT JOIN role_permissions rp ON r.id = rp.role_id
        LEFT JOIN permissions p ON rp.permission_id = p.id
        GROUP BY r.id, r.name, r.description
        ORDER BY r.id ASC;
        """
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching roles with permissions: {e}")
            return []
        finally:
            if cur: cur.close()
            if conn: conn.close()