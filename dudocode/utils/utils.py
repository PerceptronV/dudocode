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


import os, random

WHITESPACES = [' ', '\r', '\t', '\n']


def swap(s, swapDict, syntax=False):
    ret = s
    for d in swapDict:
        for o in swapDict[d]:
            if syntax:
                ret = rep(ret, o, d, syntax=True)
            else:
                ret = rep(ret, o, d)

    return ret


def border_valid(str, idx):
    if idx < 0 or idx >= len(str):
        return True
    else:
        return not str[idx].isalnum()


def rep(str, orig, targ, syntax=False):
    i = 0
    l = len(orig)
    ret = ''

    while i < len(str):
        if str[i:i+l] == orig and (not syntax or (border_valid(str, i-1) and border_valid(str, i+l))):
            ret += targ
            i += l
        else:
            ret += str[i]
            i += 1

    return ret


def general_split(str, splits = ('\n', '\r')):
    t = str.split(splits[0])
    if len(splits) > 1:
        ret = t
        t = []
        for i in ret:
            t.extend(general_split(i, splits[1:]))

    ret = t

    while '' in ret:
        ret.remove('')

    return ret.copy()


def count_front_pad(str):
    ret = 0
    for i in str:
        if i in WHITESPACES:
            ret += 1
        else:
            break

    return ret


def format_ifs(str):
    lines = general_split(str)
    indentLevs = [0]

    for i in range(len(lines)):
        line = lines[i]
        frpd = count_front_pad(line)

        if line[frpd:frpd+2] == 'if' and border_valid(line, frpd-1) and border_valid(line, frpd+2):
            line += ':'
            indentLevs.append(frpd)

            j = i + 1
            while j < len(lines):
                if lines[j][frpd:frpd + 5] != 'ENDIF':
                    lines[j] = lines[j][2:]
                    j += 1
                else:
                    break

        elif line[frpd:frpd+4] == 'else' and border_valid(line, frpd-1) and border_valid(line, frpd+4):
            line += ' '
            line = line[:frpd] + 'else:' + line[frpd + 4:]

            j = i+1
            while lines[j].strip() == '':
                j += 1

            currentIndent = max(indentLevs)
            if lines[j][currentIndent:currentIndent+2] == 'if':
                while j < len(lines):
                    if lines[j][currentIndent:currentIndent + 5] != 'ENDIF':
                        lines[j] = '  ' + lines[j]
                        j += 1
                    else:
                        lines[j] = '  ' + lines[j]
                        break

        elif line[frpd:frpd+5] == 'ENDIF' and border_valid(line, frpd-1) and border_valid(line, frpd+5):
            line = ''
            indentLevs.remove(max(indentLevs))

        lines[i] = line

    return '\n'.join(lines)


def format_outs(str):
    return str


def format_ins(str):
    return str


def format_loops(str):
    return str


def rndstr(l):
    s = ''
    for i in range(l):
        s += chr(random.randint(97, 122))
    return s


def gen_name(dir, ext, l=8):
    s = rndstr(l) + ext
    while os.path.exists(os.path.join(dir, s)):
        s = rndstr(l) + ext
    return s


def working_dir():
    return os.getcwd()


def str_equal(str, segments, idx):
    l = len(segments)
    if idx is None:
        return False
    if l == 1:
        str_len = len(segments[0])
        return str[idx:idx+str_len] == segments[0]
    else:
        str_len = len(segments[0])
        if str[idx:idx+str_len] != segments[0]:
            return False
        return str_equal(str, segments[1:], cross_whitespaces(str, idx+str_len-1))


def count(str, k, syntax=False, exp = False):
    '''
    syntax & exp ARGS CANNOT BOTH BE TRUE!!!
    OTHERWISE PROGRAM WILL BE UNPREDICTABLE
    '''
    if exp:
        segments = k.split('*')
    else:
        segments = k

    r = 0
    l = len(k)

    if str_equal(str, segments, 0):
        if syntax:
            if not str[l].isalnum():
                r += 1
        else:
            r += 1

    for i in range(1, len(str)):
        if str_equal(str, segments, i):
            if syntax:
                if not str[i - 1].isalnum() and not str[i + l].isalnum():
                    r += 1
            else:
                r += 1

    return r


def skip_whitespaces(str, index):
    i = index + 1
    if i == len(str):
        return None
    while str[i] in WHITESPACES:
        i += 1
        if i == len(str):
            return None

    return str[i]


def cross_whitespaces(str, index):
    i = index + 1
    if i == len(str):
        return None
    while str[i] in WHITESPACES:
        i += 1
        if i == len(str):
            return None

    return i


def replace_string(s, str_tok_pre='~STR', str_tok_suf='~'):
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
            dictionary[tok] += '\n'

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
