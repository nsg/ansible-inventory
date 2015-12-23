test-release:
	pip install ansible
	tests/test.sh

test-devel:
	git clone https://github.com/ansible/ansible.git
	cd ansible \
		&& git checkout stable-2.0 \
		&& git submodule update --init --recursive \
		&& make install
	tests/test.sh
