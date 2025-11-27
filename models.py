from database import get_db_connection
import pandas as pd
from datetime import datetime

class QRCodeModel:
    @staticmethod
    def save_qr_code(data, qr_type, filename=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO qr_codes (data, type, filename) VALUES (?, ?, ?)',
            (data, qr_type, filename)
        )
        
        conn.commit()
        qr_id = cursor.lastrowid
        conn.close()
        return qr_id
    
    @staticmethod
    def get_all_qr_codes():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM qr_codes ORDER BY created_at DESC')
        qr_codes = cursor.fetchall()
        
        conn.close()
        return qr_codes
    
    @staticmethod
    def export_to_excel():
        qr_codes = QRCodeModel.get_all_qr_codes()
        
        data = []
        for qr in qr_codes:
            data.append({
                'ID': qr['id'],
                'Data': qr['data'],
                'Tipo': qr['type'],
                'Arquivo': qr['filename'],
                'Data de Criação': qr['created_at']
            })
        
        df = pd.DataFrame(data)
        filename = f"qr_codes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)
        return filename
