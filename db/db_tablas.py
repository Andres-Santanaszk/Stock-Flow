import psycopg2

#? Crear las tablas necesarias:

#? Tabla items
# '''
# item_id
# item_name
# item_sku
# item_bar_code
# item_type
# item_quantity
# item_state
# category_id   -- FK
# brand_id      -- FK
# '''
#?

#? Tabla users
# '''
# user_id
# user_name
# user_age
# user_email
# user_join_date
# '''
#?

#? Tabla uoms
# '''
# uom_id
# uom_name
# uom_symbol
# uom_type
# '''
#?

#? Tabla categories
# '''
# category_id
# category_name
# '''
#?

#? Tabla brands
# '''
# brand_id
# brand_name
# '''
#?
connection = psycopg2.connect(host = 'localhost', port = '5432', user = 'postgres', password = 'contaseña de la base de datos', dbname = 'stock_flow')
cursor = connection.cursor()
tabla_users = cursor.execute('''
CREATE TABLE users(
                                user_id SERIAL PRIMARY KEY,
                                user_name VARCHAR(50),
                                user_age INTEGER,
                                user_email VARCHAR(100),
                                user_join_date DATE DEFAULT CURRENT_DATE NOT NULL
)
''')
tabla_categories = cursor.execute('''
CREATE TABLE categories(
                                category_id SERIAL PRIMARY KEY,
                                category_name VARCHAR(50)
)
''')
tabla_brands = cursor.execute('''
CREATE TABLE brands(
                                brand_id SERIAL PRIMARY KEY,
                                brand_name VARCHAR(50)
)
''')
tabla_uoms = cursor.execute('''
CREATE TABLE uoms(
                                uom_id SERIAL PRIMARY KEY,
                                uom_name VARCHAR(50),
                                uom_symbol VARCHAR(50),
                                uom_type VARCHAR(50)
)
''')
tabla_items = cursor.execute('''
CREATE TABLE items(
                                item_id SERIAL PRIMARY KEY,
                                item_name VARCHAR(50),
                                item_sku VARCHAR(50),
                                item_bar_code VARCHAR(50),
                                item_type VARCHAR(50),
                                item_quantity INTEGER,
                                item_state BOOLEAN GENERATED ALWAYS AS (item_quantity > 0) STORED,
                                category_id INTEGER,
                                CONSTRAINT fk_category
                                    FOREIGN KEY (category_id)
                                    REFERENCES categories(category_id),
                                brand_id INTEGER,
                                CONSTRAINT fk_brand
                                    FOREIGN KEY (brand_id)
                                    REFERENCES brands(brand_id)
)
''')
connection.commit()