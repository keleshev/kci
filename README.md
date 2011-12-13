
kci - Kinda C Interpreter
================================================================================

`kci` is a wrapper for C compiler on your Unix system, which behaves like an
interpreter.


Run as it is:
--------------------------------------------------------------------------------

    $ python kci.py


Or install:
--------------------------------------------------------------------------------

    $ sudo cp kci.py /usr/bin/kci


Example:
--------------------------------------------------------------------------------

    kci 1> #define five 5

    kci 2> int high_five(void) {
    ... 2>     printf("hi, %i!", five);
    ... 2> }

    kci 3> high_five()
    /tmp/kci.c:25: error: expected ‘;’ before ‘}’ token
    kci 4> //oops

    kci 5> high_five();
    hi, 5!









