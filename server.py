from waitress import serve
import app
serve(app.app, host='192.168.1.4', port=80)