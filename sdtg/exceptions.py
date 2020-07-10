class TileNotInTilesetException(Exception):
    def __init__(self):
        Exception.__init__(self, "Tile not in tileset. Please, create tile with decorator method @create_tile.")


class InvalidPositionFormat(Exception):
    def __init__(self):
        Exception.__init__(self, "Invalid position format! It must be 'x_y'!")
