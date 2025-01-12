import sys

from app import create_app

sys.path.append("./cross_detection/")
sys.path.append("./human_detection/")
sys.path.append("./lane_detection/")

app = create_app()
app.debug = True

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['JSON_AS_ASCII'] = False
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
