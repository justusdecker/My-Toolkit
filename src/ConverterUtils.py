import math

GC_BYTE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB", 'EB', 'ZB', 'YB', 'BB', 'GBP', 'SB']

def convert_byte_ammount(p_size_bytes: int) -> str:
    """
    Convert bytes to a human-readable format (e.g., KB, MB, GB).
    Returns a string representation of the size.
    """
    if p_size_bytes == 0: return "0B"
    
    l_base = 1024
    
    l_unit_index = min(
        int(math.log(p_size_bytes, l_base)), 
        len(GC_BYTE_UNITS) - 1
        )
    l_converted_size = p_size_bytes / (l_base ** l_unit_index)
    
    return f"{l_converted_size:.0f} {GC_BYTE_UNITS[l_unit_index]}"

class Color:
    def __init__(self, p_hex: str):
        if isinstance(p_hex, Color):
            self.r, self.g, self.b =p_hex.r,p_hex.g,p_hex.b
            return
        self.r, self.g, self.b = Color.convert_hex_to_rgb(p_hex)

    @staticmethod
    def convert_hex_to_rgb(p_hex: str) -> tuple[int, int, int]:
        """
        Does what the function-title sais and return a `tuple[int, int, int]` <- Color
        """
        if isinstance(p_hex, Color): return p_hex
        if p_hex[0] == '#': p_hex = p_hex[1:] # remove # prefix
        return int(p_hex[0:2], base = 16), int(p_hex[2:4], base = 16), int(p_hex[4:6], base = 16)

def get_colorized_text(p_color: str, p_text: str) -> str:
    """
    Uses Escape-Sequences to colorize the terminal text.
    
    No printing is happening here!
    
    🦄Taste the rainbow🌈
    """
    l_color = Color(p_color)
    return f'\033[38;2;{l_color.r};{l_color.g};{l_color.b}m{p_text}\033[0m'

def get_colorized_background(p_color: str, p_text: str) -> str:
    """
    Uses Escape-Sequences to colorize the terminal background.
    
    No printing is happening here!
    
    🦄Taste the rainbow🌈
    """
    l_color = Color(p_color)
    return f'\033[48;2;{l_color.r};{l_color.g};{l_color.b}m{p_text}\033[0m'