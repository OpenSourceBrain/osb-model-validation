from os.path import splitext, basename
from omv.validation.rx_validator import RXSchemaValidator
from omv.validation.utils import topological_sort, all_types_in_schema
from pkg_resources import resource_filename


class OMVValidator(RXSchemaValidator):

    def __init__(self):
        super(OMVValidator, self).__init__()
        self.add_osb_prefix()
        self.register_osb_types()

    def add_osb_prefix(self):
        self.prefix = 'tag:opensourcebrain.org,2014:schemata/omv/'
        self.rx.add_prefix('omv', self.prefix)

    def register_osb_types(self):

        self.omv_types = {}
        from glob import glob
        typedir = resource_filename('omv', 'schemata/types/')
        for omv in glob(typedir + '*.yaml') + glob(typedir + '/base/*.yaml'):
            tag = self.prefix + splitext(basename(omv))[0]
            print('registering', tag)
            self.omv_types[tag] = self.parse_yaml_file(omv)

        for tag in self.sort_types_by_dependencies(self.omv_types):
            schema = self.omv_types[tag]
            print('learning', tag)
            print('with schema', schema)
            self.rx.learn_type(tag, schema)

    def sort_types_by_dependencies(self, tag_schema_map):

        alldeps = []
        for tag, schema in tag_schema_map.items():
            depset = set([self.prefix + v[5:]
                         for v in all_types_in_schema(schema)])
            alldeps.append((tag, depset))

        return topological_sort(alldeps)


if __name__ == '__main__':
    import sys
    try:
        schema_src, doc_src = sys.argv[1:]
    except:
        print('usage: validate.py schema.yaml document.yaml')
        sys.exit(1)

    s = OMVValidator()
    # print('validating document againt schema'
    print(s.validate(schema_src, doc_src))
