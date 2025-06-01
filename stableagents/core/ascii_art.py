"""ASCII art banners for StableAgents CLI"""

STABLE_AGENTS_BANNER = """
  ____  _        _     _        _                    _       
 / ___|| |_ __ _| |__ | | ___  / \   __ _  ___ _ __ | |_ ___ 
 \___ \| __/ _` | '_ \| |/ _ \/ _ \ / _` |/ _ \ '_ \| __/ __|
  ___) | || (_| | |_) | |  __/ ___ \ (_| |  __/ | | | |_\__ \\
 |____/ \__\__,_|_.__/|_|\___/_/   \_\__, |\___|_| |_|\__|___/
                                     |___/                   
"""

SIMPLE_BANNER = """
 ===========================================
 |                                         |
 |           S T A B L E A G E N T S       |
 |                                         |
 ===========================================
"""

COMPACT_BANNER = """
 /=====\\ |====| /=====\\ |====\ |     |====== /=====\\ | \\   | |====| /=====\\
 |       |    | |     | |     | |     |       |     | |  \\  | |    | |      
 \\====\\  |====| |=====| |====<  |     |====   |=====| |   \\ | |    | \\====\\
      |  |    | |     | |     | |     |       |     | | |\\ | |    |      |
 \\=====/  |    | |     | |====/ |====| |====== |     | | | \\| |====| \\=====/
"""

def get_banner(style="default"):
    """Returns an ASCII art banner for the CLI.
    
    Args:
        style: The style of banner to return (default, simple, compact)
        
    Returns:
        str: The ASCII art banner
    """
    if style == "simple":
        return SIMPLE_BANNER
    elif style == "compact":
        return COMPACT_BANNER
    else:
        return STABLE_AGENTS_BANNER 