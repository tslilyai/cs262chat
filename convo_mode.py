import thread
from window import Window

# TODO: Synchronization

TYPE_IND_MSG = 1
TYPE_GROUP_MSG = 1

def poll_for_messages(p, delay, window):
    messages = defaultdict(list)
    try:
        while(1):
            time.sleep(delay)
            if window.group_id is None:
                continue
            msgs = p.fetch_messages(window.group_id)
            # not logged in yet, just keep looping 
            if msgs[0][0] == None:
                # print on screen "not logged in, no messages"
                continue
            else:
                for m in msgs:
                    window.display.addOutputLine(m)
    except KeyboardInterrupt:
        exit(0)

class ConvoWindow(Window):
    def __init__(self, screen):
        super(ConvoWindow, self).__init__(screen)
        self.group_id = None
        thread.start_new_thread(poll_for_messages, (p, 1, self))

    def enter_convo_mode(self, group_id, to_name, tpe):
        self.group_id = group_id
        self.to_name = to_name
        self.tpe = tpe
        self.display.displayScreen()
        self.inputw.displayScreen()

    def new_command_handler(self, line):
        if self.tpe == TYPE_IND_MSG:
            ret = p.send_individual_message(self.to_name, line)
        else:
            ret = p.send_group_message(self.to_name, line)
        if ret == 'success!\n':
            self.display.addOutputLine(m)

