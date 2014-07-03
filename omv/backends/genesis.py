import re
import subprocess as sp

from backend import OMVBackend

class GenesisBackend(OMVBackend):
    
    name = "genesis"

    @staticmethod
    def is_installed(version):
        from tempfile import NamedTemporaryFile
        print("Checking whether %s is installed..." % GenesisBackend.name)

        ret = True
        try:
            temp = NamedTemporaryFile(suffix='.g')
            temp.writelines(['echo "version: "{version} \n', 'quit \n'])
            temp.seek(0)
            out = sp.check_output(['genesis', '-nox', '-batch', '-notty', temp.name])
            m = re.search('version:'+'\s*([0-9]*\.?[0-9]+)\s*', out)
            if m:
                ret = m.groups()[0]

        except OSError:
            ret =  False
        finally:
            temp.close()
        return ret




