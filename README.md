[Nome do Projeto]
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
[Descreva os passos para instalacao e execucao do projeto. Inclua um passo-a-passo claro de como utilizar a proposta desenvolvida. Veja o exemplo abaixo.]

1. Instalação das Dependências
Certifique-se de ter o Python 3.x instalado. Clone o repositório e instale as bibliotecas listadas no requirements.txt:

# Clone o repositório
git clone [https://github.com/Kelly-0W/IA.git](https://github.com/Kelly-0W/IA)

# Entre na pasta do projeto
cd nome-do-repo

# Instale as dependências
pip install -r requirements.txt
2. Como Executar
Execute o comando abaixo no terminal para iniciar o servidor local:

# Exemplo para Streamlit
streamlit run src/app.py
Se necessário, especifique a porta ou url de acesso, ex: http://localhost:8501

Estrutura dos Arquivos
[Descreva brevemente a organização das pastas]

src/: Código-fonte da aplicação ou scripts de processamento.
notebooks/: Análises exploratórias, testes e prototipagem.
data/: Datasets utilizados (se o tamanho permitir o upload).
assets/: Imagens, logos ou gráficos de resultados.
Resultados e Demonstração
[Adicione prints da aplicação em execução ou gráficos com os resultados do modelo/agente. Se for uma aplicação Web, coloque um print da interface.]

Referências
[Link para o Dataset original]
[Artigo, Documentação ou Tutorial utilizado como base]