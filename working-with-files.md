# Working with Files

By the end of this chapter you will have
moved a file into the server and back
out again and *proved*, by checksum,
that what came back is what went in —
and you will have made a folder, renamed
a file, edited one in place, and deleted
something, all through the same API the
web page uses. The check is the checksum
itself: two identical hashes, one from
each end of the journey.

Everything here uses the token from
chapter 4, and one verb per job. The web
page does the same things with buttons;
the verbs are easier to write down
exactly, and exactly is what a check
needs.

## Upload: a POST with the file as its body

```bash
head -c 49152 /dev/urandom > roundtrip.bin
sha256sum roundtrip.bin
curl -s -X POST --data-binary @roundtrip.bin \
  "http://127.0.0.1:18080/api/resources/documents/roundtrip.bin" \
  -H "X-Auth: <token>"
```

```text
88354b7753dd13fcf6f74aca7e0d70920bcedcb74309a7b0614e0eeae6857995  roundtrip.bin
200 OK
```

The file arrives in `documents/` with
the name the URL gave it. Notice its
permissions on the server's disk:
`-rw-r-----`, mode 0640 — the creation
mode from the settings in chapter 3,
applied quietly. A file uploaded twice
to the same name is refused unless you
add `?override=true` to the URL; the
refusal is the tool declining to
overwrite in silence.

## Download: /api/raw/, and the proof

```bash
curl -s "http://127.0.0.1:18080/api/raw/documents/roundtrip.bin" \
  -H "X-Auth: <token>" -o downloaded.bin
sha256sum downloaded.bin
cmp roundtrip.bin downloaded.bin && echo IDENTICAL
```

```text
88354b7753dd13fcf6f74aca7e0d70920bcedcb74309a7b0614e0eeae6857995  downloaded.bin
IDENTICAL
```

Downloads live under `/api/raw/`; the
guide uses `/api/resources/` for
everything else. The lab ran the same
proof in the other direction — a file
placed in the tree before the server
started, downloaded, and compared with
the original on disk: identical again.
(Transcript `t06-upload-download.txt`.)
If you remember one habit from this
guide, make it this one: a transfer you
have not checksummed is a transfer you
are hoping about.

The server will also do the arithmetic
for you, which is the quicker everyday
check — ask for a file's listing with a
checksum requested:

```bash
curl -s "http://127.0.0.1:18080/api/resources/documents/roundtrip-renamed.bin?checksum=sha256" \
  -H "X-Auth: <token>"
```

```text
{'sha256': '88354b7753dd13fcf6f74aca7e0d70920bcedcb74309a7b0614e0eeae6857995'}
```

## New folder: a POST that ends in a slash

A URL ending in `/` creates a folder
instead of a file:

```bash
curl -s -X POST "http://127.0.0.1:18080/api/resources/documents/shopping/" \
  -H "X-Auth: <token>"
```

```text
200 OK
```

One trailing character is the whole
difference between "put a file here" and
"make a folder here" — the API's neatest
and easiest-to-miss convention.

## Rename and move: PATCH

```bash
curl -s -X PATCH "http://127.0.0.1:18080/api/resources/documents/roundtrip.bin?action=rename&destination=/documents/roundtrip-renamed.bin" \
  -H "X-Auth: <token>"
```

The destination is a full path inside
your scope, so the same call moves a
file to another folder when the folder
part changes. The server-side checksum
above was taken after this rename: the
hash followed the file, as it should.

## Edit: a PUT replaces the contents

Text files can be edited in the web
page's editor. Through the API the same
job is a PUT carrying the new contents:

```bash
curl -s -X PUT --data-binary @notes-v2.md \
  "http://127.0.0.1:18080/api/resources/documents/field-notes.md" \
  -H "X-Auth: <token>"
```

The lab appended a line to its field
notes this way and read the tail of the
file on the server's disk afterwards:
the new line was there. A PUT is a
replacement, not a patch — send the
whole file, every time.

## Delete: DELETE, and it is gone

```bash
curl -s -X DELETE "http://127.0.0.1:18080/api/resources/documents/shopping/" \
  -H "X-Auth: <token>"
```

```text
HTTP 204
```

There is no recycle bin in this tool and
no undo: the folder the lab made two
sections ago ceased to exist. That
bluntness is why the Delete permission
is a separate switch (chapter 6), and
why the recipe chapter builds a useful
account with that switch turned off.
(Transcripts `t07-folders-rename-delete.txt`
and `t14-edit-and-password-share.txt`.)
