from mako.template import Template
import sys
import yaml

templatefile = "example.sql"
datafile = "example.yaml"
template = open(templatefile, 'r').read()
config = yaml.safe_load(open(datafile, 'r'))
print(Template(template).render(**config))
