# Some new ideas for PoW

## And a [new repo for that on bitbucket](https://bitbucket.org/pythononwheels/copow)

## Still in the early beginnings but current work in progress. 
I work currently more on this one than on standard PoW...

## Idea is basically to make PoW with:

* MongoDB backend
* DB <---> json <---> **PoW core (coroutines)** <--> json <---> views

The coroutine idea is based on the great presentation from [dabeaz](http://www.dabeaz.com/) on [on that topic and much much more ... read it !!!!:](http://www.dabeaz.com/coroutines/Coroutines.pdf) 

## Why

* **Document oriented DBs are a good choice for most of
the small to medium web based projects** (for which Pow is intended)
* the "json to the backend and json to the frontend" approach **decouples PoW
from any specific backend** persistend storage **and frontend** template engine
* **coroutines** instead of Object Oriented Approach **will be faster and will enable a more natural feeling by implementing a processing chain.** (I'll make a separate post on that but have a look at this [great presentation on generators and coroutines:](http://www.dabeaz.com/coroutines/Coroutines.pdf) 


## PoW for SQL will evolve as well

I will definetly also update PoW for SQL. The idea is to give Pow for MongoDB and PoW for SQL (almost) the same behaviour. And to make it as interchangable as possible. There will be a gap, though, since it woulnd't make any sence to equallize the different opportunities of SQL and NoSQL by software.

You should know yourself when to choose either one or the other. 

But Anyway, since I think that the freedom of document oriented DBs also has drawbacks when developing prod applications I will give PoW for MongoDB a small layer of schema definition, migrations and relations in the PoW Framework.

That was also on reason to test something like the [typecheck decorator](https://github.com/pythononwheels/icanhastypecheck).
The Freedom of Mongo is amazing and pretty good to have, but sometimes I like to ensure some things ebfore adding them silently to the DB ;)

(see the  typo ? Mongo would have silently added that to your DB ....)




