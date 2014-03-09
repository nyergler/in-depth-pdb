from pfcalc import *


if __name__ == '__main__':

    try:
        httpd = make_server('', 8000, rpn_app,
                            server_class=CalculatorServer,
                            handler_class=CalculatorWSGIHandler,
        )
        print "Serving on port 8000..."
        httpd.serve_forever()
    except:
        import pdb
        pdb.set_trace()
