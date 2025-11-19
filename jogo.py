import random as rd
import time
from classes import Heroi, Inimigo, Gerar_inimigo, combate_guerreiro, combate_inimigo, combate_mago, herois
heroi = Heroi()
inimigo = Inimigo()
gerador = Gerar_inimigo()

andar = 1

começo = time.time()
print("=== Bem-vindo ===\n"
      "Escolha a sua classe:")
heroi.escolher_classe(herois)

while True:
    inimigo = gerador.escolher_inimigo(andar)

    if andar == 4 and inimigo is not None:
        print("Você chegou no último salão, o desafio mais difícil da sua jornada está por vir, prepare-se.")
    
    elif andar > 4:
        print("Você chegou no final de sua aventura bravo herói, pode descansar em paz, o mundo está salvo.")
        break

    if inimigo:
        inimigo_combate = combate_inimigo(heroi, inimigo, inimigo.vida, inimigo.elemento, inimigo.ataque, inimigo.drop, inimigo.andar)
        print(f"\nVocê encontrou um {inimigo.inimigo}!")
    
    if heroi.classe == 'Guerreiro':
        combate = combate_guerreiro(heroi, inimigo_combate, heroi.classe, heroi.vida, heroi.ataques, heroi.inventario)

    elif heroi.classe == 'Mago':
        combate = combate_mago(heroi, inimigo_combate, heroi.classe, heroi.vida, heroi.mana, heroi.ataques, heroi.inventario)
    
    print("O que você vai fazer?\n")

    while heroi.vida > 0 and inimigo_combate.vida > 0:
        if heroi.classe == "Guerreiro":
            print(f"Sua vida: {heroi.vida} | Vida do inimigo: {inimigo_combate.vida}")
        
        elif heroi.classe == "Mago":
            print(f"Sua vida: {heroi.vida} | Sua mana: {heroi.mana}\n"
                f"Vida do inimigo: {inimigo_combate.vida} | Elemento do inimigo: {inimigo_combate.elemento}")

        if heroi.inventario == []:
            print("--- Menu de Ações ---\n"
                    "1- Atacar\n"
                    "2- Defender\n"
                    "3- Aparar")
        
        else:
            print("--- Menu de Ações ---\n"
                    "1- Atacar\n"
                    "2- Defender\n"
                    "3- Aparar\n"
                    "4- Itens")
            
        escolha = int(input())
        açao_inimigo = rd.choice(range(1, 1001))

        if inimigo_combate.vida > 0:

            if açao_inimigo >= 25 * andar:
                inimigo_combate.atacar()
            else:
                inimigo_combate.defender()
        
        if escolha == 1:
            combate.atacar()

        elif escolha == 2:
            combate.defender()
        
        elif escolha == 3:
            combate.parry()

        elif escolha == 4 and heroi.inimigo:
            combate.usar_item()
        
        else:
            print("Escolha uma entrada válida!")
        
        if heroi.vida > 0 and inimigo.vida > 0:
            combate.reset_turno()
            inimigo_combate.reset_turno()

    if heroi.vida <= 0:
        print("Você perdeu!\n"
                f"Você perdeu no {andar}\n"
                f"Esse foi o inimigo que te matou: {inimigo.inimigo}")
        break
    
    elif inimigo_combate.vida <= 0:
        print(f"Você derrotou o {inimigo.inimigo}\n")
        inimigo_combate.dropar_item()
        andar += 1

# calcula a pontuação
def calcular_pontuacao(heroi, duracao, venceu):
    pontos = 0
    if venceu:
        pontos += 10000

    pontos += 10 * heroi.dano_causado
    pontos += 5 * heroi.dano_bloqueado
    pontos += 3 * heroi.dano_recebido
    pontos += 10000 / duracao

    return int(pontos)

# cria o arquivo txt e lê ele
def salvar_record(tempo, pontuacao, heroi):
    try:
        with open("records.txt", "r") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        linhas = []

    dados = []

    for l in linhas:
        t, p, dc, db, dr = l.strip().split("|")
        dados.append({
            "tempo": float(t),
            "pontuacao": int(p),
            "dano_causado": int(dc),
            "dano_bloqueado": int(db),
            "dano_recebido": int(dr)
        })

    # adiciona a nova run
    dados.append({
        "tempo": tempo,
        "pontuacao": pontuacao,
        "dano_causado": heroi.dano_causado,
        "dano_bloqueado": heroi.dano_bloqueado,
        "dano_recebido": heroi.dano_recebido
    })

    # ordena: maior pontuação primeiro, e em empate menor tempo vence
    dados = sorted(dados, key=lambda x: (-x["pontuacao"], x["tempo"]))

    # mantém top 10
    dados = dados[:10]

    # regrava o arquivo
    with open("records.txt", "w") as f:
        for d in dados:
            f.write(
                f"{d['tempo']}|{d['pontuacao']}|{d['dano_causado']}|{d['dano_bloqueado']}|{d['dano_recebido']}\n")

fim = time.time()

duraçao = fim - começo

print(f"Essa run durou {duraçao:.2f}")

venceu = (andar > 4 and heroi.vida > 0)
pontuacao = calcular_pontuacao(heroi, duraçao, venceu)

print(f"Sua pontuação final foi: {pontuacao}")

salvar_record(duraçao, pontuacao, heroi)