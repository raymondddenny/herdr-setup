// Cozy Pixel: your Claude plan usage (the 5-hour session and the week) as pixel bars.
// Claude Code pipes `rate_limits` into its status line command; bin/claude-usage-tap
// saves it to .cache/usage.json (hidden, so writing there does not reload this mod).

import { View, div } from "gpui-kit";
import { v_flex, h_flex } from "gpui-base";
import { theme, appHome, readTextFile, layout, exec, notify } from "herdr";

const PIXEL = "Departure Mono"; // ships in mods/pixel-spaces/fonts
const CELLS = 14;
const DAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
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

// "2H 05M" until a reset within a day, else its weekday and time ("FRI 14:00").
function resets(sec, now) {
  const m = Math.max(1, Math.ceil((sec - now) / 60));
  if (m < 60) return `${m}M`;
  if (m < 24 * 60) return `${Math.floor(m / 60)}H ${pad(m % 60)}M`;
  const d = new Date(sec * 1000);
  return `${DAYS[d.getDay()]} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default class ClaudeUsage extends View {
  init(_props, cx) {
    this.file = `${appHome()}/mods/claude-usage/.cache/usage.json`;
    this.limits = null;
    this.load(cx);
    cx.timer.every(30000, (cx) => this.load(cx));
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

  // A limit whose reset time has passed is back to 0 until Claude Code says otherwise.
  metric(lim, now) {
    if (!lim) return null;
    const live = lim.resets_at > now;
    return { pct: live ? Math.round(lim.used_percentage) : 0, when: live ? resets(lim.resets_at, now) : "" };
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
        .when(Boolean(m.when), (el) => el.child(div().flex_none().text_size(11).text_color(t.dim).child(m.when))))
      .child(h_flex().gap(2).children(Array.from({ length: CELLS }, (_, i) =>
        div().flex_1().h(7).bg(i < lit ? color : color + "26"))));
  }

  render() {
    const t = theme();
    const now = Date.now() / 1000;
    const session = this.metric(this.limits?.five_hour, now);
    const week = this.metric(this.limits?.seven_day, now);
    const root = v_flex().size_full().min_h(0).bg(t.chrome).border_t(1).border_color(t.border).font_family(PIXEL).text_size(12);

    if (narrow()) {
      return root.items_center().justify_center().gap(4)
        .children([session, week].filter(Boolean).map((m) => div().text_color(this.color(m.pct, t)).child(`${m.pct}%`)));
    }
    return root.px(16).pt(14).gap(10)
      .child(h_flex().justify_between().text_color(t.dim)
        .child(h_flex().gap(7).child(div().text_color(t.input).child("▒▒")).child("USAGE"))
        .child("CLAUDE"))
      .when(!session && !week, (el) => el.child(div().text_size(11.5).text_color(t.dim)
        .child("Shows after Claude Code's next reply (Pro and Max plans).")))
      .when(Boolean(session), (el) => el.child(this.row("SESSION", session, t)))
      .when(Boolean(week), (el) => el.child(this.row("WEEK", week, t)));
  }
}
