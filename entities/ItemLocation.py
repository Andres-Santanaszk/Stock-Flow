class ItemLocation:
    def __init__(self, id_item=None, id_location=None, qty=None):
        self.id_item = id_item
        self.id_location = id_location
        self.qty = qty

    def get(self, item_id, location_id):
        """
        Devuelve la cantidad actual de un producto en una ubicación especifica
        """
        pass

    def list_by_item(self, item_id):
        """
        Muestra todas las ubicaciones donde existe el producto y su cantidad en cada una
        """
        pass

    def __repr__(self):
        """
        Devuelve una representación corta del objeto mostrando el nombre del producto la ubicación y la cantidad diponible.
        """
        pass
    