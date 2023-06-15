from escpos.printer import Usb, Dummy
from bottle import request, response, app, BaseRequest
import traceback
import platform

if platform.system() == 'Linux':
    try:
        p = Usb(0x04b8, 0x0046)
    except Exception:
        print("Unable to declare printer: \n%s" % traceback.format_exc())
        p = False
    
    
    def enable_cors(fn):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8069'
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    
            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)
    
        return _enable_cors
    
    
    class EnableCors(object):
        name = 'enable_cors'
        api = 2
    
        def apply(self, fn, context):
            def _enable_cors(*args, **kwargs):
                # set CORS headers
                response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8069'
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
                response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    
                if request.method != 'OPTIONS':
                    # actual request; reply with the actual response
                    return fn(*args, **kwargs)
    
            return _enable_cors
    
    
    proxy_app = app()
    
    
    @proxy_app.route('/', method=['OPTIONS', 'POST'])
    @enable_cors
    def hello():
        try:
            print('okee')
            data = Dummy()
            data.set(font='a', custom_size=True, bold=False, density=1)
            align = 'left'
            # for line in request.json.get('dataline'):
            #     if line.get('align', 'left') != align:
            #         align = line.get('align', 'left')
            #         data.set(align=align)
            #     data.textln(line.get('text'))
            #     if not p:
            #         print(line.get('text'))
            # data.control('FF')
            data.textln(request.json.get('data').get('text'))
            if p:
                p._raw(data.output)
            data.close()
            return '"{"success":true, "messages":"Printing Success!"}"'
        except Exception:
            return '"{"success":false, "messages":"Something Wrong! %s"}"' % traceback.format_exc()
    
    
    BaseRequest.MEMFILE_MAX = 1024 * 1024 * 100
    proxy_app.install(EnableCors())
    proxy_app.run(host='localhost', port=5000, debug=True)
    