IA VS RPG
Disciplina: Introdução à Inteligência Artificial
Semestre: 2025.2
Professor: Andre Luis Fonseca Faustino
Turma: T03

Integrantes do Grupo
Maria Luiza de Araujo (20250032627)
Pedro Henrique Estevam Elias (20250035315)

Descrição do Projeto
O ambiente do projeto é um RPG de turnos em formato de torre, no qual o objetivo é derrotar sucessivos monstros até alcançar o topo. Em vez de um jogador humano, o controle do personagem é assumido por um agente de Inteligência Artificial, que deve aprender a tomar decisões como atacar, defender ou utilizar recursos de forma estratégica para vencer os desafios de maneira cada vez mais eficiente.
O aprendizado da IA será baseado em Aprendizado por Reforço (Reinforcement Learning). A cada partida, o agente recebe uma pontuação (recompensa) que varia de acordo com seu desempenho: a pontuação aumenta em situações de vitória, menor tempo para concluir a torre e maior dano causado aos inimigos, e diminui em casos de derrota, maior número de turnos até a vitória e alto dano sofrido. Ao longo de várias simulações, a IA ajusta suas decisões com base nessas recompensas, buscando estratégias que maximizem sua eficiência e reduzam o tempo necessário para completar o jogo. O projeto será desenvolvido em Python, utilizando estruturas de dados e, potencialmente, bibliotecas de apoio para análise e visualização dos resultados.

Guia de Instalação e Execução
    1 - Certifique-se de ter o Python 3.x instalado. Clone o repositório e instale as bibliotecas necessárias.

    2 - O projeto depende principalmente de pandas e numpy para o processamento de dados e exportação dos resultados do treinamento, e openpyxl para gerar os arquivos Excel.

    3 - Instalação das Dependências
        3.1 - Certifique-se de ter o Python 3.x instalado. Clone o repositório e instale as bibliotecas listadas no requirements.txt;
        3.2 - Em seguida, execute os comandos no terminal:
            # Clone o repositório
                git clone https://github.com/Kelly-0W/IA.git

            # Entre na pasta do projeto
                cd IA

            # Instale as dependências
                pip install -r requirements.txt

    4 - Como Executar
        O projeto possui dois modos de execução: o treinamento da IA e o modo de jogo manual (para teste humano).
            Para treinar o Agente (Modo Principal): Execute o script da IA para iniciar o processo de aprendizado por reforço. O script treinará o agente "Guerreiro" e o agente "Mago" sequencialmente e salvará os resultados em planilhas Excel.
                python IA_agente.py

            Para jogar manualmente (Modo Humano): Caso queira testar a mecânica do jogo pessoalmente:
                python jogo.py

Estrutura dos Arquivos

IA_agente.py: Código principal da Inteligência Artificial. Contém a implementação do algoritmo Q-Learning (AgenteSimples), o ambiente de simulação (AmbienteSimples) e o loop de treinamento.

classes.py: Define as classes bases do jogo (Heroi, Inimigo), lógica de combate, geração de inimigos e uso de itens.

jogo.py: Script para execução do jogo em modo manual (humano), incluindo menus interativos e sistema de salvamento de recordes (records.txt).

dicionarios.json: "Banco de dados" do jogo. Contém as estatísticas base dos Heróis, lista de Monstros (com atributos e elementos) e Itens disponíveis.

qlearning_[classe]_[data].xlsx: Arquivos de saída gerados após a execução do IA_agente.py, contendo as métricas de desempenho de cada episódio de treinamento.

Resultados e Demonstração
Terminal da aplicação em execução:
![Terminal da aplicaçao](<Terminal -1.jpg>)

Referências

Ambiente de Dados: O dataset é gerado dinamicamente a partir do arquivo dicionarios.json incluído no projeto.

Metodologia: Implementação baseada em Reinforcement Learning: An Introduction (Sutton & Barto), utilizando a abordagem Q-Learning Tabular com estratégia de exploração Epsilon-Greedy.