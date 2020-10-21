inteiro somavet(inteiro: vet[], inteiro: tam)
    inteiro: result
    result := 0
    inteiro: i
    i := 0

    repita
        result := result + vet[i]
        i := i + 1
    até i = tam - 1

    retorna(result)
fim

inteiro principal ()
    inteiro: t
    t := 4
    inteiro: v1[t]
    inteiro: x
    x := somavet(v1,t)
    retorna(0)
fim
