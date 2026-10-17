from enum import Enum
from typing import Any, LiteralString
type Color = tuple[int, int, int]

"""
* Add Icons
* Add Emojis
* Add Padding
* Add Log Time
* Colorize NULL
"""

class Color:
    def __init__(self, p_hex: str):
        if isinstance(p_hex, Color):
            self.r, self.g, self.b =p_hex.r,p_hex.g,p_hex.b
            return
        self.r, self.g, self.b = Color.convert_hex_to_rgb(p_hex)

    @staticmethod
    def convert_hex_to_rgb(p_hex: str) -> Color:
        """
        Does what the function-title sais and return a `tuple[int, int, int]` <- Color
        """
        if isinstance(p_hex, Color): return p_hex
        if p_hex[0] == '#': p_hex = p_hex[1:] # remove # prefix
        return int(p_hex[0:2], base = 16), int(p_hex[2:4], base = 16), int(p_hex[4:6], base = 16)
    
class LogTypes(Enum):
    debug = 0
    info = 1
    warning = 2
    error = 3
    critical = 4

class LogTypeColors(Enum):
    debug = '\033[34;1;1m'
    info = '\033[32;1;1m'
    warning = '\033[33;1;1m'
    error = '\033[31;1;1m'
    critical = '\033[31;1;1m\033[41;1;1m'
    
class LogVariableColorTypes(Enum):
    integer = 'int'
    string = 'str'
    boolean = 'bool'
    _float = 'float'
    dictionary = 'dict'
    _tuple = 'tuple'
    array = 'list'
    bytesequence = 'bytes'
    none = 'NoneType'

class LogVariableColors(Enum):
    integer = Color('#CCFF99')
    string = Color('#FFCC99')
    boolean = Color('#FF9999')
    _float = Color('#99FFFF')
    dictionary = Color('#FFFF99')
    _tuple = Color('#FF99FF')
    array = Color('#9999FF')
    bytesequence = Color('#FFCC00')
    none = Color("#3D5585")

class LogAttributes:
    class PaddingAttributes:
        pady: ...

    class AlignAttributes:
        ...
    class Colors(Enum): #! outsource later for a bigger color table can be useful sometimes
        ...
    class Icons: #! outsource later for a bigger icon table can be useful sometimes
        ...
    class Emojis: #! outsource later for a bigger emoji table can be useful sometimes
        ...


def get_colorized_text(p_color: str, p_text: str) -> str:
    """
    Uses Escape-Sequences to colorize the terminal text.
    
    No printing is happening here!
    
    🦄Taste the rainbow🌈
    """
    l_color = Color(p_color)
    return f'\033[38;2;{l_color.r};{l_color.g};{l_color.b}m{p_text}\033[0m'

def log(
    p_message: str, 
    p_variables: list[Any] | None = None, 
    p_logtype: LogTypes = LogTypes.debug):
    """
    The pretty way to log your things
    """
    l_logtype_cropped: LiteralString = p_logtype.name.upper()[:3]
    l_logcolor: LogTypeColors = LogTypeColors[p_logtype.name].value
    l_combined_message_content = ''
    l_variable_counter = 0
    
    def string_convert_to_color_if_possible(p_color: LogVariableColors):
        l_variable_content: str = p_variables[l_variable_counter]
        if p_color.name == LogVariableColors.string:
            if l_variable_content.startswith('#') and l_variable_content.__len__() == 7:

                l_word = get_colorized_text(l_variable_content,l_variable_content)
            else:
                l_word = get_colorized_text(p_color.value,l_variable_content)
        else:
            l_word = get_colorized_text(p_color.value,l_variable_content)
        return l_word
    
    if p_variables is not None:
        for idx,char in enumerate(p_message):
            t_word = char
            if char == '$' and l_variable_counter <= len(p_variables) - 1:
                t_temp_type_cropped = str(type(p_variables[l_variable_counter])).removeprefix('<class \'').removesuffix('\'>')
                t_variable_color_type = LogVariableColorTypes(t_temp_type_cropped)
                t_variable_color = LogVariableColors[t_variable_color_type.name]
                t_word = string_convert_to_color_if_possible(t_variable_color)
                l_variable_counter += 1
            elif l_variable_counter > len(p_variables) - 1 and char == '$':
                t_word = '[NULL]'
            l_combined_message_content += t_word
                
    else:
        l_combined_message_content = p_message
        
    print(f'[{l_logcolor}{l_logtype_cropped}\033[0m] {l_combined_message_content}\033[0m')
    
for i in range(5):
    log('Hello World', p_logtype=LogTypes(i))

log('ABC $ $ $ $ $ $ $ $ $ $ $ $ $', [0.2,None, 2, [123], (32, 3), "Hello", {'key': "test"}, b'10101', True])