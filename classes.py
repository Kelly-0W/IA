import json
import random as rd

# puxa as informações dos dicionarios e poem em diferentes variaveis
with open("dicionarios.json", "r", encoding="utf-8") as informaçoes:
    dados = json.load(informaçoes)

herois = dados['Heróis']
criaturas = dados['Monstros']
itens = dados['Itens']

# criação do heroi
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
        self.modo_ia = False
    
    # função feita para a escolha do herói e a implementação dos seus status
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
                    
                # apenas verificações de entrada
                elif indice == -1:
                    print("Jogo encerrado!")
                    return

                else:
                    print("Número inválido! Tente novamente ou digite -1 para sair")
            
            else:
                print("Entrada inválida! Tente novamente")

# criação dos status do inimigo
class Inimigo:
    def __init__(self, inimigo=None, vida=None, elemento=None, ataque=None, drop=None, andar=None):
        self.inimigo = inimigo
        self.vida = vida
        self.elemento = elemento
        self.ataque = ataque
        self.drop = drop or []
        self.andar = andar
        self.defendendo = False

# geração do inimigo com base no andar atual
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

# combate para os inimigos (todos vão agir de forma similar)
class combate_inimigo(Inimigo):
    def __init__(self, heroi, inimigo=None, vida=None, elemento=None, ataque=None, drop=None, andar=None):
        super().__init__(inimigo=inimigo, vida=vida, elemento=elemento, ataque=ataque, drop=drop, andar=andar)
        self.heroi = heroi
    
    def atacar(self):
        dano = self.ataque

        # verifica parrys
        if self.heroi.aparada == True:
            self.heroi.dano_bloqueado += dano

            if not self.heroi.modo_ia:
                print("O herói aparou o ataque! Não sofreu dano.")

            self.heroi.aparada = False

        # verifica defesa do heroi
        if self.heroi.defendendo == True and self.defendendo == True:
            if not self.heroi.modo_ia:
                print("Ambos se defenderam! Ninguém sofreu dano.\n")
        
        elif self.heroi.defendendo == True:
            dano_original = dano 
            dano_recebido_final = dano_original // 2

            dano_bloqueado_neste_turno = dano_original - dano_recebido_final

            self.heroi.dano_bloqueado += dano_bloqueado_neste_turno
            dano = dano_recebido_final

            if not self.heroi.modo_ia:
                print(f"O heroi defendeu o ataque! Causou apenas {dano}")

            else:
                if not self.heroi.modo_ia:
                    print(f"O inimigo te atacou e causou {dano} de dano!")

        self.heroi.vida -= dano
        self.heroi.dano_recebido += dano

    # funções para a defesa, o reset da defesa e o drop de itens
    def defender(self):
        self.defendendo = True
    
    def reset_turno(self):
        self.defendendo = False
    
    def dropar_item(self):
        # adiciona item ao inventário do herói; imprime apenas no modo humano
        self.heroi.inventario.append(self.drop)
        if not self.heroi.modo_ia:
            print(f"O inimigo dropou um {self.drop['Nome']}! Foi adicionado ao seu inventário")

# combate caso a classe seja guerreiro, recebe a classe heroi como parametro
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

    def atacar(self, escolha=None):

        if self.heroi.modo_ia:
            indice = None
            if escolha is not None:
                indice = escolha
            else:
                # tenta achar o primeiro ataque com cooldown 0
                for idx, atk in enumerate(self.ataques):
                    if atk.get('Cooldown atual', 0) <= 0:
                        indice = idx
                        break
                if indice is None:
                    # escolhe o primeiro
                    indice = 0
        else:
            print("\n--- Menu de Ataques ---")
            for i, ataque in enumerate(self.ataques, start=1):
                cd = ataque.get('Cooldown atual', 0)
                if cd > 0:
                    print(f"{i}- {ataque['Nome do ataque']} | Recarga: {cd} turnos restantes!")
                else:
                    print(f"{i}- {ataque['Nome do ataque']}")
            escolha_in = int(input()) - 1
            indice = escolha_in

        # valida índice
        if indice < 0 or indice >= len(self.ataques):
            if not self.heroi.modo_ia:
                print("\nEscolha inválida de ataque!")
            return

        ataque_escolhido = self.ataques[indice]

        # impede de usar ataques em recarga
        if ataque_escolhido.get('Cooldown atual', 0) > 0:
            if not self.heroi.modo_ia:
                print("\nEsse ataque ainda está em recarga!")
            return

        # aumenta o dano se tiver uma arma equipada (a arma só dura 1 combate)
        dano = ataque_escolhido['Dano'] + getattr(self.heroi, 'arma', 0)

        if self.inimigo.defendendo == True and self.defendendo == True:
            if not self.heroi.modo_ia:
                print("\nAmbos se defenderam! Ninguém sofreu dano.")

        # verifica se o inimigo está defendendo
        elif self.inimigo.defendendo == True:
            dano //= 2
            if not self.heroi.modo_ia:
                print(f"\nO inimigo se defendeu do seu ataque! Causou apenas {dano} de dano!")
        
        else:
            if not self.heroi.modo_ia:
                print(f"\nVocê usou {ataque_escolhido['Nome do ataque']} e causou {dano} de dano!")
        
        self.inimigo.vida -= dano
        self.heroi.dano_causado += dano

        ataque_escolhido['Cooldown atual'] = ataque_escolhido.get('Recarga', 0)
    
    # funções para a defesa, parry, reset de defesa, aparada e recarga dos ataques
    def defender(self):
        self.heroi.defendendo = True
        self.heroi.vida += 2
        if not self.heroi.modo_ia:
            print("\nVocê está se defendendo! Isso recupera 3 de vida!")

    def parry(self):
        if self.heroi.recarga_parry > 0:
            if not self.heroi.modo_ia:
                print("\nVocê não pode aparar nesse turno!")
            return
        else:
            self.heroi.aparada = True
            self.heroi.recarga_parry = 2
            if not self.heroi.modo_ia:
                print("\nVocê aparou o próximo golpe!")

    def reset_turno(self):
        self.heroi.aparada = False
        self.heroi.defendendo = False
        if self.heroi.recarga_parry > 0:
            self.heroi.recarga_parry -= 1

        for ataque in self.ataques:
            if ataque.get('Cooldown atual', 0) > 0:
                ataque['Cooldown atual'] -= 1
    
    # função para o uso do item
    def usar_item(self, escolha=None):
        # IA escolhe item automaticamente
        if self.heroi.modo_ia:
            if not self.heroi.inventario:
                return

            # escolhe o primeiro item de cura disponível
            for idx, item in enumerate(self.heroi.inventario):
                if item.get("Atributo") == "Vida":
                    escolha = idx
                    break

            # se não houver cura, usa o primeiro item mesmo
            if escolha is None:
                escolha = 0

        else:
            for i, item in enumerate(self.heroi.inventario, start=1):
                print(f"{i}- {item['Nome']} ({item['Atributo']}: {item['Valor']})")
            escolha = int(input()) - 1

        # validação
        if escolha < 0 or escolha >= len(self.heroi.inventario):
            if not self.heroi.modo_ia:
                print("Escolha inválida!")
            return

        item = self.heroi.inventario[escolha]

        # aplica cura
        if item['Atributo'] == 'Vida':
            self.heroi.vida += item['Valor']
            if not self.heroi.modo_ia:
                print(f"Você usou {item['Nome']} e recuperou {item['Valor']} de vida!")

        # recupera mana somente se o herói for mago
        elif item['Atributo'] == 'Mana':
            if self.heroi.classe == 'Mago':
                self.heroi.mana += item['Valor']
                if not self.heroi.modo_ia:
                    print(f"Você recuperou {item['Valor']} de mana!")
            else:
                if not self.heroi.modo_ia:
                    print("Guerreiro não usa mana!")

        # aumenta dano se for arma compatível
        elif item['Atributo'] == 'Dano':
            item_classe = item.get('Classe', None)

            if item_classe == 'Guerreiro':
                self.heroi.arma = item['Valor']
                if not self.heroi.modo_ia:
                    print(f"Aumentou dano em {item['Valor']}!")

            elif item_classe is None:
                # item consumível de dano (poção)
                if not self.heroi.modo_ia:
                    print(f"Você usou {item['Nome']} (Dano)!")

            else:
                # arma de outra classe
                if not self.heroi.modo_ia:
                    print(f"Guerreiro não pode usar esse item ({item_classe}).")

        # remove item do inventário
        self.heroi.inventario.pop(escolha)

# classe de combate para caso o heroi seja um mago
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

    def atacar(self, escolha=None):
        if self.heroi.modo_ia:
            indice = None
            if escolha is not None:
                indice = escolha
            else:
                for idx, atk in enumerate(self.ataques):
                    custo = atk.get('Custo', 0)
                    if custo <= getattr(self.heroi, 'mana', 0):
                        indice = idx
                        break
                if indice is None:
                    indice = 0

        else:
            print("\n--- Menu de Ataques ---")
            for i, ataque in enumerate(self.ataques, start=1):
                    print(f"{i}- {ataque['Nome do ataque']} | Custo: {ataque['Custo']}")
            escolha_in = int(input()) - 1
            indice = escolha_in

        # valida índice
        if indice < 0 or indice >= len(self.ataques):
            if not self.heroi.modo_ia:
                print("\nEscolha inválida de ataque!")
            return

        ataque_escolhido = self.ataques[indice]
        elemento = ataque_escolhido.get('Elemento')

        # verifica se tem mana para usar o ataque
        custo_ataque = ataque_escolhido.get('Custo', 0)
        if custo_ataque > getattr(self.heroi, 'mana', 0):
            if not self.heroi.modo_ia:
                print("\nVocê não tem mana para usar esse ataque!")
            return

        dano = ataque_escolhido['Dano'] + getattr(self.heroi, 'arma', 0)

        # aumenta ou diminui o dano conforme os elementos
        if (elemento == "Fogo" and self.inimigo.elemento == "Eletricidade") \
            or (elemento == "Água" and self.inimigo.elemento == "Fogo") \
            or (elemento == "Eletricidade" and self.inimigo.elemento == "Água"):
            dano *= 2
        
        elif (elemento == self.inimigo.elemento) or (self.inimigo.elemento == "Neutro"):
            pass
        
        else:
            dano //= 2

        if self.inimigo.defendendo == True and self.defendendo == True:
            if not self.heroi.modo_ia:
                print("\nAmbos se defenderam! Ninguém sofreu dano.")

        elif self.inimigo.defendendo:
            dano //= 2
            if not self.heroi.modo_ia:
                print(f"\nO inimigo se defendeu do seu ataque! Causou apenas {dano} de dano!")

        else:
            if not self.heroi.modo_ia:
                print(f"\nVocê usou {ataque_escolhido['Nome do ataque']} e causou {dano} de dano!")

        self.inimigo.vida -= dano
        self.heroi.dano_causado += dano

        self.heroi.mana -= custo_ataque

    def defender(self):
        self.heroi.defendendo = True
        self.heroi.mana += 2
        if not self.heroi.modo_ia:
            print("\nVocê está defendendo! Isso regenera 2 de mana.")
    
    def parry(self):
        if self.heroi.recarga_parry > 0:
            if not self.heroi.modo_ia:
                print("\nVocê não pode aparar nesse turno!")
            return
        else:
            self.heroi.aparada = True
            self.heroi.recarga_parry = 2
            if not self.heroi.modo_ia:
                print("\nVocê aparou o próximo golpe (parry)!")

    # funções para a defesa, parry, reset de defesa e aparada
    def reset_turno(self):
        self.heroi.aparada = False
        self.heroi.defendendo = False
        if self.heroi.recarga_parry > 0:
            self.heroi.recarga_parry -= 1

    def usar_item(self, escolha=None):
        # IA escolhe item automaticamente
        if self.heroi.modo_ia:
            if not self.heroi.inventario:
                return

            # escolhe o primeiro item de cura disponível
            for idx, item in enumerate(self.heroi.inventario):
                if item.get("Atributo") == "Vida":
                    escolha = idx
                    break

            # se não houver cura, usa o primeiro item mesmo
            if escolha is None:
                escolha = 0

        else:
            for i, item in enumerate(self.heroi.inventario, start=1):
                print(f"{i}- {item['Nome']} ({item['Atributo']}: {item['Valor']})")
            escolha = int(input()) - 1

        # validação
        if escolha < 0 or escolha >= len(self.heroi.inventario):
            if not self.heroi.modo_ia:
                print("Escolha inválida!")
            return

        item = self.heroi.inventario[escolha]

        # aplica cura
        if item['Atributo'] == 'Vida':
            self.heroi.vida += item['Valor']
            if not self.heroi.modo_ia:
                print(
                    f"Você usou {item['Nome']} e recuperou {item['Valor']} de vida!")

        # recupera mana somente se o herói for mago
        elif item['Atributo'] == 'Mana':
            if self.heroi.classe == 'Mago':
                self.heroi.mana += item['Valor']
                if not self.heroi.modo_ia:
                    print(f"Você recuperou {item['Valor']} de mana!")
            else:
                if not self.heroi.modo_ia:
                    print("Guerreiro não usa mana!")

        # aumenta dano se for arma compatível
        elif item['Atributo'] == 'Dano':
            item_classe = item.get('Classe', None)

            if item_classe == 'Guerreiro':
                if not self.heroi.modo_ia:
                    print("Magos não podem equipar armas de Guerreiro!")

            elif item_classe is None:
                if not self.heroi.modo_ia:
                    print(f"Você usou {item['Nome']} (Dano)!")

            else:
                if not self.heroi.modo_ia:
                    print(f"Você não pode equipar esse item ({item_classe}).")

        self.heroi.inventario.pop(escolha)