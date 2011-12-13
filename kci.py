#! /usr/bin/env python

import subprocess as sp

template = '''

#include <stdio.h>

/*** kci preprocessor area ***/
/*** end of kci preprocessor area ***/

/*** kci function definition area ***/
/*** end of kci function definition area ***/

int main() {
    /*** kci main area ***/
    /*** end of kci main area ***/
}

'''


def rollback(i):
    kci_c = ''.join(open('/tmp/kci.c').readlines())
    with open('/tmp/kci.c', 'w') as f:
        kci_c = kci_c.replace('/* kci input %i */' % i,
                              '/* kci input %i is commented out due to errors:' % i)
        f.write(kci_c)


def execute(cc, i, out_old):
    try:
        sp.check_output(cc + ' /tmp/kci.c -o /tmp/kci.out', stderr=sp.STDOUT, shell=True)
        out = sp.check_output('/tmp/kci.out', shell=True)
        print out.replace(out_old, '', 1)
        return out
    except sp.CalledProcessError as e:
        for line in e.output.split('\n'):
            if ': error: ' in line:
                print line
        rollback(i)
        return out_old


def is_prepr(inp):
    if inp.strip().startswith('#'):
        return True


def process_prepr(inp, kci_c, i):
    inp = '/* kci input %i */\n%s\n/* end of kci input %i */' % (i, inp, i)
    kci_c = kci_c.replace('/*** end of kci preprocessor area ***/', 
                          inp + '\n/*** end of kci preprocessor area ***/')
    return kci_c


def is_func(inp):
    pass


def process_func(inp, kci_c, i):
    inp = '/* kci input %i */\n%s\n/* end of kci input %i */' % (i, inp, i)
    kci_c = kci_c.replace('/*** end of kci function definition area ***/', 
                          inp + '\n    /*** end of kci function definition area ***/')
    return kci_c


def process_main(inp, kci_c, i):
    inp = '/* kci input %i */\n    %s\n    /* end of kci input %i */' % (i, inp, i)
    kci_c = kci_c.replace('/*** end of kci main area ***/', 
                          inp + '\n    /*** end of kci main area ***/')
    return kci_c


def process_input(inp, kci_c, i):
    if is_prepr(inp):
        kci_c = process_prepr(inp, kci_c, i)
    elif is_func(inp):
        kci_c = process_func(inp, kci_c, i)
    else:
        kci_c = process_main(inp, kci_c, i)
    return kci_c


def has_unbalanced_paren(inp):
    # TODO strip comments, strip string literals
    return inp.count('{') != inp.count('}') or inp.count('(') != inp.count(')')


def main():
    cc = 'c99'
    with open('/tmp/kci.c', 'w') as f:
        f.write(template)

    i = 1  # prompt iteration
    inp = ''
    out = ''
    prompt = 'kci %i> ' % i
    while True:
        inp += raw_input("\033[1;33m" + prompt + "\033[0m")  # colors

        if inp.endswith('\\') or has_unbalanced_paren(inp):
            prompt = '... %i> ' % i
            inp += '\n'  # inp will accumulate
            continue

        kci_c = ''.join(open('/tmp/kci.c').readlines())
        with open('/tmp/kci.c', 'w') as f:
            f.write(process_input(inp, kci_c, i))
        inp = ''
        out = execute(cc, i, out)
        i += 1
        prompt = 'kci %i> ' % i


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass














