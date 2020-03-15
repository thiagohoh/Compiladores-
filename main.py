import lexicon
import io
lexicon = lexicon.Lexica()
lexicon.build()
lexicon.start_count()


file = 'tests/teste-1.tpp'
with io.open(file, 'r', encoding='utf8') as f:
	textu = f.read()

lexicon.lexer.input(textu)


while True:
	tok = lexicon.lexer.token()
	if not tok:
		break
	print("Tipo:[" + tok.type+"]" " Valor:[%s]" % tok.value + " Linha:[%s]" % tok.lineno)


