""" Vérifie que @n soit bien un nombre entier ou + ou - l'infini.

    pre: @n, une chaine de caractères
    post: renvoie
      @b, un boolean, vrai si @n représente un nombre entier ou +/- infini, faux sinon
      @s, une chaine de caractères contenant un commentaire
"""
def is_integer(n):
    if n in ["+inf", "-inf", "inf"]:
        return True, "+ ou - infini"

    try:
        int(n)
        return True, "correct"
    except:
        return False, "{} n'est pas un nombre correct".format(n)

""" Vérifie que @set soit bien un ensemble de nombres entiers.

    pre: @set, une chaine de caractères
    post: renvoie
      @b, un boolean, vrai si @set représente un ensembles de nombres entiers, faux sinon
      @s, une chaine de caractères contenant un commentaire
"""
def is_set(set):
    if set == "{}":
        return True, "Ensemble vide"

    if set[0] != '{' or set[-1] != '}':
        return False, "L'ensemble {} ne commence pas par '{}' ou ne finit pas par '{}'".format(set, "{", "}")
    set = set[1:-1].split(';')
    for number in set:
        if not is_integer(number)[0]:
            return False, "{} n'est pas un nombre correct".format(number)
    return True, "correct"

""" Vérifie que @interval soit bien un intervalle.

    pre: @interval, une chaine de caractères
    post: renvoie
      @b, un boolean, vrai si @interval représente un intervalle, faux sinon
      @s, une chaine de caractères contenant un commentaire
"""
def is_simpleInterval(interval):

    if interval in ['R', 'N', 'Z', 'Q']:
        return True, "correct"

    if not interval[0] in '[]' or not interval[-1] in '[]':
        return False, "L'ensemble {} ne commence et ne finit pas par ] ou [".format(interval)

    numbers = interval[1:-1].split(';')

    if len(numbers) > 2:
        return False, "{} contient trop de nombres".format(interval)
    elif len(numbers) <= 1:
        return False, "{} ne contient pas de séparateur ';'".format(interval)

    if not is_integer(numbers[0])[0]:
        return False, "{} n'est pas un nombre correct".format(numbers[0])
    if not is_integer(numbers[1])[0]:
        return False, "{} n'est pas un nombre correct".format(numbers[1])

    if numbers[0] in ["+inf", "inf"]:
        return False, "l'ensemble {} n'existe pas".format(interval)
    elif numbers[1] == "-inf":
        return False, "l'ensemble {} n'existe pas".format(interval)
    elif numbers[0] == "-inf":
        if interval[0] != ']':
            return False, "l'infini ne doit pas être compris dans l'intervalle {}".format(interval)
    elif numbers[1] in ["+inf", "inf"]:
        if interval[-1] != '[':
            return False, "l'infini ne doit pas être compris dans l'intervalle {}".format(interval)

    elif int(numbers[0]) > int(numbers[1]):
        return False, "{}: la première borne est plus grande que la deuxième!".format(interval)
    elif int(numbers[0]) == int(numbers[1]):
        return False, "{}: les deux bornes sont égales! Utiliser un singleton ({}) à la place peut-être".format(interval, "{}")

    return True, "correct"

""" Vérifie que @interval soit bien un intervalle avec une exclusion d'un ensemble de nombres entiers.
    Vérifie aussi que les éléments exclus soient dans l'intervalle.

    pre: @interval, une chaine de caractères
    post: renvoie
      @b, un boolean, vrai si @interval représente un intervalle, faux sinon
      @s, une chaine de caractères contenant un commentaire
"""
def is_intervalExclu(interval):
    int_cpy = interval
    interval = interval.split('\\')
    if len(interval) != 2:
        return False, "{} n'est pas correct, il y a trop de symbole '\\'".format(int_cpy)
    if not is_simpleInterval(interval[0])[0]:
        return is_simpleInterval(interval[0])
    if not is_set(interval[1])[0]:
        return is_set(interval[1])

    if not interval[0] in ['R', 'N', 'Z', 'Q']:
        set = interval[1][1:-1].split(";")
        interval = interval[0][1:-1].split(";")
        n1 = interval[0]
        n2 = interval[1]

        if n1 != "-inf" and int(min(set, key=float)) <= int(n1):
            return False, "Le plus petit élément de l'ensemble est plus petit ou égal à {} dans {}".format(n1, int_cpy)
        if n2 != "+inf" and int(max(set, key=float)) >= int(n2):
            return False, "Le plus grand élément de l'ensemble est plus grand ou égal à {} dans {}".format(n2, int_cpy)

    return True, "correct"

""" Vérifie que @interval soit bien une union d'intervalles et d'ensembles avec possiblement des exclusions.

    pre: @interval, une chaine de caractères
    post: renvoie
      @b, un boolean, vrai si @interval représente une union, faux sinon
      @s, une chaine de caractères contenant un commentaire
"""
def is_interval(set):
    # @set is a string containing information about the subset
    # returns True if it is a subset or False if not

    if set == "":
        return False, "Vous n'avez rien répondu"

    set = set.replace(" ", "")
    set = set.replace("u", "U")

    intervals = set.split('U')

    for interval in intervals:
        if interval == "":
            return False, "Il y a trop de symboles 'U' dans votre expression"

        elif interval in ['R', 'N', 'Z', 'Q']:              # si c'est un ensemble spécial
            pass

        elif interval[0] == '{' and interval[-1] == '}':    # si c'est un ensemble discret
            if is_set(interval)[0] == False:
                return is_set(interval)

        elif interval[0] in '[]' and interval[-1] in '[]':  # si c'est un intervalle simple
            if is_simpleInterval(interval)[0] == False:
                return is_simpleInterval(interval)

        elif '\\' in interval:                              # si c'est un intervalle avec une exclusion
            if is_intervalExclu(interval)[0] == False:
                return is_intervalExclu(interval)

        else:
            return False, "{} n'est pas un intervalle correct".format(interval)

    return True, "correct"

""" Transforme la chaine de caractères représentant un intervalle avec une exclusion en une chaine
    de caractères contenant une union de plusieurs intervalles sans exclusions.

    pre: @interval, une chaine de caractère valide
    post: revoie
      @s, une chaine de caractère contenant la transformation en unions d'intervalles sans exclusions
"""
def expandExclu(interval):
    interval = interval.split('\\')
    set = interval[1]
    interval = interval[0]

    set = set[1:-1].split(";")
    set.sort(key=float)

    if interval == 'R':
        begin = ']'
        end = '['
        n1 = "-inf"
        n2 = "inf"
    else:
        begin = interval[0]
        end = interval[-1]
        interval = interval[1:-1].split(";")
        n1 = interval[0]
        n2 = interval[1]

    s = begin+n1+";" # ex: s = "]0;"
    for e in set:
        s = s + e + "[U]" + e + ";"
    s = s + n2 + end

    return s

""" Transforme la chaine de caractères représentant un ensemble d'entiers en une chaine
    de caractères contenant une union de plusieurs singletons.

    pre: @set, une chaine de caractère valide
    post: revoie
      @s, une chaine de caractère contenant la transformation en unions de singletons
"""
def expandSet(set):
    set = set[1:-1].split(';')
    s = ""
    for e in set:
        s = s + "{}{}{}U".format("{", e, "}")
    s = s[:-1]
    return s

""" Transforme la chaine de caractères représentant une union d'intervalles et d'ensembles avec
    possiblement des exclusions en une chaine de caractères contenant uniquement des unions d'intervalles
    et de singletons sans exclusions.

    pre: @interval, une chaine de caractère valide
    post: revoie
      @s, une chaine de caractère contenant la transformation en unions d'intervalles et de singletons
      sans exclusions
"""
def expandInterval(interval):

    interval = interval.replace(" ", "")
    interval = interval.replace("u", "U")
    interval = interval.replace("+inf", "inf")

    interval = interval.split("U")

    for i in range(len(interval)):
        if interval[i][0] == '{':
            interval[i] = expandSet(interval[i])

        if '\\' in interval[i]:
            interval[i] = expandExclu(interval[i])

    result = ""
    for e in interval:
        result = result + "{}U".format(e)
    return result[:-1]

""" Vérifie que @answer soit bien une unions d'intervalles équivalent à @expected

    pre:
      @answer: une chaine de caractères
      @expected: une chaine de caractères valide

    post: renvoie
      @b, un boolean, vrai si les deux arguments sont équivalent, faux sinon
      @s, une chaine de caractères contenant un commentaire
"""
def compareDomains(answer, expected):

    result = is_interval(answer)
    if not result[0]:
        return result

    answer = expandInterval(answer)
    expected = expandInterval(expected)

    answer = answer.split("U")
    expected = expected.split("U")

    for e in answer:
        if not e in expected:
            return False, "{} ne fait pas partie de la réponse".format(e)
    for e in expected:
        if not e in answer:
            return False, "Il vous manque des intervalles dans la réponse"

    return True, "correct"
