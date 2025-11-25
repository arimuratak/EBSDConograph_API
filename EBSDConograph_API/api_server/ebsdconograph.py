import os
from flask import Flask, request, send_file, jsonify
import subprocess
import shutil
import stat

CURRENT_DIR = os.path.dirname (os.path.abspath (__file__))
os.chdir (CURRENT_DIR)
PATH_input = os.path.join (CURRENT_DIR, 'input.txt')
PATH_data = os.path.join (CURRENT_DIR, 'data.txt')
PATH_output = os.path.join (CURRENT_DIR, 'out.txt')
PATH_log = os.path.join (CURRENT_DIR, 'LOG_CONOGRAPH.txt')

if os.name == 'nt':
    PATH_exe = '.\EBSDConograph.exe'
else:
    PATH_exe = os.path.join (CURRENT_DIR, 'EBSDConograph')
    if not os.access (PATH_exe, os.X_OK):
        os.chmod(PATH_exe, os.stat (PATH_exe).st_mode | stat.S_IEXEC)

app = Flask(__name__)

@app.route ('/run_cpp', methods = ['POST'])
def run_exec ():
    if os.path.exists (PATH_data): os.remove (PATH_data)
    if os.path.exists (PATH_output): os.remove (PATH_output)
    if os.path.exists (PATH_log): os.remove (PATH_log)

    for key in request.files:
        f = request.files[key]
        fname = f.name
        if 'data' in fname:
            path = PATH_data
        elif 'input' in fname:
            path = PATH_input
        f.save (path)

    result = subprocess.run ([PATH_exe])

    if os.path.exists (PATH_output):
        return send_file(PATH_output, as_attachment = True), 200
    else:
        return jsonify({"error": "出力ファイルがありません"}), 500

@app.route ('/log_file', methods = ['POST'])
def log_file ():
    if os.path.exists (PATH_log):
        return send_file (PATH_log, as_attachment = True), 200
    else:
        return jsonify ({'error' : '送信ファイルがありません'}), 500


if __name__ == '__main__':
    app.run (host = "0.0.0.0", port = 9000, debug = False)