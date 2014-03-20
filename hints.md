
## python relative imports:

used for example in file lib\db_conn.py

[on stackoverflow](http://stackoverflow.com/questions/11536764/attempted-relative-import-in-non-package-even-with-init-py)

[PEP 0328](http://www.python.org/dev/peps/pep-0328/)

## MongoDB


#### Intro Videos

[Michael Stearn](https://www.youtube.com/watch?v=hU8rkNT6CVk)

#### Start

    mongod --dbpath d:\test\mongodb --rest

#### HTTP Browser access [on localhost](http://localhost:28017)

    http://localhost:28017

## Sublime Text 2 MarkDown preview

    STRG+Shift+P then insert "markdown preview"

full documentation [on github](https://github.com/revolunet/sublimetext-markdown-preview)

## Copow start as a module
chdir into one dir above copow: (../copow)

    python -m copow.simple_server


## copow Schema (migrations/schemas)

#### types (only currently implemented)

	* Text 	
	** possible additional attributes: unique=true|false,length=20, regex=r"[a-z]", default="abc"
	* int
	** possible additional attributes: unique=true|false,signed=true|false, default=0
	* Blob
	** possible additional attributes: default=None (None only possible default so far)
	* object
	** possible additional attributes: default=None (None only possible default so far)

#### Looks like this:


    #
    # schema for the post_model as an example
    # 

    post = {
    	"title"		: { "type"	: 	"Text",
    				    "unique"	:	"true",
    				    "default"	:	"klaas" },    	        
        "content"	: { "type"		:	"Text" }
    }