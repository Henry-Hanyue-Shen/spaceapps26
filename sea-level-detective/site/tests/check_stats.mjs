// Check that the browser statistics (site/stats.js) reproduce pipeline/stats.py.
// Run: node site/tests/check_stats.mjs   (from the nasa_spaceapps_2026 folder)
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { fitWindow, tPPF, tSF } from "../stats.js";

const here = dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(readFileSync(join(here, "../data/series.json"), "utf8"));
const refs = JSON.parse(readFileSync(join(here, "../data/reference_fits.json"), "utf8"));
let failures = 0;
const close = (a, b, tol, label) => {
  const ok = Math.abs(a - b) <= tol * Math.max(1, Math.abs(b));
  if (!ok) { failures++; console.log(`FAIL ${label}: js=${a} py=${b}`); }
};
close(tPPF(0.975, 10), 2.2281388519649385, 1e-6, "t ppf df=10");
close(tSF(2, 5.5), 0.04851, 2e-3, "t sf");
for (const r of refs) {
  const s = data.regions[r.region];
  const end = r.end;
  const a = fitWindow(s, r.start, end);
  close(a.trend, r.trend, 1e-6, `${r.region} ${r.start} trend`);
  close(a.ci[0], r.ci[0], 1e-4, `${r.region} ${r.start} ci lo`);
  close(a.ci[1], r.ci[1], 1e-4, `${r.region} ${r.start} ci hi`);
  close(a.rho, r.rho, 1e-6, `${r.region} ${r.start} rho`);
  if (r.trend_enso !== undefined) {
    const b = fitWindow(s, r.start, end, data.indices.noaa_oni);
    close(b.trend, r.trend_enso, 1e-6, `${r.region} ${r.start} trend_enso`);
    close(b.ci[0], r.ci_enso[0], 1e-4, `${r.region} ${r.start} ci_enso lo`);
    close(b.indexCoef, r.coef_enso, 1e-6, `${r.region} ${r.start} coef_enso`);
  }
}
console.log(failures ? `${failures} check(s) failed` : `all ${refs.length} reference fits match Python`);
process.exit(failures ? 1 : 0);
