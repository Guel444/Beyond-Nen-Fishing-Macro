# Beyond Nen Fishing Macro

Aplicativo de pesca automática para **Beyond Nen (Roblox)**, com prévia da tela em tempo real e controles para iniciar, pausar e interromper a automação.

> Projeto para Windows 10/11. O Roblox precisa estar aberto e em primeiro plano durante a pesca automática.

## Recursos

- Pesca automática em loop.
- Prévia da captura de tela em tempo real, inclusive enquanto a farm está pausada.
- Detecção do marcador branco e do alvo laranja móvel do minigame.
- Controle automático do clique para manter o marcador sobre o alvo.
- Seleção da região do minigame diretamente na tela.
- Restauração da região padrão.
- Escolha do slot da vara (1 a 9).
- Tentativas de recuperação automática quando o minigame não aparece ou ocorre uma falha.

## Requisitos

- Windows 10 ou Windows 11.
- Python 3 instalado e disponível pelo comando `py`.
- Beyond Nen aberto no Roblox.

## Instalação e execução

1. Baixe o repositório pelo botão **Code → Download ZIP** e extraia a pasta.
2. Execute `Instalar_e_abrir.bat`.
3. Aguarde a instalação das dependências.
4. Com o Roblox aberto, deixe a janela do Roblox em primeiro plano.
5. Use o botão **Iniciar / pausar** ou pressione **F6**.

Também é possível instalar manualmente as dependências e executar o aplicativo:

```bat
py -m pip install opencv-python mss numpy pyautogui keyboard pillow
py beyond_nen_app.py
```

## Controles

| Tecla | Ação |
| --- | --- |
| **F6** | Iniciar ou pausar a pesca automática |
| **F7** | Parar a automação e soltar o botão do mouse |
| **F8** | Mostrar ou ocultar a prévia |

Os mesmos comandos estão disponíveis pelos botões da interface.

## Configurações

- **Slot da vara:** escolha o número da tecla (1 a 9) correspondente ao slot em que a vara está equipada. Esse slot é usado também nas tentativas de recuperação automática.
- **Selecionar área na tela:** com a automação pausada, arraste um retângulo ao redor da barra do minigame para definir a região analisada.
- **Restaurar área padrão:** retorna à região inicial configurada no aplicativo.

## Gerar um executável

Execute `Gerar_EXE.bat`. O script instala o PyInstaller e tenta gerar o arquivo `BeyondNenFishing.exe) na pasta `dist`.

## Observações

- A detecção depende da posição e das cores dos elementos do minigame. Se necessário, ajuste a área analisada.
- O Roblox precisa estar em primeiro plano para que os comandos de pesca sejam enviados.
- Este repositório contém o código-fonte e scripts de execução; não inclui um executável pronto.
- A execução foi verificada quanto à sintaxe do Python. Isso não equivale a um teste completo dentro do Roblox.

