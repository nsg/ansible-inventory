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

docker-test-ansible1: local-test-ansible1
	docker run \
		-v $(PWD):/mnt \
		-ti local-test-ansible1 \
		make -C /mnt test-ansible1

docker-test-latest: local-test-latest
	docker run \
		-v $(PWD):/mnt \
		-ti local-test-latest \
		make -C /mnt test-latest

local-test-base:
	docker build \
		--build-arg HOST_USER_UID=$$UID \
		-t $@ - < dockerfiles/$@

local-test-%: local-test-base
	docker build -t $@ - < dockerfiles/$@

diff-output: local-test-ansible1 local-test-latest
	docker run \
		-v $(PWD):/mnt \
		-ti local-test-ansible1 \
		./inventory.py --file tests/test-group-vars/inventory.yml --list \
			> ansible1.out
	docker run \
		-v $(PWD):/mnt \
		-ti local-test-latest \
		./inventory.py --file tests/test-group-vars/inventory.yml --list \
			> latest.out


.PHONY: test-ansible1 test-latest test-devel
.PHONY: docker-test-ansible1 docker-test-latest
.PHONY: local-test-base diff-output
