# File Browser for Mere Mortals

A folder of files sits on a server — a
spare machine in a cupboard, a little
board on the shelf — and you want to
reach those files from a browser: look
through them, add to them, fetch one
down, hand one to a friend. **File
Browser** is that reach. It is a single
program you run on the machine that
holds the files. It puts a web page in
front of one folder tree: you sign in,
you see the folders and files, and you
work with them — upload, download,
rename, share — without learning the
server's command line and without
giving anyone an account on the machine
itself.

This guide explains how File Browser's
few parts fit together, how to install
it and make the first account, and how
to do the everyday work. Then it does
the part most guides skip: it gives a
second person an account fenced into
one corner of the tree, and *tries to
break out* — by asking for the other
folders directly, by downloading past
the fence, by hiding the escape in
`..` — and reports exactly what the
fence did each time. Sharing links get
the same treatment: made, used with no
login at all, locked with a password,
and revoked, with the evidence kept.

One fact belongs at the front, not in
a footnote. **The File Browser project
has been wound down.** The program
itself says so, every time it starts:

```text
NOTICE: File Browser is being wound down.
NOTICE: The project is archived on 2026-09-01, after which there will be no
NOTICE: further releases and no security fixes.
```

The lab ran the final release,
**File Browser 2.63.23**, in October
2026 — after that date. The program
works, and everything in this guide was
run against it for real. But it will
never be patched again, and chapter 11
(the limits) is plain about what that
means: a fine tool on a home network
you control, and a decision to think
twice about before exposing it to the
open internet. This guide teaches the
tool as it stands, because a great many
copies are still standing — and it does
not hide the date on the box.

The lab's server held one small tree of
stock fixtures — picnic lists, recipes,
field notes, and one file of random
bytes — and two accounts: an
administrator, and **alice**, whose
world was a single folder. Against that
setup the lab uploaded and downloaded
files and proved them byte-identical by
checksum, edited a file through the
API, created and revoked share links,
fired the command runner's hooks on an
upload, and ran shell commands through
the runner's own channel — including
the commands it *refused*. What the lab
could not exercise — the look and feel
of the web pages in a real browser —
it did not fake: the pages were fetched
and their titles read, and the working
surface the lab drove was the API
underneath them, which is the same
surface the pages themselves use.
`criteria.md` keeps the full ledger.

## What this guide covers

- [**What File Browser is**](what-file-browser-is.md) —
  the mental model: one program, one
  folder tree, one web door — and the
  winding-down notice, in full, before
  anything depends on it
- [**The moving parts**](the-moving-parts.md) —
  the binary, the single-file database,
  the root, users and their scopes, and
  the eight permission switches — and
  which part holds what
- [**Installing File Browser**](installing-file-browser.md) —
  the release download, the checksum
  check, making the database, and the
  first administrator
- [**Your first login**](your-first-login.md) —
  starting the server, signing in, the
  token the login hands back, and
  reading your first listing
- [**Working with files**](working-with-files.md) —
  upload and download with checksum
  proof, new folders, rename, edit,
  delete — the everyday verbs
- [**Users, permissions and scopes**](users-and-scopes.md) —
  the second account, fenced into one
  folder, and the escape attempts the
  lab ran against the fence
- [**Sharing links**](sharing-links.md) —
  handing a file to someone with no
  account: links, passwords on links,
  expiry, and taking a link back
- [**The command runner**](the-command-runner.md) —
  the switched-off shell: hooks that
  fire on uploads, commands you may
  run from the browser, and the three
  gates that keep it shut
- [**Recipes**](recipes.md) — a family
  folder, a drop box that cannot
  delete, one file for a friend, and
  backing up File Browser itself
- [**The neighbours**](the-neighbours.md) —
  SSH and SFTP, Samba and NFS shares,
  Syncthing, Nextcloud, and a plain web
  server: what each does that File
  Browser doesn't, and vice versa
- [**Limits**](limits.md) — a finished
  project with no patches coming, one
  tree per server, deletion with no
  undo, and a database only one writer
  may touch at a time
- [**Troubleshooting**](troubleshooting.md) —
  the incorrect-password error that
  means something else, the database
  timeout, the hook that wrote its
  placeholders literally, and the traps
  this guide's lab fell into
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Running File Browser as a public
service for strangers — the winding-down
notice is reason enough, and chapter 11
says why. The Docker install route is
described by the project but was not
the route this lab verified; the lab
ran the bare binary, and the chapters
teach that. Making File Browser pretty
(branding, themes) and its extra login
methods (proxy and hook authentication)
are named where they belong and left
documented-only. And this guide is
about *reaching* files, not organising
a media library: photo and music
collections have their own tools, and
chapter 10 points at them.

## How to use this guide

Read chapter 1 for the model and
chapter 2 before installing anything —
knowing which part holds what turns
later confusion into a named problem,
and knowing the project's status turns
the install into a decision you made,
not a surprise you found. Chapters 3
and 4 get you a running server and a
login in the same sitting. Chapter 6 is
the one to read slowly: scopes and
permissions are the whole safety story
of this tool, and the lab's escape
attempts are the evidence that the
story holds. The lab's transcripts live
in `file-browser-lab/transcripts/`, and
its one script — the small program that
drove the command runner the way the
web page does — is
`file-browser-lab/ws-command.py`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [SSH for Mere Mortals](https://paulsullivan33-dev.github.io/ssh-for-mere-mortals/)
- [Samba and NFS for Mere Mortals](https://paulsullivan33-dev.github.io/samba-and-nfs-for-mere-mortals/)
- [Syncthing for Mere Mortals](https://paulsullivan33-dev.github.io/syncthing-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/file-browser-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/file-browser-for-mere-mortals/blob/main/LICENSE-CODE).
