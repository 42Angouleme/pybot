from .IA import IA

def run():
    IA()

# def get_emotion(sentence: str, choices: list[str]):
#     choices_str = ", ".join(choices)
#     preprompt = f"""Pick one word from [ {choices_str} ] that fits well with the following sentence: {sentence}.
#     Answer only one word. Answer 'unknown' if you really can't find any match"""

#     reponse = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": preprompt},
#             {"role": "user", "content": sentence},
#         ],
#     )
#     emotion = reponse.choices[0].message.content
#     if not emotion in choices:
#         return "unknown"
#     return emotion

# def read_file(filename):
#     try:
#         with open(filename, "r") as file:
#             content = file.read()
#             return content
#     except FileNotFoundError:
#         print(f"Le fichier '{filename}' est introuvable.")

# def parse():
#     print("")

# def check_API():
#     print("")

# def transmit_to_API():
#     print("")

# def receive_from_API():
#     print("")


# def run():
#     # print("Hello Module (open)IA")
#     filename = "test.txt"
#     content = read_file(filename)
#     try:
#         parse(content) != True
#     except WrongString: errrrrrrror
#             print ()
#     # check_API()
#     transmit_to_API()
#     receive_from_API()
#     return None
#     # modifier None par reponse fournie par chatGPT

# input
# parsing
# check la connexion à l'API (la faire)
# check du sujet de la question
# transmission
# reception
# check la reponse
# délivre un fichier

#if __name__ == "__main__":
#    run(question)
