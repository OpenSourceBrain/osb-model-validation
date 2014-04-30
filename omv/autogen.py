from os.path import isdir

def autogen():
    dirs_to_engines_exts = {'NEURON': {'engine':'NEURON', 'extension':'.hoc'},
                            'NeuroML2':{'engine':'LEMS', 'extension':'.nml'}}

    for d, eng_ext in dirs_to_engines_exts.iteritems():
        if isdir(d):
            print d, 'found'
                            


if __name__ == '__main__':
    autogen()
















