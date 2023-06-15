from bottle import request, response, app, BaseRequest
import traceback
import win32print

try:
    printer_name = win32print.GetDefaultPrinter()
except Exception:
    print("Unable to declare printer: \n%s" % traceback.format_exc())


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8069'
        response.headers['Access-Control-Allow-Origin'] = 'https://cam14.arkana.app'
        response.headers['Access-Control-Allow-Origin'] = 'https://ttdistindo.com'
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
            response.headers['Access-Control-Allow-Origin'] = 'https://cam14.arkana.app'
            response.headers['Access-Control-Allow-Origin'] = 'https://ttdistindo.com'
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


proxy_app = app()
proxy_app.install(EnableCors())


@proxy_app.route('/', method=['OPTIONS', 'POST'])
@enable_cors
def hello():
    try:
        ptr = win32print.OpenPrinter(printer_name)
        win32print.StartDocPrinter(
            ptr, 1, ("test of raw data", None, "RAW"))
        win32print.StartPagePrinter(ptr)
        if 'TM' not in printer_name:
            win32print.WritePrinter(
                ptr, b'\x1b!\x00\x1b!\x00\x1b!\x00\x1b{\x00\x1bE\x00\x1b-\x00\x1bM\x00\x1ba\x00')
        
        try:
            win32print.WritePrinter(ptr, bytes(
                request.json.get('data').get('text','') + '\n', "utf-8"))
            print(request.json.get('data').get('text'))
        except Exception:
            print('Gagal Textln \n%s' % traceback.format_exc())
        try:
            if 'TM' in printer_name:
                for dummy in range(0, 6):
                    win32print.WritePrinter(ptr, bytes('\n', "utf-8"))
                win32print.WritePrinter(ptr, b'\x1dV\x00')
            win32print.EndPagePrinter(ptr)
            win32print.EndDocPrinter(ptr)
            win32print.ClosePrinter(ptr)
        except Exception:
            print('Gagal Close \n%s' % traceback.format_exc())
        return '"{"success":true, "messages":"Printing Success!"}"'
    except Exception:
        print('Something Wrong! \n%s' % traceback.format_exc())
        return '"{"success":false, "messages":"Something Wrong! %s"}"' % traceback.format_exc()


BaseRequest.MEMFILE_MAX = 1024 * 1024 * 100
proxy_app.run(host='localhost', port=5000, debug=True)
