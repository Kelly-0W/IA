import importlib.util
import random
import time
import json
import pandas as pd
import numpy as np

# importa classes.py pela path relativa
spec = importlib.util.spec_from_file_location("classes_jogo", "classes.py")
classes_jogo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(classes_jogo)

with open("dicionarios.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

HERÓIS = dados.get("Heróis", [])
# parâmetros do agente
EPSILON = 0.3
ALPHA = 0.05
GAMMA = 0.8
EPISODIOS = 20

class AgenteSimples:
    def __init__(self, n_acoes):
        self.n_acoes = n_acoes
        self.q = {}

    def estado_para_chave(self, estado):
        return str(estado)

    def escolher(self, estado):
        chave = self.estado_para_chave(estado)
        if random.random() < EPSILON:
            return random.randrange(self.n_acoes)
        if chave not in self.q:
            self.q[chave] = np.zeros(self.n_acoes)
        return int(np.argmax(self.q[chave]))

    def atualizar(self, estado, acao, recompensa, prox_estado):
        chave = self.estado_para_chave(estado)
        chave2 = self.estado_para_chave(prox_estado)
        if chave not in self.q:
            self.q[chave] = np.zeros(self.n_acoes)
        if chave2 not in self.q:
            self.q[chave2] = np.zeros(self.n_acoes)
        q_old = self.q[chave][acao]
        q_max_next = np.max(self.q[chave2])
        self.q[chave][acao] = q_old + ALPHA * \
            (recompensa + GAMMA * q_max_next - q_old)

# cria o ambiente usando o classes.py
class AmbienteSimples:
    def __init__(self, classe_heroi="Guerreiro", seed=None):
        if seed is not None:
            random.seed(seed)
        # criar heroi a partir do template
        template = next((h for h in HERÓIS if h["Classe"] == classe_heroi), None)
        if not template:
            raise ValueError("Classe de heroi não encontrada no dicionarios.json")
        
        # instancia Heroi e configura como o jogo faria
        self.heroi_template = template
        self.heroi = classes_jogo.Heroi()
        self.heroi.classe = template["Classe"]
        self.heroi.vida = template["Vida"]
        self.heroi.mana = template.get("Mana", 0)
        self.heroi.ataques = [dict(a) for a in template["Ataques"]]
        self.heroi.inventario = [dict(i) for i in template["Inventário"]]

        # define o número de ações baseado na classe
        self.num_ataques = len(self.heroi.ataques)
        # 3 é o número de ações fixas
        self.n_acoes = 3 + self.num_ataques

        self.gerador = classes_jogo.Gerar_inimigo()
        self.gerador = classes_jogo.Gerar_inimigo()
        self.andar = 1
        self.reset_epoca()

    def reset_epoca(self):
        self.heroi.vida = self.heroi_template["Vida"]
        self.heroi.mana = self.heroi_template.get("Mana", 0)
        self.heroi.ataques = [dict(a) for a in self.heroi_template["Ataques"]]
        self.heroi.inventario = [dict(i)for i in self.heroi_template["Inventário"]]
        self.heroi.dano_causado = 0
        self.heroi.dano_recebido = 0
        self.heroi.dano_bloqueado = 0
        self.heroi.aparada = False
        self.heroi.defendendo = False
        self.heroi.recarga_parry = 0
        self.heroi.modo_ia = True  # ativa modo IA
        self.andar = 1
        self.start = time.time()
        return self._obter_estado()

    def _obter_estado(self, inimigo_combate=None):
        hp_base = 2 if self.heroi.vida > 25 else (1 if self.heroi.vida > 10 else 0)
        mana = getattr(self.heroi, "mana", 0)
        mana_base = 2 if mana > 10 else (1 if mana > 0 else 0)
        andar_base = min(max(self.andar - 1, 0), 3)

        inimigo_hp_base = 0
        if inimigo_combate and inimigo_combate.vida > 0:
            hp_atual_inimigo = inimigo_combate.vida
            if hp_atual_inimigo > 20:
                inimigo_hp_base = 2
            elif hp_atual_inimigo > 5:
                inimigo_hp_base = 1
            else:
                inimigo_hp_base = 0

        parry_disponivel = 1 if self.heroi.recarga_parry <= 0 else 0

        ataque_forte_disponivel = 1
        if self.heroi.classe == "Guerreiro" and self.heroi.ataques and len(self.heroi.ataques) > 1:
            if self.heroi.ataques[1].get('Cooldown atual', 0) > 0:
                ataque_forte_disponivel = 0
            
        elemento_inimigo = 0
        if inimigo_combate:
            elemento = inimigo_combate.elemento
            if elemento == "Fogo": 
                elemento_inimigo = 1
            elif elemento == "Água":
                elemento_inimigo = 2
            elif elemento == "Eletricidade":
                elemento_inimigo = 3

        return (andar_base, hp_base, mana_base, inimigo_hp_base, parry_disponivel, ataque_forte_disponivel, elemento_inimigo)

    def spawn_inimigo(self):
        inimigo = self.gerador.escolher_inimigo(self.andar)
        if not inimigo:
            return None, None
        inimigo_combate = classes_jogo.combate_inimigo(
            self.heroi, inimigo, inimigo.vida, inimigo.elemento, inimigo.ataque, inimigo.drop, inimigo.andar)
        if self.heroi.classe == "Guerreiro":
            combate = classes_jogo.combate_guerreiro(
                self.heroi, inimigo_combate, self.heroi.classe, self.heroi.vida, self.heroi.ataques, self.heroi.inventario)
        else:
            combate = classes_jogo.combate_mago(self.heroi, inimigo_combate, self.heroi.classe,
                                                self.heroi.vida, self.heroi.mana, self.heroi.ataques, self.heroi.inventario)
        return inimigo_combate, combate

    def passo_contra_inimigo(self, inimigo_combate, combate, acao):
        # acao: 0 defender, 1 parry, 2 usar_item, >=3 atacar (indice=acao-3)

        recompensa = 0.0

        dano_causado_antes = self.heroi.dano_causado
        dano_bloqueado_antes = self.heroi.dano_bloqueado
        dano_recebido_antes = self.heroi.dano_recebido

        # ação do herói
        if acao == 0:
            combate.defender()

        elif acao == 1:
            recarga_antes = self.heroi.recarga_parry
            combate.parry()
            # se a recarga_parry não mudou e era > 0, o parry falhou devido ao cooldown.
            if self.heroi.recarga_parry == recarga_antes and recarga_antes > 0:
                recompensa -= 10.0

        elif acao == 2:
            # punição se tentar usar item de forma errada
            qtd_itens_antes = len(self.heroi.inventario)
            combate.usar_item()
            if len(self.heroi.inventario) == qtd_itens_antes:
                recompensa -= 5.0

        else:
            ataque_idx = acao - 3
            combate.atacar(escolha=ataque_idx)


            if self.heroi.classe == "Guerreiro" and ataque_idx < len(self.heroi.ataques):
                ataque_escolhido = self.heroi.ataques[ataque_idx]
                if ataque_escolhido.get('Cooldown atual', 0) > 0:
                    recompensa -= 10.0

            if self.heroi.classe == "Mago" and ataque_idx < len(self.heroi.ataques):
                ataque_escolhido = self.heroi.ataques[ataque_idx]
                custo = ataque_escolhido.get('Custo', 0)
                if self.heroi.mana < custo:
                    recompensa -= 10.0

        # ação inimigo
        escolha_inimigo = random.randint(1, 100)
        if escolha_inimigo >= 25 * self.andar:
            inimigo_combate.atacar()
        else:
            inimigo_combate.defender()

        # reset turnos
        combate.reset_turno()
        inimigo_combate.reset_turno()

        dano_causado_turno = self.heroi.dano_causado - dano_causado_antes
        dano_bloqueado_turno = self.heroi.dano_bloqueado - dano_bloqueado_antes
        dano_recebido_turno = self.heroi.dano_recebido - dano_recebido_antes

        recompensa += 2.2 * dano_causado_turno
        recompensa += 1.0 * dano_bloqueado_turno
        recompensa -= 2.0 * dano_recebido_turno

        if self.heroi.classe == "Mago":
            if dano_causado_turno > 6:
                recompensa += 10.0
            elif 0 < dano_causado_turno < 4:
                recompensa -= 5.0

        if self.heroi.vida <= 0:
            recompensa -= 1000.0

            return recompensa, True, {"resultado": "heroi_morto"}
        if inimigo_combate.vida <= 0:
            inimigo_combate.dropar_item()
            self.andar += 1
            return recompensa, False, {"resultado": "inimigo_derrotado"}
        
        return recompensa, False, {"resultado": "continuar"}

    # função pra rodar cada epoca
    def executar_epoca(self, agente, max_passos=500):
        self.reset_epoca()

        self.heroi.dano_causado = 0
        self.heroi.dano_recebido = 0
        self.heroi.dano_bloqueado = 0

        recompensa = 0.0
        passos = 0
        while self.andar <= 4 and self.heroi.vida > 0 and passos < max_passos:
            inimigo_combate, combate = self.spawn_inimigo()
            if inimigo_combate is None:
                self.andar += 1
                continue
            
            while self.heroi.vida > 0 and inimigo_combate.vida > 0 and passos < max_passos:
                estado = self._obter_estado(inimigo_combate)
                acao = agente.escolher(estado)
                r, concluido, info = self.passo_contra_inimigo(inimigo_combate, combate, acao)
                proximo_estado = self._obter_estado(inimigo_combate)
                agente.atualizar(estado, acao, r, proximo_estado)

                recompensa += r
                passos += 1

                if concluido:
                    break
            if self.heroi.vida <= 0:
                break

        duracao = max(0.1, time.time() - self.start)
        venceu = (self.andar > 4 and self.heroi.vida > 0)
        pontos = 0

        if venceu:
            pontos += 10000

        # dá a recompensa a partir da pontuação
        pontos += 10 * getattr(self.heroi, "dano_causado", 0)
        pontos += 5 * getattr(self.heroi, "dano_bloqueado", 0)
        pontos -= 10 * getattr(self.heroi, "dano_recebido", 0)
        pontos += 1000.0 / duracao
        recompensa += pontos / 100.0

        if not venceu:
            recompensa -= 2000.0

        run_info = {
            "venceu": venceu,
            "tempo": duracao,
            "pontuacao": int(pontos),
            "dano_causado": int(getattr(self.heroi, "dano_causado", 0)),
            "dano_bloqueado": int(getattr(self.heroi, "dano_bloqueado", 0)),
            "dano_recebido": int(getattr(self.heroi, "dano_recebido", 0))
        }

        return recompensa, run_info

# aqui só faz rodar o treinamento e registra os dados
def treinar_simples(classe_heroi="Guerreiro", episodios=EPISODIOS):
    ambiente = AmbienteSimples(classe_heroi=classe_heroi, seed=42)
    agente = AgenteSimples(ambiente.n_acoes)
    registros = []

    for ep in range(episodios):
        recompensa, info_epoca = ambiente.executar_epoca(agente, max_passos=200)
        info_epoca['Episodio'] = ep + 1
        info_epoca['Recompensa'] = recompensa
        registros.append(info_epoca)

    df = pd.DataFrame(registros)

    # converte para float com 2 casas decimais
    if 'tempo' in df.columns:
        df['tempo'] = df['tempo'].astype(float).round(2)

    colunas = ['pontuacao', 'dano_causado',
                        'dano_bloqueado', 'dano_recebido', 'Recompensa']

    for coluna in colunas:
        if coluna in df.columns:
            # converte para int
            df.loc[:, coluna] = df[coluna].fillna(0).astype(int)

    # salva o arquivo
    nome_arquivo = f"qlearning_{classe_heroi.lower()}_{time.strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(nome_arquivo, index=False)
    print(f"Dados de treinamento salvos em: {nome_arquivo}\n")

    return agente

if __name__ == "__main__":
    print("--- Treinando Guerreiro ---")
    treinar_simples(classe_heroi="Guerreiro", episodios=5000)

    print("--- Treinando Mago ---")
    treinar_simples(classe_heroi="Mago", episodios=5000)

    print("Treinamento concluído.")