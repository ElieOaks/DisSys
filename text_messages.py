import text as tx

class text_messages:

    def __init__(self, list_of_message):
        self.texts = list_of_message

    def add_message(self, message, from_nick, to_nick):
        message = tx.text(message, from_nick, to_nick)
        self.texts.append(message)

    def add_message_print(self, message, from_nick, to_nick):
        message = tx.text(message, from_nick, to_nick)
        self.texts.append(message)
        message.print_text()

    def show_messages(self):
        for text in self.texts:
            text.print_text()

    def show_last_messages(self):
        texts = reverse(self.texts)
        for i in range(0, 10):
            texts[i].print_text()

    def save_state(self, file):
        for text in self.texts:
            text.save_state(file)

    def recover_sate(self, fil):
        text = fil.readline()
        while(text != ""):
            for i in range(0, 2):
                from_user = fil.readline().rstrip('\n')
                to_user = fil.readline().rstrip('\n')
                self.add_message(text.rstrip('\n'), from_user, to_user)
                text = fil.readline()
                
        
        
        
