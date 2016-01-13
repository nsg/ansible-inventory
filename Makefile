test-ansible1:
	pip install ansible==1.9.3
	tests/test.sh

test-latest:
	pip install ansible
	tests/test.sh

test-devel:
	git clone https://github.com/ansible/ansible.git
	cd ansible \
		&& git checkout stable-2.0 \
		&& git submodule update --init --recursive \
		&& make install
	tests/test.sh
