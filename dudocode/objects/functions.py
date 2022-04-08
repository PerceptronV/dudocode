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


import random

def _join_str(*args):
    ret = ''
    for i in args:
        ret += str(i)
    return ret

def DIV(a, b):
    return int(a // b)

def MOD(a, b):
    return a % b

def LENGTH(string):
    return len(string)

def LCASE(string):
    return string.lower()

def UCASE(string):
    return string.upper()

def SUBSTRING(string, start, length):
    return string[start-1:start-1+length]

def ROUND(num, places):
    if places == 0:
        return int(num)
    return round(num, places)

def RANDOM():
    return random.random()

def OUTPUT(*args):
    print(_join_str(*args), end='')
