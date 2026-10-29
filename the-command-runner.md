# The Command Runner

By the end of this chapter File Browser
will have run shell commands two ways:
by itself, as a hook, the moment a file
was uploaded — and interactively, at an
administrator's request, through the
same channel the web page's command box
uses. You will also have met the three
separate gates that keep all of this
switched off until you switch it on.
The check is a log line the lab did not
write: a hook wrote it, naming the file
that triggered it.

This chapter carries a plain warning
before any of its pleasures: a command
runner is a shell with a web address.
Commands run as the user the *server*
runs as, on the *server's* machine.
Only enable it for accounts you would
hand a login shell to, because that is,
in effect, what you are doing.

## Gate one and gate two: it is off twice

Out of the box the runner is disabled at
the server level — `Exec Enabled:
false` in the settings — and each user
also has an Execute switch of their own.
Both must open before anything runs.
Chapter 6's alice has Execute off, and
this chapter will show her being refused
even after the server's gate opens.

Enabling it is management work, so the
server is stopped and the CLI does it:

```bash
./filebrowser config set -d filebrowser.db \
  --shell "bash -c" --disableExec=false
```

Two settings change together. The second
opens gate one. The first names the
**shell** through which commands run —
`bash -c` here. Setting a shell matters
more than it looks: with a shell, hook
commands can use the ordinary furniture
of shell lines (redirection, pipes);
without one, each command is split into
words and run directly, and furniture
like `>>` is just an argument. The
lab's hook needs a redirection, so the
lab set the shell.

## Hooks: commands that fire on events

The `cmds` commands manage **hooks** —
commands attached to events in the
life of a file:

```bash
./filebrowser cmds add after_upload \
  'echo "hook fired for $FILE (user $USERNAME, trigger $TRIGGER, scope $SCOPE)" >> /path/to/hook.log' \
  -d filebrowser.db
./filebrowser cmds ls -d filebrowser.db
```

```text
after_upload(0): echo "hook fired for $FILE (user $USERNAME, trigger $TRIGGER, scope $SCOPE)" >> /home/hatch/workspace/file-browser-lab-work/hook.log
```

Events exist for the whole vocabulary of
chapter 5 — upload, download, save,
rename, copy, delete, most in a `before_`
and an `after_` form — and a `before_`
hook that fails can stop its event,
which makes hooks a policy tool as well
as a logging one.

Here is the trap the lab fell into
first, preserved because you would have
too. An older tradition in tools like
this is placeholders in braces —
`{FILE}` — and the lab's first hook used
them. The hook fired, and the log read:

```text
hook fired for {FILE} (user {USERNAME}, trigger {TRIGGER})
```

Nothing was substituted. This runner
passes its facts as **environment
variables** — `$FILE`, `$USERNAME`,
`$TRIGGER`, `$SCOPE` — for the shell to
expand. With the hook rewritten that
way, an ordinary upload through the API
produced, a second later:

```text
hook fired for /home/hatch/workspace/file-browser-lab-work/root/recipes/herb-oil.txt (user admin, trigger after_upload, scope /)
```

`$FILE` is the file's full path on the
server's disk, `$SCOPE` the uploader's
scope. (Transcript `t12-runner-hook.txt`.)
A hook log like this is a small audit
trail that costs one line of setup —
recipe 5 uses it.

## The interactive runner: a socket, an allowlist

The web page's command box speaks over a
**websocket** — a standing connection —
at `/api/command/`. The lab drove it
with a small Python script (kept at
`file-browser-lab/ws-command.py`), the
token in the `X-Auth` header, and got
the runner's whole character in four
exchanges:

```text
sent: echo hello-from-the-runner
received: hello-from-the-runner

sent: pwd
received: /home/hatch/workspace/file-browser-lab-work/root

sent: whoami
received: Command not allowed.

sent (as alice): echo hello-from-alice
received: Command not allowed.
```

Three facts in that transcript deserve
underlining:

- **Commands run in the user's scope.**
  `pwd` answered with the tree's root
  for the administrator; for a scoped
  user, it answers with their corner.
  The runner's feet are planted where
  the user's eyes are.
- **There is an allowlist per user.**
  The administrator's list, set with
  `users update admin --commands
  "echo,ls,pwd"`, names the commands
  that may be run at all. `whoami` is a
  harmless command that simply is not
  on it, and the refusal is instant and
  total: `Command not allowed.`
- **Gate two is real.** Alice, with
  Execute off, received the same refusal
  for a command that heads the
  administrator's own list. Server gate,
  user switch, allowlist — a command
  must pass all three, and the lab
  watched each of the three say no in
  its turn. (Transcript
  `t13-runner-websocket.txt`.)

Used with that discipline — runner on,
shell chosen, allowlists short — the
command box is a convenience for the
server's owner. Used loosely, it is a
shell prompt on the web, on a program
that will never be patched again.
Chapter 11 does not let that sentence
go unrepeated.
