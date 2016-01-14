SHELL=/bin/bash

test-ansible1:
	type ansible || pip install ansible==1.9.3
	tests/test.sh

test-latest:
	type ansible || pip install ansible
	tests/test.sh

test-devel:
	git clone https://github.com/ansible/ansible.git
	cd ansible \
		&& git checkout stable-2.0 \
		&& git submodule update --init --recursive \
		&& make install
	tests/test.sh

local-test-base:
	docker build \
		--build-arg HOST_USER_UID=$$UID \
		-t $@ - < dockerfiles/$@

local-test-ansible1: local-test-base
	docker build -t $@ - < dockerfiles/$@
	docker run \
		-v $(PWD):/mnt \
		-ti $@ \
		make -C /mnt test-ansible1

local-test-latest: local-test-base
	docker build -t $@ - < dockerfiles/$@
	docker run \
		-v $(PWD):/mnt \
		-ti $@ \
		make -C /mnt test-latest

.PHONY: test-ansible1 test-latest test-devel local-test-ansible1
