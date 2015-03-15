# ansible-intentory

[![Build Status](https://travis-ci.org/nsg/ansible-intentory.svg?branch=master)](https://travis-ci.org/nsg/ansible-intentory)

Define your Ansible inventory in YAML, with a lot of fancy features.

I wrote this script because I have hundreds of hosts saved int the 
default Ansible inventory format. We have structured them to multiple 
files and grouped them to different directories to keep the volume 
down but still we have plenty of groups and it is hard to get a good 
overview and mistakes do happen.

We considered to use a completely dynamic inventory management system 
with a fancy web interface and a REST based API that a simple python 
script talks to. This script is another take to that, everything is 
still saved in plain text in YAML-files checked in to the repository.

Basically, I got a little inspiration and I had to write this and test
it out.

## Example

You can turn this ...

```ini

[db:children]
sto
lon

[db:vars]
db_name=foo

[lon]
lon-db02.mycorp.ltd

[sto:vars]
db_name=bar

[sto]
sto-db01.mycorp.ltd
sto-db02.mycorp.ltd

```

```yaml
---

- hosts: db:&sto
  tasks:
    - debug: msg="Hello STO!"

```

... to this:

```yaml
---

groups:
  - sto-db01.mycorp.ltd
  - sto-db02.mycorp.ltd
  - lon-db02.mycorp.ltd

vars:
  db:
    - db_name=foo
  sto:
    - db_name=bar

```

```yaml
---

- hosts: db:&sto
  tasks:
    - debug: msg="Hello STO!"

```

Try someting a little more complex, lets assume that the 02's are db slaves:

```yaml
---

groups:
  - sto-db01.mycorp.ltd
  - sto-db02.mycorp.ltd
  - lon-db02.mycorp.ltd

vars:
  db:
    - db_name=foo
  sto:
    - db_name=bar
  dbslave:
    - db_slave=true

matcher:
  - regexp: 'db02'
    groups:
	  - dbslave

```

```yaml
---

- hosts: db:&sto
  tasks:
    - debug: msg="Hello STO!"

```
