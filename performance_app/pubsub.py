import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .models import *
from django.db.models import Avg
import eventlet
from eventlet import wsgi
from eventlet import websocket
from eventlet.hubs import trampoline

dbname = 'seller_perf_tool'
host = 'localhost'
user = 'postgres'
password = 'postgres123'

dsn = 'dbname=%s host=%s user=%s password=%s' % (dbname, host, user, password)

def func1():
    return Marks.objects.all().aggregate(Avg('english'))['english__avg']

def dblisten(q):
    """
    Open a db connection and add notifications to *q*.
    """
    cnn = psycopg2.connect(dsn)
    cnn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = cnn.cursor()
    cur.execute("LISTEN tester;")
    while 1:
        trampoline(cnn, read=True)
        cnn.poll()
        while cnn.notifies:
            n = cnn.notifies.pop()
            q.put(n)

@websocket.WebSocketWSGI
def handle(ws):
    """
    Receive a connection and send it database notifications.
    """
    q = eventlet.Queue()
    eventlet.spawn(dblisten, q)
    while 1:
        n = q.get()
        avg = func1()
        print(avg)
        print(n)
        #ws.send(n.payload)
        ws.send(str(avg))

def dispatch(environ, start_response):
    if environ['PATH_INFO'] == '/tester':
        return handle(environ, start_response)
    else:
        start_response('200 OK',
            [('content-type', 'text/html')])
        return [page]

def run():
    listener = eventlet.listen(('127.0.0.1', 8080))
    wsgi.server(listener, dispatch)


page = """
<html>
  <head><title>pushdemo</title>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"></script>
    <style type="text/css">
      .bar {width: 20px; height: 20px;}
    </style>
    <script>
      window.onload = function() {
        ws = new WebSocket("ws://localhost:8080/tester");
        ws.onmessage = function(msg) {
          
          document.getElementById("avg").innerHTML = msg.data;

          bar = $('#' + msg.data);
          bar.width(bar.width() + 10);
          document.write(hello);
          document.write('hellooo', 'msg.data ')
        }
      }
    </script>
  </head>
  <body>
    <div style="width: 400px;">
      <div id="red" class="bar"
          style="background-color: red;">&nbsp;</div>
      <div id="green" class="bar"
          style="background-color: green;">&nbsp;</div>
      <div id="blue" class="bar"
          style="background-color: blue;">&nbsp;</div>
      <div id="avg"> </div>

    </div>
  </body>
</html>
"""