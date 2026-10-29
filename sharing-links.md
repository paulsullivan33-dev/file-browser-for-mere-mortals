# Sharing Links

By the end of this chapter you will have
handed a file to someone who has no
account at all: a link that works in any
browser, with nothing to sign into. You
will also have locked such a link with a
password, watched it refuse the wrong
password, and taken a link back. The
check is a download made with no token,
compared byte-for-byte with the file on
the server.

A share link is a **capability**: the
address itself is the permission.
Whoever holds the link holds the file.
That is exactly its usefulness and
exactly its risk, and this chapter
treats both halves seriously — every
link below is created, used, and (in
one case) revoked on the record.

## Making a link

Any user with the Share switch (and
Download — the server will not save a
user who has Share without it) can share
what they can reach:

```bash
curl -s -X POST "http://127.0.0.1:18080/api/share/documents/picnic-supplies.txt" \
  -H "X-Auth: <token>" \
  -H 'Content-Type: application/json' \
  -d '{"password":"","expires":"","unit":"hours"}'
```

```json
{
    "hash": "wIr1z2i3",
    "path": "/documents/picnic-supplies.txt",
    "userID": 1,
    "expire": 0,
    "hasPassword": false
}
```

The **hash** — eight characters — is the
link's whole identity. The two addresses
a visitor uses are built from it:
`/share/<hash>` in the web page for a
human, and the API pair the lab used:

```bash
curl -s "http://127.0.0.1:18080/api/public/share/wIr1z2i3"
curl -s "http://127.0.0.1:18080/api/public/dl/wIr1z2i3/picnic-supplies.txt" \
  -o shared-download.txt
cmp shared-download.txt root/documents/picnic-supplies.txt && echo IDENTICAL
```

No token was sent with either request,
and none was needed: the listing answer
describes the file, and the download is
the file, byte-identical. A made-up hash
gets the same answer as a wrong
password gets elsewhere — `404 Not
Found` — so the space of links cannot be
explored by guessing at neighbours of a
real one. (Transcript
`t10-share-link.txt`.) A share can also
point at a folder, in which case the
public side lists its contents and
serves the files inside it the same way;
the lab verified the file form end to
end and the folder form is the same
mechanism.

## A password on the link

A link that anyone can forward can also
be *guarded* by anyone: set a password
when the link is made:

```bash
curl -s -X POST "http://127.0.0.1:18080/api/share/recipes/lentil-soup.txt" \
  -H "X-Auth: <token>" \
  -H 'Content-Type: application/json' \
  -d '{"password":"soup-first","expires":"","unit":"hours"}'
```

```json
{ "hash": "gfdqREe6", "path": "/recipes/lentil-soup.txt",
  "userID": 1, "expire": 0, "hasPassword": true }
```

Now the same download, unguarded by
nothing, fails:

```text
401 Unauthorized
```

The web page asks the visitor for the
password and then presents it in a
header named `X-SHARE-PASSWORD`; the lab
did the same directly:

```bash
curl -s "http://127.0.0.1:18080/api/public/dl/gfdqREe6/lentil-soup.txt" \
  -H "X-SHARE-PASSWORD: soup-first" -o soup-back.txt
cmp soup-back.txt root/recipes/lentil-soup.txt && echo IDENTICAL
```

The right password downloads the file,
byte-identical. A wrong one gets the
same 401 as none at all. Between them,
the lab had the three answers a guarded
door should give: no key, no; wrong key,
no; right key, the file. (Transcript
`t14-edit-and-password-share.txt`.)

## Expiry, the ledger, and taking a link back

The `expire` field is a moment after
which the link stops working; `0` means
never, which is what the lab's links
carry. An expiry is set at creation, in
the `expires` and `unit` fields of the
same request — the lab's chapters left
that dial untouched, and `criteria.md`
lists it as documented-only.

Every live link is a row in the
database, and the owner can read the
ledger:

```bash
curl -s "http://127.0.0.1:18080/api/shares" -H "X-Auth: <token>"
```

Note the plural: `/api/shares` lists,
while `/api/share/<path>` creates — the
singular address on its own simply
redirects. And a link ends the moment
its row is deleted:

```bash
curl -s -X DELETE "http://127.0.0.1:18080/api/share/wIr1z2i3" \
  -H "X-Auth: <token>"
curl -s "http://127.0.0.1:18080/api/public/share/wIr1z2i3"
```

```text
404 Not Found
```

Revocation is instant and total: the
hash becomes a made-up hash. (Transcript
`t16-share-revoke-and-lock.txt`.) The
habit this chapter is really teaching is
housekeeping — links are keys you have
handed out, the ledger is where they are
all written down, and the delete call is
how you change the locks.
