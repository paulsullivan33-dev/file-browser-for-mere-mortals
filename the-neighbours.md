# The Neighbours

Reaching files on another machine is an
old need with several good answers, and
File Browser is only one of them. These
are characterisations from the projects'
own documentation, not benchmarks; the
lab ran File Browser only. Four of the
neighbours have their own guides in
this series, and are pointed to where
they stand.

## SSH and SFTP: the login that is also a door

Every Linux server already carries this
one. SSH gives a person a shell on the
machine, and its sibling SFTP carries
files over the same connection — most
graphical file managers can browse an
SFTP address like a local folder. The
strengths are maturity, encryption, and
presence: it is already installed, and
it will be patched for years to come.
The cost is the shape of the key: an
SSH account is an account *on the
machine*, with a home folder and a
shell, and fencing it into one folder
with some verbs missing is possible but
fiddly. File Browser exists precisely
in that gap — its accounts are
store-only, scoped and switched per
person, and mean nothing to the machine
beneath. [SSH for Mere
Mortals](https://paulsullivan33-dev.github.io/ssh-for-mere-mortals/)
teaches the neighbour itself.

## Samba and NFS: the folder that pretends to be local

The network-share protocols make a
server's folder appear *inside* the
client machine, as a drive letter or a
mounted directory, so programs open and
save files on it as if it were their
own disk. For a household editing
documents where they live, that illusion
is better than any browser page. The
prices are setup on both ends, protocols
that chat a great deal and prefer a
local network, and permissions that are
the machine's own, with the same
all-or-nothing flavour as SSH's. File
Browser asks nothing of the client but
a browser, and reaches people a share
cannot — a friend, once, for one file,
chapter 7's whole point. [Samba and NFS
for Mere
Mortals](https://paulsullivan33-dev.github.io/samba-and-nfs-for-mere-mortals/)
covers the protocols.

## Syncthing: the copier, not the door

Syncthing answers a different question:
not "let me reach the files" but "keep
these folders the same on all my
machines". It replicates, continuously
and without a server at the centre, and
it is superb at it. It is not a way to
*visit* a folder: there is no casual
browsing of a tree you did not choose to
copy, no guest link, no per-person
corner of someone else's disk. Houses
often want both — Syncthing keeping the
working folders in step, File Browser
for reaching the archive — and nothing
about either prevents the other.
[Syncthing for Mere
Mortals](https://paulsullivan33-dev.github.io/syncthing-for-mere-mortals/)
is its guide.

## Nextcloud: the suite with a file room

Nextcloud is a whole platform — files,
calendars, contacts, office documents,
talk — of which file access is one
room. It is maintained, large, and
capable of everything in this guide and
far more: sharing with expiry and
passwords, per-user storage, guests.
The price is the platform itself: a
database server, a web server, updates
that are events. File Browser is the
opposite wager — one file, one database
file, five ideas (chapter 2) — and for
a household that wants only the file
room, the smaller wager is often the
right one. For a household that wants
the suite, or that cannot accept an
unmaintained program, Nextcloud's
ongoing maintenance is the decisive
argument, and chapter 11 would second
it. [Nextcloud for Mere
Mortals](https://paulsullivan33-dev.github.io/nextcloud-for-mere-mortals/)
takes the tour.

## A plain web server, and the download-only shelf

If the job is only *publishing* files
for reading — a folder of documents
anyone may fetch — a general web server
(Nginx, Caddy) with its directory
listing does it with fewer moving parts
and a maintenance stream behind it. It
has no logins, no uploads, no scopes, no
links to revoke: a shelf, not a door.
Several households find the shelf is
all they needed; the moment someone
must *add* a file, or a file must be
for one person's eyes, you are back to
a tool like this one — or to the shelf's
maintained cousins above.
