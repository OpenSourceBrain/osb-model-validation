import os
import subprocess as sp

from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import OMVEngine, EngineExecutionError

from omv.engines.nestsli import NestEngine
import sys


class PyNestEngine(OMVEngine):

    name = "PyNEST"

    @staticmethod
    def is_installed():

        PyNestEngine.environment_vars = NestEngine.get_nest_environment()
        sys.path.append(PyNestEngine.environment_vars["PYTHONPATH"])

        ret = True
        try:
            print('PN1')
            try:
                print('PN1a')
                ret_str_cmd_line = check_output(['python -c "import nest; print(nest.__version__ if hasattr(nest,\'__version__\') else nest.version())"'], shell=True, verbosity=2)

                #if is_verbose():
                #    inform("NEST cmd line test: <<<%s>>>" % (ret_str_cmd_line), indent=2)
                ret_str = ret_str_cmd_line.split('Version: ')[1].split('Built:')[0].strip()
                #print("ret_str: %s"%ret_str)
            except Exception as e:
                print('NEST exc: %s'%e)
                import nest
                print('PN2')
                if hasattr(nest,'__version__'):
                    print('PN3')
                    ret_str = nest.__version__
                else:
                    print('PN4')
                    ret_str = nest.version()

            ret = len(ret_str) > 0

            if ret:
                ret_str = ret_str.strip().split('\n')[-1]
                #print('NEST info: %s; <<%s>>'%(ret, ret_str))
                if 'Version' in ret_str:
                    ret = 'v%s'%ret_str.split('Version')[-1].split()[0]
                elif '-' in ret_str:
                    ret = 'v%s'%ret_str.split('-')[-1].split()[0]
                else:
                    ret = 'v%s'%ret_str.split()[-1]

            if ret and is_verbose():
                inform("%s is correctly installed..." % (PyNestEngine.name), indent=2)

            if is_verbose():
                inform("NEST is installed with Python support...", indent=2)
                inform("Env vars: %s" % PyNestEngine.environment_vars, indent=2)

        except Exception as err:
            if is_verbose():
                inform("Couldn't import (py)NEST into Python..: ", err, indent=1)
                inform("NEST env vars: %s" % PyNestEngine.environment_vars, indent=1)
                inform("sys.path: %s" % sys.path, indent=1)
            ret = False
        return ret


    @staticmethod
    def install(version):
        NestEngine.install(version)
        PyNestEngine.path = NestEngine.path
        PyNestEngine.environment_vars = NestEngine.environment_vars
        inform('Finished installation of PyNEST....', indent=2)


    def run(self):

        self.environment_vars = NestEngine.get_nest_environment()
        self.set_environment()

        sys.path.append(self.environment_vars["PYTHONPATH"])

        inform("Env vars: %s" % self.environment_vars, indent=2)
        inform("sys.path: %s" % sys.path, indent=1)

        try:
            inform("Running the file %s with %s" % (trim_path(self.modelpath), self.name), indent=1)
            self.stdout = check_output(['python', self.modelpath, '-nogui'],
                                          cwd=os.path.dirname(self.modelpath))
            self.returncode = 0
        except sp.CalledProcessError as err:
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
        except Exception as err:
            inform("Another error with running %s: "%self.name, err, indent=1)
            self.returncode = -1
            self.stdout = "???"
