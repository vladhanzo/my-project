# backend/app/utils/qr_generator.py
import os
import qrcode

def generate_qr(data: str, filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    output_dir = os.path.join(base_dir, 'qr_codes')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f'{filename}.png')
    img = qrcode.make(data)
    img.save(file_path)
    return f'/static/qr_codes/{filename}.png'
