
class text:

    def __init__(self, text, from_nick, to_nick):
        self.__text = text
        self.__sender = from_nick
        self.__recipient = to_nick

    def recover_state(self, text):
        self.__text = text[0]
        self.__sender = text[2]
        self.__recipient = text[3]


    def save_state(self, file):
        file.write("%s\n" % self.__text)
        file.write("%s\n" % self.__sender)
        file.write("%s\n" % self.__recipient)

    def equal(self, text, from_user, to_user):
        if (text == self.__text and from_user == self.__sender and to_user == self.__recipient):
            return True
        return False

       
    def print_text(self):
        print self.__sender,
        print(": "),
        print self.__text

    def get_text(self):
        return self.__text

    def set_text(self, text):
        self.__text = text
