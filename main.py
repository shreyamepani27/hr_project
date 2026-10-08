import tkinter as tk
from tkinter import ttk, messagebox
from record_manager import load_records, add_record, delete_record, search_records
from analytics import completion_statistics, department_statistics, program_statistics, average_scores_by_program
from charts import show_bar_chart, show_pie_chart, show_line_chart

records = load_records()
BG, HEADER, DARK, CARD = "#EAF4FB", "#176B87", "#0F4C63", "#FFFFFF"
TEXT, MUTED, BLUE, GREEN, ORANGE = "#243447", "#6B7280", "#2386A8", "#2E9B57", "#E39B22"
PURPLE, RED, BORDER = "#7A5AF8", "#D9534F", "#C9D9E2"

cols = ["Employee ID", "Employee Name", "Department", "Program", "Status", "Score", "Date"]

def refresh_table(data=None):
    tree.delete(*tree.get_children())
    for r in records if data is None else data:
        tree.insert("", "end", values=[r[c] for c in cols])

def update_dashboard():
    s = completion_statistics(records)
    scores = [float(r["Score"]) for r in records if r.get("Score")]
    avg = sum(scores) / len(scores) if scores else 0
    total_value.config(text=str(s["total"]))
    avg_value.config(text=f"{avg:.1f}")
    completed_value.config(text=f"{s['rate']:.1f}%")
    high_value.config(text=str(sum(x >= 80 for x in scores)))
    highest_value.config(text=f"{max(scores) if scores else 0:.0f}")

def clear_entries():
    for e in entries: e.delete(0, tk.END)
    status_var.set("Completed")

def save_record():
    data = {"Employee ID":id_entry.get().strip(), "Employee Name":name_entry.get().strip(),
            "Department":dept_entry.get().strip(), "Program":program_entry.get().strip(),
            "Status":status_var.get(), "Score":score_entry.get().strip(), "Date":date_entry.get().strip()}
    try:
        add_record(data, records); refresh_table(); update_dashboard(); clear_entries()
        messagebox.showinfo("Success", "Training record saved successfully.")
    except ValueError as e: messagebox.showerror("Validation Error", str(e))
    except Exception as e: messagebox.showerror("Error", f"Could not save record:\n{e}")

def search(): refresh_table(search_records(records, search_entry.get().strip()))
def reset_search(): search_entry.delete(0, tk.END); refresh_table()

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Delete Record", "Please select a record from the table.")
        return
    values = tree.item(selected[0], "values")
    index = next((i for i,r in enumerate(records) if [r[c] for c in cols] == list(values)), None)
    if index is None: return
    if messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?"):
        delete_record(index, records); refresh_table(); update_dashboard()
        messagebox.showinfo("Deleted", "Record deleted successfully.")

def show_statistics():
    s, d, p = completion_statistics(records), department_statistics(records), program_statistics(records)
    avg = average_scores_by_program(records)
    msg = (f"Total Training Records : {s['total']}\nCompleted              : {s['completed']}\n"
           f"In Progress            : {s['in_progress']}\nCompletion Rate        : {s['rate']:.2f}%\n"
           f"Departments            : {len(d)}\nPrograms               : {len(p)}\n\nAverage Scores by Program:\n")
    msg += "\n".join(f"• {name}: {score}" for name,score in avg.items())
    messagebox.showinfo("Training Statistics", msg)

def make_card(parent, title, value, color):
    f = tk.Frame(parent,bg=CARD,highlightbackground=BORDER,highlightthickness=1,height=70)
    f.pack(side="left",fill="x",expand=True,padx=5); f.pack_propagate(False)
    tk.Label(f,text=title,font=("Segoe UI",9,"bold"),bg=CARD,fg=MUTED).pack(pady=(9,0))
    v=tk.Label(f,text=value,font=("Segoe UI",17,"bold"),bg=CARD,fg=color); v.pack(pady=(1,0)); return v

def field(parent,label,row,col):
    tk.Label(parent,text=label,bg="#DCEFF8",fg=TEXT,font=("Segoe UI",9,"bold")).grid(row=row,column=col,sticky="w",padx=7,pady=(2,1))
    e=tk.Entry(parent,width=25,font=("Segoe UI",9),bg="white",fg=TEXT,relief="solid",bd=1)
    e.grid(row=row+1,column=col,padx=7,pady=(0,2),ipady=2); return e

def button(parent,text,command,color,**kw):
    b=tk.Button(parent,text=text,command=command,bg=color,fg="white",activebackground=DARK,activeforeground="white",
                font=("Segoe UI",9,"bold"),relief="flat",cursor="hand2",**kw)
    return b

root=tk.Tk(); root.title("HR Training Management and Analysis System"); root.geometry("1240x820"); root.minsize(1050,760); root.configure(bg=BG)
header=tk.Frame(root,bg=HEADER,height=82); header.pack(fill="x"); header.pack_propagate(False)
tf=tk.Frame(header,bg=HEADER); tf.pack(expand=True)
tk.Label(tf,text="HR TRAINING MANAGEMENT AND ANALYSIS SYSTEM",font=("Segoe UI",20,"bold"),bg=HEADER,fg="white").pack(pady=(12,0))
tk.Label(tf,text="Record  •  Analyze  •  Understand Employee Training",font=("Segoe UI",9),bg=HEADER,fg="#D8F1FA").pack(pady=(2,0))

cards=tk.Frame(root,bg=BG); cards.pack(fill="x",padx=18,pady=12)
total_value=make_card(cards,"TOTAL RECORDS","0",BLUE); avg_value=make_card(cards,"AVERAGE SCORE","0.0",PURPLE)
completed_value=make_card(cards,"COMPLETION RATE","0%",GREEN); high_value=make_card(cards,"HIGH SCORE (80+)","0",ORANGE); highest_value=make_card(cards,"HIGHEST SCORE","0",RED)

form=tk.LabelFrame(root,text="  Add Training Record  ",font=("Segoe UI",10,"bold"),bg="#DCEFF8",fg=DARK,bd=1,relief="solid",padx=10,pady=5)
form.pack(fill="x",padx=18,pady=5)
id_entry=field(form,"Employee ID",0,0); name_entry=field(form,"Employee Name",0,1); dept_entry=field(form,"Department",0,2); program_entry=field(form,"Training Program",0,3)
score_entry=field(form,"Performance Score (0-100)",2,0); date_entry=field(form,"Date (YYYY-MM-DD)",2,1)
tk.Label(form,text="Status",bg="#DCEFF8",fg=TEXT,font=("Segoe UI",9,"bold")).grid(row=2,column=2,sticky="w",padx=7,pady=(2,1))
status_var=tk.StringVar(value="Completed")
status_box=ttk.Combobox(form,textvariable=status_var,values=["Completed","In Progress","Not Started"],state="readonly",width=22)
status_box.grid(row=3,column=2,padx=7,pady=(0,2),ipady=2)
area=tk.Frame(form,bg="#DCEFF8"); area.grid(row=3,column=3,padx=7,sticky="e")
button(area,"ADD RECORD",save_record,BLUE,padx=16,pady=7).pack(side="left",padx=4)
button(area,"CLEAR",clear_entries,"#718096",padx=16,pady=7).pack(side="left",padx=4)
entries=[id_entry,name_entry,dept_entry,program_entry,score_entry,date_entry]

sf=tk.LabelFrame(root,text="  Search / Filter Records  ",font=("Segoe UI",10,"bold"),bg=BG,fg=DARK,bd=1,relief="solid",padx=10,pady=6)
sf.pack(fill="x",padx=18,pady=6)
tk.Label(sf,text="Employee / Department / Program:",bg=BG,fg=TEXT,font=("Segoe UI",9,"bold")).pack(side="left",padx=5)
search_entry=tk.Entry(sf,width=32,font=("Segoe UI",9),relief="solid",bd=1); search_entry.pack(side="left",padx=8,ipady=4)
for txt,cmd,col in [("SEARCH",search,BLUE),("SHOW ALL",reset_search,"#718096"),("STATISTICS",show_statistics,PURPLE),("DELETE RECORD",delete_selected,RED)]:
    button(sf,txt,cmd,col,padx=12,pady=5).pack(side="left",padx=3)

tk.Label(root,text="Training Records",bg=BG,fg=DARK,font=("Segoe UI",11,"bold")).pack(anchor="w",padx=20,pady=(3,1))
table_frame=tk.Frame(root,bg=BG); table_frame.pack(fill="x",padx=18,pady=2); table_frame.configure(height=205); table_frame.pack_propagate(False)
tree=ttk.Treeview(table_frame,columns=cols,show="headings",height=7)
for c in cols: tree.heading(c,text=c); tree.column(c,width=150,anchor="center")
for c,w in [("Employee ID",100),("Employee Name",155),("Department",130),("Program",190),("Status",115),("Score",80),("Date",110)]: tree.column(c,width=w)
style=ttk.Style(); style.theme_use("clam"); style.configure("Treeview",background="white",foreground=TEXT,rowheight=27,fieldbackground="white",font=("Segoe UI",9)); style.configure("Treeview.Heading",background="#D5E8F0",foreground=DARK,font=("Segoe UI",9,"bold"),padding=6); style.map("Treeview",background=[("selected","#B9E1EF")])
scroll=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview); tree.configure(yscrollcommand=scroll.set); tree.pack(side="left",fill="both",expand=True); scroll.pack(side="right",fill="y")

tk.Label(root,text="Training Analysis Reports",bg=BG,fg=DARK,font=("Segoe UI",10,"bold")).pack(pady=(4,1))
cf=tk.Frame(root,bg="#DCEFF8",highlightbackground=BORDER,highlightthickness=1); cf.pack(fill="x",padx=18,pady=(0,8),ipady=5)
def chart_btn(txt,cmd,col,hover):
    b=button(cf,txt,cmd,col,padx=15,pady=7); b.pack(side="left",padx=8,pady=2); b.bind("<Enter>",lambda e:b.configure(bg=hover)); b.bind("<Leave>",lambda e:b.configure(bg=col))
chart_btn("BAR CHART",lambda:show_bar_chart(records),BLUE,DARK); chart_btn("PIE CHART",lambda:show_pie_chart(records),ORANGE,"#B86F00")
chart_btn("LINE CHART",lambda:show_line_chart(records),GREEN,"#20753F")

refresh_table(); update_dashboard(); root.mainloop()
