# COGNUS - Certidão de CNPJ

Automação para consultar e emitir certidões de CNPJ no portal de serviços da Receita Federal. A aplicação possui uma interface web feita com Streamlit, lê uma lista de CNPJs em uma planilha Excel e usa automação visual para preencher as consultas no navegador.

Ao final do processamento, os novos arquivos PDF encontrados em `Downloads` são reunidos em uma pasta com data e hora na Área de Trabalho.

## Como funciona

1. O usuário envia uma planilha Excel pela interface.
2. A aplicação lê os valores da coluna `CNPJ`.
3. O usuário abre o portal de certidões da Receita Federal.
4. Ao clicar em **Iniciar**, a automação localiza os elementos da página pelas imagens em `assets/`.
5. Cada CNPJ é consultado e a certidão é baixada pelo navegador.
6. Os PDFs novos são movidos de `Downloads` para uma pasta `Certidoes_CNPJ_AAAA-MM-DD_HH-MM-SS` na Área de Trabalho.

## Requisitos

- Windows
- Python 3.10 ou superior
- Navegador compatível com o portal da Receita Federal
- Conexão com a internet
- Permissão para controlar mouse e teclado e para acessar `Downloads`
- Resolução, escala e zoom do navegador compatíveis com as imagens de referência em `assets/`

Como a automação usa reconhecimento de imagem e controla a interface gráfica, o computador deve permanecer desbloqueado e o navegador não pode ser coberto ou redimensionado de maneira incompatível durante a execução.

## Instalação

Abra o terminal na pasta do projeto e crie um ambiente virtual:

```powershell
python -m venv venv
venv\Scripts\activate
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

## Uso

1. Inicie a aplicação:

   ```powershell
   streamlit run app.py
   ```

2. Abra o endereço local exibido pelo Streamlit, normalmente `http://localhost:8501`.
3. Prepare uma planilha `.xlsx` ou `.xls` com uma coluna chamada `CNPJ`.
4. Envie a planilha no campo lateral da aplicação.
5. Abra o link **Certidões** exibido na tela e deixe a página visível.
6. Clique em **Iniciar** e aguarde o processamento terminar.
7. Confira a pasta de saída indicada pela aplicação na Área de Trabalho.

### Modelo da planilha

A primeira linha deve conter o cabeçalho `CNPJ`:

| CNPJ |
| --- |
| 00.000.000/0001-00 |
| 11.111.111/0001-11 |

O nome da coluna é obrigatório e diferencia maiúsculas de minúsculas. Remova linhas vazias ou valores que não sejam CNPJs válidos antes de iniciar.

## Estrutura do projeto

```text
.
├── app.py                    # Interface Streamlit e fluxo da automação
├── path.py                   # Organização dos PDFs baixados
├── requirements.txt          # Dependências Python
├── assets/                   # Imagens usadas no reconhecimento da página
└── read_cnpj/
	├── read_cnpj.py          # Leitura da coluna CNPJ do Excel
	└── teste.py              # Exemplo simples de leitura
```

## Saída dos arquivos

Antes de iniciar, a aplicação registra quais PDFs já existem em `Downloads`. Depois da execução, somente os PDFs novos são movidos para uma pasta criada na Área de Trabalho. A mensagem exibida informa:

- a quantidade de certidões encontradas;
- a quantidade esperada;
- o caminho da pasta de saída.

Não deixe outros PDFs sendo baixados ao mesmo tempo, pois eles podem ser considerados arquivos novos da execução atual.

## Solução de problemas

### A aplicação não encontra um elemento da página

Verifique se:

- o navegador está aberto na página correta;
- a janela está visível e em primeiro plano;
- o zoom está em `100%`;
- a escala do Windows e a resolução são compatíveis com as imagens em `assets/`;
- os arquivos de imagem não foram renomeados ou removidos.

A aplicação encerra a tentativa quando não encontra um elemento durante o limite de tempo configurado.

### A planilha não é carregada

Confirme se o arquivo tem extensão `.xlsx` ou `.xls` e se existe uma coluna chamada exatamente `CNPJ`.

### A quantidade de PDFs está diferente da esperada

Confira se o portal concluiu cada consulta e se todos os downloads terminaram. A aplicação conta apenas os PDFs novos presentes em `Downloads` no momento da organização.

## Observações importantes

- Esta automação depende do layout visual atual do portal da Receita Federal. Mudanças na página podem exigir a atualização das imagens em `assets/`.
- Use a ferramenta de acordo com as regras e os limites aplicáveis ao portal da Receita Federal.
- Não mova o mouse, digite ou interaja com o navegador enquanto a automação estiver em execução.
- Proteja as planilhas e as certidões geradas, pois elas podem conter dados empresariais.

## Tecnologias

- Python
- Streamlit
- Pandas e OpenPyXL
- PyAutoGUI
- Pyperclip
- OpenCV e Pillow

## Objetivo Próximo

- Substituir implementação pyautogui por selenium ou playwright.
- Integrar com airflow para agendar e automatizar a execução da automação.
- Utilizar Fargate da AWS para que a automação funcione independente do usuario.

### A partir desses objetivos, essa automação irá rodar independentemente de alguém abri-la ou não recorrentemente. Assim, as certidões sempre serão geradas de forma automatica.