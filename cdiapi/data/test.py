import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from datacatalog import DataCatalog

print(DataCatalog.schema())

filepath = 'metadatasbsgovws.yaml'
f = open(filepath, 'r', encoding='utf8')
data = yaml.load(f, Loader=Loader)            
f.close()

print(DataCatalog.parse_obj(data))