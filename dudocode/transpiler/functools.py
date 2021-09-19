"""
“Commons Clause” License Condition v1.0

The Software is provided to you by the Licensor under the License, as defined below, subject to the following condition.

Without limiting other conditions in the License, the grant of rights under the License will not include, and the License does not grant to you, the right to Sell the Software.

For purposes of the foregoing, “Sell” means practicing any or all of the rights granted to you under the License to provide to third parties, for a fee or other consideration (including without limitation fees for hosting or consulting/ support services related to the Software), a product or service whose value derives, entirely or substantially, from the functionality of the Software. Any license notice or attribution required by the License must also include this Commons Clause License Condition notice.

Software: Dudocode

License: GNU General Public License Version 3

Licensor: SONG YIDING

Dudocode is a pseudocode-to-Python transpiler based on the format specified in CIE IGCSE (Syllabus 0478).
Copyright (C) 2021  SONG YIDING

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from trilobyte import tr
from trilobyte.keypoints import *
from trilobyte.keypoints.converters import *

lower = lambda x : x.lower()
del_last2 = lambda x : x[:-2]
strip = lambda x : x.strip()


def replace_string(s, str_tok_pre='¬STR', str_tok_suf='¬'):
    ret = ''
    count = 0
    dictionary = {}
    tok = None

    in_string = False
    in_char = False

    for i in range(len(s)):
        if s[i] == '"' and s[i - 1] != '\\' and not in_char:
            in_string = not in_string
            if in_string:
                tok = str_tok_pre + str(count) + str_tok_suf
                ret += tok
                dictionary[tok] = '"'
                count += 1
            else:
                dictionary[tok] += '"'

        elif s[i] == "'" and s[i - 1] != '\\' and not in_string:
            in_char = not in_char
            if in_char:
                tok = str_tok_pre + str(count) + str_tok_suf
                ret += tok
                dictionary[tok] = "'"
                count += 1
            else:
                dictionary[tok] += "'"

        elif not in_char and not in_string:
            ret += s[i]

        else:
            dictionary[tok] += s[i]

    return ret, dictionary


def replace_comment(s, com_tok_pre='~COM', com_tok_suf='~'):
    ret = ''
    count = 0
    dictionary = {}
    tok = None

    in_single = False
    in_multi = False

    for i in range(len(s)):
        if (s[i] == '/' and s[i - 1] == '/') and (not in_single and not in_multi):
            in_single = True
            tok = com_tok_pre + str(count) + com_tok_suf
            ret = ret[:-1] + tok
            dictionary[tok] = '//'
            count += 1

        elif (s[i] == '\n' and s[i - 1] != '\\') and in_single:
            in_single = False
            ret += '\n'

        elif (s[i] == '*' and s[i - 1] == '/') and (not in_single and not in_multi):
            in_multi = True
            tok = com_tok_pre + str(count) + com_tok_suf
            ret = ret[:-1] + tok
            dictionary[tok] = '/*'
            count += 1

        elif (s[i] == '/' and s[i - 1] == '*') and in_multi:
            in_multi = False
            dictionary[tok] += '/'

        elif not in_single and not in_multi:
            ret += s[i]

        else:
            dictionary[tok] += s[i]

    return ret, dictionary


def swap(s, swapDict, **kwargs):
    ret = s
    for d in swapDict:
        for o in swapDict[d]:
            ret = rep(ret, o, d, **kwargs)

    return ret


def border_valid(string, idx):
    if idx < 0 or idx >= len(string):
        return True
    else:
        return not string[idx].isalnum()


def rep(string, orig, targ, syntax_front=False, syntax_back=False):
    i = 0
    l = len(orig)
    ret = ''

    while i < len(string):
        if (string[i:i+l] == orig and
                (not syntax_front or (border_valid(string, i-1))) and
                (not syntax_back or (border_valid(string, i+l)))):
            ret += targ
            i += l
        else:
            ret += string[i]
            i += 1

    return ret


def deindent(string):
    string = string.replace()


def format_ranges(ranges_s):
    slices = ranges_s.strip().split(',')
    ret = '['
    for e, i in enumerate(slices):
        start, end = i.split(":")
        start, end = start.strip(), end.strip()
        ret += 'slice({}, {})'.format(start, end)
        if e < len(slices) - 1:
            ret += ', '
    return ret + ']'


def reformat_arr_declarations(text):
    var_dict = {}
    text = tr([
        OptionalRepeatedAfter(Text("DECLARE "), Mono()),
        OptionalRepeatedAfter(Variable(var_name="identifier", var_dict=var_dict), Mono()),
        OptionalRepeatedAfter(Text(":"), Mono()),
        OptionalRepeatedAfter(Text("ARRAY"), Mono()),
        Text("["),
        RepeatPat(NegPat(Text("]")), var_name="params", var_dict=var_dict),
        OptionalRepeatedAfter(Text("]"), Mono()),
        OptionalRepeatedAfter(Text("OF"), Mono()),
        RepeatPat(NegPat(Flush()), var_name="type", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        VariableConverter("identifier"), TextConverter(" = _Array(slices="),
        VariableConverter("params", format_ranges), TextConverter(", type="),
        VariableConverter("type", strip), TextConverter(")")
    ], allow_nested=False)
    return text


def add_brackets(string):
    return '({})'.format(string)


def reformat_outputs(text):
    var_dict = {}
    text = tr([
        Text("OUTPUT "), RepeatPat(NegPat(Flush()), var_name="args", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        TextConverter("OUTPUT"), VariableConverter("args", add_brackets)
    ], allow_nested=False)
    return text


def reformat_inputs(text):
    var_dict = {}

    text = tr([
        Text("INPUT "), RepeatPat(NegPat(Flush()), var_name="identifier", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        VariableConverter("identifier", strip), TextConverter(" = _AnyType(input())")
    ], allow_nested=False)
    return text


def get_indent_level(string, start_idx):
    ret = ''
    for i in range(start_idx, -1, -1):
        if string[i] in ('\n', '\r'):
            break
        ret += string[i]
    return ret


def cross_line(string, start_idx):
    crossed = False
    for i in range(start_idx, len(string)):
        if string[i] in ('\n', '\r'):
            crossed = True
            continue
        if crossed:
            break
    return i


def handle_case_statement(text, var_name, start_idx):
    KEYWORD = "ENDCASE"
    KEYLEN = len(KEYWORD)

    indentation = get_indent_level(text, start_idx-1)
    indent_len = len(indentation)
    end_idx = cross_line(text, start_idx)

    end_found = False

    while end_idx != len(text) - 1:
        assert text[end_idx:end_idx+indent_len] == indentation, "Unmatched indentation level"
        if text[end_idx+indent_len:end_idx+indent_len+KEYLEN] == KEYWORD:
            end_found = True
            break
        end_idx = cross_line(text, end_idx)

    if not end_found:
        raise SyntaxError("Cannot find end of CASE statement beginning at index {}".format(start_idx))

    KEYWORD = "OTHERWISE"
    KEYLEN = len(KEYWORD)

    excerpt = text[start_idx:end_idx]
    mod = ""
    init = True
    cursor = cross_line(excerpt, 0)

    while cursor != len(excerpt) - 1:
        if excerpt[cursor+indent_len+2:cursor+indent_len+2+KEYLEN] == KEYWORD:
            next_cursor = cross_line(excerpt, cursor)
            mod += indentation + 'else: ' + excerpt[cursor+indent_len+2+KEYLEN+1:next_cursor]
        elif excerpt[cursor+indent_len+2] not in (' ', '\t', '\n', '\r', '~'):
            next_cursor = cross_line(excerpt, cursor)
            if init:
                mod += indentation + 'if {} == '.format(var_name)
            else:
                mod += indentation + 'elif {} == '.format(var_name)
            mod += excerpt[cursor+indent_len+2:next_cursor]
            init = False
        else:
            next_cursor = cross_line(excerpt, cursor)
            mod += excerpt[cursor:next_cursor]
        cursor = next_cursor

    return text[:start_idx-indent_len] + mod + '\n' + text[end_idx:]

def reformat_case(text):
    var_dict = {}
    exp = tr([
        OptionalRepeatedAfter(Text("CASE"), Mono()),
        OptionalRepeatedAfter(Text("OF "), Mono()),
        Variable(var_name="identifier", var_dict=var_dict)
    ], var_dict=var_dict)
    res = exp.find_first(text)

    while res:
        matched, start_idx, _, vdict = res
        text = handle_case_statement(text, vdict['identifier'], start_idx)
        res = exp.find_first(text)

    return text


def format_for_range(string):
    string = string.strip()
    start, end = string.split(" TO ")
    start, end = start.strip(), end.strip()
    if ' STEP ' in string:
        end, step = end.split(" STEP ")
        end, step = end.strip(), step.strip()
        return "range({}, {}+1, {})".format(start, end, step)
    return "range({}, {}+1)".format(start, end)


def reformat_for_loop(text):
    var_dict = {}
    text = tr([
        OptionalRepeatedAfter(Text("FOR"), Mono()),
        OptionalRepeatedAfter(Variable(var_name="identifier", var_dict=var_dict), Mono()),
        Text("="), RepeatPat(NegPat(Flush()), var_name="range_def", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        TextConverter("for "), VariableConverter("identifier", strip), TextConverter(" in "),
        VariableConverter("range_def", format_for_range), TextConverter(":")
    ], allow_nested=True)

    var_dict = {}
    text = tr([
        Text("NEXT "), RepeatPat(NegPat(Flush())), Flush()
    ], var_name="overall", var_dict=var_dict).replace_all(text, [
        TextConverter("\n")
    ])

    return text


def reformat_comments(text):
    var_dict = {}
    text = tr([Text("//"), RepeatPat(NegPat(Flush()), var_name="comment", var_dict=var_dict)
    ]).replace_all(text, [TextConverter("#"), VariableConverter("comment", lower)], allow_nested=False)
    return text


def reformat_repeat_loop(text):
    var_dict = {}
    text = tr([
        Text("UNTIL"),
        SequencePat([
            NegPat(AlphaNum()),
            RepeatPat(NegPat(Flush()))], var_name="condition", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        TextConverter("    if "), VariableConverter("condition", strip),
        TextConverter(": break")
    ], allow_nested=False)
    return text


def rep_do_and_strip(string):
    return rep(string, "DO", ":", syntax_front=True, syntax_back=True).strip()


def reformat_while_loop(text):
    var_dict = {}
    text = tr([
        Text("WHILE"),
        SequencePat([
            NegPat(AlphaNum()),
            RepeatPat(NegPat(Flush()))], var_name="condition", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        TextConverter("while "), VariableConverter("condition", rep_do_and_strip)
    ], allow_nested=True)
    return text


def handle_proc_constructor(string):
    string = string.strip()
    if '(' not in string:
        return string + '():'
    return string + ':'


def handle_proc_call(string):
    if string[-1] == '(':
        return string
    return string[:-1].strip() + "() " + string[-1]


def reformat_procedures(text):
    var_dict = {}
    text = tr([
        OptionalRepeatedAfter(Text("PROCEDURE "), Mono()),
        RepeatPat(NegPat(Flush()), var_name="constructor", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        TextConverter("def "), VariableConverter("constructor", handle_proc_constructor)
    ], allow_nested=True)

    var_dict = {}
    text = tr([
        OptionalRepeatedAfter(Text("CALL "), Mono()),
        SequencePat([
            OptionalRepeatedAfter(Variable(), Mono()), NegPat(Mono())
        ], var_name="proc_call", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        VariableConverter("proc_call", handle_proc_call)
    ], allow_nested=False)

    return text


def handle_func_constructor(string):
    string = string.strip()
    if '(' not in string:
        return string + '():'
    return string + ':'


def handle_func_call(string):
    string = string.strip()
    if '(' not in string:
        return string + '()'
    return string


def reformat_functions(text):
    var_dict = {}
    text = tr([
        OptionalRepeatedAfter(Text("FUNCTION "), Mono()),
        OptionalRepeatedAfter(Variable(var_name="func_name", var_dict=var_dict), Mono()),
        Text("->"), RepeatPat(NegPat(Flush()), var_name="remaining", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        TextConverter("def "), VariableConverter("func_name", strip),
        TextConverter("() -> "), VariableConverter("remaining", strip), TextConverter(":")
    ], allow_nested=False)

    var_dict = {}
    text = tr([
        OptionalRepeatedAfter(Text("FUNCTION "), Mono()),
        RepeatPat(NegPat(Flush()), var_name="remaining", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        TextConverter("def "),
        VariableConverter("remaining", strip), TextConverter(":")
    ], allow_nested=False)

    return text


#def reformat_boilerplate(text):
#    var_dict = {}
#
#    print(tr([
#
#    ], var_dict=var_dict).find_first(text))
#
#    '''
#    text = tr([
#
#    ], var_dict=var_dict).replace_all(text, [
#
#    ], allow_nested=False)'''
#    return text


def reformat_if_else(text):
    var_dict = {}
    text = tr([
        OptionalRepeatedBefore(Text("IF"), Space(), var_name="if-with-indent", var_dict=var_dict),
        SequencePat([RepeatPat(NegPat(Flush()), var_name="conditions", var_dict=var_dict), Flush()]),
        SequencePat([RepeatPat(NegPat(Flush())), Flush()]),
    ], var_dict=var_dict).replace_all(text, [
        VariableConverter("if-with-indent", lower), VariableConverter("conditions"), TextConverter(":\n")
    ])

    var_dict = {}
    text = tr([
        OptionalRepeatedBefore(Text("ELSE"), Space(), repeat_var_name="indent", var_dict=var_dict)
    ], var_dict=var_dict).replace_all(text, [
        VariableConverter("indent", del_last2), TextConverter("else:")
    ])

    return text


def check_line_by_line_closure(start_keyword, end_keyword, source):
    source = source.replace("\r", '')
    start_keylen = len(start_keyword)
    end_keylen = len(end_keyword)

    if source[:start_keylen] == start_keyword and border_valid(source, start_keylen):
        for line in source.split('\n')[1:]:
            if len(line) > 0 and line[0] not in (' ', '\t'):
                return True
        return False
    else:
        return True
