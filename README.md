<div align="center">

  <img src="https://github.com/Zerogallo/QR-Code-Manager/blob/main/static/L%20QRcode.png" style="width: 500px; height: 200px;"/>
   <img src="https://github.com/Zerogallo/QR-Code-Manager/blob/main/static/ler.png" style="width: 500px; height: 200px;"/>
        <img src="https://github.com/Zerogallo/QR-Code-Manager/blob/main/static/Gerar.png" style="width: 500px; height: 200px;"/>
    <img src="https://github.com/Zerogallo/QR-Code-Manager/blob/main/static/hostorico%20QR.png" style="width: 500px; height: 200px;"/>
    
    
     
 

</div>

## QR Code Manager - Projeto Flask

Um sistema completo para gerar e ler QR Codes desenvolvido em Python com Flask.

## Funcionalidades

1. Gerador de QR Codes: Crie QR Codes personalizados para textos, URLs, e-mails, etc
2. Leitor de QR Codes:
  3. Upload de imagens para decodificação
  4. Leitura em tempo real pela câmera web
5. Histórico: Armazenamento de todos os QR Codes gerados e lidos
6. Exportação de dados: Exporte o histórico para Excel
7. API REST: Endpoint para geração de QR Codes via API

## Tecnologias Utilizadas


 1. Backend: Flask, SQLite3
 2. Processamento de QR Codes: qrcode, OpenCV, pyzbar
 3. Processamento de dados: pandas, numpy
 4. Frontend: HTML5, Bootstrap, JavaScript
 5. Imagens: Pillow (PIL)

## Como Usar

Gerando QR Codes

1. Acesse a página "Gerar QR Code"
2. Insira os dados (texto, URL, etc.)
3. Selecione o tipo
4. Clique em "Gerar QR Code"
5. Faça download da imagem gerada



## Histórico e Exportação

· Visualize todos os QR Codes na página "Histórico"
· Exporte os dados para Excel com um clique

## Estrutura do Projeto

```
qr-code-manager/
├── app.py                 # Aplicação principal Flask
├── database.py           # Configuração do banco de dados
├── models.py            # Modelos de dados
├── requirements.txt     # Dependências do projeto
├── templates/          # Templates HTML
│   ├── index.html
│   ├── generator.html
│   ├── reader.html
│   ├── camera_reader.html
│   └── history.html
└── static/
    ├── style.css       # Estilos CSS
    └── qr_codes/       # QR Codes gerados
```

## API

Gerar QR Code via API
```
bash
POST /api/generate
Content-Type: application/json

{
    "data": "https://exemplo.com"
}


Resposta:

json
{
    "qr_code": "base64_encoded_image"
}
```

## Banco de Dados

O projeto utiliza SQLite3 com a seguinte estrutura:
```
sql
CREATE TABLE qr_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    type TEXT NOT NULL,
    filename TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```


---


