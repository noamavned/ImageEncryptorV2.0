from pathlib import Path
import random
import os
import shutil


def enc(s):
    s = [''.join(format(ord(n), 'b')) for n in s]
    n = []
    for v, i in enumerate(s):
        n.append(f'|{v*360}|'+str(int(''.join([str(random.choice([1, 2, 3, 4]))
                 if x == '1' else str(random.choice([5, 6, 7, 8])) for x in i]))+180))
    random.shuffle(n)
    n = ''.join(n)
    return n


def dec(s):
    try:
        chunks = s.split('|')[1::]
        l = [[int(int(chunks[i])/360), str(''.join(['1' if int(x) in [1, 2, 3, 4]
                                                    else '0' for x in str(int(chunks[i+1])-180)]))] for i in range(0, len(chunks), 2)]
        l = [x[1] for x in sorted(l, key=lambda x: x[0])]
        l = ''.join([chr(int(binary, 2)) for binary in l])
        return [True, l]
    except:
        return [False, "Error decrypting image"]


def extract_text_from_image(image_path):
    image_copy_path = image_path[0:-4] + '_copy.txt'

    try:
        shutil.copy(image_path, image_copy_path)
    except FileNotFoundError:
        return None
    except FileExistsError:
        return None
    successful_decode = False
    encodings_to_try = ['utf-8', 'latin-1', 'ascii']
    for encoding in encodings_to_try:
        try:
            with open(image_copy_path, 'r', encoding=encoding) as f:
                t = f.read().strip()
                t = t.split("/scb325/")[-2]
                successful_decode = True
                break
        except UnicodeDecodeError:
            continue
        except:
            t = None
            break
    if not successful_decode:
        t = None
    os.remove(image_copy_path)
    return t


def hide_text_in_jpeg(image_path, text_to_hide, output_path):
    try:
        with open(image_path, 'rb') as file:
            jpeg_data = bytearray(file.read())
        eoi_marker_index = jpeg_data.rfind(b'\xFF\xD9')

        encoded_text = text_to_hide.encode('utf-8')
        jpeg_data = jpeg_data[:eoi_marker_index] + \
            encoded_text + jpeg_data[eoi_marker_index:]

        with open(output_path, 'wb') as output_file:
            output_file.write(jpeg_data)
    except:
        return [False, "Error while hiding text in image"]
    return [True]


def hide_text(image_path, text, output_path):
    d = dec(extract_text_from_image(image_path))
    if d[0]:
        return [False, "Image already has encrypted text Or there has been an error extracting text from image"]
    try:
        text = enc(text)
    except:
        return [False, "Something went wrong while encrypting the text.\nPlease try again"]
    if not Path(image_path).is_file():
        return [False, "Image's path does not exist!"]
    if not Path(os.path.dirname(output_path)).is_dir():
        return [False, "Output's path does not exist!"]
    text = "/scb325/" + text + "/scb325/"
    a = hide_text_in_jpeg(image_path, text, output_path)
    return a