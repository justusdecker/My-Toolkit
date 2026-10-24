import math
def convert_bytes(p_size_bytes: int) -> str:
    """
    Convert bytes to a human-readable format (e.g., KB, MB, GB).
    Returns a string representation of the size.
    """
    if p_size_bytes == 0: return "0B"
    
    l_base = 1024
    l_units = ["B", "KB", "MB", "GB", "TB", "PB", 'EB', 'ZB', 'YB', 'BB', 'GBP', 'SB']
    
    l_unit_index = min(
        int(math.log(p_size_bytes, l_base)), 
        len(l_units) - 1
        )
    l_converted_size = p_size_bytes / (l_base ** l_unit_index)
    
    return f"{l_converted_size:.0f} {l_units[l_unit_index]}"
