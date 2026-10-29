# What File Browser Is

You have a machine that holds files —
the spare PC that became the house
server, the little board that runs the
backups — and the files on it are only
reachable by sitting at its keyboard or
signing into its command line. Everyone
else in the house, and you yourself
from the sofa with a tablet, are locked
out of a folder you own.

**File Browser removes the lock, in a
controlled way.** It is a program that
runs on the machine holding the files
and serves a web page: a file manager
in the browser. You sign in with a user
name and password that belong to File
Browser — not to the machine — and you
see a folder tree. You can browse it,
search it, upload files into it,
download files from it, rename, edit
text files in the page, and hand out
links that let someone fetch one file
without any account at all. Under the
page sits an **API** — the same doors,
in program form — and this guide drives
both, because a claim you can repeat
from the command line is a claim you
can check.

The administrator decides two things
about every account, and between them
they are the whole safety story:

- the account's **scope** — which part
  of the tree is that person's whole
  world, presented to them as if it
  were the root; and
- its **permissions** — eight switches
  saying whether they may create,
  rename, modify, delete, share,
  download, run commands, or administer
  other users.

Chapter 6 builds such a fenced account
and then attacks the fence.

## The fact to know before the install

Ordinarily this is where a guide says
what a tool is not. File Browser's list
is short and ordinary, and it is below.
But this tool carries one fact that is
not ordinary at all, and it goes first,
in full. Every time the server starts,
it prints this:

```text
2026/10/29 18:40:40 NOTICE: File Browser is being wound down.
2026/10/29 18:40:40 NOTICE: The project is archived on 2026-09-01, after which there will be no
2026/10/29 18:40:40 NOTICE: further releases and no security fixes. Known unfixed issues are at
2026/10/29 18:40:40 NOTICE: https://github.com/filebrowser/filebrowser/security/advisories
```

(From the lab's transcript
`file-browser-lab/transcripts/t04-server-start.txt`.)

In plain terms: the project is
finished. Version 2.63.23, the release
this guide is built on, is the last
kind there will be. The program works
— the lab ran it through every chapter
of this guide — but if a security flaw
is found in it next year, no fix is
coming, and the project keeps a public
list of the flaws it already knows
about and will not fix.

That does not make the tool useless. It
makes the *placement* of the tool the
decision that matters. On a home
network, serving your own files to your
own household, the risk is small and
the tool is genuinely handy — which is
the use this guide teaches. Facing the
open internet, the same program is a
door with no locksmith, and chapter 11
returns to this with the seriousness it
deserves. Read the notice, decide where
your copy will live, and then install
with your eyes open.

## A first taste

Installed and started (chapters 3 and
4), the whole tool is visible in two
commands. Signing in hands you a token:

```bash
curl -s -X POST http://127.0.0.1:18080/api/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"lab-admin-pass"}'
```

and the token opens the listing of your
tree:

```bash
curl -s http://127.0.0.1:18080/api/resources/ \
  -H "X-Auth: <token>"
```

The answer is a page of JSON naming the
folders — in the lab, `alice`,
`documents`, `photos`, `recipes` — with
sizes and dates. The web page shows the
same listing as a table of files; it is
talking to the same API. (Transcript
`t05-login-and-list.txt`.)

## What it is not

File Browser is not a sync tool: it
does not keep copies of your files on
your other machines, and nothing
replicates anywhere — Syncthing, in
chapter 10, is that tool. It is not a
backup: the files it serves are the
only copies unless you make others. It
is not a media library: it will show
you a folder of photos, but it is not
organising them the way a photo manager
does. It is not the machine's own login
in a new hat: its accounts live in its
own database, and chapter 6 shows a
File Browser user who can do things the
machine's owner never granted — and,
more importantly, cannot do things the
machine's owner never took away. And it
is no longer a living project; that
point has been made, and will not be
repeated on every page — but chapter 11
collects what follows from it.

## Who it is for

The household with a home server and
people in it who should reach the
shared folder, not a shell prompt. The
maker whose workshop computer collects
files the laptop wants. The club
volunteer who needs one folder where
the newsletter editor can drop this
month's draft — and nowhere else, and
no deleting. The common thread is one
tree of files, a handful of people, and
different-sized keys to different-sized
parts of it.
