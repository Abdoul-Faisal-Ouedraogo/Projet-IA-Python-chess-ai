class Color:
    def __init__(self, light, dark):
        self.light = light
        self.dark = dark

    def as_tuple(self):
        """Retourne les deux couleurs sous forme de tuple (utile pour debug)."""
        return (self.light, self.dark)
