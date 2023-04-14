from website import create_app
from flask import render_template
from flask_login import current_user
from waitress import serve

app = create_app()

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', user=current_user), 404

if __name__ == '__main__':
    # app.run(debug=True)
    serve(app.app, host='192.168.1.4', port=5000, threads=4)

#                           CHANGE TO UR IPV4
# * To run: waitress-serve --host=192.168.101.193 --port=80 --call "app:create_app"