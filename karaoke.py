import pygame
import os
import time
import re

PASTA_MIDIA = 'musicas'
LARGURA_TERMINAL = 60
LINHAS_DE_CONTEXTO = 5 

COR_TITULO = '\033[1;36m'    # Ciano
COR_DESTAQUE = '\033[1;93m'  # Amarelo Brilhante
COR_PASSADA = '\033[1;90m'   # Cinza Escuro
COR_FUTURA = '\033[0;37m'    # Branco/Cinza Claro
COR_ERRO = '\033[1;31m'      # Vermelho
RESET_COR = '\033[0m'

def limpar_tela():

    os.system('cls' if os.name == 'nt' else 'clear')

def parse_lrc(caminho_arquivo):

    if not os.path.exists(caminho_arquivo):
        return None

    lines = []
    for encoding in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
        try:
            with open(caminho_arquivo, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break 
        except UnicodeDecodeError:
            continue
    
    if not lines:
        print(f"{COR_ERRO}Erro: Falha na codificação do arquivo LRC.{RESET_COR}")
        return None

    # Regex para capturar [00:00.00]Texto
    lrc_regex = re.compile(r'((?:\[\d{2}:\d{2}[\.\:]\d{2,3}\])+)(.*)')
    lyrics = []

    for line in lines:
        match = lrc_regex.match(line)
        if not match: 
            continue
        
        timestamps_str = match.group(1)
        text = match.group(2).strip()
        
        if not text: 
            continue

        first_ts = timestamps_str[1:timestamps_str.find(']')]
        
        try:
            minutos, resto = first_ts.split(':')
            
            # Trata separador de segundos e milissegundos (. ou :)
            if '.' in resto:
                segundos, milis = resto.split('.')
            elif ':' in resto:
                segundos, milis = resto.split(':')
            else:
                segundos, milis = resto, "0"
            
            if len(milis) == 2: 
                milis_val = int(milis) / 100.0
            elif len(milis) == 3: 
                milis_val = int(milis) / 1000.0
            else:
                milis_val = 0

            tempo_total = (int(minutos) * 60) + int(segundos) + milis_val
            lyrics.append((tempo_total, text))
            
        except ValueError:
            continue

    # Ordena pelo tempo para garantir sincronia
    lyrics.sort(key=lambda x: x[0])
    return lyrics

def listar_opcoes_validas():
    """
    Escaneia a pasta definida e retorna uma lista de dicionários
    contendo apenas músicas que possuem o par MP3 + LRC.
    """
    caminho_base = os.path.join(os.getcwd(), PASTA_MIDIA)
    
    # Cria a pasta se não existir
    if not os.path.exists(caminho_base):
        try:
            os.makedirs(caminho_base)
            print(f"Pasta '{PASTA_MIDIA}' criada. Adicione suas músicas lá e reinicie.")
        except OSError as e:
            print(f"{COR_ERRO}Erro ao criar pasta: {e}{RESET_COR}")
        return []

    arquivos = os.listdir(caminho_base)
    mp3s = [f for f in arquivos if f.lower().endswith('.mp3')]
    opcoes = []

    for mp3 in mp3s:
        nome_base = os.path.splitext(mp3)[0]
        lrc_correspondente = nome_base + ".lrc"
        
        lrc_existe = any(f.lower() == lrc_correspondente.lower() for f in arquivos)
        
        if lrc_existe:
            nome_lrc_real = next(f for f in arquivos if f.lower() == lrc_correspondente.lower())
            
            opcoes.append({
                'nome': nome_base,
                'caminho_mp3': os.path.join(PASTA_MIDIA, mp3),
                'caminho_lrc': os.path.join(PASTA_MIDIA, nome_lrc_real)
            })
    
    return opcoes

def menu_escolha(opcoes):
    """Exibe o menu numérico e retorna a opção escolhida."""
    while True:
        limpar_tela()
        print(f"{COR_TITULO}=== PYTHON KARAOKE ==={RESET_COR}")
        print(f"Músicas encontradas na pasta '{PASTA_MIDIA}':\n")
        
        if not opcoes:
            print(f"{COR_ERRO}Nenhum par (.mp3 + .lrc) encontrado!{RESET_COR}")
            print("Verifique se os nomes dos arquivos são idênticos.")
            input("\nPressione ENTER para sair...")
            return None

        for i, item in enumerate(opcoes):
            print(f"[{i + 1}] {item['nome']}")
        
        print(f"\n[0] Sair")
        print("-" * 30)
        
        entrada = input(f"{COR_DESTAQUE}Digite o número da música: {RESET_COR}").strip()
        
        if entrada == '0':
            return None
            
        if entrada.isdigit():
            idx = int(entrada) - 1
            if 0 <= idx < len(opcoes):
                return opcoes[idx]
        
        print(f"{COR_ERRO}Opção inválida! Tente novamente.{RESET_COR}")
        time.sleep(1)

def tocar_karaoke(musica):
    """Executa a lógica de tocar a música e sincronizar a letra."""
    # 1. Faz o parse da letra
    lyrics = parse_lrc(musica['caminho_lrc'])
    if not lyrics:
        input("Pressione ENTER para voltar ao menu...")
        return

    # 2. Inicializa o mixer e carrega o áudio
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(musica['caminho_mp3'])
    except pygame.error as e:
        print(f"{COR_ERRO}Erro ao carregar MP3: {e}{RESET_COR}")
        input("Pressione ENTER para voltar...")
        return

    limpar_tela()
    print(f"Carregando: {COR_TITULO}{musica['nome']}{RESET_COR}")
    print("Prepare-se...")
    time.sleep(1)
    
    print("\nPressione ENTER para começar")
    input()

    pygame.mixer.music.play()
    
    idx_atual = -1
    
    try:
        while pygame.mixer.music.get_busy():
            tempo_musica = pygame.mixer.music.get_pos() / 1000.0
            
            novo_idx = -1
            for i, (timestamp, _) in enumerate(lyrics):
                if tempo_musica >= timestamp:
                    novo_idx = i
                else:
                    break
            
            if novo_idx != idx_atual:
                idx_atual = novo_idx
                
                limpar_tela()
                
                inicio = max(0, idx_atual - LINHAS_DE_CONTEXTO)
                fim = min(len(lyrics), idx_atual + LINHAS_DE_CONTEXTO + 1)
                
                padding = max(0, LINHAS_DE_CONTEXTO - idx_atual)
                print("\n" * padding)

                for i in range(inicio, fim):
                    txt = lyrics[i][1].center(LARGURA_TERMINAL)
                    
                    if i == idx_atual:
                        print(f"{COR_DESTAQUE}--> {txt} <--{RESET_COR}") # Destaque
                    elif i < idx_atual:
                        print(f"{COR_PASSADA}{txt}{RESET_COR}")          # Já cantado
                    else:
                        print(f"{COR_FUTURA}{txt}{RESET_COR}")           # Vai cantar
            
            time.sleep(0.05)

    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        print("\nMúsica interrompida pelo usuário.")
        time.sleep(1)
    
    pygame.mixer.quit()

def main():
    while True:
        # 1. Lista opções
        opcoes = listar_opcoes_validas()
        
        # 2. Menu de seleção
        escolha = menu_escolha(opcoes)
        
        # 3. Execução ou Saída
        if escolha:
            tocar_karaoke(escolha)
        else:
            print("\nEncerrando o Python Karaoke. Até mais!")
            break

if __name__ == "__main__":
    main()