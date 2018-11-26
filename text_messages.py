import text as tx

class text_messages:

    def __init__(self, list_of_message):
        self.texts = list_of_message

    def add_message(self, text, from_user, to_user, ID):
        message = tx.text(text, ID, from_user, to_user)
        self.texts.append(message)
        self.texts.sort
        return 0

    def show_messages(self):
        for text in self.texts:
            if(not text.seen):
                print(text.sender),
                print(": "),
                print(text.message)
                text.seen = True
        return 0

    def show_message(message_ID):
        return 0

    def loggout(self, file):
        for text in self.texts:
            text.loggout(file)

    def loggin(self, fil):
        text = fil.readline()

        while(text != ""):
            for i in range(0, 3):
                from_user = fil.readline().rstrip('\n')
                to_user = fil.readline().rstrip('\n')
                ID = int(fil.readline().rstrip('\n'))
                self.add_message(text.rstrip('\n'), from_user, to_user, ID)
                text = fil.readline()
                
        
        
        
