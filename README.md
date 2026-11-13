# herdr-setup

My [Herdr](https://herdr.dev) desktop app setup.
The main piece is **Cozy Pixel**, a layout with a pixel-art sidebar: spaces and agents grouped by machine, and every agent shown as a cozy chibi character in its machine's scene.

<img src="pixel/preview.png" alt="Cozy Pixel sidebar" width="300">

## Characters

Each space gets its own character, standing in its machine's scene: `DUSK` for this computer, then `DEN`, `GROVE`, `KEEP` or `CAVE` for the others.
Characters come in packs, and you can switch packs with one command.

### Cozy pack (default)

<table>
<tr>
<td align="center" width="25%"><img src="docs/chars/knight.svg" width="96" alt="Knight"><br><b>Knight</b><br>Off duty: messy hair, striped scarf, a mug of cocoa.</td>
<td align="center" width="25%"><img src="docs/chars/wizard.svg" width="96" alt="Wizard"><br><b>Wizard</b><br>Sleepy, in a floppy knit hat and a mustard sweater.</td>
<td align="center" width="25%"><img src="docs/chars/ranger.svg" width="96" alt="Ranger"><br><b>Ranger</b><br>A leaf-sprout beanie and a warm poncho.</td>
<td align="center" width="25%"><img src="docs/chars/dwarf.svg" width="96" alt="Dwarf"><br><b>Dwarf</b><br>Pompom beanie, big ginger beard, a mug.</td>
</tr>
<tr>
<td align="center"><img src="docs/chars/cleric.svg" width="96" alt="Cleric"><br><b>Cleric</b><br>Wrapped in a patchwork quilt, holding a candle.</td>
<td align="center"><img src="docs/chars/bard.svg" width="96" alt="Bard"><br><b>Bard</b><br>Beret, striped sweater, a ukulele.</td>
<td align="center"><img src="docs/chars/cat.svg" width="96" alt="Cat"><br><b>Cat</b><br>Grey tabby in a mustard scarf, with a ball of yarn.</td>
<td align="center"><img src="docs/chars/fox.svg" width="96" alt="Fox"><br><b>Fox</b><br>Green scarf and a white-tipped tail.</td>
</tr>
<tr>
<td align="center"><img src="docs/chars/bunny.svg" width="96" alt="Bunny"><br><b>Bunny</b><br>Blue knit sweater, hugging a carrot.</td>
<td align="center"><img src="docs/chars/owl.svg" width="96" alt="Owl"><br><b>Owl</b><br>Big round eyes, reading a red book.</td>
<td align="center"><img src="docs/chars/frog.svg" width="96" alt="Frog"><br><b>Frog</b><br>Yellow raincoat and a big grin.</td>
<td align="center"><img src="docs/chars/bear.svg" width="96" alt="Bear"><br><b>Bear</b><br>Red scarf, holding a honey pot.</td>
</tr>
<tr>
<td align="center"><img src="docs/chars/raccoon.svg" width="96" alt="Raccoon"><br><b>Raccoon</b><br>Teal hoodie, sneaking a cookie.</td>
<td align="center"><img src="docs/chars/penguin.svg" width="96" alt="Penguin"><br><b>Penguin</b><br>Pink earmuffs and a red striped scarf.</td>
<td></td>
<td></td>
</tr>
</table>

### Christmas pack

The scenes go festive too: a garland of lights everywhere, and snow on the porch and in the garden.

<table>
<tr>
<td align="center" width="25%"><img src="docs/chars/santa.svg" width="96" alt="Santa"><br><b>Santa</b><br>Pompom hat, fluffy beard, gold buckle.</td>
<td align="center" width="25%"><img src="docs/chars/elf.svg" width="96" alt="Elf"><br><b>Elf</b><br>Pointy ears and a hat with a bell.</td>
<td align="center" width="25%"><img src="docs/chars/reindeer.svg" width="96" alt="Reindeer"><br><b>Reindeer</b><br>Antlers, a glowing red nose, a green scarf.</td>
<td align="center" width="25%"><img src="docs/chars/snowman.svg" width="96" alt="Snowman"><br><b>Snowman</b><br>Red beanie, carrot nose, coal buttons.</td>
</tr>
<tr>
<td align="center"><img src="docs/chars/gingerbread.svg" width="96" alt="Gingerbread"><br><b>Gingerbread</b><br>Icing smile and candy buttons.</td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

### Switch packs

Press `cmd-alt-p` while the Cozy Pixel layout is shown to cycle packs, or use a terminal:

```sh
herdr-app do pixel-agents.next-pack        # cycle: Cozy -> Christmas -> Cozy
herdr-app do pixel-agents.pack-christmas   # pick one by name
herdr-app do pixel-agents.pack-cozy
```

A toast confirms the switch, and the choice survives restarts.

### Coming soon

<table>
<tr>
<td align="center" width="25%"><img src="docs/chars/soon.svg" width="96" alt="Coming soon"><br><b>Hedgehog</b><br>Coming soon</td>
<td align="center" width="25%"><img src="docs/chars/soon.svg" width="96" alt="Coming soon"><br><b>Axolotl</b><br>Coming soon</td>
</tr>
</table>

<details>
<summary><b>Every character on every scene</b></summary>

![Every Cozy character on every scene](docs/sprites.svg)

![Every Christmas character on every festive scene](docs/sprites-christmas.svg)

</details>

## Install

Copy the layout into your Herdr app home, then switch to it:

```sh
cp -R pixel/layouts pixel/themes pixel/mods ~/.config/herdr-app/
herdr-app check ~/.config/herdr-app/mods/pixel-spaces
herdr-app check ~/.config/herdr-app/mods/pixel-agents
herdr-app do layout.switch '{"name":"pixel"}'
```

For the `cmd-alt-p` pack shortcut, add the `layout:pixel` section from `pixel/keys.json` to your `~/.config/herdr-app/keys.json` (merge it; don't replace the file).

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
3. For a new character, also add its name to a pack's `chars` in `PACKS` in `main.js`. A new pack is a new entry in `PACKS`; `festive: true` makes it use the `-xmas` scenes.

To pin a machine to a scene, add it to `SCENE_OF` in `main.js`, e.g. `{ vps: "den" }`.

Want to share your changes back?
Fork this repo, copy your edited files into your fork's `pixel/mods/pixel-agents/`, and open a pull request.

</details>

<details>
<summary><b>What's in this repo</b></summary>

| Path | What it is |
|---|---|
| `pixel/` | The Cozy Pixel layout, in the herdr.dev layout format (`RECIPE.md`, `preview.png`, `layouts/`, `themes/`, `mods/`, `keys.json`). |
| `home/` | My `settings.json` and `keys.json`. |
| `docs/` | The README images: one card per character and the full sprite sheets. |
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

Copyright 2026 Denny Raymond. Two licenses apply; [NOTICE](NOTICE) says exactly which files each covers.

- **Code** (the mods, the layout, the theme, the code in `sprites.py`, `sync.sh`): [Apache License 2.0](LICENSE). Use, change and share it, including commercially, keeping the license and NOTICE.
- **Pixel art** (the characters and scenes: their drawings in `sprites.py`, the SVGs, `docs/`, `preview.png`): [CC BY-NC 4.0](LICENSE-ART). Use, change and share it with credit to "Cozy Pixel art by Denny Raymond" and a link here, for non-commercial use only. Ask me for commercial use.
- `pixel-spaces` and `pixel-agents` are modified from the `spaces` and `agents` mods shipped with [Herdr](https://github.com/herdrdev/herdr-app) 0.1.15, also Apache 2.0. Each says what changed at the top of its `main.js`.
- [Departure Mono](https://departuremono.com) by Helena Zhang is under the SIL Open Font License 1.1 (`pixel/mods/pixel-spaces/fonts/LICENSE-DepartureMono.txt`), not Apache.
- The pixel art is original, drawn for this setup in a cozy chibi fantasy style inspired by [KayKit Adventurers](https://kaylousberg.itch.io/kaykit-adventurers). No KayKit assets are used.
