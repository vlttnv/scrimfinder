scrimfinder
=======

A web service for finding competitive e-sports teams to scrim with.

Issue legend
=======
core - needed for MVP  
basic - after core is 100%~ working  
advanced - after basic is 100%~ working  
database - data storage and manipulation  
enhancements - optimisation and sugar  
security - hashing stuff, closing holes etc  
bug - everything that does not work, even the little things  
testing - to be tested  


Requirements
=======
	python 2.x

	pip install sqlalchemy
	pip install sqlalchemy-migrate
	pip install flask-sqlalchemy
	pip install flask
	pip install requests
	pip install flask-openid  

Database Setup
=======
	python db_create.py
