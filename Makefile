SHELL = /bin/bash

# Many recipes need to be run in the virtual environment, 
# so run them as $(INVENV) command
INVENV = source env/bin/activate ;

##
##  Virtual environment
##     
env:
	python3 -m venv  env
	($(INVENV) pip install -r requirements.txt )

##
## candidates list
##
Client/res/candidates.txt: 
	echo "You must have this file"

candidates:	Client/res/candidates.txt

##
## 
##
install:	env candidates

##
##
##
client_start:	env candidates
	($(INVENV) bash start_client.sh )

node_start: env candidates
	($(INVENV) bash start_node.sh )

# 'clean' and 'veryclean' are typically used before checking 
# things into git.  'clean' should leave the project ready to 
# run, while 'veryclean' may leave project in a state that 
# requires re-running installation and configuration steps
# 
clean:
	rm -f *.pyc */*.pyc
	rm -rf __pycache__

veryclean:
	make clean
	rm -rf env
	rm -rf */*.der
	rm -rf */*.dat



