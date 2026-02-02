# 🎤 PyKaraoke

> **Um player de karaokê via terminal feito em Python para fins de estudo e diversão!**

O **PyKaraoke** é um projeto simples que permite cantar suas músicas favoritas acompanhando a letra sincronizada diretamente no seu terminal/console. Ele foi desenvolvido para explorar manipulação de arquivos de áudio com `pygame`, processamento de texto (Regex) e formatação de saída CLI (Command Line Interface).

## 📋 Funcionalidades

* 🎵 **Reprodução de Áudio:** Toca arquivos `.mp3` utilizando a biblioteca `pygame`.
* 📝 **Letras Sincronizadas:** Lê arquivos padrão `.lrc` (LRC format) para sincronizar o texto com o áudio.
* 🎨 **Interface Colorida:** Destaque visual no terminal para a linha atual, linhas passadas e futuras.
* 🔄 **Menu Interativo:** Lista automaticamente as músicas disponíveis na pasta do projeto.
* 🛠 **Tratamento de Codificação:** Suporte para diferentes codificações de texto (UTF-8, Latin-1, etc.) para evitar erros de acentuação nas letras.

## 🚀 Como Usar

### Pré-requisitos

Você precisará do [Python](https://www.python.org/) instalado e da biblioteca `pygame`.

1. **Clone o repositório:**
```bash
git clone https://github.com/danieldpereira/pykaraoke.git
cd pykaraoke

```


2. **Instale as dependências:**
```bash
pip install pygame

```


3. **Execute o projeto:**
```bash
python karaoke.py

```



## 📂 Como Adicionar Músicas

O sistema escaneia automaticamente a pasta `musicas/`. Para adicionar uma nova faixa, você deve seguir estritamente esta regra:

1. Coloque o arquivo de áudio (`.mp3`) dentro da pasta `musicas`.
2. Coloque o arquivo de letra (`.lrc`) dentro da mesma pasta.
3. **Importante:** Ambos os arquivos devem ter **exatamente o mesmo nome** (exceto a extensão).

**Exemplo de estrutura correta:**

```text
pykaraoke/
├── karaoke.py
└── musicas/
    ├── Aliança-Tribalistas.mp3
    └── Aliança-Tribalistas.lrc

```

> **Dica:** Você pode encontrar arquivos `.lrc` pesquisando na internet ou criar os seus próprios com editores de LRC.

## 🛠 Tecnologias Utilizadas

* **Python 3**
* **Pygame Mixer:** Para carregamento e controle do áudio.
* **OS & Re (Regex):** Para navegação no sistema de arquivos e parsing das timestamps das letras `[00:00.00]`.

## 📸 Exemplo de Funcionamento

Ao rodar o programa, você verá um menu assim:

```text
=== PYTHON KARAOKE ===
Músicas encontradas na pasta 'musicas':

[1] Aliança-Tribalistas
[2] Balada-Gusttavo Lima
[3] Chuva de arroz-Luan Santana

[0] Sair
------------------------------
Digite o número da música: 

```

Durante a música, o terminal exibirá:

```text
       (linhas anteriores em cinza)
--> LINHA ATUAL CANTADA EM AMARELO <--
       (próximas linhas em branco)

```

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.

---

Feito com 🐍 e 🎵 por **Daniel Dias Pereira**.
