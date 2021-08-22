# Movie Town

## About
This is my Web Application project for UITSEC Internship. In 
this website you can search for different movies and tv shows. 
Explore their cast, director; see pictures of them and add them to 
your watchlist where you can get reminder to watch them. All the 
movies will be pulled from IMDb’s database.

You will be able to create an account and see all of your movies 
from watchlist. There will be other features for created accounts, 
like commenting on a movie or giving your own rating, marking 
a movie as watched etc. 

Different database applications will be used to provide better user 
experience. Such as Elasticsearch to make searching better or 
Redis to reduce loading times.
And more…

## The Design
I will try to design both HTML 
and CSS myself. If things get 
out of hand, I will try using 
Bootstrap and maybe different 
templates.

Interactive and eye-candy 
elements will be my main 
design idea. There will be things 
like blur and responsive design. 
Again, if I can not make these 
things, I will settle on a 
template. Since design is not my 
main problem here.

## The Technology
On my website users can create and login to their account. 
Most, if not all features will be only available if you login. All 
passwords and other sensitive info will be encrypted on the 
server.

Main database will be MongoDB. All the movies, users and 
other information will be stored there (locally). There will be 
Elasticsearch built on top of it. Search operations from the user 
will be from this database. The most common elements, like the 
logo and daily quotes etc. will be pulled from Redis cache. I will 
try to keep Redis synchronized with MongoDB. On the other 
hand, RabbitMQ will be used as an interface. All these CRUD 
operations are done as requests. These requests will be sent 
from ‘producers’ to ‘consumers’.

For example, when you create an account, your info will be on 
MondoDB. Unsensitive info, like profile picture, will be cached 
to Redis. Initially all movie data will be copied from MongoDB 
to Elasticsearch. If you search for a movie Elasticsearch will be 
used to find it. And all these operations will be sent from 
RabbitMQ producer to consumers.

Web security is not something I am good at, but I will try to 
make my website as bulletproof as I can. Sensitive info will be 
encrypted, and other basic security features will be applied.
There can be many different features of this website. I will come 
up with other creative and fun ways to interact with the data. 

Currently my main goal is to finish basic features like CRUD 
operations on movie and user database and creating accounts. 
After that I will improve on the system by adding features and 
making everything prettier.