from flask import Flask, request, Response
from celery import Celery
from tasks import send_email, log_time
import os

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        send_email.delay(sendmail)
        return f'Email sending to {sendmail} has been queued.'

    if talktome:
        log_time.delay()
        return 'Time logging has been queued.'

    return 'Specify either ?sendmail or ?talktome.'

@app.route('/logs')
def get_logs():
    log_path = '/var/log/messaging_system.log'

    if os.path.exists(log_path):
        with open(log_path, 'r') as log_file:
            logs = log_file.read()
        return Response(logs, mimetype='text/plain')
    else:
        return 'Log file not found.', 404

if __name__ == '__main__':
    app.run(debug=True)

