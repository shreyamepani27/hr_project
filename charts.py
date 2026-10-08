import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

BLUE, GREEN, ORANGE, RED, PURPLE = "#2F6FAE", "#16A34A", "#F59E0B", "#EF4444", "#7C3AED"

def prepare_data(records):
    df = records.copy() if isinstance(records, pd.DataFrame) else pd.DataFrame(records)
    if df.empty: return df
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    return df.dropna(subset=["Score"])

def show_bar_chart(records):
    df = prepare_data(records)
    if df.empty: return
    data = df.groupby("Program")["Score"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(data.index, data.values, color=BLUE, edgecolor="white", linewidth=1.5)
    ax.set(title="Average Performance by Training Program", xlabel="Training Program", ylabel="Average Score", ylim=(0, 100))
    ax.grid(axis="y", alpha=.20); ax.set_axisbelow(True); plt.xticks(rotation=20)
    for b, v in zip(bars, data.values): ax.text(b.get_x()+b.get_width()/2, v+2, f"{v:.1f}", ha="center", fontweight="bold")
    plt.tight_layout(); plt.show()

def show_pie_chart(records):
    df = prepare_data(records)
    if df.empty: return
    data = df["Status"].value_counts()
    colors = [{"Completed":GREEN, "In Progress":ORANGE, "Not Started":RED}.get(x, BLUE) for x in data.index]
    fig, ax = plt.subplots(figsize=(7, 7))
    _, _, texts = ax.pie(data.values, labels=data.index, autopct="%1.1f%%", startangle=90,
                         colors=colors, explode=[.03]*len(data), wedgeprops={"edgecolor":"white","linewidth":2})
    for t in texts: t.set_fontweight("bold")
    ax.set_title("Training Completion Status", fontweight="bold", pad=15)
    plt.tight_layout(); plt.show()

def show_line_chart(records):
    df = prepare_data(records)
    if df.empty: return
    scores = np.array(df["Score"], dtype=float); x = np.arange(1, len(scores)+1)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(x, scores, marker="o", markersize=7, linewidth=3, color=BLUE, markerfacecolor=GREEN, markeredgecolor="white")
    ax.fill_between(x, scores, alpha=.08, color=BLUE)
    ax.set(title="Employee Training Performance Trend", xlabel="Training Record Number", ylabel="Performance Score", ylim=(0,100), xticks=x)
    ax.grid(True, alpha=.20)
    for a,b in zip(x,scores): ax.text(a,b+3,f"{b:.0f}",ha="center",fontsize=8)
    plt.tight_layout(); plt.show()

def show_all_charts(records):
    df = prepare_data(records)
    if df.empty: return
    fig, ax = plt.subplots(1, 3, figsize=(17, 5.5))
    p = df.groupby("Program")["Score"].mean().sort_values(ascending=False)
    bars = ax[0].bar(p.index,p.values,color=BLUE,edgecolor="white")
    ax[0].set(title="Average Score by Program",ylabel="Score",ylim=(0,100)); ax[0].tick_params(axis="x",rotation=30); ax[0].grid(axis="y",alpha=.2)
    for b,v in zip(bars,p.values): ax[0].text(b.get_x()+b.get_width()/2,v+2,f"{v:.1f}",ha="center",fontsize=8,fontweight="bold")
    s=df["Status"].value_counts(); colors=[{"Completed":GREEN,"In Progress":ORANGE,"Not Started":RED}.get(x,BLUE) for x in s.index]
    ax[1].pie(s.values,labels=s.index,autopct="%1.1f%%",startangle=90,colors=colors,wedgeprops={"edgecolor":"white","linewidth":2}); ax[1].set_title("Training Completion Status",fontweight="bold")
    scores=np.array(df["Score"],dtype=float); x=np.arange(1,len(scores)+1)
    ax[2].plot(x,scores,marker="o",linewidth=2.5,color=BLUE,markerfacecolor=GREEN); ax[2].fill_between(x,scores,alpha=.08,color=BLUE)
    ax[2].set(title="Performance Trend",xlabel="Record Number",ylabel="Score",ylim=(0,100)); ax[2].grid(True,alpha=.2)
    plt.suptitle("HR Training Analysis Reports",fontsize=17,fontweight="bold"); plt.tight_layout(); plt.show()
