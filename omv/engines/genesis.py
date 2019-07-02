import re
import os
import subprocess as sp
from tempfile import NamedTemporaryFile

from omv.engines.engine import OMVEngine, EngineExecutionError
from omv.engines.utils.wdir import working_dir
from omv.common.inout import inform


class GenesisEngine(OMVEngine):

    name = "genesis"

    @classmethod
    def is_installed(cls, version):
        from tempfile import NamedTemporaryFile

        ret = True
        try:
            temp = NamedTemporaryFile(suffix='.g')
            temp.writelines([b'echo "version: "{version} \n', b'quit \n'])
            temp.seek(0)
            out = sp.check_output(
                ['genesis', '-nox', '-batch', '-notty', temp.name])
            m = re.search(b'version:\s*([0-9]*\.?[0-9]+)\s*', out)
            if m:
                ver = m.groups()[0]

                if isinstance(ver, bytes):
                    ver = ver.decode('utf-8')
                ret = 'v%s'%ver
                inform("Found GENESIS in path, version %s" % ret,
                        verbosity=1, indent=2)
        except OSError:
            ret = False
        finally:
            temp.close()

        return ret

    @classmethod
    def install(cls, engine_version):
        from omv.engines.getgenesis import install_genesis
        home = os.environ['HOME']
        cls.path = os.path.join(home, 'genesis',
                                'genesis2.4gamma-master', 'src')
        inform('Will fetch and install genesis-2.4', indent=1)
        install_genesis()

    def run(self):
        from pkg_resources import resource_filename
        with working_dir(os.path.dirname(self.modelpath)):
            try:
                temp = NamedTemporaryFile(suffix='.g')
                temp.write('include %s\n' % self.modelpath)
                temp.write('include %s\n' %
                           resource_filename('omv', 'engines/utils/genesis_utils.g'))
                temp.write('\n'.join(self.extra_pars) + '\n')
                temp.seek(0)

                with open('/tmp/omv.gen.err', 'w+') as se:
                    self.stdout = sp.check_output(['genesis', '-nox',
                                                   '-batch', '-notty', temp.name],
                                                  stderr=se)
                    se.seek(0)
                    self.stderr = se.readlines()
                self.returncode = 0
            except sp.CalledProcessError as e:
                self.returncode = e.returncode
                raise EngineExecutionError
            finally:
                temp.close()

    def build_query_string(self, name, cmd):
        return 'echo %s: {%s}' % (name, cmd)

    def query_area(self, secname):
        name = self.register_query('area_%s' % secname.translate(None, '/[]'),
                                   'total_membrane_area %s' % secname)
        return name

    def query_temperature(self):
        return self.register_query('temperature', 'celsius')
