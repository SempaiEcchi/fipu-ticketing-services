class Template:
    def __init__(self, instance_id: str, subject, body):
        self.subject = subject
        self.body = body
        self.instance_id = instance_id


class FirstReceivedMailReply:
    def run(self):
        return Template()