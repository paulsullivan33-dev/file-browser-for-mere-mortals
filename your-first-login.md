# Your First Login

By the end of this chapter your server
will be running, you will have signed
in two ways — the web page a person
uses, and the API underneath it — and
you will have read your first listing
and understood its shape. The check: a
listing of your root folder, produced
by a command in this chapter, naming
the folders you put there.

## Start the server

With the database made (chapter 3), the
server is one command:

```bash
./filebrowser -d filebrowser.db
```

It prints a short diary. The lab's read:

```text
2026/10/29 18:40:40 No config file used
2026/10/29 18:40:40 Using database: /home/hatch/workspace/file-browser-lab-work/filebrowser.db
2026/10/29 18:40:40 NOTICE: File Browser is being wound down.
…
2026/10/29 18:40:40 Listening on 127.0.0.1:18080
```

The winding-down notice is part of
every start; chapter 1 explained it, and
it is not an error. The line that
matters is the last: the server is
listening where the settings said. Leave
it running — every command from here to
the end of chapter 8 talks to it.

## The page a person sees

Open the address in a browser —
`http://127.0.0.1:8080/` with the
defaults — and the program answers with
its sign-in page. The lab, having no
browser, fetched the page and read its
title instead:

```bash
curl -s http://127.0.0.1:18080/ | sed -n '/<title>/,/<\/title>/p'
```

```text
    <title>
      File Browser
    </title>
```

Signing in there with the administrator
from chapter 3 shows the root as a table
of files — the human face of the listing
this chapter now produces the other way.

## Signing in through the API

The page signs in by posting your name
and password to `/api/login`, and the
server replies with a **token** — a long
signed ticket. Do exactly what the page
does:

```bash
curl -s -X POST http://127.0.0.1:18080/api/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"lab-admin-pass"}'
```

The lab's answer was 601 characters
beginning `eyJhbGciOiJI…` — a JWT, kept
out of the transcript beyond its first
few letters, because a live token is a
key and the lab still had work to do.
Save yours somewhere your shell can
reach it, and present it on later
requests in the `X-Auth` header. That
header is the whole ritual: no token,
no service; a wrong or expired token,
the same. Tokens last two hours by
default (a setting, like everything
else here), after which you sign in
again — a mild nuisance that is also
the point.

## Your first listing

```bash
curl -s http://127.0.0.1:18080/api/resources/ \
  -H "X-Auth: <token>"
```

The answer is JSON — the raw material
the web page renders. Trimmed to its
skeleton, the lab's root:

```json
{
    "items": [
        { "path": "/alice",     "name": "alice",     "isDir": true,  "type": "" },
        { "path": "/documents", "name": "documents", "isDir": true,  "type": "" },
        { "path": "/photos",    "name": "photos",    "isDir": true,  "type": "" },
        { "path": "/recipes",   "name": "recipes",   "isDir": true,  "type": "" }
    ],
    "numDirs": 4,
    "numFiles": 0,
    "path": "/"
}
```

(Full version in transcript
`t05-login-and-list.txt`.) Each item
carries its path, size, modification
time, and a **type**: File Browser looks
at files and classifies them — a text
file is `"text"`, an image an `"image"`,
and the lab's file of random bytes,
honestly, a `"blob"`. Ask for a folder
instead — `/api/resources/documents/` —
and the same shape describes the files
inside it. Everything in the next three
chapters is this one conversation,
extended: same address pattern, same
header, different verbs.
