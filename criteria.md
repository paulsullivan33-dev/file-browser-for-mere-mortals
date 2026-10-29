# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's sentences are stock sentences and pangrams.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 11 names what the tool
   cannot do and what time has done to it: a finished project
   with no security fixes coming, one tree per server, deletion
   with no undo, a database only one writer may touch at a
   time, and a command runner whose power is also its risk.
8. **The ethics rule is in the text, early.** File Browser is
   a door onto real files, so its two capability questions are
   stated before any procedure depends on them: the project's
   winding-down notice is quoted in full in chapter 1, before
   the install, and chapter 7 states plainly that a share link
   is a capability — whoever holds it, holds the file — ahead
   of the instructions for making one.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a small Ubuntu 24.04 sandbox with no
browser and no display. File Browser **2.63.23** — the
project's final release — was installed from the official
archive `linux-amd64-filebrowser.tar.gz`, its SHA-256 checked
against the project's published checksum file before use, and
run unmodified on loopback (127.0.0.1, port 18080). The lab's
root held a small tree of stock fixtures (a picnic list, two
recipes, field notes, a captions file, and one 64 KB file of
random bytes) and two users: an administrator (scope `/`) and
alice (scope `/alice`). All transcripts live in
`file-browser-lab/transcripts/`; the one lab script is
`file-browser-lab/ws-command.py`. The lab's passwords are
throwaways (`lab-admin-pass`, `lab-alice-pass`) and the lab
has been dismantled; nothing they protected exists anymore.

The lab had **no browser**, so the web interface's look and
feel — clicking, dragging, previews rendered on a screen —
was never exercised. What was exercised is the API beneath
the pages, which is the same surface the pages themselves
use: every verb in chapters 4–8 was run against the running
server, and the web pages were fetched and their titles read.
Claims about what a page *shows* are tied to API answers the
lab captured, not to screenshots it never took.

Run for real, with transcripts as evidence:

- Download, checksum verification (`OK`), unpacking, and
  `./filebrowser version` reporting 2.63.23; the full
  `--help` surface of the main, `users`, and `config`
  commands (t00, t01).
- The lab tree's creation and the SHA-256 of its random-byte
  fixture (t02).
- `config init`, `config set` for root/address/port, `users
  add` of the administrator with `--perm.admin`, `users ls`,
  and two full `config cat` printouts (t03) — including the
  defaults this guide cites: file mode 0o640, directory mode
  0o750, minimum password length 12, Exec disabled.
- Server start, the winding-down notice in its log, HTTP 200
  on the front page, and the page title `File Browser`
  (t04).
- API login (a 601-character token), the root listing, and
  the documents listing with the server's own type labels
  (`text`, `blob`) (t05).
- Upload of a 48 KB random file (HTTP 200), its arrival on
  disk with mode 0640, download via `/api/raw/`, and
  `cmp`/SHA-256 identity in both directions — uploaded file
  and a pre-seeded file (t06).
- Folder creation by trailing slash, rename by PATCH with
  the server-side `?checksum=sha256` following the file,
  folder deletion (HTTP 204) (t07).
- Creation of alice through the API, including the two
  failures from a missing and a misnamed (`currentPassword`)
  current-password field — `400 Bad Request (the current
  password is incorrect)` — and the success with
  `current_password`, answered 201 (t08).
- Alice's scope from the inside: her root lists only her two
  files; the real documents folder and a download past her
  scope both answer 404; dot-dot requests (plain and
  percent-encoded) are cleaned and redirected to a non-API
  path serving the web shell, with no data; her delete of her
  own file answers 403 and the file survives; `GET /api/users`
  as alice answers 403 (t09).
- Share links: creation returning hash `wIr1z2i3`, the
  public listing and public download with no token,
  byte-identical by `cmp`; a made-up hash answering 404; the
  list endpoint being `/api/shares` (plural) after the
  singular answered a redirect (t10).
- The runner's CLI: `cmds ls`, `cmds add`, `cmds rm`,
  `config set --shell "bash -c" --disableExec=false` taking
  effect (`Exec Enabled: true`) (t11).
- Hooks: an `after_upload` hook using `{FILE}` placeholders
  fired and wrote them literally; rewritten with environment
  variables, the same hook logged the uploaded file's full
  path, the user, the trigger, and the scope on a real
  upload (t12).
- The interactive runner over its websocket: an allowlisted
  `echo` answered with its output; `pwd` answered with the
  scope root; `whoami` (not allowlisted) and alice (Execute
  off) each received `Command not allowed.` — and the route's
  trailing slash and the token's place in the `X-Auth`
  header were found by experiment (t13, ws-command.py).
- Editing a text file by PUT and reading the changed tail on
  disk; a password-protected share answering 401 with no
  password and with a wrong one, and 200 with a
  byte-identical download when the password arrived in the
  `X-SHARE-PASSWORD` header (t14).
- `filebrowser hash` output (a bcrypt hash), `config
  export` and `users export` (the exports showing the
  settings signing key and both password hashes, which is
  why recipe 4 calls them secrets), the database as a
  single 64 KB file, and the final `users ls` (t15).
- The one-writer rule met on purpose: `users ls` against
  the running server's database failing with `Error:
  timeout`; then share revocation — DELETE answered 200,
  the public address answered 404, and the `/api/shares`
  ledger showed only the remaining link (t16).

Read from the project's source at this version, not run,
and flagged where the text leans on it: the refusal to save
a user with Share but without Download (the handler's check),
and the password-share gate's acceptance of the link's own
token as an alternative credential. Both are stated in the
chapters as properties of the server, and the surrounding
behaviour — the permissions themselves, and the password
flow — was run.

Documented only — described from the project's documentation
and help text, not run, and the text does not claim
otherwise:

- The web interface as a person meets it: signing in on the
  page, clicking through folders, the in-page editor's
  appearance, image thumbnails and previews on a screen,
  drag-and-drop upload.
- The quick-setup mode (server started with no database),
  the Docker installation route, and installation on
  non-Linux systems.
- Share expiry set at creation (the lab's shares carry
  `expire: 0`); sharing a folder rather than a file (same
  mechanism, only the file form run end to end).
- `before_` hooks stopping their event, the other hook
  events beyond `after_upload`, per-user file rules
  (`filebrowser rules`), and user import.
- Folder download as an archive, TUS resumable uploads, TLS
  by certificate flags, base-URL and socket serving,
  branding and themes, the proxy/hook/noauth login methods,
  sign-up, and the `FB_`-prefixed environment variables and
  `.filebrowser` config files named in `--help`.
- The restore half of recipe 4 (the export and backup halves
  were run; the lab did not dismantle its own server to walk
  the return journey).
- All neighbour characterisations in chapter 10.

Fixtures are this guide's own and deliberately generic:
stock lists, recipes, and field notes, a seed-swap list, and
random bytes — no names, organisations, real networks, or
real events, and the one person in the story, alice, is a
stock name with a stock corner of a stock tree.
