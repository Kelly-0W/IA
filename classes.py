import json
import random as rd

## puxa as informações dos dicionarios e poem em diferentes variaveis
with open("dicionarios.json", "r", encoding="utf-8") as informaçoes:
    dados = json.load(informaçoes)

herois = dados['Heróis']
criaturas = dados['Monstros']
itens = dados['Itens']

## criação do heroi
class Heroi:
    def __init__(self, classe=None, vida=None, mana=None, ataques=None, inventario=None):
        self.classe = classe
        self.vida = vida
        self.mana = mana
        self.ataques = ataques or []
        self.inventario = inventario or []
        self.aparada = False
        self.defendendo = False
        self.recarga_parry = 0
        self.dano_causado = 0
        self.dano_recebido = 0
        self.dano_bloqueado = 0
    
    ## função feita para a escolha do herói e a implementação dos seus status
    def escolher_classe(self, herois):
        print("--- Escolha sua classe ---")
        for i, classe in enumerate(herois, start=1):
            print(f"{i}º Classe: {classe['Classe']} | Vida: {classe['Vida']}")

        while True:
            escolha = input("")

            if escolha.isdigit():
                indice = int(escolha) - 1

                if 0 <= indice < len(herois):
                    heroi = herois[indice]
                    print(f"\nVocê escolheu {heroi['Classe']}\nSeus ataques são:")

                    for ataque in heroi['Ataques']:
                        if self.classe == 'Mago':
                            print(f"Nome: {ataque.get('Nome do ataque')} | Dano: {ataque.get('Dano')} | Custo: {ataque.get('Custo')}")

                        elif self.classe == 'Guerreiro':
                            print(f"Nome: {ataque.get('Nome do ataque')} | Dano: {ataque.get('Dano')}")
                    
                    self.classe = heroi['Classe']
                    self.vida = heroi['Vida']
                    self.ataques = heroi['Ataques']
                    self.mana = heroi['Mana']
                    self.inventario = heroi['Inventário']
                    break
                    
                ## apenas verificações de entrada
                elif indice == -1:
                    print("Jogo encerrado!")
                    return

                else:
                    print("Número inválido! Tente novamente ou digite -1 para sair")
            
            else:
                print("Entrada inválida! Tente novamente")

## criação dos status do inimigo
class Inimigo:
    def __init__(self, inimigo=None, vida=None, elemento=None, ataque=None, drop=None, andar=None):
        self.inimigo = inimigo
        self.vida = vida
        self.elemento = elemento
        self.ataque = ataque
        self.drop = drop or []
        self.andar = andar
        self.defendendo = False

## geração do inimigo com base no andar atual
class Gerar_inimigo:

    def escolher_inimigo(self, andar):
        criaturas_andar = []

        for inimigo in criaturas:
            if inimigo['Andar'] == andar:
                criaturas_andar.append(inimigo)
        
        if criaturas_andar:
            criatura_escolhida = rd.choice(criaturas_andar)

            item_drop = rd.choice(itens)
            
            monstro = Inimigo(
                inimigo = criatura_escolhida['Nome'],
                vida = criatura_escolhida['Vida'],
                ataque = criatura_escolhida['Ataque'],
                elemento = criatura_escolhida['Elemento'],
                drop = item_drop,
                andar = criatura_escolhida['Andar']
            )
            
            return monstro

## combate para os inimigos (todos vão agir de forma similar)
class combate_inimigo(Inimigo):
    def __init__(self, heroi, inimigo=None, vida=None, elemento=None, ataque=None, drop=None, andar=None):
        super().__init__(inimigo=inimigo, vida=vida, elemento=elemento, ataque=ataque, drop=drop, andar=andar)
        self.heroi = heroi
    
    def atacar(self):
        dano = self.ataque

        ## verifica parrys
        if self.heroi.aparada == True:
            print("O herói aparou o ataque! Não sofreu dano.")
            self.heroi.aparada = False
            return

        ## verifica defesa do heroi
        if self.heroi.defendendo == True and self.defendendo == True:
            print("Ambos se defenderam! Ninguém sofreu dano.\n")
            return
        
        elif self.heroi.defendendo == True:
            dano //= 2
            self.heroi.dano_bloqueado += dano
            print(f"O heroi defendeu o ataque! Causou apenas {dano}")

        else:
            print(f"O inimigo te atacou e causou {dano} de dano!")
        
        self.heroi.vida -= dano
        self.heroi.dano_recebido += dano

    ## funções para a defesa, o reset da defesa e o drop de itens
    def defender(self):
        self.defendendo = True
    
    def reset_turno(self):
        self.defendendo = False
    
    def dropar_item(self):
        self.heroi.inventario.append(self.drop)
        print(f"O inimigo dropou um {self.drop['Nome']}! Foi adicionado ao seu inventário")

## combate caso a classe seja guerreiro, recebe a classe heroi como parametro
class combate_guerreiro(Heroi):
    def __init__(self, heroi, inimigo, classe=None, vida=None, ataques=None, inventario=None):
        super().__init__(classe=classe, vida=vida, ataques=ataques, inventario=inventario)
        self.heroi = heroi
        self.inimigo = inimigo
        self.heroi.vida = self.vida
        self.heroi.aparada = self.aparada
        self.heroi.defendendo = self.defendendo
        self.heroi.recarga_parry = self.recarga_parry
        self.heroi.arma = 0

        for ataque in self.ataques:
            ataque['Cooldown atual'] = 0

    def atacar(self):
        print("\n--- Menu de Ataques ---")

        for i, ataque in enumerate(self.ataques, start=1):
            cd = ataque['Cooldown atual']
            if cd > 0:
                print(f"{i}- {ataque['Nome do ataque']} | Recarga: {cd} turnos restantes!")
            else:
                print(f"{i}- {ataque['Nome do ataque']}")
        
        escolha = int(input()) - 1
        ataque_escolhido = self.ataques[escolha]

        ## impede de usar ataques em recarga
        if ataque_escolhido['Cooldown atual'] > 0:
            print("\nEsse ataque ainda está em recarga!")
            return

        ##aumenta o dano se tiver uma arma equipada (a arma só dura 1 combate)
        dano = ataque_escolhido['Dano'] + self.heroi.arma

        if self.inimigo.defendendo == True and self.defendendo == True:
            print("\nAmbos se defenderam! Ninguém sofreu dano.")

        ## verifica se o inimigo está defendendo
        elif self.inimigo.defendendo == True:
            dano //= 2
            print(f"\nO inimigo se defendeu do seu ataque! Causou apenas {dano} de dano!")
        
        else:
            print(f"\nVocê usou {ataque_escolhido['Nome do ataque']} e causou {dano} de dano!")
        
        self.inimigo.vida -= dano
        self.heroi.dano_causado += dano

        ataque_escolhido['Cooldown atual'] = ataque_escolhido['Recarga']
    
    ## funções para a defesa, parry, reset de defesa, aparada e recarga dos ataques
    def defender(self):
        self.heroi.defendendo = True
        self.heroi.vida += 3
        print("\nVocê está se defendendo! Isso recupera 3 de vida!")

    def parry(self):
        if self.heroi.recarga_parry > 0:
            print("\nVocê não pode aparar nesse turno!")
            return
        
        else:
            self.heroi.aparada = True
            self.heroi.recarga_parry = 2
    
    def reset_turno(self):
        self.heroi.aparada = False
        self.heroi.defendendo = False
        if self.heroi.recarga_parry > 0:
            self.heroi.recarga_parry -= 1

        for ataque in self.ataques:
            if ataque['Cooldown atual'] > 0:
                ataque['Cooldown atual'] -= 1
    
    ## função para o uso do item baseado no seu atributo
    def usar_item(self):
        for i, item in enumerate(self.heroi.inventario, start=1):
            print(f"{i}- {item['Nome']}")

        escolha = int(input()) - 1
        item_escolhido = self.heroi.inventario[escolha]

        if item_escolhido['Atributo'] == 'Vida':
            self.heroi.vida += item_escolhido['Valor']
            print(f"Você usou {item_escolhido['Nome']} para recupear {item_escolhido['Valor']} de {item_escolhido['Atributo']}")
        
        elif item_escolhido['Atributo'] == 'Mana':
            print("O guerreiro não usa mana! Esse item não surtiu efeito!")
        
        elif item_escolhido['Atributo'] == 'Dano' and item_escolhido['Classe'] == 'Guerreiro':
            self.heroi.arma = item_escolhido['Valor']
            print(f"Você usou {item_escolhido['Nome']} para aumentar seu Dano em {item_escolhido['Valor']}")
        
        ## impede do guerreiro equipar a varinha magica
        elif item_escolhido['Atributo'] == 'Dano' and item_escolhido['Classe'] == 'Mago':
            print("O Guerreiro não pode usar essa arma!")

        if self.inimigo.defendendo:
            print("O inimigo se defendeu esperando um ataque, mas você se aproveitou do tempo para usar um item!")
        
        ## remove o item do inventario
        del self.heroi.inventario[escolha]

## classe de combate para caso o heroi seja um mago
class combate_mago(Heroi):
    def __init__(self, heroi, inimigo, classe=None, vida=None, mana=None, ataques=None, inventario=None):
        super().__init__(classe=classe, vida=vida, mana=mana, ataques=ataques, inventario=inventario)
        self.heroi = heroi
        self.inimigo = inimigo
        self.heroi.mana = self.mana
        self.heroi.aparada = self.aparada
        self.heroi.defendendo = self.defendendo
        self.heroi.recarga_parry = self.recarga_parry
        self.heroi.arma = 0

    def atacar(self):
        print("\n--- Menu de Ataques ---")

        for i, ataque in enumerate(self.ataques, start=1):
                print(f"{i}- {ataque['Nome do ataque']} | Custo: {ataque['Custo']}")

        escolha = int(input()) - 1
        ataque_escolhido = self.ataques[escolha]
        elemento = ataque_escolhido['Elemento']

        ## verifica se tem mana para usar o ataque
        if ataque_escolhido['Custo'] > self.mana:
            print("\nVocê não tem mana para usar esse ataque!")
            return

        dano = ataque_escolhido['Dano'] + self.heroi.arma

        ## aumenta ou diminui o dano conforme os elementos
        if (elemento == "Fogo" and self.inimigo.elemento == "Eletricidade") \
            or (elemento == "Água" and self.inimigo.elemento == "Fogo") \
            or (elemento == "Eletricidade" and self.inimigo.elemento == "Água"):
            dano *= 2
        
        elif (elemento == self.inimigo.elemento) or (self.inimigo.elemento == "Neutro"):
            pass
        
        else:
            dano //= 2

        if self.inimigo.defendendo == True and self.defendendo == True:
            print("\nAmbos se defenderam! Ninguém sofreu dano.")

        elif self.inimigo.defendendo:
            dano //= 2
            print(f"\nO inimigo se defendeu do seu ataque! Causou apenas {dano} de dano!")

        else:
            print(f"\nVocê usou {ataque_escolhido['Nome do ataque']} e causou {dano} de dano!")

        self.inimigo.vida -= dano
        self.heroi.dano_causado += dano

        self.heroi.mana -= ataque_escolhido['Custo']

    def defender(self):
        self.heroi.defendendo = True
        self.heroi.mana += 2
        print("\nVocê está defendendo! Isso regenera 2 de mana.")
    
    def parry(self):
        if self.heroi.recarga_parry > 0:
            print("\nVocê não pode aparar nesse turno!")
            return
        else:
            self.heroi.aparada = True
            self.heroi.recarga_parry = 2
    # funções para a defesa, parry, reset de defesa e aparada
    def reset_turno(self):
        self.heroi.aparada = False
        self.heroi.defendendo = False
        if self.heroi.recarga_parry > 0:
            self.heroi.recarga_parry -= 1

    ## mesma coisa dos itens do guerreiro
    def usar_item(self):
        for i, item in enumerate(self.heroi.inventario, start=1):
            print(f"{i}- {item['Nome']}")

        escolha = int(input()) - 1
        item_escolhido = self.heroi.inventario[escolha]

        if item_escolhido['Atributo'] == 'Vida':
            self.heroi.vida += item_escolhido['Valor']
            print(f"Você usou {item_escolhido['Nome']} para recupear {item_escolhido['Valor']} de {item_escolhido['Atributo']}")

        elif item_escolhido['Atributo'] == 'Mana':
            self.heroi.mana += item_escolhido['Valor']
            print(f"Você usou {item_escolhido['Nome']} para recupear {item_escolhido['Valor']} de {item_escolhido['Atributo']}")

        elif item_escolhido['Atributo'] == 'Dano' and item_escolhido['Classe'] == 'Mago':
            self.heroi.arma = item_escolhido['Valor']
            print(f"Você usou {item_escolhido['Nome']} para aumentar seu Dano em {item_escolhido['Valor']}")

        elif item_escolhido['Atributo'] == 'Dano' and item_escolhido['Classe'] == 'Guerreiro':
            print("O Mago não pode usar essa arma!")

        if self.inimigo.defendendo:
            print("O inimigo se defendeu esperando um ataque, mas você se aproveitou do tempo para usar um item!")

        del self.heroi.inventario[escolha]