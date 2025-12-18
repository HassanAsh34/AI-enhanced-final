#need to be retested

import random
import time

import tkinter as tk

from tkinter import  messagebox , ttk

import matplotlib.colors as colorlib

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from PIL import Image , ImageTk
from Tools.demo.sortvisu import steps
from fontTools.merge.util import first
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nltk import align
from numpy.ma.extras import average
from unicodedata import decimal

import Node as n

import BackTracking as b

import CulturalAlgorithm as CA


def add_edge(edge_input):#tested
    # global optimal_bk, optimal_ca, nodes, g , ax , ax2, ax3 , canvas , canvas2 , canvas3
    # optimal_bk = optimal_ca = optimal = None
    global  g
    result = n.addEdgesGUI(g,edges=edge_input,nodes=nodes)
    if result == 1:
        a, b = map(int, edge_input.split())
        messagebox.showinfo("Success",f"Connected node {a} and {b}")
        # n.printGraphGUI(g, canvas, ax, optimal, colors)
        # n.printGraphGUI(g, canvas2, ax2, optimal, colors)
        # n.printGraphGUI(g, canvas3, ax3, optimal, colors)
        Update_canvas()
    else:
        messagebox.showerror("error",message=result)

def add_edge_randomly():#tested
    # global optimal_bk, optimal_ca, nodes, g
    # optimal_bk = optimal_ca = optimal = None
    global  g , nodes
    if (len(nodes) > 1):
        node = nodes[0]
        n.addEdgesRandomly(g, node, nodes)
        messagebox.showinfo("Success","edges were added successfully")
        Update_canvas()
    else:
        messagebox.showerror("Error","can't generate random edges with only one node")

def add_node():#tested
    # global optimal_bk , optimal_ca , nodes ,g , ax, ax2 , ax3 , canvas3 , canvas2 , canvas
    # optimal_bk = optimal_ca = optimal = None
    global  g , nodes
    node = n.Node()
    nodes.append(node)
    g.add_node(node.Id)
    messagebox.showinfo("Success", "Node was added successfully")
    Update_canvas()

def go_to_main():#tested
    # global g, nodes , colors , ax, ax2 , ax3 , canvas3 , canvas2 , canvas
    global g, nodes , colors
    try:
        nodesCount = int(entry_node.get())
        colorCount = int(entry_color.get())
        if nodesCount <= 0 or colorCount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter positive integers")
        return
    # if nodes is None:
    #     nodes = list()
    colors = random.sample([
        c for c in list(colorlib.CSS4_COLORS.keys())
        if not any(shade in c for shade in ['light', 'dark', 'medium','black'])
    ], colorCount)
    print(colors)

    for i in range(nodesCount):
        node = n.Node()
        nodes.append(node)
        g.add_node(node.Id)
        g.add_node(node.Id)
    main_frame.pack_forget()
    controlframe.pack(fill=tk.BOTH,expand=True)
    Update_canvas()
    # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # n.printGraphGUI(g, canvas, ax, None, colors)
    # n.printGraphGUI(g, canvas2, ax2, None, colors)
    # n.printGraphGUI(g, canvas3, ax3, None, colors)

def update_ca_canvas(optimal_ca = None):
    global canvas3, canvas6, ax3 , g , colors
    # canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # canvas6.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    n.printGraphGUI(g, ax3, optimal_ca if optimal_ca is not None else None, colors,canvas3,canvas6)
    # n.printGraphGUI(g, canvas6, ax3, optimal_ca if optimal_ca is not None else None, colors)

def update_bt_canvas(optimal_bk = None):
    global canvas2, canvas5, ax2 , g ,  colors
    # canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # canvas5.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    n.printGraphGUI(g, ax2, optimal_bk if optimal_bk is not None else None, colors, canvas2,canvas5)
    # n.printGraphGUI(g, canvas5, ax2, optimal_bk if optimal_bk is not None else None, colors)

def Update_canvas(flag = 0):
    global canvas, ax,optimal_bk, optimal_ca , colors ,  g
    if(flag == 1):#update bk
        update_bt_canvas(optimal_bk)
    elif(flag == 2):#update ca
        update_ca_canvas(optimal_ca)
    else:#update all
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        n.printGraphGUI(g, ax, None, colors, canvas)
        update_bt_canvas()
        update_ca_canvas()

def create_metric_card(parent, title, var = None, color="#3498db",flag = True):
    #
    if flag:
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
    else:
        card = tk.Frame(parent, bg="white")
    card.pack(fill=tk.X, pady=8, padx=5)
    if title != "":
        title_label = tk.Label(card, text=title, bg="white", fg="#34495e",
                               font=("Arial", 10, "bold"), anchor="w")
        title_label.pack(fill=tk.X, padx=15, pady=(10, 5))
    widget = None
    if var is not None:
        if var is tk.Entry:
            widget = tk.Entry(card)
            widget.pack(fill=tk.X, padx=15, pady=(0, 10))
        elif var is tk.Button:
            widget = tk.Button(card, text=title)
            widget.pack(pady=(5, 10))
        else:
            value_label = tk.Label(card, textvariable=var, bg="white", fg=color,
                               font=("Arial", 12), anchor="w", wraplength=350)
            value_label.pack(fill=tk.X, padx=15, pady=(0, 10))

    return card , widget


def run_Backtracking():#tested
    global optimal_bk , timeBackTracking , pickbtnBT , nodes , colors
    start = time.time()
    if len(timeBackTracking) == 0 and pickbtnBT is None:
        pickbtnBT = tk.Button(left_frame2, text="Pick another solution", command=lambda: another_Sol_bt())
        pickbtnBT.pack(pady=5)
        # tk.Label(left_frame4, textvariable=minCnum, bg="white", font=("Arial", 14)).pack(pady=5)
        # tk.Label(left_frame4, textvariable=numofOptimalsolFounded, bg="white", font=("Arial", 14)).pack(pady=5)
        # tk.Label(left_frame4, textvariable=bk_average, bg="white", font=("Arial", 14)).pack(pady=5)
        # tk.Label(left_frame4, textvariable=runtime_variable, bg="white", font=("Arial", 14)).pack(pady=5)
    solutions = b.getSolutions(lnodes=nodes, lcolor=colors)
    if not solutions:
        messagebox.showerror("Error","current number of colors is insufficient")
    else:
        evsols = n.evaluateSolutions(solutions)
        minnum = evsols[0][0]
        optimal_bk = [sols for cnum, sols in evsols if cnum == minnum]
        print(evsols)
        # print(solutions)
        end = time.time()
        runtime = end - start
        messagebox.showinfo("Success",f"""chromatic number is {minnum} and {len(optimal_bk)} optimal solutions found
                it took {runtime:.6f} seconds to complete""")
        minCnum.set(f"minimum chromatic number is {minnum}")
        timeBackTracking.append(runtime)
        bk_average.set(f"average runtime take by algorithm is {np.average(timeBackTracking)} seconds")
        runtime_variable.set(f"runtime = {runtime} seconds")
        numofOptimalsolFounded.set(f"only {len(optimal_bk)} optimal solutions were found")
        Update_canvas(1)

def add_color(): #tested i want to add itto the initial screen
    global colors
    color = random.choice(list(colorlib.CSS4_COLORS.keys()))
    while color in colors:
        color = random.choice(list(colorlib.CSS4_COLORS.keys()))
    colors.append(color)
    messagebox.showinfo("Success","A new color was added")

def another_Sol_bt(ca = False):#tested
    global  optimal_bk, optimal_ca
    if(ca):
        if optimal_ca is not None and len(optimal_ca) > 0:
            Update_canvas(2)
        else:
            messagebox.showerror("Error","you should run the algorithm first")
    else:
        if optimal_bk is not None and len(optimal_bk) > 0:
           Update_canvas(1)
        else:
            messagebox.showerror("Error","you should run the algorithm first")

def run_cultural_alg():
    global g, nodes , colors , optimal_ca , timeCulturalAlgorithm , pickbtnCA , converged_at , ax4 , ax5 , ax6 , ax7 ,fig4,fig5,fig6,fig7, canvas7 , canvas8 ,canvas9,canvas10, minCnum2
    start = time.time()
    # flag = False
    try:
        pop_size = int(entry_pop_size.get()) if entry_pop_size.get() != "" else 0
        mutaion = float(entry_mutaion.get()) if entry_mutaion.get() != "" else 0.0
        belief_size = int(entry_belief_size.get()) if entry_belief_size.get() != "" else 0
        threshold = float(entry_threshold.get()) if entry_threshold.get() != "" else 1e-3
        influece = int(entry_influenceRate.get())/100 if entry_influenceRate.get() != "" else .6
        if pop_size <= 0 or mutaion <= 0  or belief_size <= 0:
            raise ValueError
    except ValueError:
        # if flag:
        #     messagebox.showerror("Error","some fields are empty")
        if mutaion > 1:
            messagebox.showerror("Error","Mutation rate should be a value between 0 and 1")
        elif threshold > 1 or threshold < 0 :
            # if entry_threshold.get() == "":
            #     threshold = 1e-3
            # else:
            messagebox.showerror("Error", "Threshold should be a value between 0 and 1")
        elif influece > .8 or influece <= 0:
            # if entry_influenceRate.get() == "":
            #     influece = .6
            # else:
            messagebox.showerror("Error","influence rate should be a value greater than 0 and less than 80% to avoid overfitting of model")
        else:
            messagebox.showerror("Error", "Please enter positive integers")
        return

    belief_space, population, average_fitnessListforPopulation, average_chromaticNumberListforPopulation, avg_fitnessforBelief, average_chromaticNumberListforBelief, converged_atiter = CA.CulturalAlgorithm(nodes, colors, g,  pop_size, mutaion,belief_size,influece,threshold)
    end = time.time()
    runtime = end - start

    # print(f"""population
    #                       {population}""")
    # print("-------------------")
    # print(f"""belief
    #                       {belief_space}""")
    # print("-------------------")
    print(f"""avg fitness for belief
                            {np.average(avg_fitnessforBelief)}
              avg fitness
                              {np.average(average_fitnessListforPopulation)}""")
    print("-------------------")
    print(f"""avg chromatic for belief 
                              {int(np.average(average_chromaticNumberListforBelief))}
              avg chromatic 
                              {int(np.average(average_chromaticNumberListforPopulation))}""")
    print(len(belief_space), len(population),len(avg_fitnessforBelief),len(average_fitnessListforPopulation))
    optimal_ca = [belief[0] for  belief in belief_space]
    minCnum2.set(belief_space[0][3])
    # print(minCnum2)
    # numofElitesFound = tk.StringVar()

    step = 1000
    converged_at.set(converged_atiter)
    numitertion = converged_atiter / 1000
    # iter = 1000 + step * np.arange(len(avg_fitnessforBelief))
    iter = step * np.arange(1.0,numitertion+1)
    # iter2 = 1000 + step * np.arange(len(average_fitnessListforPopulation))
    iter2 = step * np.arange(0.0,numitertion+1)
    print(iter)
    print(len(iter))
    print(avg_fitnessforBelief)
    print(len(avg_fitnessforBelief))
    print(iter2)
    print(len(iter2))
    print(average_fitnessListforPopulation)
    print(len(average_fitnessListforPopulation))

    if len(timeCulturalAlgorithm) == 0 and pickbtnCA is None:
        pickbtnCA = tk.Button(left_frame3, text="Pick another solution", command=lambda: another_Sol_bt(True))
        pickbtnCA.pack(pady=5)

    ax4.cla()
    ax4.set_xlabel("iteration number in 1000")
    ax4.set_ylabel("average fitness rate")
    ax4.plot(iter, avg_fitnessforBelief)
    fig4.tight_layout()

    ax6.cla()
    ax6.set_xlabel("iteration number in 1000")
    ax6.set_ylabel("average chromatic number")
    ax6.plot(iter,average_chromaticNumberListforBelief)
    fig6.tight_layout()

    ax5.cla()
    ax5.set_xlabel("iteration number in 1000")
    ax5.set_ylabel("average fitness rate")
    ax5.plot(iter2, average_fitnessListforPopulation)
    fig5.tight_layout()

    ax7.cla()
    ax7.set_xlabel("iteration number in 1000")
    ax7.set_ylabel("average chromatic number")
    ax7.plot(iter2, average_chromaticNumberListforPopulation)
    fig7.tight_layout()
    # redraw the Tk canvases so the new plots appear
    canvas7.draw()
    canvas8.draw()
    canvas9.draw()
    canvas10.draw()
    timeCulturalAlgorithm.append(runtime)
    ca_average.set(np.average(timeCulturalAlgorithm))
    Update_canvas(2)


def BacktoInitial():
    global g, nodes,optimal_ca,optimal_bk,timeBackTracking,timeCulturalAlgorithm,colors,pickbtnCA,pickbtnBT
    pickbtnCA = pickbtnBT = optimal_ca = optimal_bk = colors = None
    g.clear()
    n.Node(True)
    nodes.clear()
    timeBackTracking.clear()
    timeCulturalAlgorithm.clear()
    if pickbtnBT is not None:
        pickbtnBT.destroy()
    if pickbtnCA is not None:
        pickbtnCA.destroy()
    controlframe.pack_forget()
    main_frame.pack(fil=tk.BOTH, expand=True)


g = n.nx.Graph()

nodes = list()

pickbtnBT = None

pickbtnCA = None

optimal_ca = None

optimal_bk = None

timeBackTracking = list()

timeCulturalAlgorithm = list()

colors = None

root = tk.Tk()



# initial screen
root.title("Graph Coloring GUI")

root.geometry("1280x720")
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame_right = tk.Frame(main_frame,width=500,bg="#FAF9F6")
main_frame_right.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
main_frame_left = tk.Frame(main_frame)
main_frame_left.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

initialForm = tk.Frame(master=main_frame_right,width=400,bg="white", relief=tk.RAISED, bd=1)
initialForm.pack(fill=tk.X, padx=10, pady= 150 )
title_label = tk.Label(initialForm, text="Create Graph", bg="white", fg="#34495e",
                       font=("Arial", 10, "bold"), anchor="w")
title_label.pack(expand=True)
# entry_node.pack(pady=5)
# entry_node2 = tk.Entry(main_frame_right)
# entry_node.pack(pady=5)
card , entry_node =create_metric_card(initialForm,"Enter Number of Nodes:",tk.Entry,"white",False)
card2 , entry_color = create_metric_card(initialForm,"Enter Number of Colors:",tk.Entry,"white",False)
# btn = tk.Button(initialForm,text="Next",command=lambda  :go_to_main())
card3 , nextBtn = create_metric_card(initialForm,"",tk.Button,"white",False)
nextBtn.configure(text = "Next",command=lambda  :go_to_main(),bg="#3498db")
# card1 , _ = create_metric_card(initialForm,)
# card.forget()
# tk.Label(main_frame_right,text="",bg="lightgray").pack(pady=5)
# entry_color = tk.Entry(main_frame_right)
# entry_color.pack(pady=5)


img = Image.open("Logo.png")

canvas4= tk.Canvas(main_frame_left,highlightthickness=0)
canvas4.pack(fill=tk.BOTH,expand=True)

def resize_image(event):
    global tk_img
    resized = img.resize((event.width, event.height), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(resized)
    canvas4.delete("all")
    canvas4.create_image(0, 0, anchor="nw", image=tk_img)

canvas4.bind("<Configure>", resize_image)


# controlscreen

controlframe = tk.Frame(root)
notebook = ttk.Notebook(controlframe)
notebook.pack(fill=tk.BOTH,expand=True)

# display
tab_display = ttk.Frame(notebook)
notebook.add(tab_display,text="Draw Graph")

left_frame = tk.Frame(tab_display,width=300,bg="#FAF9F6")
left_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=5,pady=5)

drawgraphForm = tk.Frame(master=left_frame,width=200,bg="white", relief=tk.RAISED, bd=1)
drawgraphForm.pack(fill=tk.X, padx=10, pady= 15 )

title_label = tk.Label(drawgraphForm, text="Draw Graph", bg="white", fg="#34495e",
                       font=("Arial", 10, "bold"), anchor="w")
title_label.pack(expand=True)

card4 , entry_edge =create_metric_card(drawgraphForm,"Add Edge:",tk.Entry,"white",False)
card5 , AddEdgeBtn = create_metric_card(drawgraphForm,"",tk.Button,flag=False)
AddEdgeBtn.configure(text = "Add Edge",command=lambda: add_edge(entry_edge.get()), bg="#27ae60")

card6 , AddNodeBtn = create_metric_card(drawgraphForm,"",tk.Button,flag=False)
AddNodeBtn.configure(text="Add Node",command=lambda: add_node(), bg="#3498db")

card7 , AddGenerateEdgesBtn = create_metric_card(drawgraphForm,"",tk.Button,flag=False)
AddGenerateEdgesBtn.configure(text="Generate Edges",command=lambda: add_edge_randomly(), bg="#9b59b6")

card8 , BackBtn = create_metric_card(drawgraphForm,"",tk.Button,flag=False)
BackBtn.configure(text="Back to initial screen",command=lambda: BacktoInitial(),bg="#e74c3c")

# tk.Label(left_frame, text="Add Edge:").pack(pady=5)
# entry_edge = tk.Entry(left_frame)
# entry_edge.pack(pady=5)
# tk.Button(left_frame, text="Add Edge", ).pack(pady=5)
# tk.Button(left_frame, text="Add Node", command=lambda: add_node()).pack(pady=5)
# tk.Button(left_frame, text="Generate Edges", command=lambda: add_edge_randomly()).pack(pady=5)
#
# tk.Button(left_frame,text="Back to initial screen",command= lambda:  BacktoInitial()).pack(pady=5)


right_frame = tk.Frame(tab_display,bg="white")
right_frame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True,padx=5,pady=5)

fig, ax = plt.subplots(figsize=(5,5))
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



# backtracking
tab_backtracking = ttk.Frame(notebook)
notebook.add(tab_backtracking,text="Backtracking")
left_frame2 = tk.Frame(tab_backtracking,width=300,bg="#FAF9F6")
left_frame2.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=5,pady=5)
BackTrackingForm = tk.Frame(master=left_frame2,width=200,bg="white", relief=tk.RAISED, bd=1)
BackTrackingForm.pack(fill=tk.X, padx=10, pady= 15 )
title_label = tk.Label(BackTrackingForm, text="Backtracking", bg="white", fg="#34495e",
                       font=("Arial", 10, "bold"), anchor="w")
title_label.pack(expand=True)

card9 , RunBTBtn = create_metric_card(BackTrackingForm,"",tk.Button,flag=False)
RunBTBtn.configure(text = "Run",command=lambda: run_Backtracking(), bg="#27ae60")

card10 , AddColorBtn = create_metric_card(BackTrackingForm,"",tk.Button,flag=False)
AddColorBtn.configure(text="Add Color",command=lambda: add_color(), bg="#3498db")



right_frame2 = tk.Frame(tab_backtracking,bg="white")
right_frame2.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True,padx=5,pady=5)
fig2, ax2 = plt.subplots(figsize=(5,5))
canvas2 = FigureCanvasTkAgg(fig2, master=right_frame2)
canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
n.printGraphGUI(g, ax2, None, colors,canvas2)
# tk.Button(left_frame2, text="Run", command=lambda: run_Backtracking()).pack(pady=5)
# tk.Button(left_frame2,text="Add Color",command= lambda : add_color()).pack(pady=5)



#Cutural algorithm
tab_Cultural = ttk.Frame(notebook)
notebook.add(tab_Cultural,text="Cutural Algorithm")
left_frame3= tk.Frame(tab_Cultural,width=300,bg="#FAF9F6")
left_frame3.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=5,pady=5)

CAForm = tk.Frame(master=left_frame3,width=200,bg="white", relief=tk.RAISED, bd=1)
CAForm.pack(fill=tk.X, padx=10, pady= 15 )
title_label = tk.Label(CAForm, text="Cultural Algorithm", bg="white", fg="#34495e",
                       font=("Arial", 10, "bold"), anchor="w")
title_label.pack(expand=True)
# entry_node.pack(pady=5)
# entry_node2 = tk.Entry(main_frame_right)
# entry_node.pack(pady=5)
card10 , entry_pop_size =create_metric_card(CAForm,"Population Size",tk.Entry,"white",False)
card11 , entry_belief_size = create_metric_card(CAForm,"Belief space Size",tk.Entry,"white",False)
card12 , entry_mutaion =create_metric_card(CAForm,"Mutaion Rate",tk.Entry,"white",False)
card13 , entry_threshold = create_metric_card(CAForm,"Threshold: default 1x10^-3",tk.Entry,"white",False)
card14 , entry_influenceRate = create_metric_card(CAForm,"Influence Rate: default 60%",tk.Entry,"white",False)
# tk.Button(left_frame3,text="run",command= lambda : run_cultural_alg()).pack(pady=5)
card15 , RunCABtn = create_metric_card(CAForm,"",tk.Button,"white",False)
RunCABtn.configure(text = "Run",command=lambda  :run_cultural_alg(),bg="#27ae60")



right_frame3 = tk.Frame(tab_Cultural,bg="white")
right_frame3.pack(side= tk.RIGHT,fill=tk.BOTH,expand=True,padx=5,pady=5)
# tk.Label(left_frame3,text="Population Size").pack(pady=5)
# entry_pop_size = tk.Entry(left_frame3)
# entry_pop_size.pack(pady=5)
# tk.Label(left_frame3,text="Belief space Size").pack(pady=5)
# entry_belief_size = tk.Entry(left_frame3)
# entry_belief_size.pack(pady=5)
# tk.Label(left_frame3,text="Mutaion Rate").pack(pady=5)
# entry_mutaion = tk.Entry(left_frame3)
# entry_mutaion.pack(pady=5)
# tk.Label(left_frame3,text="Threshold: default 1x10^-3").pack(pady=5)
# entry_threshold = tk.Entry(left_frame3)
# entry_threshold.pack(pady=5)
# tk.Label(left_frame3,text="Influence Rate: default 60%").pack(pady=5)
# entry_influenceRate = tk.Entry(left_frame3)
# entry_influenceRate.pack(pady=5)
fig3, ax3 = plt.subplots(figsize=(5,5))
canvas3 = FigureCanvasTkAgg(fig3,master=right_frame3)
canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
n.printGraphGUI(g,ax3, None,colors,canvas3)
# tk.Button(left_frame3,text="run",command= lambda : run_cultural_alg()).pack(pady=5)

#comparison
tab_Comparison = ttk.Frame(notebook)
notebook.add(tab_Comparison,text="Performance Metrics")
notebook2 = ttk.Notebook(tab_Comparison)
notebook2.pack(fill=tk.BOTH,expand=True)
tab_backtracking_metrics = ttk.Frame(notebook2)
notebook2.add(tab_backtracking_metrics,text="Backtracking")

left_frame4 = tk.Frame(tab_backtracking_metrics, width=400, bg="white")
left_frame4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
header_frame4 = tk.Frame(left_frame4, bg="#2c3e50", relief=tk.RAISED, bd=2)
header_frame4.pack(fill=tk.X, pady=(0, 15))
tk.Label(header_frame4, text="Backtracking Algorithm", bg="#2c3e50", fg="white",
         font=("Arial", 16, "bold")).pack(pady=10)
minCnum = tk.StringVar()
numofOptimalsolFounded = tk.StringVar()
bk_average = tk.StringVar()
runtime_variable = tk.StringVar()

metrics_container4 = tk.Frame(left_frame4, bg="white")
metrics_container4.pack(fill=tk.BOTH, expand=True, padx=5)
create_metric_card(metrics_container4, "Minimum Chromatic Number", minCnum, "#e74c3c")
create_metric_card(metrics_container4, "Optimal Solutions Found", numofOptimalsolFounded, "#27ae60")
create_metric_card(metrics_container4, "Average Runtime", bk_average, "#3498db")
create_metric_card(metrics_container4, "Last Runtime", runtime_variable, "#9b59b6")

right_frame4 = tk.Frame(tab_backtracking_metrics,width=880,bg="gray")
right_frame4.pack(side= tk.RIGHT,fill=tk.BOTH,expand=True,padx=5,pady=5)
graph_header4 = tk.Frame(right_frame4, bg="#34495e", relief=tk.FLAT)
graph_header4.pack(fill=tk.X)
tk.Label(graph_header4, text="Graph Visualization", bg="#34495e", fg="white",
         font=("Arial", 12, "bold")).pack(pady=8)
canvas5 = FigureCanvasTkAgg(fig2,master=right_frame4)
canvas5.get_tk_widget().pack(fill=tk.BOTH,expand=True)

tab_Cultural_metrics = ttk.Frame(notebook2)
notebook2.add(tab_Cultural_metrics,text="Cultural")
left_frame5 = tk.Frame(tab_Cultural_metrics,width=500,bg="white")
left_frame5.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=5)
header_frame5 = tk.Frame(left_frame5, bg="#16a085", relief=tk.RAISED, bd=2)
header_frame5.pack(fill=tk.X, pady=(0, 15))
tk.Label(header_frame5, text="Cultural Algorithm", bg="#16a085", fg="white",
         font=("Arial", 16, "bold")).pack(pady=10)

minCnum2 = tk.StringVar()
converged_at = tk.StringVar()
ca_average = tk.StringVar()

right_frame5 = tk.Frame(tab_Cultural_metrics,width=780,bg="gray")
right_frame5.pack(side= tk.RIGHT,fill=tk.BOTH,expand=True,padx=5,pady=5)
graph_header5 = tk.Frame(right_frame5, bg="#16a085", relief=tk.FLAT)
graph_header5.pack(fill=tk.X)
tk.Label(graph_header5, text="Graph Visualization", bg="#16a085", fg="white",
         font=("Arial", 12, "bold")).pack(pady=8)

canvas6 = FigureCanvasTkAgg(fig3,master=right_frame5)
canvas6.get_tk_widget().pack(fill=tk.BOTH,expand=True)
scroll_canvas = tk.Canvas(left_frame5, bg="white")
scroll_canvas.pack(side="left", fill="both", expand=True)

# Scrollbar linked to canvas
scrollbar = tk.Scrollbar(left_frame5, orient="vertical", command=scroll_canvas.yview)
scrollbar.pack(side="right", fill="y")
scroll_canvas.configure(yscrollcommand=scrollbar.set)

# Frame inside canvas to hold widgets
scrollable_frame = tk.Frame(scroll_canvas, bg="white")
scrollable_frame.bind(
    "<Configure>",
    lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
)
scroll_canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
create_metric_card(scrollable_frame, "Minimum Chromatic Number", minCnum2, "#e74c3c")
# create_metric_card(scrollable_frame, "Elite Solutions Found", numofElitesFound, "#27ae60")
create_metric_card(scrollable_frame, "converged at",converged_at, "#27ae60")
create_metric_card(scrollable_frame, "Average Runtime", ca_average, "#3498db")
fig4, ax4 = plt.subplots(1, 1, figsize=(4, 6))
ax4.set_xlabel("iteration number in 1000")
ax4.set_ylabel("average fitness rate")
fig6, ax6 = plt.subplots(1, 1, figsize=(4, 6))
ax6.set_xlabel("iteration number in 1000")
ax6.set_ylabel("average chromatic number")
fig5, ax5 = plt.subplots(1, 1, figsize=(4, 6))
ax5.set_xlabel("iteration number in 1000")
ax5.set_ylabel("average fitness rate")
fig7, ax7 = plt.subplots(1, 1, figsize=(4, 6))
ax7.set_xlabel("iteration number in 1000")
ax7.set_ylabel("average chromatic number")
create_metric_card(scrollable_frame,"Belief space metrics:",None,"#e74c3c")
canvas7 = FigureCanvasTkAgg(fig4, master=scrollable_frame)
canvas7.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas9 = FigureCanvasTkAgg(fig6, master=scrollable_frame)
canvas9.get_tk_widget().pack(fill=tk.BOTH, expand=True)
create_metric_card(scrollable_frame,"Population metrics",None,"#e74c3c")
canvas8 = FigureCanvasTkAgg(fig5, master=scrollable_frame)
canvas8.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas10 = FigureCanvasTkAgg(fig7, master=scrollable_frame)
canvas10.get_tk_widget().pack(fill=tk.BOTH, expand=True)


root.mainloop()
