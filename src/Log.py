from enum import Enum
from typing import Any, LiteralString
from datetime import datetime
from ConverterUtils import Color, get_colorized_background, get_colorized_text
GC_COPYRIGHT = '© 2025 - 2026 Justus Decker - PrettyLogger'
GC_GITHUB_URL = 'https://github.com/justusdecker/My-Toolkit'
GC_VERSION = 1, 0, 0
"""
* Add Depth coloring for lists, dicts and tuples - qol
"""
    
class LogTypes(Enum):
    """
    debug = 0
    info = 1
    warning = 2
    error = 3
    critical = 4
    """
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
    critical = '\033[31;1;1m\033[3m'

class LogTypeIcons(Enum):
    debug = '🔵'
    info = '🟢'
    warning = '🟡'
    error = '🔴'
    critical = '💥'
    
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

class LogDateCrop(Enum):
    """
    nodate = 0
    fulldate = 1
    onlytime = 2
    onlydate = 3
    """
    nodate = 0
    fulldate = 1
    onlytime = 2
    onlydate = 3

def log(
    p_message: str, 
    p_variables: list[Any] | None = None, 
    p_logtype: LogTypes = LogTypes.debug,
    p_date_crop: LogDateCrop = LogDateCrop.onlytime,
    p_use_icons = False):
    """
    The pretty way to log your things
    
    Each $ will be replaced by the given variables, if nothing is there or the variable list is too short it will output a NULL in RED
    
    .. p_message:: The string message you want to print e.g. `"ABC $ $ $ $"`
    .. p_variables:: The variables you want to highlight e.g. `[0.2,None, 2]`
    .. p_logtype:: The mode: debug, warning or critical? For more information visit the `LogTypes`-Class
    .. p_date_crop:: Which way do you want to display the time? Look into the `LogDateCrop`-Class for more information
    .. p_use_icons:: True Icons like (🟡) will displayes instead of the text `"WAR"`
    
    How to use
    ***
    ```python
    from Log import log, LogTypes, LogDateCrop
    log('ABC $ $ $ $',
        [0.2,None, 2],
        LogTypes.info,
        LogDateCrop.fulldate,
        True # This enables the icon use
        )
    ```
    
    """
    l_log_icon = LogTypeIcons[p_logtype.name]
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
                t_word = get_colorized_background('#FF0000', 'NULL')
            l_combined_message_content += t_word
                
    else:
        l_combined_message_content = p_message
    
    l_datetime_format = '%d/%m/%Y %H:%M:%S'
    
    if p_date_crop == LogDateCrop.nodate:
        l_datetime_format = ''
    elif p_date_crop == LogDateCrop.onlydate:
        l_datetime_format = l_datetime_format.split(' ')[0]
    elif p_date_crop == LogDateCrop.onlytime: # 🦆
        l_datetime_format = l_datetime_format.split(' ')[1]
    l_datetime_format = (' ' if l_datetime_format else '') + l_datetime_format
        
    print(f'[{l_logcolor}{l_log_icon.value if p_use_icons else l_logtype_cropped}{datetime.now().strftime(l_datetime_format)}\033[0m] {l_combined_message_content}\033[0m')



log('Startup Version: $ $ For more information visit: $', [GC_VERSION, GC_COPYRIGHT, GC_GITHUB_URL],LogTypes.info)