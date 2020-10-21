import io
import os
import sys
import syntatic.arvore
from lexicon import lexicon
from syntatic import syntatict
from anytree.exporter import DotExporter, UniqueDotExporter
from anytree import Node, RenderTree
from ply import yacc
# test dirs #
test = "tests/"
lexicon_result = "lexicon-results/"
syntax_result = "syntax-result-tree/"
# start lexicon #
lexicon = lexicon.Lexica()


#  build lexicon - used for resetting the line counter #
def build():
	lexicon.build()
	lexicon.start_count()

# build lexicon #
#build()

def file_read():
	for file in os.listdir("tests"):
		if file.endswith(".tpp"):
			with io.open(test + file, 'r', encoding='utf8') as f:
				go = f.read()



# runs all tests in tests folder and write the lexicon results on lexicon-results folder
def run_tests():
	for file in os.listdir("tests"):
		if file.endswith(".tpp"):
			with io.open(test + file, 'r', encoding='utf8') as f:
				go = f.read()
			lexicon.lexer.input(go)
			print(go)
			print("File read " + file)
			while True:
				tok = lexicon.lexer.token()
				if not tok:
					break
				with io.open(lexicon_result + file + "_result", 'a', encoding='utf8') as j:
					j.write("Tipo:[" + tok.type + "]" " Valor:[%s]" % tok.value + " Linha:[%s]" % tok.lineno + "\n")
			print("Lexic ok")

			syn = syntatict.Syntactic(go, lexicon.tokens)
			syn.parser()

			orig_stdout = sys.stdout
			f = open(syntax_result + file + '_result.txt', 'w', encoding='utf8')
			sys.stdout = f
			syntatic.arvore.print_tree(syn.st)
			sys.stdout = orig_stdout
			f.close()

			build()
	print("Finished lexicon all test files")

#def run_syntax_test():



if __name__ == '__main__':
	build()

	#run_tests()

	with io.open('tests/somavet.tpp', 'r', encoding='utf8') as f:
		cod = f.read()
	syn = syntatict.Syntactic(cod, toke=lexicon.tokens)
	tree = syn.parser()
	syntatic.arvore.print_tree(syn.st)

	orig_stdout = sys.stdout
	f = open('syntax-result-tree/somavetor-result.txt', 'w', encoding='utf8')
	sys.stdout = f
	syntatic.arvore.print_tree(syn.st)
	sys.stdout = orig_stdout
	f.close()

	# for pre, fill, node in RenderTree(tree):
	# 	print("%s%s" % (pre, node.type))
	# UniqueDotExporter(tree).to_picture('tree.png')
