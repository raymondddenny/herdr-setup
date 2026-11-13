// Image and PDF preview pane. Open beside a terminal with
//   pane.split {direction: "right", mod: "file-preview", props: {file: "/absolute/path"}}
// (the Files panel does this on a click). image() only loads files inside Herdr's home,
// so build.sh links the image, or renders the PDF into PNG pages, under .cache/ (hidden,
// so writing there does not reload this mod). This machine's files only.
// Clean-up: a pane deletes its cache folder when it closes; folders older than a day
// (left by a crash or a quit) go the next time a preview opens.

import { View, div, image } from "gpui-kit";
import { v_flex, h_flex } from "gpui-base";
import { props, theme, exec, appHome, readTextFile } from "herdr";

const hash = (s) => [...s].reduce((h, c) => (h * 31 + c.codePointAt(0)) >>> 0, 7).toString(16);
const base = (p) => p.split("/").pop();
const PAD = 14;

export default class FilePreview extends View {
  init(_props, cx) {
    this.file = props()?.file ?? "";
    this.pages = null; // [{ src, w, h }]
    this.error = null;
    this.size = { width: 600, height: 600 };
    cx.spawn(async (cx) => {
      try { this.pages = await this.load(this.file); }
      catch (e) { this.error = String(e.message ?? e); }
      cx.notify();
    });
  }

  // The cache folder is keyed by path and modification time, so an edited file renders anew.
  async load(file) {
    if (!file.startsWith("/")) throw new Error("Needs an absolute path on this computer.");
    const st = await exec("stat", ["-f", "%m", file]);
    if (st.code !== 0) throw new Error("File not found.");
    const rel = `mods/file-preview/.cache/${hash(`${file}\u0000${st.stdout.trim()}`)}`;
    const home = appHome();
    this.dir = `${home}/${rel}`;
    // Leftovers older than a day; folders only, so the compiled pdf2png stays.
    await exec("find", [`${home}/mods/file-preview/.cache`, "-mindepth", "1", "-maxdepth", "1", "-type", "d", "-mmin", "+1440", "-exec", "rm", "-rf", "{}", "+"]).catch(() => null);
    const r = await exec("sh", [`${home}/mods/file-preview/build.sh`, file, `${home}/${rel}`], { timeout: 120000 });
    if (r.code !== 0) throw new Error(r.stderr.trim().split("\n").pop() || "Couldn't render this file.");
    const manifest = await readTextFile(`${home}/${rel}/manifest`);
    const pages = (manifest ?? "").trim().split("\n").filter(Boolean).map((line) => {
      const [name, w, h] = line.split(" ");
      return { src: `${rel}/${name}`, w: Number(w) || 1, h: Number(h) || 1 };
    });
    if (!pages.length) throw new Error("Nothing to show (a locked or empty PDF?).");
    return pages;
  }

  // The pictures stay in memory for this run; only the files on disk go.
  async close() {
    if (this.dir) await exec("rm", ["-rf", this.dir]);
  }

  // One picture fits the pane; pages fill its width and scroll.
  body(t) {
    const width = Math.max(40, this.size.width - PAD * 2);
    const height = Math.max(40, this.size.height - 32 - PAD * 2);
    if (this.pages.length === 1) {
      const p = this.pages[0];
      const s = Math.min(width / p.w, height / p.h, 1);
      return h_flex().flex_1().min_h(0).items_center().justify_center()
        .child(image(p.src).w(Math.round(p.w * s)).h(Math.round(p.h * s)));
    }
    return v_flex().id("pages").flex_1().min_h(0).overflow_y_scrollbar().p(PAD).gap(PAD).items_center()
      .children(this.pages.map((p, i) => v_flex().gap(4).items_center()
        .child(image(p.src).w(width).h(Math.round(width * p.h / p.w)).border(1).border_color(t.border))
        .child(div().text_size(11).text_color(t.dim).child(`${i + 1} / ${this.pages.length}`))));
  }

  render() {
    const t = theme();
    const count = this.pages?.length ?? 0;
    return v_flex().id("root").size_full().min_h(0).bg(t.background).text_color(t.foreground).text_size(12.5)
      .on_size_change((size, cx) => { this.size = size; cx.notify(); })
      .child(h_flex().h(32).flex_none().px(PAD).gap(8).items_center().border_b(1).border_color(t.border)
        .child(div().flex_1().min_w(0).truncate().child(base(this.file) || "Preview"))
        .when(count > 1, (el) => el.child(div().flex_none().text_color(t.dim).child(`${count} pages`)))
        .child(div().id("open").flex_none().px(8).py(2).rounded(5).cursor_pointer().text_color(t.muted)
          .hover((s) => s.bg(t.hover).text_color(t.foreground))
          .on_click(() => exec("open", [this.file]))
          .child("Open in Preview")))
      .when(Boolean(this.error), (el) => el.child(div().p(PAD).text_color(t.blocked).child(this.error)))
      .when(!this.error && !this.pages, (el) => el.child(div().p(PAD).text_color(t.dim).child("Rendering…")))
      .when(Boolean(this.pages), (el) => el.child(this.body(t)));
  }
}
