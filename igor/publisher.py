from __future__ import with_statement

from shutil import  rmtree
from os import path, makedirs
from jinja2 import Environment, FileSystemLoader

import template_tools
from template_tools import functions as template_functions,\
                           filters as template_filters,\
                           render_template

class Publisher(object):
    """
    The publisher incorperates the instantiation of the tools needed to publish
    documents it's not complicated but useful.
    """
    def __init__(self, documents, destination, templates_dir, context={}):
        self.documents = documents
        self.destination = destination
        self.templates_dir = templates_dir
        self.context = dict(documents = documents, **context)
        self.env = self.environment(context=self.context)

    def prepare_dir(self, dir, rebuild=False):
        if path.exists(dir):
            if rebuild:
                rmtree(dir)
                makedirs(dir)
        else:
            makedirs(dir)
        return dir

    def environment(self, functions=[], filters=[], context={}):
        """
        Instantiates and prepares the jinja environment
        """
        env = Environment(loader=FileSystemLoader(self.templates_dir))

        for f in functions + template_functions:
            env.globals[f.func_name] = f

        for f in filters + template_filters:
            env.filters[f.func_name] = f

        env.globals.update(context)
        return env

    def publish_document(self, doc):
        """
        Write a document (of type Document) out to file.

        Documents provide a publish_directory method which I'm not happy with
        and should be incorperated into the Publisher.
        """
        context = dict(doc=doc, **doc.headers)
        out = render_template(self.env, doc.template, context=context)

        publish_dir = self.prepare_dir(path.join(self.destination,
                                                 doc.publish_directory()))

        publish_path = path.join(publish_dir, doc.out_file)

        print("... publishing: %s to %s" % (doc.slug, publish_path))

        with open(publish_path, 'w') as f:
            f.write(out) 

        return doc

    def publish(self):
        return [self.publish_document(doc) for doc in self.documents]
