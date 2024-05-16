import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'ENTITE',
    'ADJECTIF',
    'PREDICAT',
    'DECLARATION'
)

def t_ENTITE(t):
    r'entité\s*:\s*\w+'
    t.value = t.value.split(':')[1].strip()
    return t

def t_ADJECTIF(t):
    r'adj\s*:\s*\w+\s*,\s*\w+'
    t.value = [adj.strip() for adj in t.value.split(':')[1].split(',')]
    return t

def t_PREDICAT(t):
    r'pred\s*:\s*\w+\s*,\s*\w+'
    t.value = [part.strip() for part in t.value.split(':')[1].split(',')]
    return t

def t_DECLARATION(t):
    r'\w+\s+est\s+\w+'
    t.value = t.value.split()
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Storage for entities, adjectives, and predicates
entites = {}
adjectifs = {}
predicats = {}

# Parser rules
def p_instructions(p):
    '''instructions : instruction
                    | instruction instructions'''
    pass

def p_instruction_entite(p):
    'instruction : ENTITE'
    entites[p[1]] = {}
    print(f"Entité créée : {p[1]}")

def p_instruction_adjectif(p):
    'instruction : ADJECTIF'
    adjectifs[p[1][0]] = p[1][1]
    adjectifs[p[1][1]] = p[1][0]
    print(f"Adjectifs ajoutés : {p[1][0]}, {p[1][1]}")

def p_instruction_predicat(p):
    'instruction : PREDICAT'
    entite, adj = p[1]
    if entite not in entites:
        print(f"Erreur : Entité {entite} non définie")
    else:
        entites[entite][adj] = True
        print(f"Prédicat ajouté : {entite} est {adj}")

def p_instruction_declaration(p):
    'instruction : DECLARATION'
    entite, _, adj = p[1]
    if entite in entites and adj in adjectifs:
        if any(contrary for contrary, val in entites[entite].items() if adjectifs[adj] == contrary):
            print(f"Erreur : {entite} ne peut pas être {adj} car il est déjà {adjectifs[adj]}")
        else:
            entites[entite][adj] = True
            print(f"Déclaration valide : {entite} est {adj}")
    else:
        print(f"Erreur : Entité ou adjectif non défini")

def p_error(p):
    print("Erreur de syntaxe!")

parser = yacc.yacc()

# Test Data
data = '''
entité: Jean
adj: beau, moche
pred: Jean, moche
Jean est beau
'''

lexer.input(data)
for tok in lexer:
    print(tok)

parser.parse(data)
