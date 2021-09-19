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


import os
import code
import argparse
from dudocode import Transpiler

VERSION = '0.0.1'
COPYRIGHT_LONG = 'Copyright (c) 2021 SONG YIDING. All Rights Reserved.'
COPYRIGHT_SHORT = 'Copyright (c) 2021 SONG YIDING'

def main():
    parser = argparse.ArgumentParser(
        prog='dudo',
        description='Dudocode is a Pseudocode interpreter that transpiles pseudocode to Python.'
    )
    subparsers = parser.add_subparsers(help='Dudocode subcommands (use `dudo` without any commands to launch interactive console)')
    parser.set_defaults(which='base')
    parser.add_argument('-v', '--version', action='version',
                        version='Dudocode {}. {}'.format(VERSION, COPYRIGHT_LONG))

    run_parser = subparsers.add_parser('run', help='Run pseudocode source files with Dudocode')
    run_parser.set_defaults(which='run')
    run_parser.add_argument('path', type=str, help='path to Dudocode source code', default='')
    run_parser.add_argument('-d', '--dudo', help='print the source Dudocode', action='store_true')
    run_parser.add_argument('-p', '--py', help='print the transpiled Python program', action='store_true')
    run_parser.add_argument('-s', '--save', help='save the transpiled Python program', action='store_true')
    run_parser.add_argument('-o', '--out', type=str, help='path to saved Python program when flag `--save` is passed '
                                                          '(if not specified, this defaults to that of the input '
                                                          'file, but with `.py` as file extension)', default='')
    run_parser.add_argument('-q', '--quiet', help='does not run the transpiled Python program', action='store_true')
    run_parser.add_argument('-v', '--verbose', help='print stupid comments while transpiling', action='store_true')

    args = parser.parse_args()
    trans = Transpiler('transpiler')

    if args.which == 'base':
        interactive_exec(trans)

    elif args.which == 'run':
        try:
            with open(args.path, 'r', encoding='utf-8') as f:
                src = f.read()

            if args.dudo:
                if args.verbose:
                    print('::< Source Dudocode >::')
                print(src + '\n\n')

            if args.verbose:
                print('::< Transpiling source Dudocode... >::')
            pycode = trans.transpile(source=src, initial=True, verbose=args.verbose)
            if args.verbose:
                print('::< Dodocode transpilation complete >::')

            if args.save:
                if args.out == '':
                    fname = '.'.join(args.path.split(".")[:-1] + ["py"])
                else:
                    fname = args.out
                f = open(fname, 'w')
                f.write(pycode)
                f.close()

            if args.py:
                if args.verbose:
                    print('::< Transpiled Python program >::')
                print(pycode + '\n')

            if not args.quiet:
                if args.verbose:
                    print('::< Executing source Dudocode... >::')
                code.InteractiveInterpreter().runcode(pycode)

        except KeyboardInterrupt:
            print("\nUser terminated current Dudocode tasks")


def pushlines(lines, console):
    for i in lines.split("\n"):
        ret = console.push(i)
    return ret


def interactive_exec(trans):
    print("Dudocode {} Interactive Console ::: {}".format(VERSION, COPYRIGHT_SHORT))
    c = code.InteractiveConsole()
    pushlines(trans.transpile(source='', initial=True, verbose=False), c)  # Initial objects importing
    buffer = ""

    try:
        while 1:
            src = input("::> ") + '\n'
            buffer += src

            while not trans.check_completion(buffer):
                src = input("::: ") + '\n'
                buffer += src

            pycode = trans.transpile(source=buffer, initial=False, verbose=False)

            # In case someone decides to type Python
            while pushlines(pycode, c):
                src = input("::: ") + '\n'
                pycode = trans.transpile(source=src, initial=False, verbose=False)

            buffer = ""

    except KeyboardInterrupt:
        print("\nExiting Dudocode interactive console")
