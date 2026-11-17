# -*- coding: utf-8 -*-
"""Testes da matriz do enunciado. Chamam main() e analisar_pedidos() reais."""

import io
import unittest
from contextlib import redirect_stdout

import programa


def executar(linhas):
    fila = iter(linhas)

    def ler(mensagem=""):
        try:
            return next(fila)
        except StopIteration as erro:
            raise AssertionError("Faltou entrada depois de: " + mensagem) from erro

    with redirect_stdout(io.StringIO()):
        resultado = programa.main(ler)
    resto = list(fila)
    if resto:
        raise AssertionError("Sobraram entradas: " + str(resto))
    return resultado


def pares_para_linhas(pares):
    linhas = []
    for prioridade, tempo in pares:
        linhas.append(str(prioridade))
        linhas.append(str(tempo))
    return linhas


class TesteGestaoPedidos(unittest.TestCase):
    def test_t1_normal(self):
        pares = [(1, 40), (2, 40)] + [(5, 40)] * 8
        resultado = executar(pares_para_linhas(pares))
        self.assertEqual(resultado["urgentes"], 2)
        self.assertEqual(resultado["total_minutos"], 400)
        self.assertEqual(resultado["media"], 40)
        self.assertEqual(resultado["maior_estimativa"], 40)
        self.assertEqual(resultado["classificacao"], "NORMAL")
        texto = programa.formatar_resumo(resultado)
        self.assertIn("Pedidos urgentes: 2", texto)
        self.assertIn("Classificação: NORMAL", texto)

    def test_t2_prioridade_invalida_nao_conta(self):
        # texto, prioridade 0 e prioridade 6 são recusados; só entram 10 prioridades 3
        linhas = ["abc", "0", "15", "6", "15"] + pares_para_linhas([(3, 20)] * 10)
        resultado = executar(linhas)
        self.assertEqual(resultado["urgentes"], 0)
        self.assertEqual(resultado["total_minutos"], 200)
        self.assertEqual(resultado["media"], 20)
        self.assertEqual(resultado["maior_estimativa"], 20)
        self.assertEqual(resultado["classificacao"], "NORMAL")

    def test_t3_tempo_invalido_nao_conta(self):
        linhas = ["4", "0", "4", "-5", "4", "xyz", "50"] + pares_para_linhas([(4, 50)] * 9)
        resultado = executar(linhas)
        self.assertEqual(resultado["urgentes"], 0)
        self.assertEqual(resultado["total_minutos"], 500)
        self.assertEqual(resultado["media"], 50)
        self.assertEqual(resultado["maior_estimativa"], 50)
        self.assertEqual(resultado["classificacao"], "ELEVADA")

    def test_t4_fronteira_3_urgentes(self):
        pares = [(1, 10), (2, 10), (2, 10)] + [(3, 10)] * 7
        resultado = programa.analisar_pedidos(pares)
        self.assertEqual(resultado["urgentes"], 3)
        self.assertEqual(resultado["total_minutos"], 100)
        self.assertEqual(resultado["classificacao"], "ELEVADA")

    def test_t4_fronteira_5_urgentes(self):
        pares = [(1, 10)] * 5 + [(5, 10)] * 5
        resultado = programa.analisar_pedidos(pares)
        self.assertEqual(resultado["urgentes"], 5)
        self.assertEqual(resultado["total_minutos"], 100)
        self.assertEqual(resultado["classificacao"], "CRÍTICA")

    def test_t4_fronteira_480_minutos(self):
        pares = [(1, 48), (2, 48)] + [(5, 48)] * 8
        resultado = programa.analisar_pedidos(pares)
        self.assertEqual(resultado["urgentes"], 2)
        self.assertEqual(resultado["total_minutos"], 480)
        self.assertEqual(resultado["classificacao"], "NORMAL")

    def test_t4_fronteira_481_minutos(self):
        pares = [(1, 49), (2, 48)] + [(5, 48)] * 8
        resultado = programa.analisar_pedidos(pares)
        self.assertEqual(resultado["total_minutos"], 481)
        self.assertEqual(resultado["urgentes"], 2)
        self.assertEqual(resultado["classificacao"], "ELEVADA")

    def test_t4_fronteira_600_minutos(self):
        pares = [(1, 60), (2, 60)] + [(5, 60)] * 8
        resultado = programa.analisar_pedidos(pares)
        self.assertEqual(resultado["total_minutos"], 600)
        self.assertEqual(resultado["urgentes"], 2)
        self.assertEqual(resultado["classificacao"], "ELEVADA")

    def test_t4_fronteira_601_minutos(self):
        pares = [(1, 61), (2, 60)] + [(5, 60)] * 8
        resultado = programa.analisar_pedidos(pares)
        self.assertEqual(resultado["total_minutos"], 601)
        self.assertEqual(resultado["classificacao"], "CRÍTICA")

    def test_t5_extremo_dez_urgentes_de_um_minuto(self):
        pares = [(1, 1)] * 10
        resultado = executar(pares_para_linhas(pares))
        self.assertEqual(resultado["urgentes"], 10)
        self.assertEqual(resultado["total_minutos"], 10)
        self.assertEqual(resultado["media"], 1)
        self.assertEqual(resultado["maior_estimativa"], 1)
        self.assertEqual(resultado["classificacao"], "CRÍTICA")

    def test_t6_regressao_prioridade_2_conta_como_urgente(self):
        self.assertTrue(programa.e_urgente(1))
        self.assertTrue(programa.e_urgente(2))
        self.assertFalse(programa.e_urgente(3))
        # A condição do colega (prioridade < 2) não conta a prioridade 2.
        self.assertFalse(2 < 2)
        pares = [(2, 1)] * 10
        resultado = programa.analisar_pedidos(pares)
        self.assertEqual(resultado["urgentes"], 10)
        self.assertEqual(resultado["classificacao"], "CRÍTICA")

    def test_rejeita_contagem_diferente_de_dez(self):
        with self.assertRaises(ValueError):
            programa.analisar_pedidos([(1, 10)] * 9)

    def test_rejeita_pedido_invalido_na_analise(self):
        pares = [(1, 10)] * 9 + [(1, 0)]
        with self.assertRaises(ValueError):
            programa.analisar_pedidos(pares)


if __name__ == "__main__":
    unittest.main()
