from ply import yacc
# BNF gramma
from anytree import Node
from syntatic.arvore import Arvore


# Sub-árvore.
#       (programa)
#           |
#   (lista_declaracoes)
#     /     |      \
#   ...    ...     ...

class Syntactic:
	def __init__(self, code, toke):
		""" Syntactic analysis|
		Rules for the compiler
		:param code: Code to be analysed
		:param toke: List of token from lexicon
		"""
		self.tokens = toke
		self.code = code
		print(self.tokens)
		# List of rules for precedence to resolve ambiguity, especially in expression grammars
		self.precedence = (
			('left', 'IGUAL', 'MAIORQ', 'MAIOR', 'MENORQ', 'MENOR'),
			('left', 'SOMA', 'SUB'),
			('left', 'DIVISAO', 'VEZES'),
		)
		self.st = ""
		self.tree = Node("root")

	# Parser build.
	def parser(self):
		parser = yacc.yacc(debug=True, start='programa', check_recursion=True, module=self, optimize=True)
		self.st = parser.parse(self.code)
		return self.tree

	def p_programa(self, p):
		'''
		programa : lista_declaracoes
		'''
		p[0] = Arvore('programa', [p[1]])

	def p_lista_declaracoes(self, p):
		'''
		lista_declaracoes : lista_declaracoes declaracao
		| declaracao
		'''
		if len(p) == 3:
			p[0] = Arvore('lista_declaracoes', [p[1], p[2]])
		elif len(p) == 2:
			p[0] = Arvore('lista_declaracoes', [p[1]])

	def p_declaracao(self, p):
		'''
		declaracao : declaracao_variaveis
		| inicializacao_variaveis
		| declaracao_funcao
		'''
		p[0] = Arvore('declaracao', [p[1]])

	def p_declaracao_variaveis(self, p):
		'''
		declaracao_variaveis : tipo DOISPONTOS lista_variaveis
		'''
		p[0] = Arvore('declaracao_variaveis', [p[1], p[3]])

	def p_inicializacao_variaveis(self, p):
		'''
		inicializacao_variaveis : ATRIBUICAO
		'''
		p[0] = Arvore('inicializacao_variaveis', [p[1]])

	def p_lista_variaveis(self, p):
		'''
		lista_variaveis : lista_variaveis VIRGULA var
		| var
		'''
		if len(p) == 4:
			p[0] = Arvore('lista_variaveis', [p[1], p[3]])
		elif len(p) == 2:
			p[0] = Arvore('lista_variaveis', [p[1]])

	def p_var(self, p):
		'''
		var : ID
		| ID indice
		'''
		if len(p) == 2:
			p[0] = Arvore('var', [], p[1])
		elif len(p) == 3:
			p[0] = Arvore('var', [p[2]], p[1])

	def p_indice(self, p):
		'''
		indice : indice ACOLCHETE expressao FCOLCHETE
		| ACOLCHETE expressao FCOLCHETE
		'''
		if len(p) == 5:
			p[0] = Arvore('indice', [p[1], p[3]])
		elif len(p) == 4:
			p[0] = Arvore('indice', [p[2]])

	def p_tipo(self, p):
		'''
		tipo : INTEIRO
		| FLUTUANTE
		'''
		p[0] = Arvore(p[1], [], p[1])

	def p_declaracao_funcao(self, p):
		'''
		declaracao_funcao : tipo cabecalho
		| cabecalho
		'''
		if len(p) == 3:
			p[0] = Arvore('declaracao_funcao', [p[1], p[2]])
		elif len(p) == 2:
			p[0] = Arvore('declaracao_funcao', [p[1]])

	def p_cabecalho(self, p):
		'''
		cabecalho : ID APAREN lista_parametros FPAREN corpo FIM
		'''
		p[0] = Arvore('cabecalho', [p[3], p[5]], p[1])

	def p_lista_parametros(self, p):
		'''
		lista_parametros : lista_parametros VIRGULA parametro
		| parametro
		| vazio
		'''
		if len(p) == 4:
			p[0] = Arvore('lista_parametros', [p[1], p[3]])
		elif len(p) == 2:
			p[0] = Arvore('lista_parametros', [p[1]])

	def p_parametro(self, p):
		'''
		parametro : tipo DOISPONTOS ID
		| ID
		'''
		if len(p) == 4:
			p[0] = Arvore('parametro', [p[1]], p[3])
		else:
			p[0] = Arvore('parametro', [], p[1])

	def p_parametro2(self, p):
		'''
		parametro : parametro ACOLCHETE FCOLCHETE
		'''
		p[0] = Arvore('parametro', [p[1]])

	def p_corpo(self, p):
		'''
		corpo : corpo acao
		| vazio
		'''
		if len(p) == 3:
			p[0] = Arvore('corpo', [p[1], p[2]])
		elif len(p) == 2:
			p[0] = Arvore('corpo', [p[1]])

	def p_acao(self, p):
		'''
		acao : expressao
		| declaracao_variaveis
		| se
		| repita
		| leia
		| escreva
		| retorna
		| error
		'''
		p[0] = Arvore('acao', [p[1]])

	def p_se(self, p):
		'''
		se : SE expressao ENTAO corpo FIM
		| SE expressao ENTAO corpo SENAO corpo FIM
		'''
		if len(p) == 6:
			p[0] = Arvore('se', [p[2], p[4]])
		elif len(p) == 8:
			p[0] = Arvore('se', [p[2], p[4], p[6]])

	def p_repita(self, p):
		'''
		repita : REPITA corpo ATE expressao
		'''
		p[0] = Arvore('repita', [p[2], p[4]])

	def p_atribuicao(self, p):
		'''
		atribuicao : var ATRIBUICAO expressao
		'''
		p[0] = Arvore('atribuicao', [p[1], p[3]])

	def p_leia(self, p):
		'''
		leia : LEIA APAREN ID FPAREN
		'''
		p[0] = Arvore('leia', [], p[3])

	def p_escreva(self, p):
		'''
		escreva : ESCREVA APAREN expressao FPAREN
		'''
		p[0] = Arvore('escreva', [p[3]])

	def p_retorna(self, p):
		'''
		retorna : RETORNA APAREN expressao FPAREN
		'''
		p[0] = Arvore('retorna', [p[3]])

	def p_expressao(self, p): # expressao_simples
		'''
		expressao : expressao_logica
		| atribuicao
		'''
		p[0] = Arvore('expressao', [p[1]])

	def p_expressao_logica(self, p):
		'''
		expressao_logica : expressao_simples
		| expressao_logica operador_logico expressao_simples
		'''
		if len(p) == 2:
			p[0] = Arvore('expressao_logica', [p[1]])
		elif len(p) == 4:
			p[0] = Arvore('expressao_logica', [p[1], p[2], p[3]])

	def p_operador_logico(self, p):
		'''
		operador_logico : ELOGICO
		| OULOGICO
		'''
		p[0] = Arvore('operador_logico', [], p[1])

	def p_expressao_simples(self, p):
		'''
		expressao_simples : expressao_aditiva
		| expressao_simples operador_relacional expressao_aditiva
		'''
		if len(p) == 2:
			p[0] = Arvore('expressao_simples', [p[1]])
		elif len(p) == 4:
			p[0] = Arvore('expressao_simples', [p[1], p[2], p[3]])

	def p_expressao_aditiva(self, p):
		'''
		expressao_aditiva : expressao_multiplicativa
		| expressao_aditiva operador_soma expressao_multiplicativa
		'''
		if len(p) == 2:
			p[0] = Arvore('expressao_aditiva', [p[1]])
		elif len(p) == 4:
			p[0] = Arvore('expressao_aditiva', [p[1], p[2], p[3]])

	def p_expressao_multiplicativa(self, p):
		'''
		expressao_multiplicativa : expressao_unaria
		| expressao_multiplicativa operador_multiplicacao expressao_unaria
		'''
		if len(p) == 2:
			p[0] = Arvore('expressao_multiplicativa', [p[1]])
		elif len(p) == 4:
			p[0] = Arvore('expressao_multiplicativa', [p[1], p[2], p[3]])

	def p_expressao_unaria(self, p):
		'''
		expressao_unaria : fator
		| operador_unario fator
		'''
		if len(p) == 2:
			p[0] = Arvore('expressao_unaria', [p[1]])
		elif len(p) == 3:
			p[0] = Arvore('expressao_unaria', [p[1], p[2]])

	def p_operador_relacional(self, p):
		'''
		operador_relacional : MENOR
		| MAIOR
		| IGUAL
		| DIFERENCA
		| MENORQ
		| MAIORQ
		'''
		p[0] = Arvore('operador_relacional', [], p[1])

	def p_operador_soma(self, p):
		'''
		operador_soma : SOMA
		| SUB
		'''
		p[0] = Arvore('operador_soma', [], p[1])

	def p_operador_unario(self, p):
		'''
		operador_unario : SOMA
		| SUB
		| operador_negacao
		'''
		p[0] = Arvore('operador_unario', [], p[1])

	def p_operador_multiplicacao(self, p):
		'''
		operador_multiplicacao : VEZES
		| DIVISAO
		'''
		p[0] = Arvore('operador_multiplicacao', [], p[1])

	def p_operador_negacao(self, p):
		'''
		operador_negacao : NEGACAO
		'''
		p[0] = Arvore('operador_negacao', [], p[1])

	def p_fator(self, p):
		'''
		fator : APAREN expressao FPAREN
		| var
		| chamada_funcao
		| numero
		'''
		if len(p) == 4:
			p[0] = Arvore('fator', [p[2]])
		elif len(p) == 2:
			p[0] = Arvore('fator', [p[1]])

	def p_numero(self, p):
		'''
		numero : NUMINTEIRO
		| NUMFLUTUANTE
		| NOTCIENTIFICA
		'''
		p[0] = Arvore('numero', [], p[1])

	def p_chamada_funcao(self, p):
		'''
		chamada_funcao : ID APAREN lista_argumentos FPAREN
		'''
		p[0] = Arvore('chamada_funcao', [p[3]], p[1])

	def p_lista_argumentos(self, p):
		'''
		lista_argumentos : lista_argumentos VIRGULA expressao
		| expressao
		| vazio
		'''
		if len(p) == 4:
			p[0] = Arvore('lista_argumentos', [p[1], p[3]])
		elif len(p) == 2:
			p[0] = Arvore('lista_argumentos', [p[1]])

	def p_vazio(self, p):
		'''
		vazio :
		'''
		pass

	def p_error(self, p):
		if p:
			print('Error: Syntax ' + "At line " + str(p.lineno) + " TYPE " + p.type)
			exit(1)
			#raise SyntaxError(("At line " + str(p.lineno) + " TYPE " + p.type))
		else:
			#yacc.restart()
			print('Error: incomplete definitions')
			exit(1)

