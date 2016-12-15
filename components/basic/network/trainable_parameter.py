import numpy as np
import theano

from components.component import Component


class TrainableParameter(Component):
    name = "Parameter"
    links_out = [{'position': [0, -20],
                  'name': 'Output'}]

    attributes = {'dimension': '1',
                  'initialization': 'normal(0,0.1)'}

    parsed_attributes = None

    def compile_theano(self):
        self.variable = theano.shared(self.parsed_attributes['initialization'](self.parsed_attributes['dimension']))
        self.push_by_index(0, self.variable)

    def get_upstream_trainables(self):
        return [self.variable]

    def copy(self, identifier=None):
        return TrainableParameter(identifier=identifier)

    def parse_dimension_string(self, string):
        return np.fromstring(string, sep=' ', dtype=np.uint8)

    def parse_initialization_string(self, string):
        if string.startswith('normal(') and string.endswith(')'):
            value = string[7:-1].strip().split(',')
            mu = float(value[0].strip())
            sigma = float(value[1].strip())
            return lambda dim : np.random.normal(mu, sigma, size=dim).astype(np.float32)

        return None

    def parse_attributes(self):
        d = {'dimension': self.parse_dimension_string(self.attributes['dimension']),
             'initialization': self.parse_initialization_string(self.attributes['initialization'])}

        for k in d:
            if d[k] is None:
                return False

        self.parsed_attributes = d

        return True
