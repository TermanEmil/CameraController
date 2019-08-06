class LazyDict(dict):
    def __getitem__(self, key):
        func = dict.__getitem__(self, key)
        
        if callable(func):
        	return func()

        return super().__getitem__(key)

    def __missing__(self, key):
        return '{' + key + '}'


class MyK:
	@property
	def k(self):
		print('hey')
		return 1


my_k = MyK()
my_dict = LazyDict({ 'k': lambda: my_k.k })

print('---{m}'.format_map(my_dict))
	