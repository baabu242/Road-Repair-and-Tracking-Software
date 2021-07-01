import mysql.connector as cnctr
from tkinter import*
from tkinter import messagebox
from tkinter import ttk
import RRTSpackage as rrts
from datetime import date

mydb = cnctr.connect(host="localhost", user="root", passwd="1234", database="RRTS")

mycursor = mydb.cursor()

window = Tk()
window.title("RRTS")
window.geometry("600x300")
window.configure(bg='deep sky blue')

def openadminlgn():
    # Toplevel object which will
    # be treated as a new window
    admWindow = Toplevel(window)

    # sets the title of the
    # Toplevel widget
    admWindow.title("Administrator Login")

    # sets the geometry of toplevel
    admWindow.geometry("600x400")
    admWindow.configure(bg='deep sky blue')

    frame_spl = Frame(admWindow, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
    frame_spl.place(relwidth=1, relheight=1)

    def log():
        mycursor.execute("SELECT passwd FROM account WHERE type = 'administrator'")
        psswrd3 = mycursor.fetchall()
        def setpsssp():
            mycursor.execute("SELECT * FROM account WHERE type = 'administrator'")
            x = mycursor.fetchall()
            sprv = rrts.user(x[0][1], x[0][2], x[0][3])
            sprv.setPassword(psswd_eb.get())
            mycursor.execute("UPDATE account SET passwd = %s WHERE type = 'administrator'",
                            (sprv.getPassword(),))
            mydb.commit()
            setpss_b.destroy()
            log()

        def opensprwin():
            sprvwin = Toplevel(admWindow)
            sprvwin.title("Supervisor Window")
            sprvwin.geometry("1200x700")
            sprvwin.configure(bg='deep sky blue')

            frame_a1 = Frame(sprvwin, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
            frame_a1.place(relwidth=0.75, relheight=1)

            frame_a2 = Frame(sprvwin, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
            frame_a2.place(relwidth=0.25, relheight=1, relx=0.75)

            wrkrs_eb = Entry(frame_a2, font=('Arial', 12))
            wrkrs_eb.place(relx=0.5, y=100, x=10)

            rorlrs_eb = Entry(frame_a2, font=('Arial', 12))
            rorlrs_eb.place(relx=0.5, y=150, x=10)

            apv_eb = Entry(frame_a2, font=('Arial', 12))
            apv_eb.place(relx=0.5, y=200, x=10)

            bit_eb = Entry(frame_a2, font=('Arial', 12))
            bit_eb.place(relx=0.5, y=250, x=10)

            h_l = Label(frame_a2, font=("arial", 12), text="Available Resources", bg='sky blue', highlightthickness=2)
            h_l.place(y=50, relx=0.5, x=-60)

            wr_l = Label(frame_a2, font=("arial", 12), text="Workers", bg='sky blue', highlightthickness=2)
            wr_l.place(y=100, relx=0.5, x=-85)

            rr_l = Label(frame_a2, font=("arial", 12), text="RoadRollers", bg='sky blue', highlightthickness=2)
            rr_l.place(y=150, relx=0.5, x=-100)

            ap_l = Label(frame_a2, font=("arial", 12), text="Asphaltpavers", bg='sky blue', highlightthickness=2)
            ap_l.place(y=200, relx=0.5, x=-120)

            bt_l = Label(frame_a2, font=("arial", 12), text="Bitumen (KGs)", bg='sky blue', highlightthickness=2)
            bt_l.place(y=250, relx=0.5, x=-120)

            def updater():
                mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s, rb = %s WHERE type = 'slot1'",
                                 (int(wrkrs_eb.get()), int(rorlrs_eb.get()),int(apv_eb.get()), 0))
                mydb.commit()
                mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s, rb = %s WHERE type = 'slot2'",
                                 (int(wrkrs_eb.get()), int(rorlrs_eb.get()), int(apv_eb.get()), 0))
                mydb.commit()
                mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s, rb = %s WHERE type = 'available'",
                                 (int(wrkrs_eb.get()), int(rorlrs_eb.get()), int(apv_eb.get()), int(bit_eb.get())))
                mydb.commit()

                mycursor.execute("DELETE FROM schedule")
                mydb.commit()
                mycursor.execute("SELECT id, rw, rr, ra, rb, road, location, priority, severity, branch FROM complaint WHERE "
                                 "status LIKE 's%' ORDER BY priority DESC")
                x = mycursor.fetchall()
                for c in x:
                    mycursor.execute("SELECT * FROM resources")
                    r = mycursor.fetchall()
                    if c[1] <= r[1][1] and c[2] <= r[1][2] and c[3] <= r[1][3] and c[4] <= r[0][4]:
                        mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s WHERE type = 'slot1'",
                                         (r[1][1] - c[1], r[1][2] - c[2], r[1][3] - c[3],))
                        mydb.commit()
                        mycursor.execute("UPDATE resources SET rb = %s WHERE type = 'available'",
                                         (r[0][4] - c[4],))
                        mydb.commit()
                        mycursor.execute(
                            "INSERT INTO schedule (branch, id, road, location, priority, severity, rw, rr, ra, rb, slot1, slot2)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '1', '-')",
                            (c[9], c[0], c[5], c[6], c[7], c[8], c[1], c[2], c[3], c[4]))
                        mydb.commit()
                        mycursor.execute("UPDATE complaint SET status = 'sc' WHERE id = %s", (c[0],))
                        mydb.commit()
                    elif c[1] <= 2 * min(r[1][1], r[2][1]) and c[2] <= 2 * min(r[1][2], r[2][2]) and c[3] <= 2 * min(
                            r[1][3], r[2][3]) and c[1] <= r[0][4]:

                        mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s WHERE type = 'slot1'",
                                         (r[1][1] - int((c[1] + 1) / 2), r[1][2] - int((c[2] + 1) / 2),
                                          r[1][3] - int((c[3] + 1) / 2),))
                        mydb.commit()
                        mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s WHERE type = 'slot2'",
                                         (r[2][1] - int((c[1] + 1) / 2), r[2][2] - int((c[2] + 1) / 2),
                                          r[2][3] - int((c[3] + 1) / 2),))
                        mydb.commit()
                        mycursor.execute("UPDATE resources SET rb = %s WHERE type = 'available'",
                                         (r[0][4] - c[4],))
                        mydb.commit()
                        mycursor.execute(
                            "INSERT INTO schedule (branch, id, road, location, priority, severity, rw, rr, ra, rb, slot1, slot2)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '1', '1')",
                            (c[9], c[0], c[5], c[6], c[7], c[8], int((c[1] + 1) / 2), int((c[2] + 1) / 2),
                            int((c[3] + 1)), c[4]))
                        mydb.commit()
                        mycursor.execute("UPDATE complaint SET status = 'sc' WHERE id = %s", (c[0],))
                        mydb.commit()
                    elif c[1] <= r[2][1] and c[2] <= r[2][2] and c[3] <= r[2][3] and c[4] <= r[0][4]:
                        mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s WHERE type = 'slot2'",
                                         (r[2][1] - c[1], r[2][2] - c[2], r[2][3] - c[3],))
                        mydb.commit()
                        mycursor.execute("UPDATE resources SET rb = %s WHERE type = 'available'",
                                         (r[0][4] - c[4],))
                        mydb.commit()
                        mycursor.execute(
                            "INSERT INTO schedule (branch, id, road, location, priority, severity, rw, rr, ra, rb, slot1, slot2)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '-', '1')",
                            (c[9], c[0], c[5], c[6], c[7], c[8], c[1], c[2], c[3], c[4]))
                        mydb.commit()
                        mycursor.execute("UPDATE complaint SET status = 'sc' WHERE id = %s", (c[0],))
                        mydb.commit()


            updt_b = Button(frame_a2, text="Update Resources", command=updater)
            updt_b.place(relx=0.5, x=-60, y=300)

            mycursor.execute("SELECT * FROM resources")
            x = mycursor.fetchall()
            wrkrs_eb.insert(0, str(x[0][1]))
            rorlrs_eb.insert(0, str(x[0][2]))
            apv_eb.insert(0, str(x[0][3]))
            bit_eb.insert(0, str(x[0][4]))


            def statistics():
                mycursor.execute("SELECT id, branch, road, location, priority, severity, rw, rr, ra, rb, date FROM complaint WHERE status = 'c'")

                tree3.delete(*tree3.get_children())
                rows = mycursor.fetchall()
                srw = 0
                srr = 0
                sra = 0
                srb = 0
                for row in rows:
                    tree3.insert("", END, values=row)
                    srw += row[6]
                    srr += row[7]
                    sra += row[8]
                    srb += row[9]

                sch_l = Label(frame_a1, font=("arial", 12), text="Resources used : " + str(srw)+" worker slots, "+str(srr)+" road roller slots,"
                                                                 +str(sra)+" Asphaltpaver slots, "+str(srb)+" KGs of bitumen", bg='sky blue',
                              highlightthickness=2)
                sch_l.place(relwidth=1, relheight=0.1, rely=0.9)

            tree3 = ttk.Treeview(frame_a1, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"),
                                 show='headings')

            tree3.column("#1", anchor=CENTER, width=50)
            tree3.heading("#1", text="ID")

            tree3.column("#2", anchor=CENTER, width=50)
            tree3.heading("#2", text="BRANCH")

            tree3.column("#3", anchor=CENTER, width=50)
            tree3.heading("#3", text="ROAD")

            tree3.column("#4", anchor=CENTER, width=50)
            tree3.heading("#4", text="LOCATION")

            tree3.column("#5", anchor=CENTER, width=50)
            tree3.heading("#5", text="PRIORITY")

            tree3.column("#6", anchor=CENTER, width=50)
            tree3.heading("#6", text="SEVERITY")

            tree3.column("#7", anchor=CENTER, width=50)
            tree3.heading("#7", text="Workers")
            tree3.column("#8", anchor=CENTER, width=50)
            tree3.heading("#8", text="RoadRollers")
            tree3.column("#9", anchor=CENTER, width=50)
            tree3.heading("#9", text="AsphaltPaver")
            tree3.column("#10", anchor=CENTER, width=50)
            tree3.heading("#10", text="Bitumen")
            tree3.column("#11", anchor=CENTER, width=50)
            tree3.heading("#11", text="DATE")


            tree3.place(relwidth=1, relheight=0.8, rely=0.1)
            statistics()



        def loginspr():  # check password
            mycursor.execute("SELECT * FROM account WHERE type = 'administrator'")
            x = mycursor.fetchall()
            admn = rrts.user(x[0][1], x[0][2], x[0][3])
            pw = admn.getPassword()
            if pw != psswd_eb.get():
                messagebox.showerror("error", "wrong password try again")
            else:
                opensprwin()

        setpss_b = Button(frame_spl, text="Set Password", command=setpsssp)
        setpss_b.place(relx=0.5, y=250, x=10)

        lgnspr_b = Button(frame_spl, text="      Login       ", command=loginspr)
        lgnspr_b.place(relx=0.5, y=250, x=10)

        if psswrd3[0][0] == "#none":
            lgnspr_b.destroy()
        else:
            setpss_b.destroy()

    psswd_eb = Entry(frame_spl, show='*', font=('Arial', 12))
    psswd_eb.place(relx=0.5, y=200, x=10)

    psswd_l = Label(frame_spl, font=("arial", 12), text="Password", bg='sky blue', highlightthickness=2)
    psswd_l.place(y=200, relx=0.5, x=-100)

    backsp_b = Button(frame_spl, text="BACK", command=admWindow.destroy)
    backsp_b.place(relx=1, rely=1, x=-45, y=-32)

    log()

def openSuperLogin():
    # Toplevel object which will
    # be treated as a new window
    sprWindow = Toplevel(window)

    # sets the title of the
    # Toplevel widget
    sprWindow.title("Supervisor Login")

    # sets the geometry of toplevel
    sprWindow.geometry("600x400")
    sprWindow.configure(bg='deep sky blue')

    def sel_sprid(*args):
        mycursor.execute("SELECT passwd FROM account WHERE branch = %s and type = 'supervisor'",
                         (sel_spr.get()[2:-3],))
        psswrd2 = mycursor.fetchall()

        def setpsssp():  # set password for first time login
            mycursor.execute("SELECT * FROM account WHERE branch = %s and type = 'supervisor'",
                             (sel_spr.get()[2:-3],))
            x = mycursor.fetchall()
            sprv = rrts.user(x[0][1], x[0][2], x[0][3])
            sprv.setPassword(psswd_eb.get())
            mycursor.execute("UPDATE account SET passwd = %s WHERE branch = %s and type = 'supervisor'",
                             (sprv.getPassword(), sel_spr.get()[2:-3],))
            mydb.commit()
            setpss_b.destroy()
            sel_sprid()

        def opensprwin():  # if password is correct open this window
            sprvwin = Toplevel(sprWindow)
            sprvwin.title("Supervisor Window")
            sprvwin.geometry("1200x700")
            sprvwin.configure(bg='deep sky blue')

            def dis_com():
                tree.delete(*tree.get_children())
                mycursor.execute("SELECT id, road, location, description FROM complaint WHERE branch = %s and status = 'r'", (sel_spr.get()[2:-3],))
                rows = mycursor.fetchall()

                for row in rows:
                    tree.insert("", END, values=row)

            def dis_wq():
                tree2.delete(*tree2.get_children())
                mycursor.execute(
                    "SELECT id, road, location, priority, severity, rw, rr, ra, rb FROM complaint WHERE branch = %s and status = 'sp'",
                    (sel_spr.get()[2:-3],))
                rows = mycursor.fetchall()
                for row in rows:
                    tree2.insert("", END, values=row)

            def dis_sched():
                tree3.delete(*tree3.get_children())
                mycursor.execute(
                    "SELECT id, road, location, priority, severity, rw, rr, ra, rb, slot1, slot2 FROM schedule WHERE branch = %s ORDER BY priority DESC",
                    (sel_spr.get()[2:-3],))
                rows = mycursor.fetchall()
                for row in rows:
                    tree3.insert("", END, values=row)

            def update_com():
                mycursor.execute("UPDATE complaint SET priority = %s, severity = %s, rw = %s, rr = %s, ra = %s, rb = %s, status = 'sp' WHERE id = %s",
                                 (int(sel_pri.get()),int(sel_sev.get()),int(rw_eb.get()),int(rr_eb.get()),int(ra_eb.get()),int(rb_eb.get()),int(comid_eb.get())))
                mydb.commit()
                dis_wq()
                dis_com()
                sel_pri.set("select priority")
                sel_sev.set("select severity")
                rw_eb.delete(0, END)
                rr_eb.delete(0, END)
                ra_eb.delete(0, END)
                rb_eb.delete(0, END)



            def schedule():
                mycursor.execute("DELETE FROM schedule WHERE branch = %s",(sel_spr.get()[2:-3],))
                mydb.commit()
                mycursor.execute("SELECT id, rw, rr, ra, rb, road, location, priority, severity FROM complaint WHERE "
                                 "branch = %s and status LIKE 's%' ORDER BY priority DESC",(sel_spr.get()[2:-3],))
                x = mycursor.fetchall()
                for c in x:
                    mycursor.execute("SELECT * FROM resources")
                    r = mycursor.fetchall()
                    if c[1] <= r[1][1] and c[2] <= r[1][2] and c[3] <= r[1][3] and c[4] <= r[0][4] :
                        mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s WHERE type = 'slot1'",
                                         (r[1][1] - c[1], r[1][2] - c[2], r[1][3] - c[3], ))
                        mydb.commit()
                        mycursor.execute("UPDATE resources SET rb = %s WHERE type = 'available'",
                                         (r[0][4] - c[4],))
                        mydb.commit()
                        mycursor.execute("INSERT INTO schedule (branch, id, road, location, priority, severity, rw, rr, ra, rb, slot1, slot2)"
                                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '1', '-')",(sel_spr.get()[2:-3],c[0],c[5],c[6],c[7],c[8],c[1],c[2],c[3],c[4]))
                        mydb.commit()
                        mycursor.execute("UPDATE complaint SET status = 'sc' WHERE id = %s",(c[0],))
                        mydb.commit()
                    elif c[1] <= 2*min(r[1][1], r[2][1]) and c[2] <= 2*min(r[1][2], r[2][2]) and c[3] <= 2*min(r[1][3], r[2][3]) and c[1] <= r[0][4]:

                        mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s WHERE type = 'slot1'",
                                         (r[1][1] - int((c[1] + 1)/2), r[1][2] - int((c[2] + 1)/2), r[1][3] - int((c[3] + 1)/2),))
                        mydb.commit()
                        mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s WHERE type = 'slot2'",
                                         (r[2][1] - int((c[1] + 1) / 2), r[2][2] - int((c[2] + 1) / 2), r[2][3] - int((c[3] + 1) / 2),))
                        mydb.commit()
                        mycursor.execute("UPDATE resources SET rb = %s WHERE type = 'available'",
                                         (r[0][4] - c[4],))
                        mydb.commit()
                        mycursor.execute(
                            "INSERT INTO schedule (branch, id, road, location, priority, severity, rw, rr, ra, rb, slot1, slot2)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '1', '1')",
                            (sel_spr.get()[2:-3], c[0], c[5], c[6], c[7], c[8], int((c[1]+1)/2), int((c[2]+1)/2), int((c[3]+1)), c[4]))
                        mydb.commit()
                        mycursor.execute("UPDATE complaint SET status = 'sc' WHERE id = %s", (c[0],))
                        mydb.commit()
                    elif c[1] <= r[2][1] and c[2] <= r[2][2] and c[3] <= r[2][3] and c[4] <= r[0][4]:
                        mycursor.execute("UPDATE resources SET rw = %s, rr = %s, ra = %s WHERE type = 'slot2'",
                                         (r[2][1] - c[1], r[2][2] - c[2], r[2][3] - c[3],))
                        mydb.commit()
                        mycursor.execute("UPDATE resources SET rb = %s WHERE type = 'available'",
                                         (r[0][4] - c[4],))
                        mydb.commit()
                        mycursor.execute(
                            "INSERT INTO schedule (branch, id, road, location, priority, severity, rw, rr, ra, rb, slot1, slot2)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '-', '1')",
                            (sel_spr.get()[2:-3], c[0], c[5], c[6], c[7], c[8], c[1], c[2], c[3], c[4]))
                        mydb.commit()
                        mycursor.execute("UPDATE complaint SET status = 'sc' WHERE id = %s", (c[0],))
                        mydb.commit()
                dis_wq()
                dis_sched()



            def completed():
                mycursor.execute("UPDATE complaint SET status = 'c', date = %s WHERE id = %s",(str(date.today()), compl_eb.get(),))
                mydb.commit()
                mycursor.execute("DELETE FROM schedule WHERE id = %s", (compl_eb.get(),))
                mydb.commit()

                compl_eb.delete(0, END)

                dis_sched()

            def addclerk():
                mycursor.execute("SELECT * FROM account WHERE type = 'clerk' and branch = %s",(sel_spr.get()[2:-3],))
                x = mycursor.fetchall()
                idc = x.__len__() + 1
                mycursor.execute("INSERT INTO account (type, userid, branch, passwd) VALUES (%s, %s, %s, %s)",('clerk',idc,sel_spr.get()[2:-3],'#none'))

            frame_s1 = Frame(sprvwin, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
            frame_s1.place(relwidth=0.66, relheight=0.33, relx=0, rely=0.66)

            frame_s2 = Frame(sprvwin, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
            frame_s2.place(relwidth=0.33, relheight=0.66, relx=0.66, rely=0.33)

            frame_s4 = Frame(sprvwin, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
            frame_s4.place(relwidth=0.75, relheight=0.33)

            frame_s5 = Frame(sprvwin, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
            frame_s5.place(relwidth=0.25, relheight=0.33, relx=0.75)

            recomp_l = Label(frame_s1, font=("arial", 12), text="Unsupervised Complaints", bg='sky blue',
                             highlightthickness=2)
            recomp_l.place(relwidth=1, relheight=0.1)

            sch_l = Label(frame_s4, font=("arial", 12), text="Schedule for "+str(date.today()), bg='sky blue',
                             highlightthickness=2)
            sch_l.place(relwidth=1, relheight=0.1)

            tree = ttk.Treeview(frame_s1, column=("c1", "c2", "c3", "c4"), show='headings')

            tree.column("#1", anchor=CENTER, width=100)
            tree.heading("#1", text="ID")

            tree.column("#2", anchor=CENTER)
            tree.heading("#2", text="ROAD")

            tree.column("#3", anchor=CENTER)
            tree.heading("#3", text="LOCATION")

            tree.column("#4", anchor=CENTER)
            tree.heading("#4", text="DESCRIPTION")

            tree.place(relwidth=1, relheight=0.9, rely=0.1)

            dis_com()

            frame_s3 = Frame(sprvwin, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
            frame_s3.place(relwidth=0.66, relheight=0.33, rely=0.33)

            wq_l = Label(frame_s3, font=("arial", 12), text="Waiting Queue", bg='sky blue', highlightthickness=2)
            wq_l.place(relwidth=1, relheight=0.1)

            tree2 = ttk.Treeview(frame_s3, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"), show='headings')

            tree2.column("#1", anchor=CENTER, width=50)
            tree2.heading("#1", text="ID")

            tree2.column("#2", anchor=CENTER, width=50)
            tree2.heading("#2", text="ROAD")

            tree2.column("#3", anchor=CENTER, width=50)
            tree2.heading("#3", text="LOCATION")

            tree2.column("#4", anchor=CENTER, width=50)
            tree2.heading("#4", text="PRIORITY")

            tree2.column("#5", anchor=CENTER, width=50)
            tree2.heading("#5", text="SEVERITY")

            tree2.column("#6", anchor=CENTER, width=50)
            tree2.heading("#6", text="Workers")
            tree2.column("#7", anchor=CENTER, width=50)
            tree2.heading("#7", text="RoadRollers")
            tree2.column("#8", anchor=CENTER, width=50)
            tree2.heading("#8", text="AsphaltPaver")
            tree2.column("#9", anchor=CENTER, width=50)
            tree2.heading("#9", text="Bitumen")

            tree2.place(relwidth=1, relheight=0.9, rely=0.1)

            tree3 = ttk.Treeview(frame_s4, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"),
                                 show='headings')

            tree3.column("#1", anchor=CENTER, width=50)
            tree3.heading("#1", text="ID")

            tree3.column("#2", anchor=CENTER, width=50)
            tree3.heading("#2", text="ROAD")

            tree3.column("#3", anchor=CENTER, width=50)
            tree3.heading("#3", text="LOCATION")

            tree3.column("#4", anchor=CENTER, width=50)
            tree3.heading("#4", text="PRIORITY")

            tree3.column("#5", anchor=CENTER, width=50)
            tree3.heading("#5", text="SEVERITY")

            tree3.column("#6", anchor=CENTER, width=50)
            tree3.heading("#6", text="Workers")
            tree3.column("#7", anchor=CENTER, width=50)
            tree3.heading("#7", text="RoadRollers")
            tree3.column("#8", anchor=CENTER, width=50)
            tree3.heading("#8", text="AsphaltPaver")
            tree3.column("#9", anchor=CENTER, width=50)
            tree3.heading("#9", text="Bitumen")
            tree3.column("#10", anchor=CENTER, width=50)
            tree3.heading("#10", text="Slot 1")
            tree3.column("#11", anchor=CENTER, width=50)
            tree3.heading("#11", text="Slot 2")


            tree3.place(relwidth=1, relheight=0.9, rely=0.1)

            dis_wq()
            dis_sched()

            sel_pri = StringVar(frame_s2)
            sel_pri.set("select priority")
            sel_sev = StringVar(frame_s2)
            sel_sev.set("select severity")


            comid_eb = Entry(frame_s2, font=('Arial', 12))
            comid_eb.place(relx=0.5, y=75, x=10)

            prior_db = OptionMenu(frame_s2, sel_pri, *range(1, 6))
            prior_db.place(relx=0.5, y=125, x=10)

            sever_db = OptionMenu(frame_s2, sel_sev, *range(1, 6))
            sever_db.place(relx=0.5, y=175, x=10)

            rw_eb = Entry(frame_s2, font=('Arial', 12))
            rw_eb.place(relx=0.5, y=275, x=10)
            rr_eb = Entry(frame_s2, font=('Arial', 12))
            rr_eb.place(relx=0.5, y=305, x=10)
            ra_eb = Entry(frame_s2, font=('Arial', 12))
            ra_eb.place(relx=0.5, y=335, x=10)
            rb_eb = Entry(frame_s2, font=('Arial', 12))
            rb_eb.place(relx=0.5, y=365, x=10)

            comup_l = Label(frame_s2, font=("arial", 12), text="Update Complaint", bg='sky blue', highlightthickness=2)
            comup_l.place(y=25, relx=0.5, x=-50 )

            comid_l = Label(frame_s2, font=("arial", 12), text="Complaint ID", bg='sky blue', highlightthickness=2)
            comid_l.place(y=75, relx=0.5, x=-90)

            prior_l = Label(frame_s2, font=("arial", 12), text="Priority", bg='sky blue', highlightthickness=2)
            prior_l.place(y=125, relx=0.5, x=-70)

            damsev_l = Label(frame_s2, font=("arial", 12), text="Damage Severity", bg='sky blue', highlightthickness=2)
            damsev_l.place(y=175, relx=0.5, x=-120)

            resour_l = Label(frame_s2, font=("arial", 12), text="Resources needed (in terms of single slot)", bg='sky blue', highlightthickness=2)
            resour_l.place(y=225, relx=0.5, x=-120)

            rw_l = Label(frame_s2, font=("arial", 12), text="Workers", bg='sky blue', highlightthickness=2)
            rw_l.place(y=275, relx=0.5, x=-75)

            rr_l = Label(frame_s2, font=("arial", 12), text="RoadRoller(s)", bg='sky blue', highlightthickness=2)
            rr_l.place(y=305, relx=0.5, x=-105)

            ra_l = Label(frame_s2, font=("arial", 12), text="AsphaltPaver(s)", bg='sky blue', highlightthickness=2)
            ra_l.place(y=335, relx=0.5, x=-115)

            rb_l = Label(frame_s2, font=("arial", 12), text="Bitumen (in KGs)", bg='sky blue', highlightthickness=2)
            rb_l.place(y=365, relx=0.5, x=-120)

            shedule_b = Button(frame_s5, text="Shedule", command=schedule)
            shedule_b.place(relx=0.5, y=25)

            compl_eb = Entry(frame_s5, font=('Arial', 12))
            compl_eb.place(relx=0.5, y=75, x=-75)

            compl_b = Button(frame_s5, text="Completed", command=completed)
            compl_b.place(relx=0.5, y=75, x=40)

            addcl_b = Button(frame_s5, text="Add clerk to this Branch", command=addclerk)
            addcl_b.place(relx=0.5, y=125, x=-70)

            update_b = Button(frame_s2, text="Update", command=update_com)
            update_b.place(relx=0.5, y=395)

            backsp_b = Button(frame_s2, text="BACK", command=sprvwin.destroy)
            backsp_b.place(relx=1, rely=1, x=-45, y=-32)

        def loginspr():  # check password
            mycursor.execute("SELECT * FROM account WHERE branch = %s and type = 'supervisor'",
                             (sel_spr.get()[2:-3],))
            x = mycursor.fetchall()
            clrk = rrts.user(x[0][1], x[0][2], x[0][3])
            pw = clrk.getPassword()
            if pw != psswd_eb.get():
                messagebox.showerror("error", "wrong password try again")
            else:
                opensprwin()

        setpss_b = Button(frame_spl, text="Set Password", command=setpsssp)
        setpss_b.place(relx=0.5, y=250, x=10)

        lgnspr_b = Button(frame_spl, text="      Login       ", command=loginspr)
        lgnspr_b.place(relx=0.5, y=250, x=10)

        if psswrd2[0][0] == "#none":
            lgnspr_b.destroy()
        else:
            setpss_b.destroy()

    frame_spl = Frame(sprWindow, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
    frame_spl.place(relwidth=1, relheight=1)

    cld_l = Label(frame_spl, font=("arial", 12), text="Enter Credentials", bg='sky blue', highlightthickness=2)
    cld_l.place(relwidth=1, y=50)

    sel_spr = StringVar(frame_spl)
    sel_spr.set("Select ID")

    mycursor.execute("SELECT userid FROM account WHERE type = 'supervisor'")

    x = mycursor.fetchall()

    sprid_db = OptionMenu(frame_spl, sel_spr, *x)
    sprid_db.place(relx=0.5, y=150, x=10)
    sel_spr.trace("w", sel_sprid)

    psswd_eb = Entry(frame_spl, show='*', font=('Arial', 12))
    psswd_eb.place(relx=0.5, y=200, x=10)

    sprv_l = Label(frame_spl, font=("arial", 12), text="Supervisor of Branch", bg='sky blue', highlightthickness=2)
    sprv_l.place(y=150, relx=0.5, x=-150)

    psswd_l = Label(frame_spl, font=("arial", 12), text="Password", bg='sky blue', highlightthickness=2)
    psswd_l.place(y=200, relx=0.5, x=-100)

    backsp_b = Button(frame_spl, text="BACK", command=sprWindow.destroy)
    backsp_b.place(relx=1, rely=1, x=-45, y=-32)


def openClerkLogin():  # clerk login window
    # Toplevel object which will
    # be treated as a new window
    clWindow = Toplevel(window)

    # sets the title of the
    # Toplevel widget
    clWindow.title("Clerk Login")

    # sets the geometry of toplevel
    clWindow.geometry("600x400")
    clWindow.configure(bg='deep sky blue')

    def sel_br(*args):  # function after selecting branch
        clrk_db['menu'].delete(0, END)
        sel_clrk.set("Select ID")

        mycursor.execute("SELECT type, userid FROM account WHERE type = 'clerk' and branch = %s", (sel_brnch.get(),))

        x = mycursor.fetchall()

        for cont in x:
            clrk_db['menu'].add_command(label=cont, command=lambda x_1=cont: sel_clrk.set(x_1))



    def sel_clid(*args):  # function after selecting clerk id
        if sel_clrk.get() != "Select ID":
            l = sel_clrk.get().split()
            mycursor.execute("SELECT passwd FROM account WHERE branch = %s and userid = %s and type = 'clerk'",
                             (sel_brnch.get(), l[1][1:-2]))
            psswrd1 = mycursor.fetchall()

            def setpssclrk():  # set password for first time login
                mycursor.execute("SELECT * FROM account WHERE branch = %s and userid = %s and type = 'clerk'",
                                 (sel_brnch.get(), (sel_clrk.get().split())[1][1:-2]))
                x = mycursor.fetchall()
                clrk = rrts.user(x[0][1], x[0][2], x[0][3])
                clrk.setPassword(psswd_eb.get())
                mycursor.execute("UPDATE account SET passwd = %s WHERE branch = %s and userid = %s and type = 'clerk'",
                                 (clrk.getPassword(), sel_brnch.get(), (sel_clrk.get().split())[1][1:-2],))
                mydb.commit()
                setpss_b.destroy()
                sel_clid()

            def openclrkwin():  # if password correct, open register complaint window
                clrkwin = Toplevel(clWindow)
                clrkwin.title("Clerk Window")
                clrkwin.geometry("600x400")
                clrkwin.configure(bg='deep sky blue')

                def registercomp():
                    mycursor.execute("SELECT * FROM complaint")
                    x = mycursor.fetchall()
                    c_id = x.__len__() + 1

                    mycursor.execute("INSERT INTO complaint (id, branch, road, location, description, status) "
                                     "VALUES (%s, %s, %s, %s, %s, %s)", (c_id, sel_brnch.get(), road_eb.get(),
                                                                    location_eb.get(), descript_eb.get(), "r"))
                    mydb.commit()
                    road_eb.delete(0, END)
                    location_eb.delete(0, END)
                    descript_eb.delete(0, END)
                    

                frame_3 = Frame(clrkwin, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
                frame_3.place(relwidth=1, relheight=1)
                clrkw_l = Label(frame_3, font=("arial", 12), text="Enter Complaint Details", bg='sky blue',
                                highlightthickness=2)
                clrkw_l.place(relwidth=1, y=30)

                road_eb = Entry(frame_3, font=('Arial', 12))
                road_eb.place(relx=0.5, y=100, x=10)

                location_eb = Entry(frame_3, font=('Arial', 12))
                location_eb.place(relx=0.5, y=150, x=10)

                descript_eb = Entry(frame_3, font=('Arial', 12))
                descript_eb.place(relx=0.5, y=200, x=10)

                road_l = Label(frame_3, font=("arial", 12), text="Road", bg='sky blue', highlightthickness=2)
                road_l.place(y=100, relx=0.5, x=-85)

                location_l = Label(frame_3, font=("arial", 12), text="Location", bg='sky blue', highlightthickness=2)
                location_l.place(y=150, relx=0.5, x=-100)

                descript_l = Label(frame_3, font=("arial", 12), text="description", bg='sky blue', highlightthickness=2)
                descript_l.place(y=200, relx=0.5, x=-120)

                regclw_b = Button(frame_3, text="Register", command=registercomp)
                regclw_b.place(relx=0.5, y=250, x=10)

                backclw_b = Button(frame_3, text="BACK", command=clrkwin.destroy)
                backclw_b.place(relx=1, rely=1, x=-45, y=-32)

            def loginclrk():  # check password
                mycursor.execute("SELECT * FROM account WHERE branch = %s and userid = %s and type = 'clerk'",
                                 (sel_brnch.get(), (sel_clrk.get().split())[1][1:-2]))
                x = mycursor.fetchall()
                clrk = rrts.user(x[0][1], x[0][2], x[0][3])
                pw = clrk.getPassword()
                if pw != psswd_eb.get():
                    messagebox.showerror("error", "wrong password try again")
                else:
                    openclrkwin()

            setpss_b = Button(frame_2, text="Set Password", command=setpssclrk)
            setpss_b.place(relx=0.5, y=250, x=10)

            lgnclr_b = Button(frame_2, text="      Login       ", command=loginclrk)
            lgnclr_b.place(relx=0.5, y=250, x=10)
            if psswrd1[0][0] == "#none":
                lgnclr_b.destroy()
            else:
                setpss_b.destroy()

    frame_2 = Frame(clWindow, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
    frame_2.place(relwidth=1, relheight=1)

    cld_l = Label(frame_2, font=("arial", 12), text="Enter Credentials", bg='sky blue', highlightthickness=2)
    cld_l.place(relwidth=1, y=50)

    sel_brnch = StringVar(frame_2)
    sel_brnch.set("Select Branch")

    mycursor.execute("SELECT * FROM account WHERE type = 'supervisor'")

    x = mycursor.fetchall()

    brnch_db = OptionMenu(frame_2, sel_brnch, *range(1, x.__len__() + 1))
    brnch_db.place(y=100, x=10, relx=0.5)

    sel_brnch.trace("w", sel_br)

    sel_clrk = StringVar(frame_2)
    sel_clrk.set("Select id")

    mycursor.execute("SELECT * FROM account WHERE type = 'supervisor' ")

    x = mycursor.fetchall()

    clrk_db = OptionMenu(frame_2, sel_clrk, *range(1, x.__len__() + 1))
    clrk_db.place(relx=0.5, y=150, x=10)
    sel_clrk.trace("w", sel_clid)

    psswd_eb = Entry(frame_2, show='*', font=('Arial', 12))
    psswd_eb.place(relx=0.5, y=200, x=10)

    brnch_l = Label(frame_2, font=("arial", 12), text="Branch", bg='sky blue', highlightthickness=2)
    brnch_l.place(y=100, relx=0.5, x=-100)

    clerk_l = Label(frame_2, font=("arial", 12), text="UserID", bg='sky blue', highlightthickness=2)
    clerk_l.place(y=150, relx=0.5, x=-100)

    psswd_l = Label(frame_2, font=("arial", 12), text="Password", bg='sky blue', highlightthickness=2)
    psswd_l.place(y=200, relx=0.5, x=-120)

    backcl_b = Button(frame_2, text="BACK", command=clWindow.destroy)
    backcl_b.place(relx=1, rely=1, x=-45, y=-32)


frame_1 = Frame(window, bg='sky blue', highlightbackground="deep sky blue", highlightthickness=2)
frame_1.place(relwidth=1, relheight=1)

head_l = Label(frame_1, font=("arial", 20), text="Road Repair and Tracking Software", bg='sky blue', highlightthickness=2)
head_l.place(relwidth=1, relx=0)

login_l = Label(frame_1, font=("arial", 12), text="Login as", bg='sky blue', highlightthickness=2)
login_l.place(relwidth=1, y=50)

admin_b = Button(frame_1, text="Administrator", command=openadminlgn)
admin_b.place(relx=0.5, y=90, x=-40)

super_b = Button(frame_1, text="Supervisor", command=openSuperLogin)
super_b.place(relx=0.5, y=120, x=-30)



clerk_b = Button(frame_1, text="Clerk", command=openClerkLogin)
clerk_b.place(relx=0.5, y=150, x=-17)

exit_b = Button(frame_1, text="EXIT", command=exit)
exit_b.place(relx=1, rely=1, x=-40, y=-32)


window.mainloop()