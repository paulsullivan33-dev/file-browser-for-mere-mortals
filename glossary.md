# Glossary

**API** — The program-shaped set of
doors under the web pages. Every action
in this guide was done through it with
`curl`, at addresses under `/api/`,
because the pages themselves use the
same doors.

**Allowlist** — The per-user list of
commands the interactive runner will
run at all (`users update --commands`).
A command not on the list is refused
whatever the other gates say.

**bcrypt** — The one-way hashing method
the database stores passwords with. A
stored hash (beginning `$2a$10$`) can
check a password offered later, but
cannot be turned back into it.

**Bolt** — The single-file,
key-and-value database format File
Browser keeps its mind in. No separate
database server; one file; one writer
at a time.

**Command runner** — The part that runs
shell commands: hooks on file events,
and the interactive command box. Off by
default at two levels (chapter 8).

**current_password** — The field in a
user-management API request that must
repeat the *signed-in administrator's*
password, in snake_case, exactly — the
cause of this guide's most misleading
error (chapter 12).

**Database** — In this guide, always
the Bolt file (`filebrowser.db` unless
renamed): users, permissions, settings,
and share links in one place.

**Hash (of a file)** — A fingerprint
computed from a file's contents, used
here to prove a transfer: SHA-256 sums
that match are the same file, in
practice, whatever the journey between.

**Hash (of a share)** — The eight
characters that name a share link. Not
a fingerprint of anything; a short,
unguessable address.

**Hook** — A command attached to a file
event (`after_upload` and kin) by the
`cmds` management commands, run by the
runner when the event happens, with the
facts passed as environment variables.

**JWT** — The signed-ticket format of a
login token. Presented in the `X-Auth`
header; expires after the configured
lifetime (two hours by default).

**Permission** — One of eight per-user
switches: Admin, Execute, Create,
Rename, Modify, Delete, Share,
Download. Off is a complete answer,
whatever the file and whoever the user.

**Public link** — The two addresses a
share hash opens without any login:
`/api/public/share/<hash>` for the
listing and `/api/public/dl/<hash>/<name>`
for the download itself.

**Root** — The folder on the server's
disk that an instance serves. The whole
of File Browser's world; every scope
lives inside it.

**Scope** — The folder inside the root
that is one user's entire world,
presented to them as `/`. Paths in
their view are relative to it, and
outside it is not forbidden but absent.

**Shell** — The program hook and runner
commands are fed through when one is
set (the lab used `bash -c`). Without a
shell, commands are split into words
and run bare.

**Token** — The ticket a login returns.
Whoever holds it is, to the server, the
user it names, until it expires.

**TUS** — The resumable-upload protocol
whose settings (a 10 MB chunk size by
default) appear in the configuration.
Large uploads can resume rather than
restart; named here because the
settings screen names it.

**X-SHARE-PASSWORD** — The header in
which a visitor to a password-protected
share presents the password; the web
page collects it and does the same.
