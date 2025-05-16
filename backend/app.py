# backend/app.py

from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Code Runner API is live! Use POST /run to execute Python code.'

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get("code")
    user_input = request.json.get("input", "")

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(code.encode())
        temp.flush()

    try:
        result = subprocess.run(
            ["python3", temp.name],
            input=user_input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        output = result.stdout.decode()
        error = result.stderr.decode()
        os.unlink(temp.name)
        return jsonify({"output": output, "error": error})
    except Exception as e:
        return jsonify({"output": "", "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
