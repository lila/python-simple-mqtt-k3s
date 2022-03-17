# makefile to deploy secret keys into kubernetes cluster

create:
	kubectl create secret generic gcal-credentials --from-file ./secrets.py

delete:
	kubectl delete secret gcal-credentials