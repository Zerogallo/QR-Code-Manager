from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from io import BytesIO
import base64
import os
import cv2
from pyzbar.pyzbar import decode
import numpy as np
from database import init_db
from models import QRCodeModel

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qr_codes'

# Criar diretórios necessários
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generator', methods=['GET', 'POST'])
def generator():
    if request.method == 'POST':
        data = request.form.get('data')
        qr_type = request.form.get('type', 'text')
        
        if data:
            # Gerar QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Salvar imagem
            filename = f"qr_{len(QRCodeModel.get_all_qr_codes()) + 1}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(filepath)
            
            # Salvar no banco de dados
            QRCodeModel.save_qr_code(data, qr_type, filename)
            
            # Converter para base64 para exibição
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return render_template('generator.html', 
                                 qr_code=img_str, 
                                 data=data,
                                 success=True)
    
    return render_template('generator.html')

@app.route('/reader', methods=['GET', 'POST'])
def reader():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('reader.html', error="Nenhum arquivo selecionado")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('reader.html', error="Nenhum arquivo selecionado")
        
        if file:
            # Ler imagem
            img_array = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            # Decodificar QR Code
            decoded_objects = decode(img)
            
            if decoded_objects:
                results = []
                for obj in decoded_objects:
                    data = obj.data.decode('utf-8')
                    qr_type = obj.type
                    results.append({
                        'data': data,
                        'type': qr_type
                    })
                    # Salvar no banco de dados
                    QRCodeModel.save_qr_code(data, f"leitura_{qr_type}")
                
                return render_template('reader.html', results=results, success=True)
            else:
                return render_template('reader.html', error="Nenhum QR Code encontrado na imagem")
    
    return render_template('reader.html')

@app.route('/history')
def history():
    qr_codes = QRCodeModel.get_all_qr_codes()
    return render_template('history.html', qr_codes=qr_codes)

@app.route('/export')
def export_data():
    filename = QRCodeModel.export_to_excel()
    return send_file(filename, as_attachment=True)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    QRCodeModel.save_qr_code(data, 'api_text')
    
    return jsonify({'qr_code': img_str})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
