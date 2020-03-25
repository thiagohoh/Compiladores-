import io
import os
from lexicon import lexicon
# test dirs #
test = "tests/"
lexicon_result = "lexicon-results/"
# start lexicon #
lexicon = lexicon.Lexica()

#  build lexicon - used for resetting the line counter #
def build():
	lexicon.build()
	lexicon.start_count()

# build lexicon #
build()

# runs all tests in tests folder and write the lexicon results on lexicon-results folder
for file in os.listdir("tests"):
	if file.endswith(".tpp"):
		with io.open(test + file, 'r', encoding='utf8') as f:
			go = f.read()
		lexicon.lexer.input(go)
		while True:
			tok = lexicon.lexer.token()
			if not tok:
				break
			with io.open(lexicon_result + file + "_result", 'a', encoding='utf8') as j:
				j.write("Tipo:[" + tok.type + "]" " Valor:[%s]" % tok.value + " Linha:[%s]" % tok.lineno + "\n")
		build()

print("Finished lexicon all test files")

