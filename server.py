from waitress import serve
import app
serve(app.app, host='192.168.102.25', port=5001, threads=8)