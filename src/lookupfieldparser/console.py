import click

from parsley import makeGrammar

from . import __version__

cell_grammar = r"""
ws = (' ' | '\r' | '\n' | '\t')*
hexdigit = :x ?(x in '0123456789abcdefABCDEF') -> x
escapedUnicode = 'u' <hexdigit{4}>:hs -> unichr(int(hs, 16))
escapedChar = '\\' (('"' -> '"')    |('\\' -> '\\')
                   |('/' -> '/')    |('b' -> '\b')
                   |('f' -> '\f')   |('n' -> '\n')
                   |('r' -> '\r')   |('t' -> '\t')
                   |('\'' -> '\'')  | escapedUnicode)
string = (singleQuotedString | doubleQuotedString)
singleQuotedString = '\'' (escapedChar | ~'\'' anything)*:c '\'' -> ''.join(c)
doubleQuotedString = '"' (escapedChar | ~'"' anything)*:c '"' -> ''.join(c)
value = ws (string | lookupField)
elements = (value:first (ws ',' value)*:rest -> [first] + rest) | -> []
lookupField = '=LOOKUPFIELD(' elements:m ws ')' -> list(m)
"""


@click.command()
@click.argument('text')
@click.version_option(version=__version__)
def main(text):
    cells = makeGrammar(cell_grammar, {})
    print(u"Found: {}".format(cells(text).lookupField()))
