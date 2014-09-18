import re
import os
import subprocess as sp
from tempfile import NamedTemporaryFile

from backend import OMVBackend
from utils.wdir import working_dir
from ..common.inout import inform


class GenesisBackend(OMVBackend):

    name = "genesis"

    @classmethod
    def is_installed(cls, version):
        from tempfile import NamedTemporaryFile
        inform("Checking whether %s is installed..." % cls.name, indent=1)

        ret = True
        try:
            temp = NamedTemporaryFile(suffix='.g')
            temp.writelines(['echo "version: "{version} \n', 'quit \n'])
            temp.seek(0)
            out = sp.check_output(
                ['nxgenesis', '-nox', '-batch', '-notty', temp.name])
            m = re.search('version:' + '\s*([0-9]*\.?[0-9]+)\s*', out)
            if m:
                ret = m.groups()[0]
        except OSError:
            ret = False
        finally:
            temp.close()

        return ret

    @classmethod
    def install(cls, backend_version):
        import getgenesis
        home = os.environ['HOME']
        cls.path = os.path.join(home, 'genesis', 'genesis-2.3', 'src')
        inform('Will fetch and install genesis-2.3', indent=1)
        getgenesis.install_genesis()

    def run(self):
        from pkg_resources import resource_filename
        with working_dir(os.path.dirname(self.modelpath)):
            try:
                temp = NamedTemporaryFile(suffix='.g')
                temp.write('include %s\n' % self.modelpath)
                temp.write('include %s\n' %
                           resource_filename('omv', 'backends/utils/genesis_utils.g'))
                temp.write('\n'.join(self.extra_pars) + '\n')
                temp.seek(0)

                with open('/tmp/omv.gen.err', 'w+') as se:
                    self.stdout = sp.check_output(['nxgenesis', '-nox',
                                                   '-batch', '-notty', temp.name],
                                                  stderr=se)
                    se.seek(0)
                    self.stderr = se.readlines()
                self.returncode = 0
            except sp.CalledProcessError as e:
                self.returncode = e.returncode
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
