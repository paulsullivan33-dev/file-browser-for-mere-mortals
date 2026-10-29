# Limits

What File Browser cannot do, will not
do, and — in one case that outweighs
the rest of this chapter — will never
again be fixed to do. A reasonable
reader finishes this chapter able to
say where the tool's edges are before
they lean on them.

## The project is finished

This is the limit the others are
footnotes to. File Browser is archived:
the final release is 2.63.23, the
project prints its winding-down notice
at every start, and there will be no
further releases and **no security
fixes** — the notice's own words. The
project publishes a list of known,
unfixed security issues; anything found
tomorrow joins that list rather than a
release note.

What follows, practically:

- **Placement is the security decision
  now.** On a home network, reached by
  your household, the exposure is the
  exposure of your network itself. On
  the open internet, the program is an
  unpatchable door with a password —
  and with share links, chapter 7's
  capabilities that need no password.
  If strangers can reach it, choose a
  maintained neighbour (chapter 10)
  instead.
- **The runner raises the stakes.** A
  command runner on an unmaintained
  server (chapter 8) should stay off
  unless a specific job needs it, and
  its allowlists should stay short.
- **Time is not neutral.** Every year
  adds discoveries the tool will never
  absorb. The household that adopts it
  today should plan, calmly, to retire
  it — the exports of recipe 4 keep the
  users and settings portable, and the
  files themselves were never in a
  proprietary shape at all: they are
  files, in folders, untouched.

## One tree, one server

An instance serves one root. Scopes
divide that tree among people, but the
tree is the unit: files that live on
another machine, or outside the root,
are not File Browser's to show. It also
does not follow you from machine to
machine — nothing syncs, nothing
replicates (chapter 10's copier does
that job), and a second server is a
second installation with its own
database and its own users.

## Deletion is deletion

There is no recycle bin and no undo in
the interface this guide verified. The
DELETE call of chapter 5 ended the
folder it named, in the same moment,
with a 204 and no ceremony. Backups of
the *files* are the reader's own affair
(the guide series has a backups guide);
this tool neither makes them nor keeps
versions of what it serves. The
permission design is the mitigation on
offer: accounts that should not be able
to destroy should not hold the Delete
switch, and chapter 6 watched that
switch hold.

## One writer at a time

The database is a single file with a
single-writer lock. The running server
holds it; the management CLI, asked to
so much as list the users while the
server runs, waits and fails with
`Error: timeout`. Administration is
therefore a small ceremony — stop,
manage, start — or else done through
the running server's own API and pages,
as chapter 6 did. For a household this
is a shrug. For anyone imagining scripts
that adjust users while the service
runs, it is a design constraint to plan
around.

## A file manager, not a library

File Browser shows the tree it is
given. It classifies files by type,
makes thumbnails and previews of common
media, and searches names — and it does
not organise a photo collection,
transcode a video library, keep a
catalogue, or know what anything *is*
beyond its name and type. Households
with real media collections want a
media tool beside it or instead of it.
Nor is it an editor of anything but
text: its in-page editing, verified
here as a whole-file replacement, is
for notes and configuration-shaped
things, not documents with formatting.

## Small print

A few lesser edges, plainly. Tokens
expire (two hours by default), so long
API sessions re-login as a matter of
routine. Large-tree browsing is as fast
as the disk and the network allow and
no faster; there is no index to make a
slow disk quick. The tool speaks HTTP
in the clear unless you give it a
certificate or put a proxy in front —
on a home network that is ordinary; off
one, with this project's status, it is
another reason chapter 10's maintained
neighbours win. And a share link, once
sent, cannot be unsent — only revoked
(chapter 7); the distinction matters
every time you press send.
