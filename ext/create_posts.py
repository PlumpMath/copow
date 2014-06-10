#
# create some post entries
# just for testing purposes.
#
#


from atest.models.post import Post

if __name__ == "__main__":
	p = Post()
	
	p.schema
	
	for i in range(0,10):
		p.author = "klaas"
		p.content = """
				Lorem ipsum dolor sit amet, consetetur sadipscing elitr, 
				sed diam nonumy eirmod tempor invidunt ut labore et dolore magna 
				aliquyam erat, sed diam voluptua. At vero eos et accusam et justo 
				duo dolores et ea rebum. Stet clita kasd gubergren, no sea 
				takimata sanctus est Lorem 
				"""
		p.title = "Breaking News " + str(i)
		p.save()
		