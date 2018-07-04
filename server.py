from gevent import monkey; monkey.patch_all()
import gevent
import gevent.queue

import uwsgi

curr_conn = None


# ============================================================================
def application(env, start_response):
    global curr_conn
    if curr_conn:
        print('Close Prev')
        curr_conn.close()

    curr_conn = AudioProxy()

    if 'HTTP_SEC_WEBSOCKET_KEY' in env:
        curr_conn.handle_ws(env)
    else:
        return curr_conn.handle_http(env, start_response)


# ============================================================================
class AudioProxy(object):
    PORT = 6082

    def __init__(self):
        self.connected = True
        self.buff_size = 16384*4
        self.proc = None

    def start_proc(self):
        print('Starting Audio Server')


    def get_audio_buff(self):
        with open("./Death_By_Unga_-_09_-_Young_Girls.webm", mode="rb") as webm:
            while True:
                data = webm.read(300) # too fast
                #data = webm.read(169) # OK
                #data = webm.read(165) # OK
                #data = webm.read(150) # little bit slow
                #data = webm.read(130)  # too slow

                if not data:
                    break
                yield data
                gevent.sleep(0.01)

    def handle_ws(self, env):
        # complete the handshake
        uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'],
                                  env.get('HTTP_ORIGIN', ''))

        print('WS Connected: ' + env.get('QUERY_STRING', ''))

        ready = uwsgi.websocket_recv()

        print('Ready, Starting Audio Stream')

        self.start_proc()
        gevent.sleep(0.3)

        try:
            for buff in self.get_audio_buff():
                if not buff:
                    break

                uwsgi.websocket_send_binary(buff)
            print("stream end")

        except Exception as e:
            import traceback
            traceback.print_exc()

        finally:
            self.close()
            print('WS Disconnected')

    def close(self):
        self.connected = False
        if self.proc:
            self.proc.kill()


