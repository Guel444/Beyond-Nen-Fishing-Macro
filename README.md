# Beyond Nen Fishing Macro

<p align="center">
  <strong>Pesca automática para Beyond Nen (Roblox)</strong><br>
  Configure uma vez, deixe o Roblox em primeiro plano e controle a automação pelo teclado.
</p>

<p align="center">
  <a href="https://github.com/Guel444/Beyond-Nen-Fishing-Macro/releases/latest">
    <img src="https://img.shields.io/badge/⬇%20BAIXAR%20PARA%20WINDOWS-Release%20mais%20recente-2ea44f?style=for-the-badge" alt="Baixar a versão mais recente para Windows">
  </a>
</p>

<p align="center">
  <a href="#-comece-por-aqui">Começar</a> ·
  <a href="#-como-usar">Como usar</a> ·
  <a href="#-controles">Controles</a> ·
  <a href="#-solução-de-problemas">Ajuda</a> ·
  <a href="#english">English</a>
</p>

---

## 🇧🇷 Português

### 🎣 O que é?

O **Beyond Nen Fishing Macro** automatiza a pesca no minigame de Beyond Nen, dentro do Roblox. Ele identifica o alvo laranja e o marcador branco, controla o mouse e oferece uma prévia da tela em tempo real.

<blockquote>
  <strong>Este projeto é para Windows 10/11 de 64 bits.</strong><br>
  Para a maioria das pessoas, basta baixar o programa pronto. Não é necessário instalar Python.
</blockquote>

### 🚀 Comece por aqui

1. Clique no botão verde **BAIXAR PARA WINDOWS** no início desta página.
2. Na página que abrir, encontre a seção **Assets** e baixe <code>Beyond-Nen-Fishing-Windows.zip</code>.
3. Quando o download terminar, clique com o botão direito no ZIP e escolha **Extrair tudo...**.
4. Abra a pasta extraída e execute <code>BeyondNenFishing.exe</code>.
5. Abra o Beyond Nen no Roblox e mantenha a janela do Roblox em primeiro plano.
6. No macro, pressione **F6** para iniciar.

<p align="center">
  <a href="https://github.com/Guel444/Beyond-Nen-Fishing-Macro/releases/latest">
    <img src="https://img.shields.io/badge/CLIQUE%20AQUI%20PARA%20BAIXAR-⬇%20Beyond%20Nen%20Fishing-238636?style=for-the-badge" alt="Ir para o download">
  </a>
</p>

**Importante:** na página de Releases, baixe o arquivo <code>Beyond-Nen-Fishing-Windows.zip</code> que aparece em **Assets**. Os arquivos chamados **Source code** são apenas o código-fonte e não são o programa pronto.

### 📦 O que vem no ZIP?

- **BeyondNenFishing.exe** — o aplicativo. É só abrir para executar.
- **LEIA-ME.txt** — instruções rápidas de instalação, uso e atalhos. Ele fica junto do executável para você poder consultar mesmo sem internet.

### ✨ Recursos

- Pesca automática em loop.
- Prévia da tela em tempo real, inclusive enquanto a automação está pausada.
- Detecção do marcador branco e do alvo laranja móvel.
- Controle automático do mouse para manter o marcador sobre o alvo.
- Seleção manual da região do minigame na tela.
- Restauração da região padrão.
- Escolha do slot da vara (teclas 1 a 9).
- Tentativas de recuperação automática quando o minigame não aparece ou ocorre uma falha.

### 🎮 Como usar

1. Equipe a vara no slot configurado no aplicativo.
2. Abra o Beyond Nen e deixe o Roblox visível, em primeiro plano.
3. Se necessário, ajuste a região de detecção para incluir a barra do minigame.
4. Pressione **F6** para iniciar ou pausar a pesca.
5. Para encerrar completamente, pressione **F7**.

### ⌨️ Controles

| Tecla | Ação |
| --- | --- |
| **F6** | Iniciar ou pausar a pesca automática |
| **F7** | Parar a automação e soltar o botão do mouse |
| **F8** | Mostrar ou ocultar a prévia da tela |

Os mesmos comandos também podem ser usados pelos botões da interface.

### ⚙️ Configurações

- **Slot da vara:** selecione o número (1 a 9) correspondente ao slot em que a vara está equipada. Esse slot também é usado nas tentativas de recuperação automática.
- **Selecionar área na tela:** pause a automação e arraste um retângulo ao redor da barra do minigame para definir a região analisada.
- **Restaurar área padrão:** retorna à região inicial configurada no aplicativo.

### 🛠️ Solução de problemas

- **O macro não detecta o minigame:** confira se a região selecionada inclui toda a barra do minigame e se os elementos estão visíveis.
- **O macro não controla o jogo:** confirme que o Roblox está aberto e em primeiro plano.
- **O Windows exibiu o SmartScreen:** executáveis sem assinatura digital podem receber esse aviso. Confira se baixou o ZIP desta página e, se necessário, verifique o arquivo com o Microsoft Defender. Não desative o antivírus.
- **Ainda precisa de ajuda?** Abra uma [Issue no GitHub](https://github.com/Guel444/Beyond-Nen-Fishing-Macro/issues) e descreva o problema. Se possível, inclua uma captura de tela.

### 🔒 Segurança e requisitos

- Windows 10 ou Windows 11, 64 bits.
- Python não é necessário para a versão pronta.
- O Roblox precisa permanecer em primeiro plano durante a automação.
- Baixe o programa somente pela [página oficial de Releases](https://github.com/Guel444/Beyond-Nen-Fishing-Macro/releases/latest).

### 👨‍💻 Para desenvolvedores

O código-fonte e os arquivos para executar ou compilar o projeto manualmente estão disponíveis neste repositório. Para executar a versão Python, instale Python 3 e as dependências listadas em <code>requirements.txt</code>. Depois, execute:

```bat
py -m pip install -r requirements.txt
py beyond_nen_app.py
```

Para gerar um executável, use <code>Gerar_EXE.bat</code> ou o fluxo de build do GitHub Actions.

---

## English

<details>
<summary>Click to expand the English guide</summary>

### What is it?

**Beyond Nen Fishing Macro** automates the fishing minigame in Beyond Nen (Roblox). It detects the moving orange target and white marker, controls the mouse, and provides a live screen preview.

**Windows 10/11 (64-bit).** The ready-to-run version does not require Python.

### Download and run

1. Click the green **DOWNLOAD FOR WINDOWS** button at the top of this page.
2. On the Releases page, find **Assets** and download <code>Beyond-Nen-Fishing-Windows.zip</code>.
3. Right-click the ZIP and select **Extract All...**.
4. Open the extracted folder and run <code>BeyondNenFishing.exe</code>.
5. Open Beyond Nen in Roblox and keep the Roblox window in the foreground.
6. Press **F6** to start.

**Note:** Download <code>Beyond-Nen-Fishing-Windows.zip</code> under **Assets**. GitHub's **Source code** archives contain source files, not the ready-to-run application.

### What's included?

- **BeyondNenFishing.exe** — the application.
- **LEIA-ME.txt** — a quick-start guide included in the ZIP for offline reference.

### Features

- Automatic fishing loop and live screen preview.
- Detection of the moving white marker and orange target.
- Automatic mouse control.
- Manual minigame region selection and default-region restore.
- Fishing rod hotbar slot selection (1–9).
- Automatic recovery attempts.

### Controls

| Key | Action |
| --- | --- |
| **F6** | Start or pause fishing |
| **F7** | Stop the macro and release the mouse button |
| **F8** | Show or hide the live preview |

Roblox must remain in the foreground while the macro is running.

### Troubleshooting

- If the minigame is not detected, check the selected detection region.
- If inputs are not reaching the game, keep the Roblox window in the foreground.
- Unsigned PyInstaller executables may trigger Windows SmartScreen. Verify the download and scan it with Microsoft Defender if needed. Do not disable antivirus protection.
- For help, [open a GitHub Issue](https://github.com/Guel444/Beyond-Nen-Fishing-Macro/issues).

</details>

---

<p align="center">
  <sub>Beyond Nen Fishing Macro · Windows 10/11 · <a href="https://github.com/Guel444/Beyond-Nen-Fishing-Macro/releases/latest">Download latest release</a></sub>
</p>
