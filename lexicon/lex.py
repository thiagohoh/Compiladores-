# -*- coding: utf-8 -*-
import ply.lex as lex
# -*- coding: utf-8 -*-
import io

reserved = {
	'se': "SE",
	u'então': 'ENTAO',
	u'senão': 'SENAO',
	u'até': 'ATE',
	'repita': 'REPITA',
	'flutuante': 'FLUTUANTE',
	'retorna': 'RETORNA',
	'leia': 'LEIA',
	'escreva': 'ESCREVA',
	'inteiro': 'INTEIRO',
	'fim': 'FIM'
}


#tokens
# APAREN ABRE PARENTS - FPAREN FECHA PARENT
tokens = [
	'SOMA',
	'SUB',
	'VEZES',
	'DIVISAO',
	'APAREN',
	'FPAREN',
	'ID',
	'VIRGULA',
	'DOISPONTOS',
	'ACOLCHETE',
	'FCOLCHETE',
	'NEGACAO',
	'MAIOR',
	'MENOR',
	'IGUAL',
	'MAIORQ',
	'MENORQ',
	'ATRIBUICAO',
	'ELOGICO',
	'OULOGICO',
	'DIFERENCA',
	'NUMFLUTUANTE',
	'NUMINTEIRO',
	'NOTCIENTIFICA',
	'COMMENT'
] + list(reserved.values())



# REGULAR EXPRESSION
t_SOMA = r'\+'
t_SUB = r'-'
t_VEZES = r'\*'
t_DIVISAO = r'/'
t_APAREN = r'\('
t_FPAREN = r'\)'
t_ATRIBUICAO = r'(\?<\!<|>|:|=)=(?!=)'
t_IGUAL = r'\='
t_NEGACAO = r'\!'
t_VIRGULA = r','
t_DOISPONTOS = r'\:'
t_DIFERENCA = r'<>'
t_ACOLCHETE = r'\['
t_FCOLCHETE = r'\]'
t_OULOGICO = r"\|\|"
t_ELOGICO = r'&&'
t_MAIOR = r'\>'
t_MENOR = r'\<'
t_MENORQ = r'\<='
t_MAIORQ = r'\>='


def t_ID(t):
	r"""[a-zA-ZÀ-ÿ_][a-zÀ-ÿ_0-9]*"""
	t.type = reserved.get(t.value, 'ID')
	t.lexer.id_count += 1
	return t


def t_NOTCIENTIFICA(t):
	r"""([+-]?(\d+)(.\d+)([eE][+|-]?(\d+)))"""
	return t

def t_NUMFLUTUANTE(t):
	r"""([+-]?\d+)?(\.(\d)+)|((\d)\.)"""
	return t

#indentifica comentario
def t_COMMENT(t):
	r"""\{[^}]*[^{]*\}.*"""
	pass


def t_NUMINTEIRO(t):
	r"""([+-]?\d+)"""
	t.lexer.num_count += 1
	t.value = int(t.value)
	return t


#  new linha
def t_newline(t):
	r"""\n+"""
	t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0] + " Na linha %s" % lexer.lineno)
	t.lexer.skip(1)


test = " até i < tam"
file = 'tests/teste-1.tpp'
with io.open(file, 'r', encoding='utf8') as f:
	textu = f.read()

lexer = lex.lex()
lexer.num_count = 0
lexer.id_count = 0
lexer.input(textu)


while True:
	tok = lexer.token()
	if not tok:
		break
	print("Tipo:[" + tok.type+"]" " Valor:[%s]" % tok.value + " Linha:[%s]" % tok.lineno)


print("Quantidade de Linhas [%s] " % lexer.lineno + "| Quantidade de numeros [%s]" % lexer.num_count + " | Quantidade de IDS [%s]" % lexer.id_count)

