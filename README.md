# ansible-inventory

[![Build Status](https://travis-ci.org/nsg/ansible-inventory.svg?branch=master)](https://travis-ci.org/nsg/ansible-inventory)

Define your Ansible inventory in YAML, with a lot of fancy features.

I wrote this script because I have hundreds of hosts saved in the 
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

## Examples

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

... to this:

```yaml
---

groups:
  - sto-db01.mycorp.ltd
  - sto-db02.mycorp.ltd
  - lon-db02.mycorp.ltd

tagvars:
  db:
    db_name: foo
  sto:
    db_name: bar

```

Try someting a little more complex, lets assume that the 02's are db slaves:

```yaml
---

groups:
  - sto-db01.mycorp.ltd
  - sto-db02.mycorp.ltd
  - lon-db02.mycorp.ltd

tagvars:
  dbslave:
    db_slave: true

matcher:
  - regexp: 'db02'
    groups:
	  - dbslave

```

## Documentation

For Full documentation see [the wiki](https://github.com/nsg/ansible-inventory/wiki/)!
