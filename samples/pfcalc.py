from wsgiref.simple_server import make_server
from pfcalc_wsgi import (
    CalculatorServer,
    CalculatorWSGIHandler,
)


class Calculator(object):

    OPERATORS = {
        '+': int.__add__,
        '*': int.__mul__,
        '/': int.__div__,
    }

    def __init__(self):

        self.state = []

    def push(self, value_or_operator):

        if value_or_operator in self.OPERATORS:
            value = self.OPERATORS[value_or_operator](
                self.state.pop(),
                self.state.pop(),
            )
        else:
            value = int(value_or_operator)

        self.state.append(value)

    def result(self):

        if len(self.state) > 1:
            # incomplete expressions
            raise SyntaxError("Invalid expression.")

        return self.state[0]


def rpn_app(environ, start_response):

    c = Calculator()

    for element in environ['PATH_INFO'][1:].split('/'):
        c.push(element)

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)

    return [
        "The answer is %d" % (c.result(),),
    ]

if __name__ == '__main__':

    httpd = make_server('', 8000, rpn_app,
                        server_class=CalculatorServer,
                        handler_class=CalculatorWSGIHandler,
    )
    print "Serving on port 8000..."
    httpd.serve_forever()
