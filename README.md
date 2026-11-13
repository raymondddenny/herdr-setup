# herdr-setup

My [Herdr](https://herdr.dev) desktop app setup.
The main piece is **Cozy Pixel**, a layout with a pixel-art sidebar: spaces and agents grouped by machine, and every agent shown as a chibi adventurer in a cozy scene.

<img src="pixel/preview.png" alt="Cozy Pixel sidebar" width="300">

## What's here

| Path | What it is |
|---|---|
| `pixel/` | The Cozy Pixel layout, in the herdr.dev layout format (`RECIPE.md`, `preview.png`, `layouts/`, `themes/`, `mods/`). |
| `home/` | My `settings.json` and `keys.json`. |
| `docs/sprites.svg` | Every adventurer on every scene. |
| `sync.sh` | Copies the live setup from `~/.config/herdr-app` into this repo. |

![Sprites](docs/sprites.svg)

## Install Cozy Pixel

Copy the layout into your Herdr app home, then switch to it.

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

## Restore my whole setup

On a new machine, also copy the personal files:

```sh
cp home/settings.json home/keys.json ~/.config/herdr-app/
```

## Change the art

The scenes and adventurers are text grids in `pixel/mods/pixel-agents/sprites.py`.
Edit a grid or add a character, run `python3 sprites.py` in that folder, and Herdr picks up the new SVGs right away.
To pin a machine to a scene, add it to `SCENE_OF` in `pixel/mods/pixel-agents/main.js`.

## Keep this repo in sync

After changing anything in the app:

```sh
./sync.sh && git add -A && git commit -m "Sync Herdr setup"
```

## Credits

- `pixel-spaces` and `pixel-agents` are modified from the `spaces` and `agents` mods shipped with [Herdr](https://github.com/herdrdev/herdr-app) 0.1.15, Apache License 2.0 (see `LICENSE`).
- [Departure Mono](https://departuremono.com) by Helena Zhang, SIL Open Font License 1.1 (`pixel/mods/pixel-spaces/fonts/LICENSE-DepartureMono.txt`).
- The pixel art is original, drawn for this setup in a cozy chibi fantasy style inspired by [KayKit Adventurers](https://kaylousberg.itch.io/kaykit-adventurers); no KayKit assets are used.
