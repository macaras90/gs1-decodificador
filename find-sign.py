import base64
import os

TARGET_SIGNATURE = "@author: r1g312"

def encode_base64(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decode_base64(text):
    return base64.b64decode(text.encode('utf-8')).decode('utf-8')

LOGS_DIR = "logs_ofuscados"

def encontrar_logs(caminho_raiz):
    arquivos_log = []
    for raiz, _, arquivos in os.walk(caminho_raiz):
        for arquivo in arquivos:
            if arquivo.endswith(".log"):
                arquivos_log.append(os.path.join(raiz, arquivo))
    return arquivos_log

# Busca todos os arquivos .log
logs = encontrar_logs(LOGS_DIR)
print(f"Total de arquivos encontrados: {len(logs)}")

# Gera versão codificada da assinatura
assinatura_codificada = encode_base64(TARGET_SIGNATURE)

# Verifica qual arquivo contém a assinatura e salva o conteúdo decodificado em author.txt
for caminho_log in logs:
    try:
        with open(caminho_log, 'r') as arquivo:
            conteudo = arquivo.read()
            if assinatura_codificada in conteudo:
                conteudo_decodificado = decode_base64(conteudo)
                with open("author.txt", "w") as f_out:
                    f_out.write(conteudo_decodificado)
                print(f"Assinatura encontrada em: {caminho_log}")
                break
    except Exception as e:
        print(f"Erro ao ler {caminho_log}: {e}")

# Decodifica todos os arquivos e recria a estrutura na pasta 'decodificados'
DESTINO = "decodificados"

for caminho_log in logs:
    try:
        with open(caminho_log, 'r') as arquivo:
            conteudo = arquivo.read()
            conteudo_decodificado = decode_base64(conteudo)

            caminho_relativo = os.path.relpath(caminho_log, LOGS_DIR)
            novo_caminho = os.path.join(DESTINO, caminho_relativo)

            os.makedirs(os.path.dirname(novo_caminho), exist_ok=True)

            with open(novo_caminho, 'w') as f_out:
                f_out.write(conteudo_decodificado)

    except Exception as e:
        print(f"Erro ao processar {caminho_log}: {e}")