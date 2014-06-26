#
# create some post entries
# just for testing purposes.
#
#


from atest.models.post import Post

if __name__ == "__main__":
	p = Post()
	print(p.to_json())
	
	for i in range(0,10):
		p.author = "klaas"
		p.content = """Lorem ipsum dolor sit amet, ..."""
		p.title = "Breaking News " + str(i)
		p.create()
		