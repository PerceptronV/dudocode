# Dudocode
This repository contains the source code for Dudocode, a pseudocode-to-Python transpiler based on the format specified in CIE IGCSE (Syllabus 0478). It allows you to run pseudocode source files, as well as executing pseudocode interactively in the console.

The pseudocode syntax is specified in [this PDF](./pseudocode_specification.pdf) (downloaded from the [official CIE IGCSE website](https://www.cambridgeinternational.org/programmes-and-qualifications/cambridge-igcse-computer-science-0478/)). **Dudocode supports all of these documented features**, except for filestream operations.

Note that the arrow assignment operator (`←`) can be replaced with `<-` for easier typing.

**Contents**:
* [Dudocode](#dudocode)
    * [Getting started](#getting-started)
    * [Demos](#demos)
    * [Documentation](#documentation)
    * [Pseudocode Quick Reference](#quick-reference)

## Getting started

1. Dudocode is built on top of Python. If you do not have Python, please download and install it [here](https://www.python.org/downloads/).

2. Add your Python installation to PATH.

3. To download and install the latest version of Dudocode, run
    ```shell
    pip install dudocode
    ```
    
4. Interact with the `dudo` CLI in terminal. See [documentation](#documentation) for help, or try out the examples in [demos](#demos).

### Notepad++ Integration

We have created a User Defined Language file to aid you in coding with pseudocode. Download [`notepadpp_udl_dudocode.xml`](./notepadpp_udl_dudocode.xml), and import it into Notepad via `Language -> Define your language... -> Import`. This language file supports syntax highlighting, code folding, and auto-completion for all of Dudocode's features. It's recognised file endings are `.ddo` and `.notcode`.

## Demos

Try running the following pseudocode programs if you're not sure how to get started!

In all the examples below, any output line that starts with an `>` denotes where user input is required.

### Hello World
Pseudocode:
```c++
OUTPUT "Hello World!"
```

Output:
```shell
Hello World!
```

### Triangular Stars
Pseudocode:
```c++
INPUT NumRows
FOR i ← 0 TO NumRows
    FOR j ← 0 TO i
        OUTPUT '*'
    NEXT j
    OUTPUT '\n'
NEXT i
```
Output:
```shell
> 10
*
**
***
****
*****
******
*******
********
*********
**********
***********
```

### Arithmetic
Pseudocode:
```c++
OUTPUT "Enter a number: "
INPUT NumA

OUTPUT "Enter another number: "
INPUT NumB

NumA <- REAL(NumA)
NumB <- REAL(NumB)

OUTPUT "Enter operator: "
INPUT Operator

// Awesome CASE statements are supported by Dudocode!
CASE OF Operator
  "add": OUTPUT NumA + NumB
  "sub": OUTPUT NumA - NumB
  "mul": OUTPUT NumA * NumB
  "div": OUTPUT NumA / NumB
  "mod": OUTPUT MOD(NumA, NumB)
  OTHERWISE OUTPUT "Unknown operator"
ENDCASE
```

Output:
```shell
> Enter a number: 14
> Enter another number: 7
> Enter operator: mod
0.0
```

### Sieve of Eratosthenes
Pseudocode:
```c++
INPUT Limit

DECLARE IsPrime : ARRAY[2:Limit] OF BOOLEAN

// Initialise array
FOR Number ← 2 TO Limit
    IsPrime[Number] ← TRUE
NEXT Number

FOR Number ← 2 TO Limit
    IF IsPrime[Number] = TRUE
      THEN
        // Print Number if it is prime
        OUTPUT Number, " "
        
        // Then mark all its multiples as not prime
        FOR Multiple ← 2 TO DIV(Limit, Number)
            IsPrime[Number * Multiple] ← FALSE
        NEXT Multiple
    ENDIF
NEXT Number
```

Output:
```shell
> 100
2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 
```

### Recursion
Pseudocode:
```c++
FUNCTION Factorial(Num:INTEGER) RETURNS INTEGER
    IF Num = 0 OR Num = 1
      THEN
        RETURN 1
      ELSE
        RETURN Num * Factorial(Num - 1)
    ENDIF
ENDFUNCTION

INPUT Number

OUTPUT Factorial(Number), "\n"
```

Output:
```shell
> 20
2432902008176640000
```

<!--
### Boilerplate
Pseudocode:
```c++

```

Output:
```shell

```
-->

----------

## Documentation

### `dudo`
Dudo is Dudocode's versatile CLI, allowing you to convert and run pseudocode source files. It also supports interactive pseudocode execution.

The following commands may be run on the command line:
```
usage: dudo [-h] [-v] {run} ...

Dudocode is a Pseudocode interpreter that transpiles pseudocode to Python.

positional arguments:
  {run}          Dudocode subcommands (use `dudo` without any commands to launch interactive console)
    run          Run pseudocode source files with Dudocode

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

To launch the interactive console, simply run `dudo`.

### `dudo run`
The `dudo run` subcommand deals with transpiling and running pseudocode source files:
```
usage: dudo run [-h] [-d] [-p] [-s] [-o OUT] [-q] [-v] path

positional arguments:
  path               path to Dudocode source code

optional arguments:
  -h, --help         show this help message and exit
  -d, --dudo         print the source Dudocode
  -p, --py           print the transpiled Python program
  -s, --save         save the transpiled Python program
  -o OUT, --out OUT  path to saved Python program when flag `--save` is passed (if not specified, this defaults to that of the input file, but with `.py` as file extension)
  -q, --quiet        does not run the transpiled Python program
  -v, --verbose      print stupid comments while transpiling
```

## Quick Reference

This section contains snippets of common pseudocode patterns, taken from the CIE IGCSE specification.

### Data types
* `INTEGER`
* `REAL`
* `CHAR`
* `STRING`
* `BOOLEAN`

### Array Declaration
1D
```c++
DECLARE <identifier> : ARRAY[<l1>:<u1>, <l2>:<u2>] OF <data type>
```

2D
```c++
DECLARE <identifier> : ARRAY[<l1>:<u1>, <l2>:<u2>] OF <data type>
```

*n*D
```c++
DECLARE <identifier> : ARRAY[<l1>:<u1>, <l2>:<u2>, ..., <ln>:<un>] OF <data type>
```

### Control Flow

_Note the use of 2 spaces instead of 4 in some of these indentations._

Simple IF statement
```c++
IF <condition>
  THEN
    <statements>
ENDIF
```

IF-ELSE statement
```c++
IF <condition>
  THEN
    <statements>
  ELSE
    <statements>
ENDIF
```

CASE statement (without default)
```c++
CASE OF <identifier>
    <value 1> : <statement>
    <value 2> : <statement>
    ...
ENDCASE
```

CASE statement (with default)
```c++
CASE OF <identifier>
  <value 1> : <statement>
  <value 2> : <statement>
  ...
  OTHERWISE <statement>
ENDCASE
```

### Loops
FOR loop
```c++
FOR <identifier> ← <value1> TO <value2> STEP <increment>
    <statements>
NEXT <identifier>
```

REPEAT-UNTIL loop
```c++
REPEAT
<Statements>
UNTIL <condition>
```

WHILE loop
```c++
WHILE <condition> DO
    <statements>
ENDWHILE
```

### Procedure Declaration
Without arguments
```c++
PROCEDURE <identifier>
    <statements>
ENDPROCEDURE
```

With arguments
```c++
PROCEDURE <identifier>(<param1>:<datatype>, <param2>:<datatype>...)
    <statements>
ENDPROCEDURE
```

### Function Declaration
```c++
FUNCTION <identifier>(<param1>:<datatype>, <param2>:<datatype>...) RETURNS <data type>
    <statements>
ENDFUNCTION
```
