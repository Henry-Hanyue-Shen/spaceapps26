# Space Apps project page — draft (fill the [NASA: …] blanks after the NASA run)

**Project name:** Sea Level Detective

**High-level summary (≈ 150 words)**
Sea level is rising, but El Niño can raise or lower a coast by 20 cm in a single year, enough to fake or hide a trend
for years. Sea Level Detective is a web tool that lets anyone pick a place and a time window and get a straight answer:
how fast is sea level changing here, is that trend statistically significant, and how much of the change is El Niño?
It uses 33 years of NASA satellite altimetry (NASA-SSH, from TOPEX/Poseidon to Sentinel-6 Michael Freilich) and NASA's
own ENSO indicator. It removes the seasonal cycle, regresses out El Niño, and tests the remaining trend with a method
that accounts for sea level's month-to-month memory. We show why that matters: in 1,000 simulated records with no
trend, ordinary tests claimed a trend 40% of the time, and our test about 7% (a fair test: 5%).

**Link to project demo:** [7-slide deck or ≤30 s video — public link]

**Link to final project:** [GitHub Pages URL of site/ + repository URL]

**Detailed description**
- *What it does.* The user chooses a place (NASA satellite regions: global ocean, western/eastern equatorial Pacific,
  California coast, New York Bight; and NOAA tide gauges at La Jolla, San Francisco and the Battery), a start and end
  year, and whether to remove El Niño. The tool shows the monthly series, the trend with its 95% range, a
  plain-language verdict, the El Niño effect (mm per index unit), and how many years of data a trend of that size needs
  before it can be detected (Weatherhead et al. 1998).
- *How it works.* A Python pipeline downloads NASA-SSH weekly grids and indicators. It converts everything to one
  standard (mm, 1993–2012 average = 0, ocean only, ISO dates) and computes regional series. The statistics fit the
  trend, the annual and semiannual cycles and the ENSO index jointly, with an AR(1) effective-sample-size correction.
  The website repeats exactly the same statistics in the browser (tested against the Python results), so any window
  can be explored.
- *What we found so far.*
  - Only the autocorrelation-adjusted test keeps false alarms near 5%. Hamed–Rao Mann–Kendall gave 18%, plain
    Mann–Kendall 38%, ordinary least squares 40%.
  - On the California coast, sea level rises about 4 cm per °C of the Oceanic Niño Index, with 15–30 cm peaks in
    1997–98 and 2015–16.
  - At New York's Battery, El Niño winters are only 15 mm higher, which is not significant (p = 0.29).
  - [NASA: global rate and acceleration; the west–east seesaw; trends before and after removing El Niño.]
- *Why it matters.* Coastal planning needs regional sea level, and regional trends over short records are easily
  misread. The tool makes the distinction between a real trend and an El Niño year visible and testable.
- *Tools.* Python (xarray, numpy, scipy, statsmodels, pymannkendall, earthaccess), JavaScript, Plotly.js, LaTeX.

**NASA data**
- NASA-SSH Simple Gridded Sea Surface Height from Standardized Reference Missions Only, V1 (PO.DAAC,
  doi:10.5067/NSREF-SG0V1);
- NASA-SSH GMSL indicator (doi:10.5067/NSIND-GMSV1);
- NASA-SSH ENSO and PDO indicators (PO.DAAC).

**Space agency partner data and other references**
- NOAA CO-OPS tide gauges 8518750, 9410230, 9414290;
- NOAA CPC Oceanic Niño Index.

Literature (verified): Nerem et al. 2018; Zhang & Church 2012; Alory & Delcroix 2002; Widlansky et al. 2017;
Boening et al. 2012; Weatherhead et al. 1998; Hamed & Rao 1998; Hamlington et al. 2015, 2020; Sweet & Zervas 2011;
Colle et al. 2010; Matsuno 1966; Boulanger & Menkes 1995 (full list: `argument_tree/`).

**Use of AI (required disclosure)**
- AI tools (Anthropic Claude, OpenAI Codex, Moonshot Kimi) assisted with literature search and citation checking,
  with writing and testing code, and with drafting text.
- The topic (El Niño and sea level from NASA altimetry) came from the team. AI tools helped compare ways to frame it
  for this challenge and to plan the analysis.
- [TEAM TO CONFIRM: this wording against the Space Apps rule that AI should not be used to come up with the idea.]
- Every number comes from the open-source pipeline and was checked by the team.
- No AI-generated images are used; if any are added, they will carry a visible watermark.
