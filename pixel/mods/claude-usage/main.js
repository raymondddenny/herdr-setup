// Cozy Pixel: your Claude plan usage (the 5-hour session and the week) as pixel bars.
// Claude Code pipes `rate_limits` into its status line command; bin/claude-usage-tap
// saves it to .cache/usage.json (hidden, so writing there does not reload this mod).

import { View, div, svg } from "gpui-kit";
import { v_flex, h_flex } from "gpui-base";
import { theme, appHome, readTextFile, layout, exec, notify, nextCommand } from "herdr";

const PIXEL = "Departure Mono"; // ships in mods/pixel-spaces/fonts
const CELLS = 14;
const pad = (n) => String(n).padStart(2, "0");

function find(node, id) {
  if (node?.id === id) return node;
  for (const child of node?.children ?? []) {
    const found = find(child, id);
    if (found) return found;
  }
  return null;
}
const narrow = () => (find(layout(), "sidebar")?.size?.px ?? Infinity) < 160;

const MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
const SPAN = { five_hour: 5 * 3600, seven_day: 7 * 86400 }; // each window's length

// Time left: "42M", "3H 05M", "6D 02H".
function left(sec, now) {
  const m = Math.max(1, Math.ceil((sec - now) / 60));
  if (m < 60) return `${m}M`;
  const h = Math.floor(m / 60);
  return h < 24 ? `${h}H ${pad(m % 60)}M` : `${Math.floor(h / 24)}D ${pad(h % 24)}H`;
}

// How long ago the numbers were confirmed: "NOW", "4M AGO", "2H AGO".
function ago(sec, now) {
  const m = Math.floor((now - sec) / 60);
  return m < 1 ? "NOW" : m < 60 ? `${m}M AGO` : m < 1440 ? `${Math.floor(m / 60)}H AGO` : `${Math.floor(m / 1440)}D AGO`;
}

// A reset moment: its time for the session ("16:00"), its date for the week ("NOV 13").
function stamp(sec, long) {
  const d = new Date(sec * 1000);
  return long ? `${MONTHS[d.getMonth()]} ${d.getDate()}` : `${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default class ClaudeUsage extends View {
  init(_props, cx) {
    this.file = `${appHome()}/mods/claude-usage/.cache/usage.json`;
    this.limits = null;
    this.load(cx);
    cx.timer.every(30000, (cx) => this.load(cx));
    // `herdr-app do claude-usage.refresh` does what the refresh button does.
    cx.spawn(async (cx) => {
      for (;;) if ((await nextCommand()) === "refresh") this.refresh(cx);
    });
  }

  // Also puts the tap back if something reset Claude Code's status line (Orca does when
  // it updates); the replaced command is kept and still runs after the tap.
  load(cx) {
    cx.spawn(async (cx) => {
      const fix = await exec("python3", [`${appHome()}/bin/claude-usage-tap`, "--ensure"]).catch(() => null);
      if (fix?.stdout.includes("repaired")) notify({ title: "Claude usage", body: "Re-added the status line tap; your other status line still runs after it." });
      const text = await readTextFile(this.file).catch(() => null);
      try { this.limits = text ? JSON.parse(text) : null; } catch { /* half-written; next time */ }
      cx.notify();
    });
  }

  // The refresh button: asks Anthropic for the current numbers, signed in as Claude Code.
  refresh(cx) {
    if (this.busy) return;
    this.busy = true;
    cx.notify();
    cx.spawn(async (cx) => {
      const r = await exec("python3", [`${appHome()}/bin/claude-usage-tap`, "--fetch"], { timeout: 30000 }).catch((e) => ({ code: 1, stderr: String(e.message ?? e) }));
      this.busy = false;
      if (r.code !== 0) notify({ title: "Couldn't refresh Claude usage", body: (r.stderr ?? "").trim().split("\n").pop() || "Unknown error.", level: "warning" });
      this.load(cx);
    });
  }

  // The window started (last reset) one span before its reset time. Once that time has
  // passed the limit is back to 0, shown as RESET until Claude Code sends new numbers.
  metric(key, now) {
    const lim = this.limits?.[key];
    if (!lim) return null;
    const long = key === "seven_day";
    if (lim.resets_at <= now) return { pct: 0, reset: true, when: "RESET", note: `RESET ${stamp(lim.resets_at, long)}` };
    return {
      pct: Math.round(lim.used_percentage),
      when: left(lim.resets_at, now),
      note: `RESET ${stamp(lim.resets_at - SPAN[key], long)} · NEXT ${stamp(lim.resets_at, long)}`,
    };
  }

  color(pct, t) {
    return pct >= 90 ? t.blocked : pct >= 70 ? t.accent : t.working;
  }

  row(label, m, t) {
    const color = this.color(m.pct, t);
    const lit = m.pct > 0 ? Math.max(1, Math.round((m.pct / 100) * CELLS)) : 0;
    return v_flex().gap(5)
      .child(h_flex().gap(8).items_center()
        .child(div().flex_none().text_color(t.muted).child(label))
        .child(div().flex_none().text_color(color).child(`${m.pct}%`))
        .child(div().flex_1())
        .child(div().flex_none().text_size(11).text_color(m.reset ? t.done : t.dim).child(m.when)))
      .child(h_flex().gap(2).children(Array.from({ length: CELLS }, (_, i) =>
        div().flex_1().h(7).bg(i < lit ? color : color + "26"))))
      .child(div().text_size(10.5).text_color(t.dim).child(m.note));
  }

  render() {
    const t = theme();
    const now = Date.now() / 1000;
    const session = this.metric("five_hour", now);
    const week = this.metric("seven_day", now);
    const root = v_flex().size_full().min_h(0).bg(t.chrome).border_t(1).border_color(t.border).font_family(PIXEL).text_size(12);

    if (narrow()) {
      return root.items_center().justify_center().gap(4)
        .children([session, week].filter(Boolean).map((m) => div().text_color(this.color(m.pct, t)).child(`${m.pct}%`)));
    }
    return root.px(16).pt(14).gap(10)
      .child(h_flex().justify_between().text_color(t.dim)
        .child(h_flex().gap(7).child(div().text_color(t.input).child("▒▒")).child("USAGE"))
        .child(h_flex().gap(8).items_center()
          .when(Boolean(this.limits?.at), (el) => el.child(this.busy ? "CHECKING" : ago(this.limits.at, now)))
          .child(div().id("refresh").flex_none().cursor_pointer().text_color(this.busy ? t.input : t.dim)
            .hover((s) => s.text_color(t.foreground))
            .tooltip("Check Claude usage now")
            .on_click((_e, cx) => this.refresh(cx))
            .child(svg(this.busy ? "mods/workspace-chrome/spinner.svg" : "mods/claude-usage/refresh.svg").size(12)))))
      .when(!session && !week, (el) => el.child(div().text_size(11.5).text_color(t.dim)
        .child("Shows after Claude Code's next reply (Pro and Max plans).")))
      .when(Boolean(session), (el) => el.child(this.row("SESSION", session, t)))
      .when(Boolean(week), (el) => el.child(this.row("WEEK", week, t)));
  }
}
