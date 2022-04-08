"""
“Commons Clause” License Condition v1.0

The Software is provided to you by the Licensor under the License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant of rights under the License will not include, and the License does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or all of the rights granted to you under the License to provide to third parties, for a fee or other consideration (including without limitation fees for hosting or consulting/ support services related to the Software), a product or service whose value derives, entirely or substantially, from the functionality of the Software. Any license notice or attribution required by the License must also include this Commons Clause License Condition notice.

Software: Dudocode

License: GNU General Public License Version 3

Licensor: SONG YIDING

Dudocode is a pseudocode-to-Python transpiler based on the format specified in CIE IGCSE (Syllabus 0478).
Copyright (C) 2022  SONG YIDING

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import colorama
from colorama import Fore, Back, Style
from dudocode.transpiler.functools import replace_string, replace_comment, swap, check_line_by_line_closure
from dudocode.transpiler.functools import reformat_if_else
from dudocode.transpiler.functools import reformat_arr_declarations
from dudocode.transpiler.functools import reformat_outputs
from dudocode.transpiler.functools import reformat_inputs
from dudocode.transpiler.functools import reformat_case
from dudocode.transpiler.functools import reformat_comments
from dudocode.transpiler.functools import reformat_for_loop
from dudocode.transpiler.functools import reformat_repeat_loop
from dudocode.transpiler.functools import reformat_while_loop
from dudocode.transpiler.functools import reformat_procedures
from dudocode.transpiler.functools import reformat_functions
from dudocode.transpiler.functools import reformat_fileIO

# ============================================================
# ============================================================
#                    CONSTANT DECLARATIONS
# ============================================================
# ============================================================
CLOSED_PAIRS = [
    ['IF', 'ENDIF'],
    ['CASE', 'ENDCASE'],
    ['FOR', 'NEXT'],
    ['REPEAT', 'UNTIL'],
    ['WHILE', 'ENDWHILE'],
    ['PROCEDURE', 'ENDPROCEDURE'],
    ['FUNCTION', 'ENDFUNCTION']
]


WORDOP_SWAP = {
    'and': ['AND'],
    'or': ['OR'],
    'not': ['NOT'],
    'while 1:': ['REPEAT'],
    '->': ['RETURNS'],
    'return': ['RETURN']
}

RESERVERVED_SWAP = {
    '_True': ['True'],
    '_False': ['False'],
}

OPERATOR_SWAP = {
    "'": ["ꞌ"],
    "-": ["–"],
    '==': ['='],
    '<=': ['<=='],
    '>=': ['>=='],
    '←': ['<-'],
    '=': ['←'],
    '**': ['^'],
    '!=': ['<>'],
}

MISC_SWAP = {
    '': ['ENDCASE', 'ENDIF', 'ENDWHILE', 'ENDPROCEDURE', 'ENDFUNCTION']
}

MISC_SWAP_BACKPADDED = {
    '': ['DECLARE ', 'CONSTANT '],
}


HEADER = """
# ============================== Dudocode Artifacts ============================== #
from dudocode.objects import *
from dudocode.objects import _AnyType, _ArrayTemplateDummy, _Array, _Filestream
_Fs = _Filestream()
# ================================================================================ #
"""


# ============================================================
# ============================================================
#                      TRANSPILER OBJECT
# ============================================================
# ============================================================


class Transpiler(object):
    def __init__(self, name):
        self.name = name
        self.trans_prog_head = "::: "

    def devprint(self, s):
        print(Fore.YELLOW + s + Style.RESET_ALL)

    def check_completion(self, source):
        completed = [
                        check_line_by_line_closure(start_keyword, end_keyword, source)
                        for (start_keyword, end_keyword) in CLOSED_PAIRS
                    ]
        return False not in completed  # Only returns True if all is True

    def preprocess(self, source):
        source = source.replace("\r", '')
        source = source + "\n"
        return source

    def transpile(self, source, initial=True, verbose=False):
        proc = self.preprocess(source)

        if verbose:
            self.devprint("{}Tokenising stings and comments...".format(self.trans_prog_head))
        proc, str_dict = replace_string(proc)
        proc, com_dict = replace_comment(proc)

        if verbose:
            self.devprint("{}Transpiling operators (1/2)...".format(self.trans_prog_head))
        proc = swap(proc, WORDOP_SWAP, syntax_front=True, syntax_back=True)
        proc = swap(proc, RESERVERVED_SWAP, syntax_front=True, syntax_back=True)
        proc = swap(proc, OPERATOR_SWAP, syntax_front=False, syntax_back=False)

        if verbose:
            self.devprint("{}Transpiling IF-ELSE statements...".format(self.trans_prog_head))
        proc = reformat_if_else(proc)
        if verbose:
            self.devprint("{}Transpiling ARRAY declarations...".format(self.trans_prog_head))
        proc = reformat_arr_declarations(proc)

        if verbose:
            self.devprint("{}Transpiling CASE statements...".format(self.trans_prog_head))
        proc = reformat_case(proc)
        if verbose:
            self.devprint("{}Transpiling FOR loops...".format(self.trans_prog_head))
        proc = reformat_for_loop(proc)
        if verbose:
            self.devprint("{}Transpiling REPEAT-UNTIL loops...".format(self.trans_prog_head))
        proc = reformat_repeat_loop(proc)
        if verbose:
            self.devprint("{}Transpiling WHILE-DO loops...".format(self.trans_prog_head))
        proc = reformat_while_loop(proc)
        if verbose:
            self.devprint("{}Transpiling PROCEDURE definitions...".format(self.trans_prog_head))
        proc = reformat_procedures(proc)
        if verbose:
            self.devprint("{}Transpiling FUNCTION definitions...".format(self.trans_prog_head))
        proc = reformat_functions(proc)

        if verbose:
            self.devprint("{}Transpiling OUTPUT statements...".format(self.trans_prog_head))
        proc = reformat_outputs(proc)
        if verbose:
            self.devprint("{}Transpiling INPUT statements...".format(self.trans_prog_head))
        proc = reformat_inputs(proc)
        if verbose:
            self.devprint("{}Transpiling FILE operations...".format(self.trans_prog_head))
        proc = reformat_fileIO(proc)

        if verbose:
            self.devprint("{}Transpiling operators (2/2)...".format(self.trans_prog_head))
        proc = swap(proc, MISC_SWAP, syntax_front=True, syntax_back=True)
        proc = swap(proc, MISC_SWAP_BACKPADDED, syntax_front=True, syntax_back=False)

        if verbose:
            self.devprint("{}Substituting string and comment tokens...".format(self.trans_prog_head))
        for i in com_dict:
            proc = proc.replace(i, com_dict[i])
        for i in str_dict:
            proc = proc.replace(i, str_dict[i])

        if verbose:
            self.devprint("{}Transpiling comments...".format(self.trans_prog_head))
        proc = reformat_comments(proc)

        if initial:
            proc = HEADER + proc

        return proc.strip('\n')


# ============================================================
# ============================================================
#                        INITIALISATION
# ============================================================
# ============================================================
colorama.init()
