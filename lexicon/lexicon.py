import ply.lex as lex


# Class Lexica
class Lexica(object):

	def __init__(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

# List of reserved words
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

	# tokens
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

# Indentifica os IDs
	def t_ID(self, t):
		# regex pros acentos
		r"""[a-zA-ZÀ-ÿ_][a-zÀ-ÿ_0-9]*"""
		t.type = self.reserved.get(t.value, 'ID')
		t.lexer.id_count += 1
		return t

# Notaçao cientifica
	def t_NOTCIENTIFICA(self, t):
		r"""([+-]?(\d+)(.\d+)([eE][+|-]?(\d+)))"""
		return t

# Numero flutuante
	def t_NUMFLUTUANTE(self, t):
		r"""([+-]?\d+)?(\.(\d)+)|((\d)\.)"""
		return t

	# indentifica comentario
	def t_COMMENT(self, t):
		r"""\{[^}]*[^{]*\}.*"""
		pass

# Numero inteiro
	def t_NUMINTEIRO(self, t):
		r"""([+-]?\d+)"""
		t.lexer.num_count += 1
		t.value = int(t.value)
		return t

	#  new linha
	def t_newline(self, t):
		r"""\n+"""
		t.lexer.lineno += len(t.value)

	# A string containing ignored characters (spaces and tabs)
	t_ignore = ' \t'

	# Error handling rule
	def t_error(self, t):
		print("Illegal character '%s'" % t.value[0] + " Na linha %s" % self.lexer.lineno)
		t.lexer.skip(1)

	# counter for the number counter and id counter
	def start_count(self):
		self.lexer.num_count = 0
		self.lexer.id_count = 0

# build
	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)
