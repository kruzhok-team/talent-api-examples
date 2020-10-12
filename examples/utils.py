import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

def pprint(data):
    """
    Pretty print helper for json output
    """
    print(
        highlight(
            json.dumps(data, indent=4, sort_keys=True), 
            JsonLexer(), 
            TerminalFormatter()
        )
    )
