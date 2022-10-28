from tkinter import *
from tkinter.messagebox import *
import matplotlib.pyplot as plt
from tkinter.scrolledtext import *
import bs4
import requests
from sqlite3 import *
import re

def f1():      #add functiom
	emp_add_window.deiconify()
	ems_main.withdraw()
	
def f2(): 	#view 
	emp_view_window.deiconify()
	ems_main.withdraw()
	emp_vw_st_data.delete(1.0,END)
	info = ""
	con = None
	try:
		con = connect("emsdata.db")
		cursor = con.cursor()
		sql = "select * from ems"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "Id: " + str(d[0])+ "\n" + "Name: " + d[1] +"\n" + "Salary: " + str(d[2]) +"\n\n" 
		emp_vw_st_data.insert(INSERT, info)
	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()	


def f3(): 	# update
	emp_update_window.deiconify()
	ems_main.withdraw()
	
	
def f4():	# delete
	emp_delete_window.deiconify()
	ems_main.withdraw()
	
def chart_close(event):   # function call from close 
	ems_main.deiconify()	

def f5():	# chart
	ems_main.withdraw()
	
	sal_graph = []
	name_graph = []

	con = None	
	try:
		
		con = connect("emsdata.db")
		cursor = con.cursor()
		sql= "select * from ems order by sal desc limit 5";

		cursor.execute(sql)
		con.commit()
		data = cursor.fetchall()
		for d in data:
			sal_graph.append(int(d[2]))
			name_graph.append(str(d[1]))

	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()	
			
	fig=plt.figure()
	plt.title("Chart")
	plt.ylabel("Salary")
	plt.xlabel("Top 5 highest Salary Employee Name")
	chart = plt.bar(name_graph,sal_graph,color='red',width = 0.4, label="Salary")
	fig.canvas.mpl_connect('close_event', chart_close)
	plt.grid()
	plt.legend(shadow=True)
	plt.show()
	

def f6():	#close add and open main window
	entry_add.delete(0,END)
	entry_add2.delete(0,END)
	entry_add3.delete(0,END)
	ems_main.deiconify()
	emp_add_window.withdraw()


def f7():		#save database
	con = None	
	try:
		con = connect("emsdata.db")
		cursor = con.cursor()
		sql = "insert into ems values('%d','%s',%f)"
		#print(entry_add.get())
		#print(entry_add2.get())
		#print(entry_add3.get())
		
		emp_id = entry_add.get()
		emp_name = entry_add2.get()
		emp_salary = entry_add3.get()
		
		  
		entry_add.delete(0,END)
		entry_add2.delete(0,END)
		entry_add3.delete(0,END)
		entry_add.focus() 
		 
		if(not emp_id):
			showerror("Error","Employee ID should no Empty")
			return
			
		elif(not re.search("^[1-9]*$", emp_id)):
			showerror("error", "Employee ID Should be in Number format")
			return	
		
		if(not emp_name):
			showerror("error","Employee Name should no Empty")
			return	
		
		elif(not re.search("^[a-zA-Z]*$", emp_name)):
			showerror("error", "Employee Name,Number or special character not allow")
			return
		elif(len(emp_name) < 2):
			showerror("error", "Employee Name should have 2 or more lettter ")
			return	
		
		if(not emp_salary):
			showerror("Error","Employee Salary Should be not Empty")	
			return	
		
		elif(not re.search("^[0-9]*$", emp_salary)):
			showerror("error", "Employee Salary should be in number format")
			return
		elif(int(emp_salary) < 8000):
			showerror("Error","Employee Salary should be 8000 or 8000 Above")
			return
			
		cursor.execute(sql%(int(emp_id), emp_name, int(emp_salary)))
		con.commit()
		showinfo("EMS","Employee Data Insert")
		entry_add.delete(0,END)
		entry_add2.delete(0,END)
		entry_add3.delete(0,END)
		entry_add.focus()
	except Exception as e:
		showerror("Error", "ID already exist")
	finally:
		if con is not None:
			con.close()


def f8(): #update database
	con = None
	try:
		con = connect("emsdata.db")
		cursor = con.cursor()
		#print(entry_update.get())
		#print(entry_update4.get())
		#print(entry_update5.get())
		
		emp_id = entry_update.get()
		emp_name1 = entry_update4.get()
		emp_salary2 = entry_update5.get()
		
		
		count = 0
		name_flag = False
		salary_flag = False
		error_flag = False
		
		if len(emp_name1) > 0:		
			if(not re.search("^[a-zA-Z]*$", emp_name1)):
				showerror("error", "Invalid Employee Name ")
				error_flag = True	
			elif(len(emp_name1) < 2):  
				showerror("error","Employee Name should have 2 or more lettter")
				error_flag = True	
			else:
				name_flag = True
			
		if len(emp_salary2) > 0:
			if(not re.search("^[0-9]*$", emp_salary2)):
				showerror("error", "Invalid Employee Salary")
				error_flag = True
			elif(int(emp_salary2) < 8000):
				showerror("Error","Employee Salary should be 8000 or 8000 Above")
				error_flag = True	
			else:
				salary_flag = True	
				
		if name_flag and not error_flag:
			sql = "update ems set name = '%s' where id = '%d'"
			cursor.execute(sql%(emp_name1, int(emp_id)))
			con.commit()
			
		if salary_flag and not error_flag:
			sql = "update ems set sal = '%d' where id = '%d'"
			cursor.execute(sql%(int(emp_salary2), int(emp_id)))
			con.commit()
			
		if (name_flag or salary_flag) and not error_flag: 
			showinfo("Update Info", f"{'Name' if name_flag else ''}{' and ' if name_flag and salary_flag else ''}{'Salary' if salary_flag else ''} Updated!")
			f14()
			
		entry_update.delete(0,END)
		entry_update2.delete(0,END)
		entry_update3.delete(0,END)
		entry_update4.delete(0,END)
		entry_update5.delete(0,END)	
			
	except Exception as e:
		print("invalid", e)
	finally:
		if con is not None:
			con.close()
			
def f9():	#delete database
	con = None
	try:
		con = connect("emsdata.db")
		cursor = con.cursor()
		sql = "select id from ems where id = '%d'"
		id = entry_delete.get()
		cursor.execute(sql%(int(id)))
		data = cursor.fetchall()
		if not data:
			showerror("Error","Id doesn't exist")
			entry_delete.focus()
			return
		else:	
			sql = "delete from ems where id = '%d'"
			id = entry_delete.get()
			print(id)
			cursor.execute(sql%(int(id)))	
			con.commit()
			showinfo("EMS","Employee Detail Deleted ")
			entry_delete.delete(0,END)
			entry_delete.focus()
			
		entry_delete.delete(0,END)
		entry_delete.focus()	
	except Exception as e:
		showerror("Error","Invalid Employee Id ")
	finally:
		if con is not None:
			con.close()
	
def f10():
	entry_delete.delete(0,END)
	ems_main.deiconify()
	emp_delete_window.withdraw()
	
def f11():
	entry_add.delete(0,END)
	entry_update.delete(0,END)
	entry_update2.delete(0,END)
	entry_update3.delete(0,END)
	entry_update4.delete(0,END)
	entry_update5.delete(0,END)
	ems_main.deiconify()
	emp_update_window.withdraw()

def f12():
	ems_main.deiconify()
	emp_view_window.withdraw()

def f13():  #Quote
	try:
		wa = "https://www.brainyquote.com/quote_of_the_day"
		res=requests.get(wa)
		data=bs4.BeautifulSoup(res.text,"html.parser")	
		info = data.find("img", {"class","p-qotd"})
		quote=info["alt"]
		label_quote.config(text = f"Quote = {quote}")
		
	except Exception as e:
		print("issue",e)

def f14():        # show data in update 
	con = None	
	try:
		
		con = connect("emsdata.db")
		cursor = con.cursor()
		sql= "select * from ems where id = %d";
		a = entry_update.get()
		print(int(a))
		cursor.execute(sql%(int(a)))
		con.commit()
		data = cursor.fetchall()
		
		if (len(data) == 0):
			showerror("error","id doen't exist")
			return
			
		for d in data:
			a = d[1]
			b = str(d[2])
		entry_update2.delete(0,END)
		entry_update3.delete(0,END)
		entry_update2.insert(INSERT,a)
		entry_update3.insert(INSERT,b)	
			
		
		
		
		
	except Exception as e:
		showerror("Error","Invalid Employee Id")
	finally:
		if con is not None:
			con.close()	
			
			

		
		
		
		
		
	

ems_main=Tk()
ems_main.title("Employee Management System")
ems_main.geometry("900x600")
f=("Arial Rounded MT",16,"bold")
ems_main['bg']='red'

label_main=Label(ems_main,text="Employee Management System",font=f)
btn_add = Button(ems_main, text="ADD", font=f,width=10,command=f1)
btn_view = Button(ems_main, text="View", font=f,width=10,command=f2)
btn_update = Button(ems_main, text="Update", font=f,width=10,command=f3)
btn_delete = Button(ems_main, text="Delete", font=f,width=10,command=f4)
btn_chart = Button(ems_main, text="Chart", font=f,width=10,command=f5)
label_quote=Label(ems_main,text="",font=f)
f13()

label_main.pack(pady=30)
btn_add.pack(pady=10)
btn_view.pack(padx=10)
btn_update.pack(pady=10)
btn_delete.pack(pady=10)
btn_chart.pack(pady=10)
label_quote.pack(pady=50)

# Add 
emp_add_window=Toplevel(ems_main)
emp_add_window.title("ADD Employee details")
emp_add_window.geometry("900x600")
emp_add_window['bg']='blue'

label_add = Label(emp_add_window,text="Enter Employee ID",font=f)
entry_add = Entry(emp_add_window,font=f,bd=2)
label_add2 = Label(emp_add_window,text="Enter Employee Name",font=f)
entry_add2 = Entry(emp_add_window,font=f,bd=2)
label_add3 = Label(emp_add_window,text="Enter Employee Salary",font=f)
entry_add3 = Entry(emp_add_window,font=f,bd=2)
add_button = Button(emp_add_window,text="Save",font=f,command=f7)
back_button = Button(emp_add_window,text="Back",font=f,command=f6)

label_add.pack(pady=10)
entry_add.pack(pady=10)
label_add2.pack(pady=10)
entry_add2.pack(pady=10)
label_add3.pack(pady=10)
entry_add3.pack(pady=10)
add_button.pack(pady=10)
back_button.pack(pady=10)

emp_add_window.withdraw()



#view window

emp_view_window= Toplevel(ems_main)
emp_view_window.title("view student")
emp_view_window.geometry("900x600")
emp_view_window['bg']='yellow'

emp_vw_st_data = ScrolledText(emp_view_window,width=20,height=10,font=f)
emp_bt_back = Button(emp_view_window,text="Back",font=f,command=f12)
emp_vw_st_data.pack(pady=10)
emp_bt_back.pack(pady=10)

emp_view_window.withdraw()

#update window

emp_update_window= Toplevel(ems_main)
emp_update_window.title("Update student")
emp_update_window.geometry("900x900")
emp_update_window['bg']='blue'

label_update = Label(emp_update_window,text="Enter ID to Update",font=f)
entry_update = Entry(emp_update_window,font=f,bd=2)
getvalue_btn_update = Button(emp_update_window,text="Show Data",font=f,command=f14)
label_update2 = Label(emp_update_window,text="Exists Name",font=f)
entry_update2 = Entry(emp_update_window,font=f,bd=2)
label_update3 = Label(emp_update_window,text="Exists Salary",font=f)
entry_update3 = Entry(emp_update_window,font=f,bd=2)

label_update4 = Label(emp_update_window,text=" Enter New Name for update",font=f)
entry_update4 = Entry(emp_update_window,font=f,bd=2)
label_update5 = Label(emp_update_window,text="Enter New Salary for update",font=f)
entry_update5 = Entry(emp_update_window,font=f,bd=2)

submit_btn_update = Button(emp_update_window,text="Submit",font=f,command = f8)
back_btn_update = Button(emp_update_window,text="Back",font=f,command=f11)



label_update.pack(pady=10)
entry_update.pack(pady=10)
getvalue_btn_update.pack(pady=10)
label_update2.pack(pady=10)
entry_update2.pack(pady=10)
label_update3.pack(pady=10)
entry_update3.pack(pady=10)
label_update4.pack(pady=10)
entry_update4.pack(pady=10)
label_update5.pack(pady=10)
entry_update5.pack(pady=10)
submit_btn_update.pack(pady=10)
back_btn_update.pack(pady=10)


emp_update_window.withdraw()

#Delete window

emp_delete_window = Toplevel(ems_main)
emp_delete_window.title("Delete student")
emp_delete_window.geometry("900x600")
emp_delete_window['bg']='pink'

label_delete = Label(emp_delete_window,text="Enter ID to Delete",font=f)
entry_delete = Entry(emp_delete_window,font=f,bd=2)
submit_btn_delete = Button(emp_delete_window,text="Submit",font=f,command=f9)
back_btn_delete = Button(emp_delete_window,text="Back",font=f,command=f10)

label_delete.pack(pady=10)
entry_delete.pack(pady=10)
submit_btn_delete.pack(pady=10)
back_btn_delete.pack(pady=10)

emp_delete_window.withdraw()




print("mainwork")




ems_main.mainloop()