## The Pesapal Junior Programmer Challenge '24
### The problems
#### 0: source control system

Build a distributed source control system in the style of Git. It should be possible to initialise a repository in a directory and the repository proper should be stored in a dot-prefixed subdirectory. There should be support for staging files (git add) and committing them. There should be a way to view the commit history, to create branches, merge and do diffs between them. Conflicting changes should be detected but there's no need to build resolution features for them, or anything like rebasing. It should also be possible to clone the repository (on disk—it doesn't have to work over network). Finally, there should be a way to ignore files.

#### 1: image hash spoofing

Build a tool that takes an image and an arbitrary hexstring and outputs an adjusted file that displays identically to the human eye (when opened in image viewers) but has a hash that begins with the given hexstring.

It should work in such a way that we can run, e.g.
```bash
spoof 0x24 original.jpg altered.jpg
```
and get a file altered.jpg such that running the sum on a Linux machine produces output like this:
```bash
sha512sum altered.jpg
2448a6512f[...more bytes...]93de43f4b5b  altered.jpg
```
You can use a different image format (PNG, TIFF, etc.) if you find it better suited to the problem. Also, you can change the hash algorithm to another SHA-based one if you deem it more appropriate. (Obviously, the name spoof is only used as an example; you can name your program as you wish.)

#### 2: arbitrary precision integer calculator

Write an arbitrary-precision-integer calculator in a language that doesn't have native support and without relying on any libraries for the core functionality. Wrap it in a REPL. It should support at least addition, subtraction, multiplication, division (and modulo), exponentiation and factorial. Bonus points for supporting non-decimal bases, fractions, logarithms, etc.

#### 3: terminal screen

Imagine a stream of bytes supplied to a program to render them in a screen inside a terminal. Below is the definition of the binary format used for communication between a computer and the screen:

```
+--------------+-------------+-------------+-------------+--- ··· ---+----------------+
| Command Byte | Length Byte | Data Byte 0 | Data Byte 1 |    ···    |  Data Byte n-1 |
+--------------+-------------+-------------+-------------+--- ··· ---+----------------+
```

The data format is an array of bytes, containing sections of above form, in succession. Each section begins with a command byte, specifying the type of operation to be performed on the screen, followed by a length byte, and then a sequence of data bytes, which function as arguments to the command, as specified below:
```
0x1 - Screen setup: Defines the dimensions and colour setting of the screen. The screen must be set up before any other command is sent. Commands are ignored if the screen hasn't been set up.

Data format:

Byte 0: Screen Width (in characters)
Byte 1: Screen Height (in characters)
Byte 2: Color Mode (0x00 for monochrome, 0x01 for 16 colors, 0x02 for 256 colors)

0x2 - Draw character: Places a character at a given coordinate of the screen.

Data format:

Byte 0: x coordinate
Byte 1: y coordinate
Byte 2: Color index
Byte 3: Character to display (ASCII)

0x3 - Draw line: Draws a line from one coordinate of the screen to another.

Data format:

Byte 0: x1 (starting coordinate)
Byte 1: y1 (starting coordinate)
Byte 2: x2 (ending coordinate) Byte 4: y2 (ending coordinate)
Byte 4: Color index
Byte 5: Character to use (ASCII)

0x4 - Render text: Renders a string starting from a specific position.

Data format:

Byte 0: x coordinate
Byte 1: y coordinate
Byte 2: Color index
Byte 3-n: Text data (ASCII characters)

0x5 - Cursor movement: Moves cursor to a specific location without drawing on the screen.

Data format:

Byte 0: x coordinate
Byte 1: y coordinate

0x6 - Draw at cursor: Draws a character at the cursor location.

Data format:

Byte 0: Character to draw (ASCII)
Byte 1: Color index

0x7 - Clear screen:

Data format: No additional data.

0xFF - End of file: Marks the end of binary stream.

Data format: No additional data.
```
The program should draw the screen from within a terminal window, but the question of whether to do so inside the terminal from which it is launched or to launch a separate terminal window is left to the implementer.

#### 4: you tell us

If the above problems are too easy or boring or they don't match your tastes, email us with the subject "Suggested Problem" and your suggestion before 23:59:59 UTC+03:00 on 4th December 2024 and we will consider adding it to the list.