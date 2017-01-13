# Trabalho de Avaliação de Desempenho de 2016-2

## Rodando uma simulação
Para rodar uma simulação é necessário saber qual das políticas de fila será utilizada e qual o arquivo de amostras deverá ser usado.
O simulador está preparado para as seguintes políticas:

  1. FCFS - FCFS sem distinção de classes (fila unica)
  2. LCFS - LCFS sem preempção e sem distinção de classes (fila unica)
  3. PreemptiveLCFS - LCFS com preempção e sem distinção de classes (fila unica)
  4. PreemptiveFCFS - FCFS sem preempção e com classe 1 com prioridade sobre classe 2
  5. FCFSWithPriority - FCFS com preempção e com classe 1 com prioridade sobre classe 2
  
Um exemplo de execução:
``` sh
$ python main.py FCFS arrivals/arrivals-2.0_5.0_2.0_5.0_100
```

## Gerando amostras
Para gerar uma amostra basta seguir o padrao:
``` sh
python arrivals-generator.py <lambda1> <mu1> <lambda2> <mu2> <tempo_maximo>
```
As amostras são guardadas por default no diretório arrivals

## Plotando os gráficos
Para plotar os gráficos basta executar o programa plot.py informando a política de escalonamento e o diretório onde se encontram os arquivos das amostras.
O programa simulará a fila uma vez para cada arquivo no diretório passado.

Exemplo:
``` sh
$ python plot.py FCFS arrivals/lambda_variation/
```
