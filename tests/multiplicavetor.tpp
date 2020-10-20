flutuante: v[100]
flutuante: v2[100]

multivet(inteiro: t)
	inteiro: i
	i := 0
	repita
		v2[i] = v[i] * 2
		i := i + 1
	até i = t
fim

inteiro principal()
	inteiro: i
	i := 0
	repita
		v[i] := i+1
		i := i + 1
	até i = 100

	multivet(100)
