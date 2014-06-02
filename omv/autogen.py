from os.path import isdir, join, split
from glob import glob
import yaml

#ugly hack to get .travis.yaml closer to manual version
from collections import OrderedDict
class UnsortableList(list):
    def sort(self, *args, **kwargs):
        pass
class UnsortableOrderedDict(OrderedDict):
    def items(self, *args, **kwargs):
        return UnsortableList(OrderedDict.items(self, *args, **kwargs))
yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)

def read_option(options, default=0, silent=False):
    for i, opt in enumerate(options):
        print '\t\t', i, opt
    opt = None
    if silent:
        opt = default
    while opt is None:
        try:
            sel = int(
                raw_input('Select option number [default: %s]: ' % default))
            opt = options[sel]
        except IndexError:
            print 'invalid index!'
        except ValueError:
            print 'selecting default: ', default
            opt = options[default]
    return opt

def find_targets(auto=False):
    #TODO: should belong to backend
    dirs_to_engines_exts = {'NEURON': {'engine': 'NEURON', 'extension': '.hoc'},
                            'NeuroML2': {'engine': 'jNeuroML', 'extension': '.nml'}}
    targets = []
    for d, eng_ext in dirs_to_engines_exts.iteritems():
        if isdir(d):
            engine = dirs_to_engines_exts[d]['engine']
            ext = dirs_to_engines_exts[d]['extension']
            print 'Default directory for {0} engine found.'.format(engine)
            print '  Will look for scripts with {0} extension'.format(ext)
            scripts = glob(join(d, '*' + ext))
            # print '    found', scripts
            if auto:
                print 'selecting default: ', scripts[0]
                script = scripts[0]
            else:
                script = read_option(scripts)
            targets.append((engine, script))
            # print 'selected', script
    return targets


def create_dryrun(engine, target):
    print ' '.join(('Generating dry run test for file', target,
                    ', using engine', engine))
    dirname, fname = split(target)
    omt = {'target': fname, 'engine': engine}
    with open(target + '.dry.omt', 'w') as fh:
        yaml.dump(omt, fh, default_flow_style=False)


def generate_dottravis(targets):
    from backends import be_paths, be_env_vars

    backends = [t[0] for t in targets]
    paths = ':'.join(["$PATH"]+[be_paths[be] for be in backends if
        be in be_paths])

    extra_envs = ' '.join([be_env_vars[be] for be in backends if
        be in be_env_vars])

    pp = 'PYTHONPATH=$PYTHONPATH:$HOME/local/lib/python/site-packages'
    pa = 'PATH=' + paths
    gls = ' '.join([pp, extra_envs, pa])

    engines = ['OST_ENGINE='+be for be in backends]
    #TODO: softcode 
    repo = "git+https://github.com/borismarin/osb-model-validation.git"

    travis = UnsortableOrderedDict([
        ('language', 'python'),
        ('python', 2.7),
        ('env', {'global' : gls, 'matrix': engines}), 
        ('install',  ['pip install ' + repo]),
        ('script',  ['omv all'])
    ])

    with open('.travis.yml', 'w') as fh:
        fh.write(yaml.dump(travis, default_flow_style=False))

def autogen(auto=False, dry=True):
    targets = find_targets(auto)
    for engine, target in targets:
        if dry:
            create_dryrun(engine, target)
    generate_dottravis(targets)


if __name__ == '__main__':
    autogen()
