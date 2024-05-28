import os
from openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts.prompt import PromptTemplate

from .. import ensure


class ChatBot:

    def __init__(self, emotion_list: list[str]):
        """
            Set connection with AI API (ChatGpt 3.5 turbo)
            Do not forget to add .env with OPENAI_API_KEY and OPENAI_API_ORG_ID
        """
        if (os.getenv("OPENAI_API_KEY") == None or os.getenv("OPENAI_API_ORG_ID") == None):
            ensure.err(
                "OPENAI_API_KEY or OPENAI_API_ORG_ID are missing from the environment.", "en")
            raise Exception("")
        self.__chatGPT: ChatOpenAI = None
        self.__memory: ConversationSummaryBufferMemory = None
        self.__template = """ """
        self.__conversation: ConversationChain = None
        self.__emotion_list: list[str] = emotion_list

    @ensure.no_conversation("en")
    def start_conversation(self):
        """
        Starts a conversation with the robot.

        This method initializes the necessary components for a conversation with the robot.

        It checks if another discussion is already underway and returns an error message if so.

        Otherwise, it sets up the chatGPT instance, memory, and template for the conversation.

        If no conversation has been started with the robot, an error message is displayed.

        Parameters:
        -----------
            None

        Returns:
        --------
            None
        """
        self.__chatGPT = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv(
            "OPENAI_API_ORG_ID"), model_name="gpt-3.5-turbo")
        self.__memory = ConversationSummaryBufferMemory(
            llm=self.__chatGPT, max_token_limit=256)
        try:
            prompt_file = open("prompt.txt", "r")
            if prompt_file is not None:
                file_content = prompt_file.read()
        except Exception:
            file_content = ""
        self.__template = file_content + """
        Current conversation:
        {history}
        Human: {input}
        """
        PROMPT = PromptTemplate(
            input_variables=["history", "input"], template=self.__template)
        self.__conversation = ConversationChain(
            llm=self.__chatGPT, prompt=PROMPT, memory=self.__memory)

    @ensure.no_conversation("fr")
    def demarrer_discussion(self):
        """
        Démarre une discussion avec le robot.

        Cette méthode permet de démarrer une nouvelle discussion avec le robot.

        Si une discussion est déjà en cours, un message d'erreur est affiché.

        Paramètres:
        -----------
            Aucun.

        Retour:
        -------
            Aucun.
        """
        self.start_conversation()

    def stop_conversation(self):
        """
        Stops the conversation and resets the robot's internal state.

        This method sets the chatGPT, memory, template, and conversation variables to None,
        effectively stopping the ongoing conversation and clearing the robot's memory.

        If no conversation has been started with the robot, an error message is displayed.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        self.__chatGPT = None
        self.__memory = None
        self.__template = """ """
        self.__conversation = None

    def arreter_discussion(self):
        """
        Arrête la discussion en cours avec le robot.

        Si une discussion est déjà en cours, un message d'erreur est affiché.

        Paramètres:
        ----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.stop_conversation()

    @ensure.conversation("en")
    def ask_question(self, question: str) -> str:
        """
        Ask a question to the robot and get a response.

        If no conversation has been started with the robot, an error message is displayed.

        Args:
        -----
            question (str): The question to ask.

        Returns:
        --------
            str: The response from the robot.
        """
        if (question is None):
            ensure.msg["en"]["no_questoin"]
            return ''
        completion = self.__conversation.predict(input=question)
        return completion

    @ensure.conversation("fr")
    def poser_question(self, question: str) -> str:
        """
        Pose une question au robot et retourne la réponse.

        Si une discussion est déjà en cours, un message d'erreur est affiché.

        Paramètres:
        -----
            question (str): La question à poser au robot.

        Retour:
        --------
            str: La réponse du robot à la question posée.
        """
        if (question is None):
            ensure.msg['fr']['no_question']
            return

        return self.ask_question(question)

    @ensure.conversation("en")
    def get_conversation_history(self) -> str:
        """
        Get the conversation history.

        If no conversation has been started with the robot, an error message is displayed.

        Args:
        -----
            None

        Returns:
        --------
            str: The conversation history.
        """
        messages = self.__memory.chat_memory.messages
        prev_summary = self.__memory.moving_summary_buffer
        next_summary = self.__memory.predict_new_summary(
            messages, prev_summary)
        return next_summary

    @ensure.conversation("fr")
    def obtenir_historique_conversation(self) -> str:
        """
        Obtenez l'historique de la conversation.

        Si une discussion est déjà en cours, un message d'erreur est affiché.

        Paramètres:
        -----------
            None

        Retour:
        -------
            str: L'historique de la conversation.
        """
        return self.get_conversation_history()

    @ensure.conversation("en")
    def load_conversation_history(self, summary: str | None):
        """
        Load the conversation history.

        If no conversation has been started with the robot, an error message is displayed.

        Args:
        -----
            summary (str): The conversation history to set.

        Returns:
        --------
            None
        """
        if summary is None:
            summary = ""
        self.__memory.clear()
        self.__memory.moving_summary_buffer = summary

    @ensure.conversation("fr")
    def charger_historique_conversation(self, resumer: str | None):
        """
        Charge l'historique de la conversation.

        Si une discussion est déjà en cours, un message d'erreur est affiché.

        Paramètres:
        -----------
            summary (str): L'historique de la conversation à définir.

        Retour:
        -------
            Aucun
        """
        self.load_conversation_history(resumer)

    @ensure.conversation("en")
    def clear_conversation_history(self):
        """
        Clear the conversation history.

        If no conversation has been started with the robot, an error message is displayed.

        Args:
        -----
            None

        Returns:
        --------
            None
        """
        self.__memory.clear()

    @ensure.conversation("fr")
    def effacer_historique_conversation(self):
        """
        Efface l'historique de la conversation.

        Si une discussion n'a pas été démarrée avec le robot, un message d'erreur est affiché.

        Paramètres:
        -----------
            Aucun

        Retour:
        -------
            Aucun
        """
        self.clear_conversation_history()

    def get_emotion(self, sentence: str) -> str:
        """
        Get the emotion associated with a given sentence.

        Args:
        -----
            sentence (str): The input sentence from which the emotion needs to be determined.

        Returns:
        --------
            str: The emotion associated with the sentence. Returns 'Neutre' if no match is found.
        """
        if (sentence is None):
            ensure.msg['en']["is_empty"]("sentence")
            return ''
        choices_str = ", ".join(self.__emotion_list)
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        # openai.organization = os.getenv("OPENAI_API_ORG_ID")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                        organization=os.getenv("OPENAI_API_ORG_ID"))
        preprompt = f"""Pick the word from [ {choices_str} ] that fits the best the emotion would have when reading the following sentence: {sentence}.
        Answer only one word. Answer 'reflexion' if you really can't find any match"""
        # reponse =  openai.ChatCompletion.create(
        reponse = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": preprompt},
                {"role": "user", "content": sentence},
            ],
        )

        emotion = reponse.choices[0].message.content
        if emotion not in self.__emotion_list:
            return "Neutre"

        return emotion

    def donner_emotion(self, phrase: str) -> str:
        """
        Obtenez l'émotion associée à une phrase donnée.

        Paramètres:
        ------------
            phrase (str): La phrase d'entrée à partir de laquelle l'émotion doit être déterminée.

        Retour:
        -------
            str: L'émotion associée à la phrase. Renvoie 'Neutre' si aucune correspondance n'est trouvée.
        """
        if (phrase is None):
            ensure.msg['fr']["is_empty"]('La phrase')
            return ''
        return self.get_emotion(phrase)

    ### Private Methode ###

    def _change_preprompt(self, new_preprompt: str):
        """
            Allows the user to change the basic AIs behaviour

            :param new_preprompt : (str)
        """
        new_preprompt += """
            Current conversation:
            {history}
            Human: {input}
            AI Assistant:
        """
        if (self.__chatGPT == None):
            print("No API connection started")
            return
        PROMPT = PromptTemplate(
            input_variables=["history", "input"], template=self.__template)
        self.__conversation.prompt = PROMPT
