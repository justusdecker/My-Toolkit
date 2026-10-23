from pathlib import Path
from Log import log, LogTypes

UTF8 = 'utf8'

def overwrite_file(p_path: str, p_data: bytes | str, p_debug_text: str | None = None, p_encoding: str = UTF8, mode='wb'):
    """
    Uses `with open` to overwrite a file.
    
    * A debug statement will be printed if `p_debug_text` is not None
    * The Encoding is default `utf-8`
    """
    
    try:
        if p_debug_text is not None:
            log(
                'Start writing $ bytes to $ - $',
                [p_data.__len__(), p_path, p_debug_text]
            )
        with open(p_path, mode = 'w', encoding = p_encoding) as t_file:
            t_file.write(p_data)
    except Exception as E:
        log(
            '$',
            [str(E)],
            LogTypes.critical
        )
        raise E