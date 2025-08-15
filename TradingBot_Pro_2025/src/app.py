import os
from flask import Flask, jsonify, send_from_directory

# Determine the correct static folder path
static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public'))

app = Flask(__name__, static_folder=static_folder, static_url_path='')

# In-memory status for the bot
bot_status = {"status": "OFF"}

@app.route('/api/status', methods=['GET'])
def get_status():
    """API endpoint to get the bot status."""
    return jsonify(bot_status)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Serves the frontend application."""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
