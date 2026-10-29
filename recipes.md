# Recipes

Five small jobs, each assembled from
parts the earlier chapters verified.
Each names the outcome first and the
check last; anything a recipe relies on
that the lab did not run is marked
documented-only where it stands.

## 1. A family folder on the home server

**Outcome:** a spare machine in the
house serves one shared tree; each
person has their own login and their
own subfolder, and nobody has a shell
account.

Install as in chapter 3, with the root
set to the shared folder and the address
set to `0.0.0.0` so the house can reach
it — on your own network, behind your
own router, with chapter 11 read. Make
one folder per person inside the root,
then one account per person scoped to
their folder (chapter 6). Work that
belongs to everyone goes in a `shared`
folder; because a scope is a single
folder, give the household's *shared*
work its own account scoped to
`/shared`, whose password the household
shares, or accept the administrator's
all-tree account as the shared one.
Check: sign in as one person and ask
for your root listing — it shows that
person's files, and the escape attempts
of chapter 6 answer for everyone.

## 2. A drop box that cannot delete

**Outcome:** a club's newsletter editor
can deliver each month's draft into a
folder — and cannot remove last month's,
or anything else, by accident or
otherwise.

Make the account with the chapter 6
shape: scope set to the submissions
folder, Create, Modify, Rename and
Download on, **Delete off**, Admin and
Execute off. The editor uploads and
corrects drafts freely; the refused
delete of chapter 6 is the guarantee,
and it was watched working on a file
inside the account's own scope. Check:
with the editor's token, attempt to
delete a file. `403 Forbidden`, and the
file still listed afterwards, is the
recipe working.

## 3. One file for a friend, no account

**Outcome:** a friend downloads exactly
one document from a link you send, and
the link stops working when you say so.

Share the file as in chapter 7, with a
password if the contents deserve one,
and send the link and the password by
different routes (the link in the
message, the password in a call) — a
forwarded message then carries only
half a key. When the friend confirms
receipt, revoke the link
(`DELETE /api/share/<hash>`) and confirm
the public address now answers 404.
Check: the revocation check is the
recipe — a link you have not revoked is
a link that still works.

## 4. Back up File Browser itself

**Outcome:** the server's whole mind —
users, settings, shares — copied to
safety as one small file, and restorable
by copying it back.

Stop the server (chapter 2's one-writer
rule leaves no choice, and no shortcut),
then copy the database:

```bash
cp filebrowser.db filebrowser-backup-2026-10-29.db
```

Restart the server. The lab's database
was 64 KB holding everything chapters
3–8 built. For a copy you can also read
and move between machines, add the
exports while the server is stopped:

```bash
./filebrowser config export config.json -d filebrowser.db
./filebrowser users export users.json -d filebrowser.db
```

Handle the exports as secrets: the
config export contains the key that
signs login tokens, and the users export
contains every password hash. Check:
the backup file exists, its size is in
the tens of kilobytes, and a
`users ls` against the *backup* lists
your accounts. Restoring — putting the
file back beside the binary and
starting — is the same commands in
reverse (documented-only: the lab
exported and listed, and did not
dismantle its own server to prove the
return journey).

## 5. An upload log that writes itself

**Outcome:** every upload to the server
leaves a line in a log — who, what,
where — without anyone remembering to
write it.

Set the shell and enable the runner
(chapter 8), then attach the hook:

```bash
./filebrowser cmds add after_upload \
  'echo "$TRIGGER $FILE by $USERNAME (scope $SCOPE)" >> /var/log/filebrowser-uploads.log' \
  -d filebrowser.db
```

Restart and upload anything through the
page or the API. Check: the log gains a
line naming the file's full path, the
uploader, and their scope — the exact
line shape the lab's own hook produced.
From here the variations are ordinary
shell work: an `after_delete` hook that
notes removals the same way is a second
line of the same kind (the event name
is documented; the lab fired
`after_upload` itself).
