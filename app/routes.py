from app import app_instance

@app_instance.route('/')
@app_instance.route('/index')
def index():
    return "Great courier app soon!"