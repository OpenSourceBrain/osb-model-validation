from os.path import isdir, join
from glob import glob


def read_option(options, default=0):
    print [(i, opt) for i, opt in enumerate(options)]
    sel = None
    while not sel:
        try:
            sel = int(raw_input('option [%s]' % default))
            if sel is '':
                sel = 0
        except IndexError:
            print 'invalid index!'
    return options[sel]

def autogen():
    dirs_to_engines_exts = {'NEURON': {'engine':'NEURON', 'extension':'.hoc'},
                            'NeuroML2':{'engine':'LEMS', 'extension':'.nml'}}

    for d, eng_ext in dirs_to_engines_exts.iteritems():
        if isdir(d):
            engine = dirs_to_engines_exts[d]['engine']
            ext = dirs_to_engines_exts[d]['extension']
            print 'Default directory for {0} engine found.'.format(engine)
            print '  Will look for scripts with {0} extension'.format(ext)
            scripts = glob(join(d,'*'+ext))
            print '    found', scripts
            script = read_option(scripts)
            print 'selected', script 


if __name__ == '__main__':
    autogen()
















