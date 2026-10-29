# Installing File Browser

By the end of this chapter you will have
the program on disk, checked against the
project's own checksum, a database made,
and the first administrator created —
everything done from the command line,
before the server is ever started. The
check to run is the last command in each
section: if its output matches what is
shown, that stage is truly done.

A word before the download, because
chapter 1 promised no surprises: you are
installing a finished, unmaintained
program. Install it somewhere its
placement makes sense — a machine on
your own network is the intended home —
and keep chapter 11 in mind when you
decide who can reach it.

## Get the release

The project publishes ready-made
archives on its GitHub releases page,
one per operating system and processor.
The lab took the Linux amd64 build of
the final release, 2.63.23, together
with the checksum file:

```bash
curl -sLO https://github.com/filebrowser/filebrowser/releases/download/v2.63.23/linux-amd64-filebrowser.tar.gz
curl -sLO https://github.com/filebrowser/filebrowser/releases/download/v2.63.23/filebrowser_2.63.23_checksums.txt
```

Check the download against the project's
own numbers before trusting it:

```bash
grep linux-amd64-filebrowser.tar.gz filebrowser_2.63.23_checksums.txt | sha256sum -c -
```

```text
linux-amd64-filebrowser.tar.gz: OK
```

Then unpack it. The archive holds the
program and little else:

```bash
tar xzf linux-amd64-filebrowser.tar.gz
./filebrowser version
```

```text
File Browser v2.63.23/e8a388f8
```

(Transcript `t00-download-and-version.txt`.)
That version line is the first check:
the binary runs, unmodified, exactly as
published. The project also offers a
Docker image and one-line install
scripts; the lab verified the bare
binary, and it is the route this guide
teaches.

## Make the database

File Browser keeps its mind in one file
(chapter 2). Create it, and set the two
facts the server needs first — the root
folder it will serve, and where it will
listen. The lab served a folder called
`root` and listened on port 18080; on
your own machine, port 8080, the
default, is the usual choice.

```bash
./filebrowser config init -d filebrowser.db
./filebrowser config set -d filebrowser.db \
  --root /path/to/your/folder \
  --address 127.0.0.1 --port 8080
```

`config init` prints the full settings
it has created — defaults for things
this guide meets later: new files are
created with mode `0o640`, new folders
with `0o750`, the command runner is
disabled, and the minimum password
length is 12. Read that printout once;
it is the tool's whole posture on one
screen. (Transcript
`t03-init-config-admin.txt`.)

Listening on `127.0.0.1` means the server
answers only the machine it runs on —
the right default while you learn. To
serve the household, set the address to
`0.0.0.0` later, deliberately, knowing
chapter 11's warning; a reader who
wants the wider world to reach it
should put a maintained reverse proxy
in front, not change this address and
hope.

## Make the first administrator

```bash
./filebrowser users add admin lab-admin-pass --perm.admin -d filebrowser.db
```

```text
ID  Username  Scope  Locale  V. Mode  S.Click  Red. After C/M  Admin  Execute  Create  Rename  Modify  Delete  Share  Download  Pwd Lock
1   admin     /      en      list     false    false           true   true     true    true    true    true    true   true      false
```

Choose a real password on a real
machine; `lab-admin-pass` is this
guide's throwaway, shown so the examples
stay honest, and it protects nothing
anymore — the lab is dismantled. Two
details in that table matter. The new
administrator's scope is `/`: the whole
root. And the password you typed was
hashed before it was stored — the
database holds a bcrypt fingerprint
(chapter 2), never the words.

Check the whole stage in one command:

```bash
./filebrowser users ls -d filebrowser.db
```

If your administrator is listed with
Admin true, the install is done. There
is also a shortcut this guide
deliberately did not take: run the
server with no database and it enters a
quick setup that creates one, with a
first user from its `--username` and
`--password` flags. It is quicker and
teaches nothing; the long way round
showed you the database, the settings,
and the user table — the three things
every later chapter leans on.
