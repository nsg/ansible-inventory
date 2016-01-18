SHELL=/bin/bash

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

.PHONY: test-latest test-devel
.PHONY: docker-test-latest
.PHONY: local-test-base
