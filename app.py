from flask import Flask, render_template, request, jsonify, url_for
from funcs import *
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import threading
import webbrowser
import time


def ask_for_image():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    file_options = dict(
        title="Select Image File",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    image_file_path = filedialog.askopenfilename(**file_options)
    root.destroy()
    return image_file_path


def ask_for_text():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    file_options = dict(
        title="Select Text File",
        filetypes=[("Text files", "*.txt")]
    )
    text_file_path = filedialog.askopenfilename(**file_options)
    root.destroy()
    return text_file_path


def ask_for_output():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    file_options = dict(
        title="Save output",
        filetypes=[("Image files", "*.jpg;")]
    )
    image_file_path = filedialog.asksaveasfilename(**file_options)
    root.destroy()
    return image_file_path


def ask_for_dir():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    options = dict(
        title="Output Directory",
    )
    dir = filedialog.askdirectory(**options)
    root.destroy()
    return dir


def askfileImg():
    result = None
    def thread_function():
        nonlocal result
        result = ask_for_image()
    thread = threading.Thread(target=thread_function)
    thread.start()
    thread.join()
    return result


def askfileTxt():
    result = None
    def thread_function():
        nonlocal result
        result = ask_for_text()
    thread = threading.Thread(target=thread_function)
    thread.start()
    thread.join()
    return result


def askoutput():
    result = None
    def thread_function():
        nonlocal result
        result = ask_for_output()
    thread = threading.Thread(target=thread_function)
    thread.start()
    thread.join()
    return result+'.jpg'


def askdir():
    result = None
    def thread_function():
        nonlocal result
        result = ask_for_dir()
    thread = threading.Thread(target=thread_function)
    thread.start()
    thread.join()
    return result


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/img', methods=['POST'])
def save_img():
    data = request.json
    p = askfileImg()
    return jsonify({'message': 'Image received successfully', 'img': p})


@app.route('/txt', methods=['POST'])
def save_txt():
    data = request.json
    p = askfileTxt()
    return jsonify({'message': 'Text received successfully', 'txt': p})


@app.route('/output', methods=['POST'])
def save_out():
    data = request.json
    p = askoutput()
    return jsonify({'message': 'Text received successfully', 'out': p})


@app.route('/sendData', methods=['POST'])
def get_data():
    data = request.json
    imgPath = data.get('imgPath')
    outPath = data.get('outPath')
    txt = data.get('txt')
    isDirect = data.get('isDirect')
    if not isDirect:
        try:
            with open(txt) as f:
                txt = f.read().strip()
        except:
            return jsonify({'message': "There was a problem reading the text file", "rs": False})
    a = hide_text(imgPath, txt, outPath)
    if a[0]:
        return jsonify({'message': 'Successfully encrypted text in image', "rs": True})
    else:
        return jsonify({'message': f'Error: {a[1]}', "rs": False})


@app.route('/sendData1', methods=['POST'])
def get_data1():
    data = request.json
    imgPath = data.get("path")
    if not Path(imgPath).is_file():
        return jsonify({'message': 'The path of the image does not exist', 'rs': False})
    d = extract_text_from_image(imgPath)
    if d == None:
        return jsonify({'message': 'There was an error decrypting the file', 'rs': False})
    d = dec(d)
    if d[0]:
        return jsonify({'message': 'Successfully encrypted text in image', 'txt': d[1], 'rs': True})
    else:
        return jsonify({'message': d[1], 'rs': False})


@app.route('/dir', methods=['POST'])
def save_dir():
    data = request.json
    p = askdir()
    return jsonify({'message': 'Text received successfully', 'out': p})

@app.route('/saveFile', methods=['POST'])
def saveFile():
    data = request.json
    output_path = data['path']
    output_name = data['name']
    text_content = data['txt']
    full = os.path.join(output_path, output_name)
    n = 1
    while os.path.exists(full):
        temp_name = output_name
        n += 1
        base_name, extension = os.path.splitext(temp_name)
        temp_name = f"{base_name} ({n}){extension}"
        full = os.path.join(output_path, temp_name)
    try:
        with open(full, 'w') as file:
            file.write(text_content)
            return jsonify({'message':f'Text successfully saved to {full}', 'rs': True})
    except Exception as e:
        return jsonify({'message': f'Error saving file: {e}', 'rs': False})


def open_browser_with_delay(au):
    time.sleep(0.5)
    webbrowser.open(au)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5151
    base_url = f'http://{host}:{port}'
    thread = threading.Thread(target=lambda:open_browser_with_delay(base_url))
    thread.start()
    app.run(host=host, port=port, use_reloader=False)
