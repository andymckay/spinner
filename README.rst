A playing around prototype. If you've got an AWS account, keys and security
groups set up then you might be able to set up a copy of the Firefox
Marketplace on AWS using the following commands::

  python cmds.py create

If that crashes (it might)::

  python cmds.py update --instance_id=INSTANCE_ID

Should continue it.

This is a prototype, do not use for anything serious (yet).
