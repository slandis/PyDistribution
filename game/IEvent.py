class IEvent(object):
    callbacks = None

    def on(self, event, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if event not in self.callbacks:
            self.callbacks[event] = [callback]
        else:
            self.callbacks[event].append(callback)
    
    def fire(self, event, *args):
        if self.callbacks is not None and event in self.callbacks:
            for callback in self.callbacks[event]:
                callback(self, *args)