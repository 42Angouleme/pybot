
def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Le fichier '{filename}' est introuvable.")

def parse():
    print("")

# def check_API():
#     print("")

def transmit_to_API():
    print("")

def receive_from_API():
    print("")


def run():
    # print("Hello Module (open)IA")
    filename = "test.txt"
    content = read_file(filename)
    try:
        parse(content) != True
    except WrongString: errrrrrrror
            print ()
    # check_API()
    transmit_to_API()
    receive_from_API()
    return None
    # modifier None par reponse fournie par chatGPT

# input
# parsing
# check la connexion à l'API (la faire)
# check du sujet de la question
# transmission
# reception
# check la reponse
# délivre un fichier