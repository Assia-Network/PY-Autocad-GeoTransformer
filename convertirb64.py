import base64
with open("ico.png", "rb") as image_file:
    texto_puro = base64.b64encode(image_file.read()).decode('utf-8')
with open("b64_ico.txt", "w") as archivo:
    archivo.write(texto_puro)