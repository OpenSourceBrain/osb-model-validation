import pyrx
import yaml

class RXSchemaValidator(object):
    def __init__(self):
        self.rx = pyrx.Factory({"register_core_types": True})
        
    def generate_schema(self, schema_src):
        schema = self.parse_yaml_file(schema_src)
        print('generating schema from %s'%schema)
        return self.rx.make_schema(schema) 

    def parse_yaml_file(self, fname):
        with open(fname) as f:
            y = yaml.safe_load(f)
        return y
        
    def validate(self, schema_src, doc_src):
        doc = self.parse_yaml_file(doc_src)
        print('validating document %s'%doc)
        return self.generate_schema(schema_src).check(doc)

if __name__ == '__main__':
    import sys
    try:
        schema_src, doc_src = sys.argv[1:]
    except:
        print('usage: validate_rx.py schema.yaml document.yaml')
        sys.exit(1)


    s = RXSchemaValidator()
    print(s.validate(schema_src, doc_src))
