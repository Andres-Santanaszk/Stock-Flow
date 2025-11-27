from db.connection import get_connection

class DashboardService:
    
    @staticmethod
    def get_category_distribution():
        """
        Data para el DONUT CHART (Como el 'Budget Report' de la imagen).
        Muestra qué categorías ocupan más espacio en inventario.
        """
        sql = """
        SELECT 
            c.name,
            SUM(il.qty) as total_stock
        FROM item_locations il
        JOIN items i ON il.id_item = i.id_item
        JOIN categories c ON i.category_id = c.id_category
        GROUP BY c.name
        HAVING SUM(il.qty) > 0
        ORDER BY total_stock DESC
        LIMIT 6; -- Limitamos a 6 para que el gráfico no se sature
        """
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall() # [(Category, Count), ...]
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
        finally:
            if conn: conn.close()

    @staticmethod
    def get_critical_stock():
        """
        Data para BARRAS HORIZONTALES (Como las barras de 'Savings' de la imagen).
        Muestra items con stock bajo comparado con su mínimo.
        """
        sql = """
        SELECT 
            i.name, 
            i.min_qty, 
            COALESCE(SUM(il.qty), 0) as current_stock
        FROM items i
        LEFT JOIN item_locations il ON i.id_item = il.id_item
        LEFT JOIN locations l ON il.id_location = l.id_location 
        WHERE i.active = TRUE 
          AND (l.type IS NULL OR l.type != 'ScrapArea')
        GROUP BY i.id_item
        HAVING COALESCE(SUM(il.qty), 0) <= i.min_qty
        ORDER BY current_stock ASC 
        LIMIT 5;
        """
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall() # [(Name, Min, Current), ...]
        except Exception as e:
            print(f"Error fetching critical stock: {e}")
            return []
        finally:
            if conn: conn.close()

    @staticmethod
    def get_top_users_movements():
        """Consulta: Ranking de usuarios con más actividad (IN/OUT/ADJUST)"""
        sql = """
        SELECT 
            u.full_name, -- Asegúrate que tu tabla users tiene 'username' o cambia por 'email'
            COUNT(m.id_mov) as total_movs
        FROM movements m
        JOIN users u ON m.id_user = u.id_user
        GROUP BY u.full_name
        ORDER BY total_movs DESC
        LIMIT 7;
        """
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
        except Exception as e:
            print(f"Error user stats: {e}")
            return []
        finally:
            if conn: conn.close()