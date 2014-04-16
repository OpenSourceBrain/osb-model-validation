from os.path import splitext, basename
from rx_validator import RXSchemaValidator
from utils import topological_sort, all_types_in_schema


class OMVValidator(RXSchemaValidator):

    def __init__(self):
        super(OMVValidator, self).__init__()
        self.add_osb_prefix()
        self.register_osb_types()

    def add_osb_prefix(self):
        self.prefix = 'tag:opensourcebrain.org,2014:schemata/omv/'
        self.rx.add_prefix('ost', self.prefix)

    def register_osb_types(self):

        self.ost_types = {}
        from glob import glob
        for ost in glob('../schemata/types/*.yaml') + glob('../schemata/types/base/*.yaml'):
            tag = self.prefix + splitext(basename(ost))[0]
            self.ost_types[tag] = self.parse_yaml_file(ost)

        for tag in self.sort_types_by_dependencies(self.ost_types):
            schema = self.ost_types[tag]
            # print 'learning', tag
            # print 'with schema', schema
            self.rx.learn_type(tag, schema)

    def sort_types_by_dependencies(self, tag_schema_map):

        alldeps = []
        for tag, schema in tag_schema_map.iteritems():
            depset = set([self.prefix + v[5:]
                         for v in all_types_in_schema(schema)])
            alldeps.append((tag, depset))

        return topological_sort(alldeps)


if __name__ == '__main__':
    import sys
    try:
        schema_src, doc_src = sys.argv[1:]
    except:
        print 'usage: validate.py schema.yaml document.yaml'
        sys.exit(1)

    s = OMVValidator()
    # print 'validating document againt schema'
    print s.validate(schema_src, doc_src)
