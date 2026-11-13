# herdr-setup

My [Herdr](https://herdr.dev) desktop app setup.
The main piece is **Cozy Pixel**, a layout with a pixel-art sidebar: spaces and agents grouped by machine, and every agent shown as a cozy chibi character in its machine's scene.

<img src="pixel/preview.png" alt="Cozy Pixel sidebar" width="300">

![All characters on every scene](docs/sprites.svg)

## Install

Copy the layout into your Herdr app home, then switch to it:

```sh
cp -R pixel/layouts pixel/themes pixel/mods ~/.config/herdr-app/
herdr-app check ~/.config/herdr-app/mods/pixel-spaces
herdr-app check ~/.config/herdr-app/mods/pixel-agents
herdr-app do layout.switch '{"name":"pixel"}'
```

Restart Herdr once so the pixel font loads.
`ctrl-shift-l` switches back to your previous layout.

The spaces mod runs `git` in each space's folder and `hc machine` commands, the same as Herdr's own spaces list.
Neither mod downloads anything from the internet.

<details>
<summary><b>Change the art</b></summary>

Anyone who installed Cozy Pixel can change its art on their own machine.
Edit the installed copy in `~/.config/herdr-app/mods/pixel-agents/`, not the one in this repo: Herdr only reads its own folder.

1. Edit a grid in `sprites.py`, or add a new entry to `CHARS` there.
2. Run `python3 sprites.py` in that folder. Herdr picks up the new SVGs right away.
3. For a new character, also add its name to `AVATARS` in `main.js`.

To pin a machine to a scene, add it to `SCENE_OF` in `main.js`, e.g. `{ vps: "den" }`.

Want to share your changes back?
Fork this repo, copy your edited files into your fork's `pixel/mods/pixel-agents/`, and open a pull request.

</details>

<details>
<summary><b>What's in this repo</b></summary>

| Path | What it is |
|---|---|
| `pixel/` | The Cozy Pixel layout, in the herdr.dev layout format (`RECIPE.md`, `preview.png`, `layouts/`, `themes/`, `mods/`). |
| `home/` | My `settings.json` and `keys.json`. |
| `docs/sprites.svg` | Every character on every scene. |
| `sync.sh` | Copies the live setup from `~/.config/herdr-app` into this repo. |

</details>

<details>
<summary><b>Owner notes: restore and sync</b></summary>

This repo is my backup.
On a new machine, after installing, I also copy my personal files:

```sh
cp home/settings.json home/keys.json ~/.config/herdr-app/
```

After changing anything in the app, I copy the live files in and push:

```sh
./sync.sh && git add -A && git commit -m "Sync Herdr setup" && git push
```

In a fork, `sync.sh` works the same way, but it also copies your own `settings.json` and `keys.json` into `home/`.

</details>

## License

The code, layout, theme and pixel art are licensed under the [Apache License 2.0](LICENSE), Copyright 2026 Denny Raymond.
You can use, change and share them, including commercially, as long as you keep the license and the notices in [NOTICE](NOTICE).

- `pixel-spaces` and `pixel-agents` are modified from the `spaces` and `agents` mods shipped with [Herdr](https://github.com/herdrdev/herdr-app) 0.1.15, also Apache 2.0. Each says what changed at the top of its `main.js`.
- [Departure Mono](https://departuremono.com) by Helena Zhang is under the SIL Open Font License 1.1 (`pixel/mods/pixel-spaces/fonts/LICENSE-DepartureMono.txt`), not Apache.
- The pixel art is original, drawn for this setup in a cozy chibi fantasy style inspired by [KayKit Adventurers](https://kaylousberg.itch.io/kaykit-adventurers). No KayKit assets are used.
