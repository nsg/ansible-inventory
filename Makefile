SHELL=/bin/bash
DOCKER ?= docker
VERSION ?= 2.3.0

# Setup a test env in docker
docker-%:
	${DOCKER} run -ti -v ${PWD}:/wd \
		$(shell echo $@ | cut -d'-' -f2) bash -c ' \
		apt-get -y update \
		&& apt-get -y install \
			python-pip \
			python-dev \
			libffi-dev \
			libssl-dev \
		&& pip install ansible==${VERSION} \
		&& cd /wd \
		&& tests/test.sh \
		'

