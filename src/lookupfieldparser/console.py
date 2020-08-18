import click

from ometa.runtime import ParseError
from parsley import makeGrammar

from . import __version__

cell_grammar = r"""
string = (singleQuotedString | doubleQuotedString)
singleQuotedString = '\'' ( ~'\'' anything)*:c '\'' -> ''.join(c)
doubleQuotedString = '"' ( ~'"' anything)*:c '"' -> ''.join(c)
value = ws (string | lookupField)
elements = (value:first (ws ',' value)*:rest -> [first] + rest) | -> []
lookupField = 'LOOKUPFIELD(' elements:m ws ')' -> list(m)
cellFormula = '=' lookupField
"""


@click.command()
@click.argument('text')
@click.version_option(version=__version__)
def main(text):
    value_locations = []
    def traceit(grammar_src, grammar_pos, input_pos):
        if grammar_src in ["singleQuotedString", "doubleQuotedString"]:
            value_locations.append(input_pos)

    cells = makeGrammar(cell_grammar, {}, tracefunc=traceit)
    try:
        lookup_field_args = cells(text).cellFormula()
        lookup_field_args_and_pos = zip(lookup_field_args, value_locations)
        print("Found the following lookup field args at positions:")
        for arg, pos in lookup_field_args_and_pos:
            print("\t- {} {}".format(arg, pos))
    except ParseError:
        print("No LOOKUPFIELD found in input")
