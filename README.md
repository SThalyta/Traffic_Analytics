### Projeto contador de veículos

A ideia inicial era realizar a contagem dos veículos selecionando uma área (poligon_zone) e depois disso linhas (line_zone) para assim contar os veículos que entraram e saíram da cidade (área do vídeo).

##### 1 - Por que delimitar zonas?

O modelo vai identificar objetos no frame inteiro, mas uns vão estar perto e outros longe da câmera. Quando formos realizar o tracking, pode ser que esses frames pisquem devido a baixa resolução e detectem os objetos de forma intermitente, e induza o modelo a atribuir um novo ID para o mesmo objeto, dificultando assim um rastreamento preciso. Logo, ao definirmos uma zona, vamos trabalhar apenas com os objetos dentro dela, isso reduz o número de falsas detecções.

#### Problema inicial (app.py)

Eu tive algumas complicações na contagem porque o centro do objeto precisa passar pela linha para que o objeto possa ser contado e, devido ao ângulo do vídeo, isso seria mais preciso se a zona selecionada estivesse mais longe da câmera para que a linha fosse melhor posicionada, mas, quanto mais longe da câmera, mais difícil é para o modelo reconhecer os veículos individualmente, então eu tive que traçar outra estratégia de contagem.

#### Solução (app_3.py)

Quando você realiza o tracking, cada objeto recebe um ID único, então a solução encontrada foi delimitar duas zonas(uma para os veículos que entram e uma para os que saem) e criar duas tuplas para armazenar os IDs únicos nas zonas. Ou seja, quando o modelo identifica um objeto, ele o mapeia, atribui um ID e esse ID é adicionado em uma tupla e o contador é incrementado, caso o ID já exista, ele é ignorado e caso não, o contador é incrementado e assim sucessivamente.

### Explicação do código

Eu gostaria de iniciar a explicação pelo nosso main principal. Durante as pesquisas eu descobri a biblioteca argparse, ela é muito útil principalmente por dois pontos:
1. *Automatização e usabilidade*: Torna o uso do script mais intuitivo e reduz erros por parte do usuário ao documentar e validar os argumentos.

2. *Flexibilidade*: Permite lidar com arquivos em locais diversos, não limitando o programa ao diretório onde está sendo executado. Isso é bastante útil porque reduz os erros com as sintaxes de diferentes sistemas operacionais.

Primeiro criamos um objeto ArgumentParser da biblioteca argparse, que será usado para definir e interpretar os argumentos da linha de comando.
```bash
parser = argparse.ArgumentParser()
```
Depois adicionamos um argumento iniciando com dois hífens, isso é usado para criar argumentos nomeados que ajudam a instruir o usuário sobre o que passar na linha de comando:
```bash
parser.add_argument("--video_file_path", required= True, help='Caminho para o arquivo')
```
Nós poderíamos executar tanto com:
```bash
python app_3.py "caminho_do_arquivo"
```
Quanto com:
```bash
python app_3.py --video_file_path "caminho_do_arquivo"
```
Mas nesse caso com a flag required=True, eu indico que é o argumento é obrigatório, logo a execução precisa ser com: 

python app_3.py --video_file_path "caminho_do_arquivo"

Isso é muito útil por alguns pontos:

1. *Clareza*: Fica mais fácil para o usuário saber o que o script espera.

2. *Flexibilidade*: Os argumentos podem ser opcionais ou obrigatórios, dependendo da configuração.

3. *Escalabilidade*: Para scripts mais complexos com vários argumentos, os nomes dos parâmetros tornam o uso mais intuitivo.

Podemos ter tantos argumentos opcionais quanto obrigatórios. Opcional é quando eu defino um valor padrão no código e posso mudar na linha de comando, por exemplo, caso eu quisesse configurar a taxa de frames por segundos (fps):
```bash
parser.add_argument("--fps", default=30, type=int, help="Taxa de quadros (padrão: 30)")
```
Já um argumento obrigatório é quando eu necessariamente preciso passar na linha de comando para o código funcionar, como é o caso do caminho do arquivo.

Em seguida o método parse_args() analisa os argumentos fornecidos na linha de comando e os organiza em um objeto chamado args. Esse objeto é como um contêiner que contém os valores dos argumentos:
```bash
args = parser.parse_args()
```
Depois esses valores são passados para função process com:
```bash
process(args.video_file_path)
```
Se eu tivesse mais de um argumento, independente de ser obrigatório ou opcional, eu alteraria a função process:
```bash
process(video_file_path, fps)
```
E chamaria no main: 
```bash
process(args.video_file_path, args.fps)
```
O primeiro passo é delimitar as zonas, para isso eu utilizei o site makesense.ai. Antes disso vamos rodar o código step_1.py para reproduzir o vídeo e salvar o primeiro frame (imagem) para conseguirmos desenhar a zona no site e obter as coordenadas.

Para entender melhor o porquê da delimitação das zonas, vamos reproduzir o arquivo step_2.py. Vemos que as caixas delimitadoras piscam em torno de alguns objetos, identicando, perdendo o objeto "de vista" e identifica novamente, quanto mais longe da câmera, mais isso acontece. Exatamente por isso que precisamos definir uma zona para identificarmos os objetos quando eles estiverem nela.

Definição das zonas: step_3.py

Identificação dos objetos na zona: step_4.py

Lógica de contagem: app_3.py

## Como rodar?

1. Criar ambiente virtual e ativar:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
.\venv\Scripts\activate    # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Executar o código principal:
```bash
python app_3.py --video_file_path "caminho/do/video.mp4"
```

