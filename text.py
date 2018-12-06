
class text:

    def __init__(self, message, from_nick, to_nick):
        self.__message = message
        self.__sender = from_nick
        self.__recipient = to_nick

    def save_state(self, text):
        self.__message = text[0]
        self.__sender = text[2]
        self.__recipient = text[3]


    def recover_state(self, file):
        file.write("%s\n" % self.__message)
        file.write("%s\n" % self.__sender)
        file.write("%s\n" % self.__recipient)

       
    def print_text(self):
        print self.__sender,
        print(": ")
        print self.__message,

    def get_message(self):
        return self.__message

    def set_message(self, message):
        self.__message = message
