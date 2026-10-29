# The Moving Parts

File Browser arrives as one file and
behaves like one program, but five parts
do five different jobs inside it. Nearly
every surprise in this guide — including
most of the troubleshooting chapter — is
one of these parts behaving exactly as
designed while the reader expected
another part's behaviour. This chapter
names them.

## The binary

Everything ships as a single executable,
about 36 MB in the lab's download: the
server, the web pages, the API, and the
management command line are all inside
`filebrowser`. The release archive holds
little else:

```text
CHANGELOG.md
LICENSE
README.md
filebrowser
```

(Transcript `t00-download-and-version.txt`.)
There is nothing to compile and no
runtime to install beside it. The same
binary that serves your files also
answers to `filebrowser users ls` and
`filebrowser config cat` — one program,
two faces: a server face and a
management face. The management face is
how chapter 3 sets everything up before
the server ever starts.

## The database: one small file

Users, permissions, settings, and share
links do not live in configuration files
spread across the system. They live in
a **database**: a single file, managed
by the program itself, in the Bolt
format — a key-and-value store that
needs no database server of its own.
The lab's database, holding two users,
two shares, and all the settings of a
worked example, was 64 KB:

```text
-rw-r----- 1 root root 65536 … filebrowser.db
```

Two consequences follow, and both get
their own moments later. First, backing
up File Browser's *mind* is copying one
file (recipe 4). Second, Bolt allows
exactly **one writer at a time**, and
the running server holds the file open —
so the management face refuses to work
while the server runs, failing with a
bare error the lab met on purpose:

```text
Error: timeout
```

(Transcript `t16-share-revoke-and-lock.txt`.)
Stop the server to manage; manage, then
start the server. Chapter 12 lists this
among the limits because it shapes how
you will actually run the thing.

Passwords inside the database are kept
as **bcrypt hashes** — one-way
fingerprints, never the password itself:

```text
admin | scope: / | password begins: $2a$10$ | admin: True
alice | scope: /alice | password begins: $2a$10$ | admin: False
```

(From the users export, transcript
`t15-exports-and-hash.txt`.) Anyone who
steals the database file gets hashes to
attack, not keys to use — and should
still be treated as having stolen
something, since the same file carries
the secret that signs login tokens
(chapter 12).

## The root: the tree being served

The **root** is a folder on the server's
disk that File Browser serves. Everything
the tool can show, download, or share is
inside it; the program's own flag says
what it is:

```text
-r, --root string   root to prepend to relative paths (default ".")
```

The lab's root held four folders —
`alice`, `documents`, `photos`,
`recipes`. The root is a boundary, not
a suggestion: chapter 6's tests include
paths that climb and paths that hide,
and none of them produced a file from
outside the tree an account was allowed.

## Users and scopes

A **user** is a name, a password hash,
and a set of answers about what that
name may do. The answer that shapes
everything is the **scope**: a folder
inside the root that becomes that
user's entire world. The administrator's
scope in the lab was `/` — the whole
tree. Alice's was `/alice`. To alice,
signing in shows a root containing two
files, `welcome.txt` and `seed-swap.txt`,
and nothing in her view admits that
anything else exists:

```text
path: / | items: ['seed-swap.txt', 'welcome.txt']
```

(Transcript `t09-alice-scope.txt`.)
Paths, for a user, are always relative
to their scope. That one design decision
explains both the tool's safety and its
most common confusion (chapter 12).

## The eight switches

On top of the scope sit eight
**permissions**, true or false per user:

| Switch | What it allows |
| --- | --- |
| Admin | Manage users and settings |
| Execute | Run commands through the runner (chapter 8) |
| Create | Upload and make new files and folders |
| Rename | Rename and move |
| Modify | Edit and replace existing files |
| Delete | Delete files and folders |
| Share | Create share links |
| Download | Download files |

The lab's administrator had all eight.
Alice was made with Create, Rename,
Modify, Share and Download — and
without Admin, Execute, or Delete, each
of which the lab then watched being
refused in turn. One pairing is enforced
by the server itself: Share without
Download is refused when a user is
saved, because a link that cannot be
downloaded through is pointless.

## The two doors: pages and API

Everything a user can do arrives through
one HTTP API — listings, uploads,
shares, commands. The web interface is a
program that runs in the visitor's
browser and knocks on that API; the
`curl` commands in this guide knock on
the same doors directly. That is why the
lab, which had no browser to click with,
could still verify nearly everything:
the API is not a side entrance, it is
the only entrance. Signing in
(`POST /api/login`) returns a **token** —
a signed ticket (a JWT, in the jargon)
that later requests carry in an
`X-Auth` header. Tokens expire; the
default lifetime is two hours.

## Which part holds what

| Question | The part that answers it |
| --- | --- |
| Why can't the CLI open the database? | The database — the running server holds its one writer's lock |
| Why does this user see only two files? | Their scope — that folder is their whole tree |
| Why was Delete refused for her own file? | The Delete switch — ownership is not the test, the switch is |
| Why did the upload land with mode 0640? | The settings — new files take the configured creation mode |
| Why did the share link stop working? | The database — the link was a row in it, and the row was deleted |
| Why did the hook write `{FILE}` unchanged? | The runner — it passes facts as environment variables, not placeholders (chapter 8) |

Keep this table in mind. When File
Browser surprises you, the surprise has
an address, and the address is one of
these five.
