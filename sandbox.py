class Aba:
    def __init__(self, a):
        self.a = a

    def do_the_thing(self, b):
        print(self.a + b)


def run(func):
    func()


k = Aba(1)
kf = lambda: k.do_the_thing(2)

run(kf)