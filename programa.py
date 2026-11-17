# -*- coding: utf-8 -*-
"""UC00245 — Gestão de pedidos de suporte técnico.

Analisa exatamente 10 pedidos válidos e resume a carga de trabalho.
A lógica segue o pseudocódigo da entrega: validar, repetir, calcular
e só depois classificar, pela ordem CRÍTICA, ELEVADA, NORMAL.
"""

NUMERO_PEDIDOS = 10
PRIORIDADE_MIN = 1
PRIORIDADE_MAX = 5
LIMITE_CRITICA_URGENTES = 5
LIMITE_ELEVADA_URGENTES = 3
LIMITE_CRITICA_MINUTOS = 600
LIMITE_ELEVADA_MINUTOS = 480


def prioridade_valida(prioridade):
    """Inteiro de 1 a 5. Rejeita booleanos e outros tipos."""
    if isinstance(prioridade, bool) or not isinstance(prioridade, int):
        return False
    return PRIORIDADE_MIN <= prioridade <= PRIORIDADE_MAX


def tempo_valido(tempo):
    """Inteiro superior a zero. Rejeita booleanos e outros tipos."""
    if isinstance(tempo, bool) or not isinstance(tempo, int):
        return False
    return tempo > 0


def e_urgente(prioridade):
    """Urgente é prioridade 1 ou 2. A condição prioridade < 2 está errada."""
    return prioridade == 1 or prioridade == 2


def classificar_carga(urgentes, total_minutos):
    """CRÍTICA antes de ELEVADA. Os minutos usam comparação estrita (>)."""
    if urgentes >= LIMITE_CRITICA_URGENTES or total_minutos > LIMITE_CRITICA_MINUTOS:
        return "CRÍTICA"
    if urgentes >= LIMITE_ELEVADA_URGENTES or total_minutos > LIMITE_ELEVADA_MINUTOS:
        return "ELEVADA"
    return "NORMAL"


def analisar_pedidos(pedidos):
    """Resume exatamente 10 pares (prioridade, tempo) já validados.

    Valores iniciais: urgentes 0, total 0, máximo 0.
    A média só é calculada depois de fechar os 10 pedidos.
    """
    if len(pedidos) != NUMERO_PEDIDOS:
        raise ValueError("São necessários exatamente 10 pedidos válidos.")

    contador_urgentes = 0
    total_minutos = 0
    maior_estimativa = 0

    for prioridade, tempo in pedidos:
        if not prioridade_valida(prioridade) or not tempo_valido(tempo):
            raise ValueError("Pedido inválido na análise.")
        if e_urgente(prioridade):
            contador_urgentes += 1
        total_minutos += tempo
        if tempo > maior_estimativa:
            maior_estimativa = tempo

    media = total_minutos / NUMERO_PEDIDOS
    return {
        "urgentes": contador_urgentes,
        "total_minutos": total_minutos,
        "media": media,
        "maior_estimativa": maior_estimativa,
        "classificacao": classificar_carga(contador_urgentes, total_minutos),
    }


def _texto_inteiro(texto):
    corpo = texto.strip()
    if corpo.startswith("-"):
        corpo = corpo[1:]
    return corpo.isdigit()


def ler_inteiro(mensagem, ler):
    """Pede um inteiro. Não aceita texto vazio nem valores não inteiros."""
    while True:
        texto = ler(mensagem)
        if texto is not None and _texto_inteiro(texto):
            return int(texto.strip())
        print("Valor inválido. Introduza um número inteiro.")


def recolher_pedidos(ler):
    """Lê pedidos até existirem exatamente 10 válidos. Os inválidos não contam."""
    pedidos = []
    while len(pedidos) < NUMERO_PEDIDOS:
        numero = len(pedidos) + 1
        print("Pedido " + str(numero) + " de " + str(NUMERO_PEDIDOS))
        prioridade = ler_inteiro("Prioridade (1 a 5, sendo 1 a mais urgente): ", ler)
        tempo = ler_inteiro("Tempo estimado de resolução (minutos): ", ler)
        if not prioridade_valida(prioridade):
            print("Prioridade inválida. Não aceito valores fora de 1 a 5.")
            continue
        if not tempo_valido(tempo):
            print("Tempo inválido. Não aceito tempos iguais ou inferiores a zero.")
            continue
        pedidos.append((prioridade, tempo))
    return pedidos


def formatar_resumo(resultado):
    media = resultado["media"]
    if media == int(media):
        media_texto = str(int(media))
    else:
        media_texto = str(media)
    linhas = [
        "Pedidos urgentes: " + str(resultado["urgentes"]),
        "Total de minutos: " + str(resultado["total_minutos"]),
        "Média: " + media_texto,
        "Maior estimativa: " + str(resultado["maior_estimativa"]),
        "Classificação: " + resultado["classificacao"],
    ]
    return "\n".join(linhas)


def main(ler=None):
    if ler is None:
        ler = input
    pedidos = recolher_pedidos(ler)
    resultado = analisar_pedidos(pedidos)
    print(formatar_resumo(resultado))
    return resultado


if __name__ == "__main__":
    main()
