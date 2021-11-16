from flask import Flask
import sys
import time
from celery import Celery

app=Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def some_fn():
    with app.app_context():
        time.sleep(10)
    #time.sleep(10)
    print("success")
    return "success"

@app.route("/")
def index():
    some_fn.apply_async()
    return {"msg":"Index page"}

if __name__=='__main__':
    #print(sys.version)
    app.run(debug=True)