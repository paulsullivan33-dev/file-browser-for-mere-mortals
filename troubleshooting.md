# Troubleshooting

The failures this guide's lab actually
met, in the order you are likeliest to
meet them, each with the check that
separates it from its neighbours. Most
of this chapter was earned the honest
way: something above did not work, and
the transcript kept the evidence.

## "the current password is incorrect" — and every password is right

Creating or changing a user through the
API fails with `400 Bad Request (the
current password is incorrect)`, although
you are signed in as administrator and
your password demonstrably works — you
just signed in with it.

**Cause.** The request must repeat the
*signed-in administrator's* password in
a field named `current_password` —
snake_case, exactly. Omit it, or write
it `currentPassword` as most APIs
would, and the server compares an empty
string against your hash and reports,
accurately and uselessly, that it does
not match. **Check.** Look at your
request body before you look at your
passwords. The lab's two failures and
the success that followed are in
transcript `t08-create-alice.txt`.

## The CLI says "Error: timeout" and nothing else

Any management command — `users ls`,
`config cat` — hangs for some seconds
and fails with a bare `Error: timeout`
while the server is running.

**Cause.** The database admits one
writer (chapter 2), and the running
server is it. This is the lock working,
not corruption. **Check.** Stop the
server and run the same command: it
answers at once. Do management in the
gap, or use the API against the running
server where the job allows it.
(Transcript `t16-share-revoke-and-lock.txt`.)

## A user "can't see" a folder that is definitely there

A signed-in user reports a folder
missing, or a path from the
administrator's view answers 404 in
theirs.

**Cause.** Paths are relative to the
user's scope (chapter 6). The folder at
`/documents` for the administrator is,
in a scoped user's world, simply not a
place that exists; what they call `/`
is their scope folder wearing the root's
name. **Check.** Compare scopes, not
paths: `users ls` shows each user's
corner in one table. Nine times out of
ten the file is fine and the map in the
reader's head is the administrator's.

## A hook fires, but writes its placeholders literally

The upload hook from chapter 8 runs,
and its log line contains the literal
text `{FILE}`.

**Cause.** This runner does not
substitute brace placeholders. It passes
its facts as environment variables —
`$FILE`, `$USERNAME`, `$TRIGGER`,
`$SCOPE` — and a hook written with
braces echoes them unchanged.
**Check.** Rewrite the hook with the
dollar forms, and confirm a shell is
set (`config cat` shows `Shell:`), or
the variables and the redirection have
nothing to interpret them. The lab's
wrong line and right line sit side by
side in transcript `t12-runner-hook.txt`.

## "Command not allowed." — from a command that should be allowed

The interactive runner refuses a command
the reader expected to work.

**Cause.** Three gates, and the message
does not say which one closed (chapter
8): the server's Exec setting, the
user's Execute switch, or the user's
allowlist of commands. **Check them in
that order:** `config cat` for
`Exec Enabled: true`; `users ls` for
the Execute column; and the user's
command list for the command's name —
`whoami` failed the lab purely by not
being listed. A scoped user runs in
their scope, so a command can also be
*allowed* and still look in a different
folder than expected: `pwd` is the
check, and its answer is the scope.
(Transcript `t13-runner-websocket.txt`.)

## A password is refused as too short

Making a user fails, or a new password
is rejected, though it is a perfectly
reasonable password by household
standards.

**Cause.** The default minimum length
is 12, a setting like any other
(`Minimum Password Length` in
`config cat`, set with
`--minimumPasswordLength`). **Check.**
Count the characters before suspecting
the hashing; lengthen the password, or
lower the setting deliberately — and
know that you did.

## A share link answers 401, 404, or works for the wrong people

Three different answers, three different
causes, all from chapter 7. **404:**
the hash is wrong, expired, or revoked
— the ledger at `GET /api/shares` is
the check. **401:** the link carries a
password and none (or the wrong one)
was given; the web page asks, and API
callers send the `X-SHARE-PASSWORD`
header. **Works, but shouldn't:** the
link was forwarded, as links are — the
remedy is revocation, not complaint,
and a password on the replacement.

## The server prints a warning about being wound down

It is not a warning about your
installation, and nothing you configured
caused it. The program announces its
project's status on every start
(chapters 1 and 11). Read it once,
decide where your copy lives, and let
the rest of the diary — `Listening
on …` — tell you the server is up.
