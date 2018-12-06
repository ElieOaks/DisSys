import text as tx

class text_messages:

    def __init__(self, list_of_message):
        self.texts = list_of_message

    def add_text(self, text, from_nick, to_nick):
        message = tx.text(text, from_nick, to_nick)
        self.texts.append(message)
        return message

    def add_text_print(self, text, from_nick, to_nick):
        message = tx.text(text, from_nick, to_nick)
        self.texts.append(message)
        message.print_text()
        return message

    def add_message(self, message):
        self.texts.append(message)
        message.print_text()

    def show_messages(self):
        for text in self.texts:
            text.print_text()
            

    def save_state(self, file):
        for text in self.texts:
            text.save_state(file)

    def recover_state(self, fil):
        text = fil.readline()
        while(text != ""):
            for i in range(0, 2):
                from_user = fil.readline().rstrip('\n')
                to_user = fil.readline().rstrip('\n')
                self.add_text(text.rstrip('\n'), from_user, to_user)
                text = fil.readline()
                
        
        
        
