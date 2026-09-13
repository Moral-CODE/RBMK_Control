RBMK Control

Sobre o projeto:

RBMK Control é um jogo desenvolvido em Python como projeto escolar.
O jogador assume o papel de operador de um reator nuclear RBMK-1000 e precisa interromper um cronômetro o mais próximo possível de um tempo-alvo aleatório.
O objetivo é testar precisão, atenção e tempo de reação.

Como o jogo funciona:

Ao iniciar o jogo, o sistema passa por uma sequência de inicialização e apresenta uma situação de emergência no reator.
Depois disso, uma rodada começa com um tempo-alvo aleatório.

Exemplo:

ALVO: 3.5 SEG
O cronômetro começa a contar e o jogador precisa pressionar ESPAÇO para pará-lo.
O resultado depende da diferença entre o tempo desejado e o tempo em que o jogador parou o cronômetro.

Resultado:

Se a diferença for de até 0,15 segundo, o jogador acerta.
Se a diferença for de até 0,03 segundo, o resultado é considerado um:

"CRAVADO"

Caso o jogador erre, o reator entra em falha e ocorre a sequência de explosão e morte.

Controles:

Tecla	Função
ENTER	Inicializa o sistema
ESPAÇO	Inicia o cronômetro
ESPAÇO	Para o cronômetro
ENTER	Reinicia após o resultado/morte

Sistema de HUD:

Durante a partida, o HUD apresenta informações simuladas do reator:

Temperatura do núcleo;
Nível de radiação;
Saída de potência;
Sistema de resfriamento;
Estado do núcleo;
Estado do sistema de controle;
Tempo atual;
Tempo-alvo;
Estatísticas do jogador;

Os indicadores mudam de acordo com o progresso da rodada.

O sistema utiliza diferentes estados visuais:

Verde — sistema estável
Amarelo — aviso/instabilidade
Vermelho — condição crítica

Sistema de resultados:

O jogo registra estatísticas durante a execução.

São contabilizados:

Número de tentativas;
Número de acertos;
Número de erros;
Precisão;
Número de resultados cravados;

Um resultado perfeito também gera uma animação especial com:

WOW - CRAVOU 🥇

e efeitos de confete.

Sistema de morte:

Quando o jogador erra uma rodada, o reator entra em estado crítico.

O jogo apresenta:

Falha do reator;
Explosão;
Tela de morte;
Mensagem:
ERROR - VOCÊ MORREU ☠️

A tela de morte possui efeito visual de transparência e permite tentar novamente pressionando ENTER.

Banco de dados:

O jogo utiliza SQLite para armazenar os resultados das partidas.
O banco de dados é criado automaticamente pelo sistema e possui o arquivo:

"rbmk.db"

A tabela principal utilizada pelo jogo é:

"partidas"

Dados armazenados;

Cada partida registra:

Campo	Tipo	Descrição
id	INTEGER	Identificador da partida
hora_teste	TEXT	Horário em que a partida foi realizada
tempo_alvo	REAL	Tempo-alvo escolhido pelo jogo
tempo_jogador	REAL	Tempo em que o jogador parou o cronômetro
acertou	INTEGER	Indica se o jogador acertou
cravado	INTEGER	Indica se o resultado foi perfeito

No SQLite, os valores booleanos são armazenados como:

1 = verdadeiro
0 = falso
Exemplo de registro

Uma partida pode ser armazenada aproximadamente assim:

ID: 15
Hora: 14:32:07
Tempo-alvo: 3.5
Tempo do jogador: 3.48
Acertou: 1
Cravado: 1

Isso significa que o jogador parou o cronômetro em aproximadamente 3,48 segundos, com alvo de 3,50 segundos, obtendo um resultado perfeito.

Consultas SQL:

Como os resultados são armazenados em SQLite, é possível consultar o histórico diretamente utilizando SQL.

Mostrar todas as partidas
SELECT * FROM partidas;
Mostrar apenas partidas acertadas
SELECT *
FROM partidas
WHERE acertou = 1;
Mostrar apenas os cravados
SELECT *
FROM partidas
WHERE cravado = 1;
Mostrar horário, alvo e tempo do jogador
SELECT
    hora_teste,
    tempo_alvo,
    tempo_jogador
FROM partidas;
Contar quantas partidas foram realizadas
SELECT COUNT(*) AS total_partidas
FROM partidas;
Contar quantos acertos foram realizados
SELECT COUNT(*) AS total_acertos
FROM partidas
WHERE acertou = 1;
Estrutura do projeto

Os principais arquivos do projeto são:

RBMK_Control/
│
├── main.py
├── interface.py
├── jogo.py
├── banco.py
├── efeitos.py
└── rbmk.db
main.py

É o ponto de entrada do programa.

Responsável por iniciar a aplicação e criar a interface principal.

interface.py

Contém a interface gráfica do jogo.

É responsável por:

HUD
Cronômetro
Controles
Alertas
Animações
Tela de morte
Tela de resultado
Confetes
Estatísticas
Interação com o jogador
jogo.py

Contém a lógica principal da partida.

É responsável por:

Gerar o tempo-alvo
Iniciar o cronômetro
Calcular o tempo decorrido
Calcular a diferença entre o alvo e o resultado
Determinar se o jogador acertou
banco.py

Responsável pelo banco de dados.

Contém as funções utilizadas para:

Conectar ao SQLite
Criar a tabela
Salvar os resultados das partidas
Armazenar o histórico dos testes
efeitos.py

Contém os efeitos visuais utilizados durante eventos do jogo, principalmente os efeitos relacionados à explosão e falha do reator.

rbmk.db

É o banco de dados SQLite do projeto.

Ele contém o histórico das partidas realizadas.

Não é necessário editar esse arquivo manualmente.

As informações são inseridas pelo próprio jogo.

Tecnologias utilizadas:

Python
PySide6 — interface gráfica
SQLite — armazenamento dos resultados
SQL — consulta dos dados
random — geração dos tempos-alvo
time — controle preciso do cronômetro
Como executar

Com Python instalado, abra o terminal na pasta do projeto:

RBMK_Control

Execute:

python main.py

O jogo será iniciado em uma janela maximizada.

Objetivo do projeto

O projeto foi desenvolvido com finalidade escolar para demonstrar conceitos de:

Programação em Python
Interface gráfica
Eventos de teclado
Manipulação de tempo
Estruturação de programas
Banco de dados
SQL
Armazenamento de informações
Animações e efeitos visuais
Status

Projeto concluído.

O sistema possui:

Jogo funcional
Cronômetro de precisão
Tempos-alvo aleatórios
Sistema de acerto e erro
Sistema de resultado perfeito
HUD dinâmico
Alertas
Explosão
Tela de morte
Efeitos de confete
Estatísticas
Banco de dados SQLite
Registro das partidas
Consultas SQL

Autor:

Moral

Projeto desenvolvido para fins escolares.

RBMK Control — Unidade 4
