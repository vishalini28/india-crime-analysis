import pandas as pd
import matplotlib.pyplot as plt

# 1. Load and prepare data
ipc = pd.read_csv("1_datasets/processed/ipc_city_2021_2023.csv")
vio = pd.read_csv("1_datasets/processed/violent_city_2021_2023.csv")
df = ipc.merge(vio[["city", "violent_2023"]], on="city")
df["growth_pct"] = (df.ipc_2023 - df.ipc_2021) / df.ipc_2021 * 100
df["violent_share"] = df.violent_2023 / df.ipc_2023 * 100

# 2. Page setup (A4)
fig, axs = plt.subplots(2, 2, figsize=(8.27, 11.69))
fig.subplots_adjust(top=0.82, bottom=0.24, left=0.2, right=0.95, hspace=0.45, wspace=0.75)
fig.suptitle("Crime in Indian Metropolitan Cities, 2021-2023", fontsize=16, fontweight="bold", y=0.96)
fig.text(0.5, 0.905, "Based on NCRB 'Crime in India 2023' | 34 cities", ha="center", fontsize=10, color="gray")

# 3. Chart 1: highest crime rate
top = df.nlargest(8, "ipc_rate_2023").sort_values("ipc_rate_2023")
axs[0, 0].barh(top.city, top.ipc_rate_2023, color="#d94f4f")
axs[0, 0].set_title("Highest crime rate (2023)\ncases per lakh people", fontsize=10)

# 4. Chart 2: total crimes by year
totals = [df.ipc_2021.sum(), df.ipc_2022.sum(), df.ipc_2023.sum()]
axs[0, 1].bar(["2021", "2022", "2023"], totals, color="#4f81d9")
axs[0, 1].set_title("Total crimes, all 34 cities", fontsize=10)

# 5. Chart 3: fastest growth
grow = df.nlargest(8, "growth_pct").sort_values("growth_pct")
axs[1, 0].barh(grow.city, grow.growth_pct, color="#e8a33d")
axs[1, 0].set_title("Fastest growth, 2021 to 2023\n% change in reported crimes", fontsize=10)

# 6. Chart 4: violent crime share
vs = df.nlargest(8, "violent_share").sort_values("violent_share")
axs[1, 1].barh(vs.city, vs.violent_share, color="#7a4fd9")
axs[1, 1].set_title("Violent crime share (2023)\n% of all IPC crimes", fontsize=10)

for ax in axs.flat:
    ax.tick_params(labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)

# 7. Key findings text, written from the data
hi = df.loc[df.ipc_rate_2023.idxmax()]
gr = df.loc[df.growth_pct.idxmax()]
vi = df.loc[df.violent_share.idxmax()]
change = (totals[2] - totals[0]) / totals[0] * 100
findings = (
    "KEY FINDINGS\n"
    f"1. {hi.city} has the highest crime rate: {hi.ipc_rate_2023:.0f} cases per lakh people.\n"
    f"2. {gr.city} grew fastest: {gr.growth_pct:.0f}% more reported crimes than in 2021.\n"
    f"3. {vi.city} has the highest violent share: {vi.violent_share:.0f}% of its crimes.\n"
    f"4. Total crimes across the 34 cities changed by {change:.1f}% from 2021 to 2023."
)
fig.text(0.08, 0.15, findings, fontsize=10, va="top", linespacing=1.6,
         bbox=dict(boxstyle="round", facecolor="#f2f2f2", edgecolor="#cccccc"))

fig.text(0.08, 0.045,
         "Source: NCRB, Crime in India 2023 (Table 1B.1, 1C.3), via OpenCity.in. "
         "Rates use 2011 Census population.\nLarge jumps may reflect changes in reporting, "
         "not only real changes in crime. Covers only the 34 cities in the table.",
         fontsize=7, color="gray", va="top")

# 8. Save
fig.savefig("3_visual_report/crime_report.png", dpi=200)
fig.savefig("3_visual_report/crime_report.pdf")
print("Saved 3_visual_report/crime_report.png and 3_visual_report/crime_report.pdf")
