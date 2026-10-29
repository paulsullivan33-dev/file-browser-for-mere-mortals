# Users, Permissions and Scopes

By the end of this chapter there will be
a second person on your server — with
their own login, their own corner of the
tree, and a shorter list of allowed
verbs than yours — and you will have
watched the fences hold: folders outside
the corner answering as if they did not
exist, a delete refused, the user list
itself refused. The check is alice's own
root listing: two files, and nothing
else in her world.

## The shape of a user

Chapter 2 named the parts: a scope that
decides *where* a user lives, and eight
permission switches that decide *what*
they may do there. The defaults a new
user starts from are settings, visible
in `config cat` — in the lab, Create,
Rename, Modify, Delete, Share, Download
and Execute all defaulted to true, and
Admin to false. Defaults are a starting
point, not a decision; make the decision
per user.

## Making alice: two ways, one trap

With the server stopped, the command
line does it in one line — chapter 3's
pattern with different answers:

```bash
./filebrowser users add alice lab-alice-pass --scope /alice -d filebrowser.db
```

The lab instead made alice *while the
server was running*, through the API —
partly to prove it can be done live,
partly because that is how an admin
working from the web page does it. The
request carries the whole user as JSON:

```bash
curl -s -X POST http://127.0.0.1:18080/api/users \
  -H "X-Auth: <admin token>" \
  -H 'Content-Type: application/json' \
  -d '{"what":"user","which":[],"current_password":"lab-admin-pass",
       "data":{"username":"alice","password":"lab-alice-pass",
               "scope":"/alice", … }}'
```

The trap is the field
`current_password`. Creating a user
requires the *signed-in administrator's
own* password, repeated inside the
request — a deliberate "prove it is
still you" step. Leave it out, or spell
it the camelCase way (`currentPassword`)
that most APIs would use, and the server
answers with the most misleading error
in this guide:

```text
400 Bad Request (the current password is incorrect)
```

Nothing is wrong with any password. The
field was missing or misnamed, so the
check compared an empty string against
your hash. The lab hit this twice before
reading the handler's source and finding
the snake_case name. With it, the answer
is `201 Created`, and the user list
shows the pair:

```text
1 admin scope: / perm: {'admin': True, 'execute': True, 'create': True, 'rename': True, 'modify': True, 'delete': True, 'share': True, 'download': True}
2 alice scope: /alice perm: {'admin': False, 'execute': False, 'create': True, 'rename': True, 'modify': True, 'delete': False, 'share': True, 'download': True}
```

(Transcript `t08-create-alice.txt`.)
Alice was given Create, Rename, Modify,
Share and Download — a person who can
work in her folder and hand files out of
it — and refused Admin, Execute, and
Delete. The sections below spend those
refusals.

## What alice sees

Alice signs in the same way and asks for
her root. Her token's answer:

```text
path: / | items: ['seed-swap.txt', 'welcome.txt']
```

That is not a filtered view of the real
root. It *is* her root — the folder
`/alice` inside the server's tree,
presented as `/` because every path a
user speaks is relative to their scope.
The rest of the tree is not hidden from
her; as far as any answer she can
receive is concerned, it is not there.

## The escape attempts

The lab then tried, with alice's token,
the obvious ways out:

**Ask for the folder by its real path.**
`GET /api/resources/documents/` →

```text
404 Not Found
```

Read through her scope, that path means
"a folder called documents inside
alice's folder", which does not exist.
The server does not say *forbidden*; it
says *nothing here*, which leaks less.

**Download past the fence.**
`GET /api/raw/documents/picnic-supplies.txt` →

```text
HTTP 404
```

Same story: the path is resolved inside
her world first, and outside never
enters into it.

**Climb out with dot-dot.** A request
for `/api/resources/../documents/`,
sent with the dots intact, is cleaned
by the server before it is routed, and
answered with a redirect to
`/api/documents/` — a path that is not
an API route at all and returns the web
page's own shell, the same HTML as the
front door. No listing, no file, no
error worth the name. The encoded form
of the same trick (`%2e%2e%2f`) met the
same cleaning. (Transcript
`t09-alice-scope.txt`.)

## The switches, refused one by one

Alice tries to delete her *own* welcome
file — inside her scope, a file she can
read, rename, and edit:

```text
403 Forbidden
```

The file survived; the check afterwards
lists it still in place. Ownership was
never the question. The Delete switch
was off, and off is the whole answer.

And the user list — `GET /api/users`,
the door chapter 3 used freely as
administrator:

```text
HTTP 403
```

User administration is Admin's work, and
alice is not Admin. Between the scope
that bounds *where* and the switches
that bound *what*, her account is a
small, honest set of abilities: exactly
the ones on her line of the user list,
no more, each refusal verified rather
than assumed.
