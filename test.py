#
#
#
import datetime
import os
from copow.models.comment import Comment
from copow.models.post import Post

if __name__ == "__main__":
	c = Comment()
	p = Post()
	p.schema
	p.has_many(c)