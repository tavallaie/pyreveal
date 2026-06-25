class CSS:
    def __init__(self):
        self._properties = {}

    def __setitem__(self, key, value):
        """Allows setting properties using dictionary-like syntax."""
        self._properties[key] = value

    def __getitem__(self, key):
        """Allows getting properties using dictionary-like syntax."""
        return self._properties.get(key)

    def __delitem__(self, key):
        """Allows deleting properties using dictionary-like syntax."""
        if key in self._properties:
            del self._properties[key]

    def set_position(self, x, y, unit="px"):
        self["position"] = "absolute"
        self["left"] = f"{x}{unit}"
        self["top"] = f"{y}{unit}"

    def set_size(self, width, height, unit="px"):
        self["width"] = f"{width}{unit}"
        self["height"] = f"{height}{unit}"

    def set_rotation(self, angle, unit="deg"):
        self["transform"] = f"rotate({angle}{unit})"

    def set_background(self, color):
        self["background-color"] = color

    def set_border(self, width, style, color):
        self["border"] = f"{width}px {style} {color}"

    def __str__(self):
        return "; ".join([f"{k}: {v}" for k, v in self._properties.items()])


class Style:
    def __init__(self, **kwargs):
        self.properties = kwargs

    def generate_css(self):
        css_mappings = {
            "width": "width",
            "height": "height",
            "top": "top",
            "left": "left",
            "rotate": "transform",
            "font_size": "font-size",
            "color": "color",
            "background_color": "background-color",
            "border": "border",
            "border_radius": "border-radius",
            "margin": "margin",
            "padding": "padding",
            "text_align": "text-align",
        }

        css = []
        for prop, value in self.properties.items():
            if prop == "rotate":
                css.append(f"{css_mappings[prop]}: rotate({value}deg);")
            else:
                css.append(f"{css_mappings[prop]}: {value};")

        return " ".join(css)
