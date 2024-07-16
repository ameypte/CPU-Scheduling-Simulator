from tkinter  import *
from matplotlib import pyplot as plt

w = Tk()
w.title("Python")

l = []
at = []
bt = []
ct = []
wt = []
tat = []
processId = []
arrivalTime = []
burstTime = []
turnarroundTime = []
waitingTime = []
completionTime = []
startingTime = []

avgTat = "Avarage Turnaround Time = "
avgWt = "Avarage Waiting Time = "
lbl_avgTat = Label()
lbl_avgWt = Label()


def submit():
    global lbl_avgTat
    global lbl_avgWt
    global completionTime
    global waitingTime
    global turnarroundTime
    global startingTime

    n = int(ent_n.get())
    completionTime = [None] * n
    waitingTime = [None] * n
    turnarroundTime = [None] * n
    startingTime = [None] * n

    for i in range(n):
        s = 'P' + str(i+1)
        processId.append(s)
        l.append(Label(w, font=('arial', 13), text=s))
        l[i].grid(row=int(i+2), column=0, pady=(13, 10), padx=(20, 10))

        at.append(Entry(w, font=('arial', 13), justify=CENTER,
                  width=10, borderwidth=6, relief=FLAT))
        at[i].grid(row=int(i+2), column=1, pady=(13, 10), padx=(20, 10))

        bt.append(Entry(w, font=('arial', 13), justify=CENTER,
                  width=10, borderwidth=6, relief=FLAT))
        bt[i].grid(row=int(i+2), column=2, pady=(13, 10), padx=(20, 10))

        ct.append(Label(w, font=('arial', 13), text=s))
        ct[i].grid(row=int(i+2), column=3, pady=(13, 10), padx=(20, 10))

        tat.append(Label(w, font=('arial', 13), text=s))
        tat[i].grid(row=int(i+2), column=4, pady=(13, 10), padx=(20, 10))

        wt.append(Label(w, font=('arial', 13), text=s))
        wt[i].grid(row=int(i+2), column=5, pady=(13, 10), padx=(20, 10))

    lbl_avgTat = Label(w, font=('arial', 13), text=avgTat)
    lbl_avgTat.grid(row=int(i+3), column=0, columnspan=4, pady=12)
    lbl_avgWt = Label(w, font=('arial', 13), text=avgWt)
    lbl_avgWt.grid(row=int(i+4), column=0, columnspan=4, pady=12)

    btn_fcfs = Button(w, text="FCFS", font=(
        'arial', 13), command=fcfs)
    btn_fcfs.grid(row=int(i+3), column=4, rowspan=2, pady=30)

    btn_sjf = Button(w, text="SJF", font=('arial', 13), command=sjf)
    btn_sjf.grid(column=5, row=(i+3), rowspan=2, pady=30)


class SJF:
    def processData(self, no_of_processes):
        process_data = []
        for i in range(no_of_processes):
            process_Id = processId[i]
            arrival_time = arrivalTime[i]
            burst_time = burstTime[i]
            temporary = ([process_Id, arrival_time, burst_time, 0])
            process_data.append(temporary)
        print(arrivalTime)
        print(burstTime)
        SJF.schedulingProcess(self, process_data)

    def schedulingProcess(self, process_data):
        start_time = []
        exit_time = []
        s_time = 0
        process_data.sort(key=lambda x: x[1])
        # Sort processes according to the Arrival Time
        
        for i in range(len(process_data)):
            ready_queue = []
            temp = []
            normal_queue = []

            for j in range(len(process_data)):
                if (process_data[j][1] <= s_time) and (process_data[j][3] == 0):
                    temp.extend(
                        [process_data[j][0], process_data[j][1], process_data[j][2]])
                    ready_queue.append(temp)
                    temp = []
                elif process_data[j][3] == 0:
                    temp.extend(
                        [process_data[j][0], process_data[j][1], process_data[j][2]])
                    normal_queue.append(temp)
                    temp = []

            if len(ready_queue) != 0:
                ready_queue.sort(key=lambda x: x[2])
                # Sort the processes according to the Burst Time
                
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                for k in range(len(process_data)):
                    if process_data[k][0] == ready_queue[0][0]:
                        break
                process_data[k][3] = 1
                process_data[k].append(e_time)

            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                for k in range(len(process_data)):
                    if process_data[k][0] == normal_queue[0][0]:
                        break
                process_data[k][3] = 1
                process_data[k].append(e_time)

        t_time = SJF.calculateTurnaroundTime(self, process_data)
        w_time = SJF.calculateWaitingTime(self, process_data)
        SJF.printData(self, process_data, t_time, w_time)

    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][4] - process_data[i][1]
            # turnaround_time = completion_time - arrival_time
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_turnaround_time = total_turnaround_time / len(process_data)
        # average_turnaround_time = total_turnaround_time / no_of_processes

        return average_turnaround_time

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][5] - process_data[i][2]
            # waiting_time = turnaround_time - burst_time
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(process_data)
        # average_waiting_time = total_waiting_time / no_of_processes

        return average_waiting_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time):
        global avgTat
        global avgWt
        process_data.sort(key=lambda x: x[0])

        for i in range(len(process_data)):
            for j in range(len(process_data[i])):
                if j == 4:
                    completionTime[i] = int(process_data[i][j])
                    ct[i].config(text=process_data[i][j])
                elif j == 5:
                    turnarroundTime[i] = int(process_data[i][j])
                    tat[i].config(text=process_data[i][j])
                elif j == 6:
                    waitingTime[i] = int(process_data[i][j])
                    wt[i].config(text=process_data[i][j])
            startingTime[i] = (completionTime[i] -
                               turnarroundTime[i])+waitingTime[i]
        avgTat = avgTat + str(average_turnaround_time)
        lbl_avgTat.config(text=avgTat)
        avgWt = avgWt + str(average_waiting_time)
        lbl_avgWt.config(text=avgWt)
        gantt()


def sjf():    
    for i in range(len(at)):
        arrivalTime.append(int(at[i].get()))
        burstTime.append(int(bt[i].get()))
    sjf = SJF()
    sjf.processData(int(ent_n.get()))
    return


def fcfs():
    global avgTat
    global avgWt

    for i in range(len(at)):
        arrivalTime.append(int(at[i].get()))
        burstTime.append(int(bt[i].get()))
    print(arrivalTime)
    print(burstTime)

    i = 0
    zaleleIndex = []

    while (i < sum(burstTime)):
        temp = False
        for j in range(len(arrivalTime)):
            if (arrivalTime[j] <= i):
                if j not in zaleleIndex:
                    remPro = []
                    for t in range(len(arrivalTime)):
                        if t not in zaleleIndex:
                            remPro.append(arrivalTime[t])

                    if min(remPro) >= arrivalTime[j]:
                        i = i + burstTime[j]
                        ct[j].config(text=str(i))
                        completionTime[j] = i

                        tat[j].config(text=str(i-arrivalTime[j]))
                        turnarroundTime[j] = i-arrivalTime[j]

                        wt[j].config(text=str((i-arrivalTime[j])-burstTime[j]))
                        waitingTime[j] = ((i-arrivalTime[j])-burstTime[j])

                        startingTime[j] = (completionTime[j] -
                                           turnarroundTime[j])+waitingTime[j]
                        zaleleIndex.append(j)
                        temp = True
                        break
        if not temp:
            i = i + 1
            temp = False
    avgTat = avgTat + str(sum(turnarroundTime)/len(turnarroundTime))
    lbl_avgTat.config(text=avgTat)
    avgWt = avgWt + str(sum(waitingTime)/len(waitingTime))
    lbl_avgWt.config(text=avgWt)
    gantt()

def gantt():
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 10*len(completionTime))
    gnt.set_xlim(0, max(completionTime))
    gnt.set_title('Gantt Chart')

    yticks = []
    temp = 5
    for i in range(1, len(completionTime)+1):
        yticks.append(temp)
        temp = temp+10

    gnt.set_yticks(yticks)
    gnt.set_yticklabels(processId)
    gnt.grid(True)

    list = ['red', 'orange', 'blue', 'green', 'purple', 'pink', 'brown']

    for i in range(len(arrivalTime)):
        gnt.broken_barh([(startingTime[i], burstTime[i])],
                        (i*10, 10), facecolors=('tab:'+list[i % len(list)]))

    plt.show()


lbl = Label(w, text="Enter number of processes: ", font=('arial', 13))
lbl.grid(row=0, column=0, columnspan=3, pady=(18, 10))

ent_n = Entry(w, font=('arial', 14), width=14, justify=CENTER)
ent_n.grid(row=0, column=3, pady=(18, 10))

btn_sub = Button(w, text="Submit", font=('arial', 13), command=submit)
btn_sub.grid(row=0, column=4, pady=(18, 10))

lbl_pId = Label(w, text="Process Id", font=('arial', 13))
lbl_pId.grid(row=1, column=0, pady=(18, 10), padx=(20, 10))

lbl_aTime = Label(w, text="Arrivel Time", font=('arial', 13))
lbl_aTime.grid(row=1, column=1, pady=(18, 10), padx=(10))

lbl_bTime = Label(w, text="Burst Time", font=('arial', 13))
lbl_bTime.grid(row=1, column=2, pady=(18, 10), padx=(10))

lbl_cTime = Label(w, text="Completion Time", font=('arial', 13))
lbl_cTime.grid(row=1, column=3, pady=(18, 10), padx=(10))

lbl_tTime = Label(w, text="Turnaround Time", font=('arial', 13))
lbl_tTime.grid(row=1, column=4, pady=(18, 10), padx=(10, 20))

lbl_wTime = Label(w, text="Waiting Time", font=('arial', 13))
lbl_wTime.grid(row=1, column=5, pady=(18, 10), padx=(10, 20))

w.mainloop()

