
class text:

    def __init__(self, message, ID, from_user, to_user):
        self.message = message
        self.message_ID = ID
        self.sender = from_user
        self.recipient = to_user
        self.seen = False

    def loggin(self, text):
        self.message = text[0]
        self.message_ID = int(text[1])
        self.sender = text[2]
        self.recipient = text[3]
        self.seen = bool(text[4])


    def loggout(self, file):
        file.write("%s\n" % self.message)
        file.write("%s\n" % self.sender)
        file.write("%s\n" % self.recipient)        
        file.write("%d\n" % self.message_ID)
        #file.write("%d\n" % self.seen)

       
    def print_text_info(self):
        print self.message,
        print self.message_ID,
        print self.sender,
        print self.recipient,
        print self.seen
