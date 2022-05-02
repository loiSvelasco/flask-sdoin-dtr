from waitress import serve
import app
serve(app.app, host='192.168.101.80', port=5000, threads=8)