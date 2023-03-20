from asyncio.windows_events import NULL
from operator import methodcaller
from os import sep
from MySQLdb import connect
from flask import Flask, render_template, request, session, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from flask import jsonify
import json
import re

with open('config.json','r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)

app.config['MYSQL_HOST'] = params['MYSQL_HOST']
app.config['MYSQL_USER'] = params['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = params['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = params['MYSQL_DB']
app.config['MYSQL_CURSORCLASS'] = params['MYSQL_CURSORCLASS']

app.secret_key = 'super-secret-key'
mysql = MySQL(app)


@app.route("/")
def Home():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Admin(admin_id INTEGER PRIMARY KEY AUTO_INCREMENT, admin_name VARCHAR(20) NOT NULL, admin_email VARCHAR(20) UNIQUE, admin_department VARCHAR(20), admin_designation VARCHAR(20), admin_password VARCHAR(20))")
    cur.execute("CREATE TABLE IF NOT EXISTS Employees(emp_id INTEGER PRIMARY KEY AUTO_INCREMENT, emp_name VARCHAR(20) NOT NULL, emp_designation VARCHAR(20) NOT NULL, emp_department VARCHAR(20) NOT NULL, UNIQUE(emp_name, emp_designation))")
    cur.execute("CREATE TABLE IF NOT EXISTS Tests(test_no INTEGER PRIMARY KEY AUTO_INCREMENT, test_subject VARCHAR(40) NOT NULL, admin_id INTEGER, FOREIGN KEY(admin_id) REFERENCES Admin(admin_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS Questions(question_no INTEGER NOT NULL, test_no INTEGER, question_text VARCHAR(200) NOT NULL, no_of_scenarios INTEGER NOT NULL, PRIMARY KEY(test_no, question_no), FOREIGN KEY (test_no) REFERENCES Tests(test_no))")
    cur.execute("CREATE TABLE IF NOT EXISTS QuestionDepartments(test_no INTEGER, question_no INTEGER, department_name VARCHAR(20), PRIMARY KEY(department_name, question_no, test_no), FOREIGN KEY (test_no,question_no) REFERENCES Questions(test_no, question_no))")
    cur.execute("CREATE TABLE IF NOT EXISTS Scenario(scenario_id INTEGER, test_no INTEGER, question_no INTEGER, scenario_options VARCHAR(200), deduction VARCHAR(200),Show_In_Sort_By INTEGER, PRIMARY KEY(scenario_id, question_no, test_no), FOREIGN KEY (test_no,question_no) REFERENCES Questions(test_no, question_no))")
    cur.execute("CREATE TABLE IF NOT EXISTS Answer_Recorded(answer_id INTEGER PRIMARY KEY AUTO_INCREMENT,test_no INTEGER, question_no INTEGER, emp_id INTEGER, scenario_id INTEGER, FOREIGN KEY(test_no,question_no,scenario_id) REFERENCES Scenario(test_no,question_no,scenario_id), FOREIGN KEY(emp_id) REFERENCES Employees(emp_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS SuperAdmin(super_admin_id INTEGER PRIMARY KEY AUTO_INCREMENT, super_admin_name VARCHAR(20) NOT NULL, super_admin_email VARCHAR(20) NOT NULL, super_admin_password VARCHAR(20) NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS Temperory_Tests(test_no INTEGER PRIMARY KEY AUTO_INCREMENT, test_subject VARCHAR(40) NOT NULL, admin_id INTEGER, FOREIGN KEY(admin_id) REFERENCES Admin(admin_id))")
    cur.execute("CREATE TABLE IF NOT EXISTS Temperory_Questions(question_no INTEGER NOT NULL, test_no INTEGER, question_text VARCHAR(200) NOT NULL, no_of_scenarios INTEGER NOT NULL, PRIMARY KEY(test_no, question_no), FOREIGN KEY (test_no) REFERENCES Temperory_Tests(test_no))")
    cur.execute("CREATE TABLE IF NOT EXISTS Temperory_Scenario(scenario_id INTEGER, test_no INTEGER, question_no INTEGER, scenario_options VARCHAR(200), deduction VARCHAR(200),Show_In_Sort_By INTEGER, PRIMARY KEY(scenario_id, question_no, test_no), FOREIGN KEY (test_no,question_no) REFERENCES Temperory_Questions(test_no, question_no))")
    cur.execute("CREATE TABLE IF NOT EXISTS Temperory_QuestionDepartments(test_no INTEGER, question_no INTEGER, department_name VARCHAR(20), PRIMARY KEY(department_name, question_no, test_no), FOREIGN KEY (test_no,question_no) REFERENCES Temperory_Questions(test_no, question_no))")

    cur.close()
    session['list_of_sort_by'] = ['Vulnerable Risky','Safe']
    if 'loggedin' in session:
        return redirect(url_for("AdminFunctions"))
    elif 'super_loggedin' in session:
        return redirect(url_for("SuperAdminTestFunctions"))
    else:
        return redirect(url_for("UserInfo"))

@app.route("/UserInfo" , methods=['GET','POST'])
def UserInfo():
    if 'employee_loggedin' in session and 'employee_employee_id' in session:
        return redirect(url_for("UserTests"))

    if request.method == 'POST':
        name = request.form.get("name")
        designation = request.form.get("designation")
        department = request.form.get("department")

        # department = department.upper()
        cur = mysql.connection.cursor()

        cur.execute("select emp_name,emp_designation from employees")
        employee_records = cur.fetchall()

        for records in employee_records:
            if records['emp_name'] == name and records['emp_designation'] == designation:
                message = "you've already attempted test once"
                return render_template("UserInfo.html", params = params, message = message)

        cur.execute("INSERT INTO employees (emp_name,emp_designation,emp_department) values (%s,%s,%s)",([name],[designation],[department],))
        mysql.connection.commit()
        
        cur.execute("select max(emp_id) as employee_id from employees")
        emp_id = cur.fetchone()

        session['employee_loggedin'] = True 
        session['employee_employee_id'] = emp_id['employee_id']

        cur.close()
        return redirect(url_for("UserTests"))

    message = ''
    return render_template("UserInfo.html", params = params, message = message)

@app.route("/UserTests", methods=['GET','POST'])
def UserTests():
    if request.method=='POST':
        count_questions = request.form.get("count_of_ques")
        cur = mysql.connection.cursor()
        test_no = session['launch_test_num']

        #changing yahan bhi hui hai
        cur.execute("select * from employees where emp_id = %s",([session['employee_employee_id']]))
        employee = cur.fetchone()
        cur.execute("select * from QuestionDepartments where test_no = %s",([test_no]),)
        question_departments = cur.fetchall()
        ques_list = []
        non_ques_list = []
        for questions in question_departments:
            if(questions['department_name'] == employee['emp_department']):
                if questions['question_no'] in non_ques_list:
                    non_ques_list.remove(questions['question_no'])
                ques_list.append(questions['question_no'])
            elif questions['question_no'] not in ques_list and questions['question_no'] not in non_ques_list:
                non_ques_list.append(questions['question_no'])

        cur.execute("select t.test_no, t.test_subject, q.question_no, q.question_text from tests t, questions q where t.test_no = q.test_no and q.test_no = %s", ([test_no],))
        test_questions = cur.fetchall()

        list_test_questions = list(test_questions)
        question_numbers = []

        for ques in list_test_questions: 
            sub_dict = dict(ques)
            if sub_dict['question_no'] not in non_ques_list:
                question_numbers.append(sub_dict['question_no'])

        for i in question_numbers:
            option_no = "option_" + str(i)
            scenario_no = request.form.get(option_no)
            cur.execute("INSERT INTO Answer_Recorded(test_no,question_no,emp_id,scenario_id) values(%s,%s,%s,%s)", ([test_no],[i],[session['employee_employee_id']],[scenario_no],))
            mysql.connection.commit()

        cur.close()
        return redirect(url_for("logout"))


    elif 'employee_loggedin' in session and 'employee_employee_id' in session:
        if "launch_test_num" in session:
            test_no = session["launch_test_num"]
            if (session["launch_test_type"] == "Complete"):
                cur = mysql.connection.cursor()

                #changing yahan se
                cur.execute("select * from employees where emp_id = %s",([session['employee_employee_id']]))
                employee = cur.fetchone()
                cur.execute("select * from QuestionDepartments where test_no = %s",([test_no]),)
                question_departments = cur.fetchall()

                ques_list = []
                non_ques_list = []
                for questions in question_departments:
                    if(questions['department_name'] == employee['emp_department']):
                        if questions['question_no'] in non_ques_list:
                            non_ques_list.remove(questions['question_no'])
                        ques_list.append(questions['question_no'])
                    elif questions['question_no'] not in ques_list and questions['question_no'] not in non_ques_list:
                        non_ques_list.append(questions['question_no'])

                cur.execute("select t.test_no, t.test_subject, q.question_no, q.question_text from tests t, questions q where t.test_no = q.test_no and q.test_no = %s", ([test_no],))
                test_questions = cur.fetchall()

                list_test_questions = list(test_questions)

                for ques_no in non_ques_list:
                    for ques in list_test_questions:
                        sub_dict = dict(ques)
                        if sub_dict['question_no'] == ques_no:
                            list_test_questions.pop(list_test_questions.index(ques))

                test_questions = tuple(list_test_questions)

                cur.execute("select scenario_id, test_no, question_no, scenario_options from scenario where test_no = %s order by question_no, scenario_id asc", ([test_no],))
                scenarios = cur.fetchall()

                list_scenarios = list(scenarios)
                new_list = []
                for i in range(0, len(list_scenarios)):
                    sub_dict = dict(list_scenarios[i])
                    if sub_dict['question_no'] not in non_ques_list:
                        new_list.append(list_scenarios[i])

                scenarios = tuple(new_list)

                cur.execute("select count(scenario_id) as 'count' from scenario where test_no = %s group by question_no", ([test_no],))
                count = cur.fetchall()
                return render_template("StartTest.html", params = params, test_questions = test_questions, scenarios = scenarios, count = count)
        else:
            message = "Test is not launched yet, please re-try!"
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM EMPLOYEES WHERE emp_id = %s",([session['employee_employee_id']],))
            mysql.connection.commit()
            session.pop('employee_employee_id', None)
            session.pop('employee_loggedin', None)
            cur.close()
            return render_template("UserInfo.html", params = params, message = message)
    else:
        return redirect(url_for("UserInfo"))


@app.route("/adminLogin", methods=['GET', 'POST'])
def AdminLogin():
    message = ""
    if request.method == 'POST':
        if 'Departments' in session:
            session.pop('Departments')
        email = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Admin where admin_email = %s AND admin_password=%s",([email],[password],))
        admin_user = cur.fetchone()
        cur.close()
        if(admin_user != None and  len(admin_user)>0):
            session['loggedin']= True
            session['id'] = admin_user['admin_id']
            session['username'] = admin_user['admin_name']
            return render_template("AdminFunctions.html", params = params, admin_user = admin_user)
        else:
            message = "Invalid Email or Password"
            return render_template("AdminLogin.html", params = params, message = message)
    return render_template("AdminLogin.html", params = params, message = message)

@app.route("/adminSignup", methods=['GET', 'POST'])
def AdminSignup():
    if request.method == 'POST':
        if 'Departments' in session:
            session.pop('Departments')
        name = request.form.get("name")
        designation = request.form.get("designation")
        department = request.form.get("department")
        email = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Admin(admin_name,admin_email,admin_department, admin_designation, admin_password) VALUES(%s,%s,%s,%s,%s)", ([name],[email],[department],[designation], [password],))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("AdminLogin"))

    return render_template("AdminSignup.html", params = params)

@app.route("/adminFunctions", methods = ['GET','POST'])
def AdminFunctions():
    if('loggedin' in session):
        if 'Departments' in session:
            session.pop('Departments')
        admin_id = session['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Admin where admin_id = %s", ([admin_id],))
        admin_user = cur.fetchone()
        message = ""
        return render_template("AdminFunctions.html", pasams = params, admin_user = admin_user, message = message)
    elif ('loggedin' not in session):
        return redirect(url_for("AdminLogin"))

@app.route("/TestFunctions", methods=['GET', 'POST'])
def TestFunctions():
    if request.method == 'POST':
        if 'Departments' in session:
            session.pop('Departments')
        text = request.form.get("operation")
        admin_id = session['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Admin where admin_id = %s", ([admin_id],))
        admin = cur.fetchone()

        message = ""        
        if (text == 'Create Test'):
            return render_template("CreateTest.html", pasams = params, admin = admin)
        elif (text == "Modify Test"):
            cur.execute("SELECT * FROM TESTS where admin_id = %s", ([admin_id],))
            tests = cur.fetchone()
            if (tests != None):
                cur.execute("SELECT * FROM TESTS where admin_id = %s", ([admin_id],))
                tests = cur.fetchall()
                return render_template("ModifyTest.html", pasams = params, tests = tests, text = text)
            else:
                cur.execute("SELECT * FROM Temperory_TESTS where admin_id = %s", ([admin_id],))
                tests = cur.fetchall()
                if(len(tests)>0):
                    message = "Your tests haven't been approved yet"
                else:
                    message = "No test found!"
        elif (text == "View Results"):
            cur.execute("SELECT * FROM TESTS where admin_id = %s", ([admin_id],))
            tests = cur.fetchall()
            if(len(tests) > 0):
                return render_template("ViewTest.html", params = params, tests = tests)
            else:
                cur.execute("SELECT * FROM Temperory_TESTS where admin_id = %s", ([admin_id],))
                tests = cur.fetchall()
                if(len(tests)>0):
                    message = "Your tests haven't been approved yet"
                else:
                    message = "No test found!"
                
    if('loggedin' in session):
        admin_id = session['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Admin where admin_id = %s", ([admin_id],))
        admin_user = cur.fetchone()
        return render_template("AdminFunctions.html", pasams = params, admin_user = admin_user, message = message)
    elif ('loggedin' not in session):
        return redirect(url_for("AdminLogin"))

@app.route("/Questions", methods=['GET', 'POST'])
def Questions():
    if request.method == 'POST':
        test_subject = request.form.get("test_subject")
        admin_id = session['id']
        cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO Tests (test_subject,admin_id) values(%s,%s)",([test_subject],[admin_id],))
        cur.execute("INSERT INTO Temperory_Tests (test_subject,admin_id) values(%s,%s)",([test_subject],[admin_id],))
        mysql.connection.commit()

        return redirect(url_for("SubQuestions"))
    
    if ('loggedin' not in session):
        return redirect(url_for("AdminLogin"))
    else:
        return redirect(url_for("AdminFunctions"))       

@app.route("/SubQuestions", methods=['GET', 'POST'])
def SubQuestions():
    if request.method == 'POST':
        Question = request.form.get("Question")
        Scenario1 = request.form.get("Scenario1")
        Deduction1 = request.form.get("Deduction1")
        Scenario2 = request.form.get("Scenario2")
        Deduction2 = request.form.get("Deduction2")
        Scenario3 = request.form.get("Scenario3")
        Deduction3 = request.form.get("Deduction3")
        Scenario4 = request.form.get("Scenario4")
        Deduction4 = request.form.get("Deduction4")
        Scenario5 = request.form.get("Scenario5")
        Deduction5 = request.form.get("Deduction5")
        operation = request.form.get("operation")  

        
        scenario = []
        deduction = []
        if(Scenario1 != ''):
            scenario.append(Scenario1)
            deduction.append(Deduction1)
        if (Scenario2 != ''):
            scenario.append(Scenario2)
            deduction.append(Deduction2)
        if (Scenario3 != ''):
            scenario.append(Scenario3)
            deduction.append(Deduction3)
        if (Scenario4 != ''):
            scenario.append(Scenario4)
            deduction.append(Deduction4)
        if (Scenario5 != ''):
            scenario.append(Scenario5)
            deduction.append(Deduction5)
        count = len(scenario)



        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Temperory_Questions where test_no = %s", ([session['current_test_no']],))
        q_no = cur.fetchone()

        if(q_no is None):
            # new
            if (Question != ''):
            # finish
                question_no = 1
                cur.execute("INSERT INTO Temperory_Questions (question_no, test_no,question_text) values(%s,%s,%s)",([question_no],[session['current_test_no']],[Question],))
                # cur.execute("INSERT INTO Questions (question_no, test_no,question_text) values(%s,%s,%s)",([question_no],[session['current_test_no']],[Question],))
                mysql.connection.commit()
        else:
            # new
            if (Question != ''):
            # finish
                cur.execute("SELECT question_no FROM Temperory_Questions where question_no = (select max(question_no) from Temperory_Questions where test_no = %s)", ([session['current_test_no']],))
                questionNumber = cur.fetchone()
                question_no = questionNumber['question_no'] + 1
                cur.execute("INSERT INTO Temperory_Questions (question_no, test_no,question_text) values(%s,%s,%s)",([question_no],[session['current_test_no']],[Question],))
                mysql.connection.commit()

        for i in range(1, count+1):
            if (deduction[i-1] not in session['list_of_sort_by']):
                Show_In_Sort_By = 0
            else:
                Show_In_Sort_By = 1
            cur.execute("INSERT INTO Temperory_Scenario (scenario_id, test_no, question_no, scenario_options, deduction,Show_In_Sort_By) values(%s,%s,%s,%s,%s,%s)",([i],[session['current_test_no']],[question_no],[scenario[i-1]],[deduction[i-1]],[Show_In_Sort_By],))
            # cur.execute("INSERT INTO Scenario (scenario_id, test_no, question_no, scenario_options, deduction,Show_In_Sort_By) values(%s,%s,%s,%s,%s,%s)",([i],[session['current_test_no']],[question_no],[scenario[i-1]],[deduction[i-1]],[Show_In_Sort_By],))
            mysql.connection.commit()
        if ('Departments'  in session):
            Total_Department = list(session['Departments'])
            length_of_departments = len(Total_Department)
            for i in range(1,length_of_departments+1):
                cur.execute("INSERT INTO Temperory_QuestionDepartments (test_no, question_no,department_name) values(%s,%s,%s)",([session['current_test_no']],[question_no],[Total_Department[i-1]['DepartmentName']],))
                mysql.connection.commit()
            session.pop('Departments')
        cur.close()     
        if (operation == "add question"):
            return redirect(url_for("SubQuestions"))
        elif (operation == "complete test"):
            return redirect(url_for("AdminFunctions"))

    
    cur = mysql.connection.cursor()
    cur.execute("Select * from Temperory_Tests where test_no = (select max(test_no) from Temperory_Tests)")
    test_number = cur.fetchone()
    session['current_test_no'] = test_number['test_no']
    cur.execute("SELECT DISTINCT(department_name) FROM Temperory_QuestionDepartments")
    Departments = cur.fetchall()
    cur.execute("SELECT DISTINCT(deduction) FROM Temperory_Scenario")
    Deductions = cur.fetchall()
    cur.close()
    test_sub = test_number['test_subject']
    return render_template("Questions.html", params = params, test_sub = test_sub, Departments = Departments , Deductions = Deductions)



@app.route("/SendDataToDb", methods=['POST'])
def SendDataToDb():
    DepartmentName = request.form['NewDepartment']
    
    if 'Departments' not in session:
        session['Departments'] = []
        Departments = []
    else:
        Departments = list(session['Departments'])
    if DepartmentName == '' or {'DepartmentName':DepartmentName} in session['Departments']:
        return jsonify(session['Departments'])
    Departments.append({'DepartmentName':DepartmentName})
    session['Departments'] = list(Departments)
    return jsonify(session['Departments'])

@app.route("/RemoveDataFromDb", methods=['POST'])
def RemoveDataFromDb():
    DepartmentName = request.form['RemoveDepartment']
    Departments = list(session['Departments'])
    Departments.remove({'DepartmentName':DepartmentName})
    session['Departments'] = list(Departments)
    return json.dumps("Your shown data is removed")

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('super_loggedin', None)
    session.pop('super_id', None)
    session.pop('super_admin_name', None)
    session.pop('employee_loggedin', None)
    session.pop('employee_employee_id', None)
    
    return redirect(url_for("Home"))


@app.route("/ModifySpecificTest",methods=['GET', 'POST'])
def ModifySpecificTest():
    if('loggedin' in session):
        admin_id = session['id']
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            if 'Departments' in session:
                session.pop('Departments')
            test_number = request.form.get("test_number")
            session['current_test_no'] = [test_number]
            cur.execute("SELECT * FROM Tests where test_no = %s",([test_number],))
            test = cur.fetchone()
            cur.execute("SELECT * FROM Questions where test_no = %s",([test_number],))
            questions = cur.fetchall()
            return render_template("ModifySpecificTest.html", params = params, questions = questions,test = test)   
        else:
            cur.execute("SELECT * FROM Admin where admin_id = %s",([session['id']],))
            admin_user = cur.fetchone()
            return render_template("AdminFunctions.html",params = params,admin_user = admin_user)
    elif ('loggedin' not in session):
        return redirect(url_for("AdminLogin"))

@app.route("/choose_option",methods=['GET', 'POST'])
def choose_option():
    if('loggedin' in session):
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            if 'Departments' in session:
                session.pop('Departments')
            operation = request.form.get("operation")
            listt = operation.split()
            operation = listt[0]
            test_number = listt[1]
            question_number = listt[2]
            
            cur.execute("SELECT * FROM Scenario where question_no = %s AND test_no = %s",([question_number],[test_number],))
            scenarios = cur.fetchall()
            cur.execute("SELECT * FROM Questions where question_no = %s AND test_no = %s ",([question_number],[test_number],))
            question = cur.fetchone()
            cur.execute("SELECT * FROM tests where test_no = %s",([test_number],))
            test = cur.fetchone()

            length = len(scenarios)
            if (operation == "update_question"):
                if(length < 5 ):
                    for i in range(len(scenarios)+1,6):
                        t1 = list(scenarios)
                        t1.append({'scenario_id': i, 'test_no': test_number, 'question_no': question_number,'scenario_options':'','deduction':'' })
                        scenarios = tuple(t1)
                    cur.execute("SELECT DISTINCT(department_name) FROM QuestionDepartments")
                    Departments = cur.fetchall()
                    cur.execute("SELECT DISTINCT(deduction) FROM Scenario")
                    Deductions = cur.fetchall()
                    if 'Departments' not in session:
                        session['Departments'] = []
                    cur.execute("SELECT department_name AS 'DepartmentName' FROM QuestionDepartments where question_no = %s AND test_no = %s",([question_number],[session['current_test_no']],))
                    departments_of_this_question = cur.fetchall()
                    session['Departments'] = list(departments_of_this_question)
                return render_template("UpdateQuestionForm.html",test = test,question = question,scenarios = scenarios, length = length,Departments = Departments, Deductions = Deductions,departments_of_this_question = departments_of_this_question)
            elif (operation == "view_question"):
                return render_template("ViewQuestion.html",test = test, question = question,scenarios = scenarios)
            elif(operation == "Add_Question"):
                cur.execute("SELECT DISTINCT(department_name) FROM QuestionDepartments")
                Departments = cur.fetchall()
                cur.execute("SELECT DISTINCT(deduction) FROM Scenario")
                Deductions = cur.fetchall()
                return render_template("UpdateAddQuestion.html", params = params, test = test, Departments = Departments, Deductions = Deductions)
            elif (operation == "Complete_Changes"):
                cur.execute("SELECT * FROM Admin where admin_id = %s",([session['id']],))
                admin_user = cur.fetchone()
                return render_template("AdminFunctions.html",params = params,admin_user = admin_user)
    return redirect(url_for("AdminFunctions"))


@app.route("/UpdateQuestionForm", methods=['GET', 'POST'])
def UpdateQuestionForm():
    if request.method == 'POST':
        length_of_prev_scenarios = request.form.get("length_of_previous_scenarios")
        Question = request.form.get("Question")
        Scenario1 = request.form.get("Scenario1")
        Deduction1 = request.form.get("Deduction1")
        Scenario2 = request.form.get("Scenario2")
        Deduction2 = request.form.get("Deduction2")
        Scenario3 = request.form.get("Scenario3")
        Deduction3 = request.form.get("Deduction3")
        Scenario4 = request.form.get("Scenario4")
        Deduction4 = request.form.get("Deduction4")
        Scenario5 = request.form.get("Scenario5")
        Deduction5 = request.form.get("Deduction5")
        question_number = request.form.get("question_number")

        
        scenario = []
        deduction = []
        if(Scenario1 != ''):
            scenario.append(Scenario1)
            deduction.append(Deduction1)
        if (Scenario2 != ''):
            scenario.append(Scenario2)
            deduction.append(Deduction2)
        if (Scenario3 != ''):
            scenario.append(Scenario3)
            deduction.append(Deduction3)
        if (Scenario4 != ''):
            scenario.append(Scenario4)
            deduction.append(Deduction4)
        if (Scenario5 != ''):
            scenario.append(Scenario5)
            deduction.append(Deduction5)
        count = len(scenario)
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Questions SET question_text = %s where question_no = %s AND test_no = %s",([Question],[question_number],[session['current_test_no']],))
        mysql.connection.commit()
        to_scenarios = int(length_of_prev_scenarios)+1
        for i in range (1,to_scenarios):
            if (deduction[i-1] not in session['list_of_sort_by']):
                Show_In_Sort_By = 0
            else:
                Show_In_Sort_By = 1
            cur.execute("UPDATE Scenario SET scenario_options = %s, deduction = %s,Show_In_Sort_By = %s where question_no = %s AND test_no = %s AND scenario_id = %s",([scenario[i-1]],[deduction[i-1]],[Show_In_Sort_By],[question_number],[session['current_test_no']],[i],))
            mysql.connection.commit()
        for i in range(to_scenarios,count+1):
            if (deduction[i-1] not in session['list_of_sort_by']):
                Show_In_Sort_By = 0
            else:
                Show_In_Sort_By = 1
            cur.execute("INSERT INTO Scenario (scenario_id, test_no, question_no, scenario_options, deduction,Show_In_Sort_By) values(%s,%s,%s,%s,%s,%s)",([i],[session['current_test_no']],[question_number],[scenario[i-1]],[deduction[i-1]],[Show_In_Sort_By],))
            mysql.connection.commit()
        cur.execute("DELETE from QuestionDepartments where question_no = %s AND test_no = %s",([question_number],[session['current_test_no']],))
        mysql.connection.commit()
        if ('Departments'  in session):
            Total_Department = list(session['Departments'])
            length_of_departments = len(Total_Department)
            
            for i in range(1,length_of_departments+1):
                cur.execute("INSERT INTO QuestionDepartments (test_no, question_no,department_name) values(%s,%s,%s)",([session['current_test_no']],[question_number],[Total_Department[i-1]['DepartmentName']],))
                mysql.connection.commit()
            session.pop('Departments')
        
        cur.execute("SELECT * FROM Tests where test_no = %s",([session['current_test_no']],))
        test = cur.fetchone()
        cur.execute("SELECT * FROM Questions where test_no = %s",([session['current_test_no']],))
        questions = cur.fetchall()
        cur.close()
        return render_template("ModifySpecificTest.html", params = params, questions = questions,test = test)
    return render_template("ModifySpecificTest.html", params = params)



@app.route("/ViewQuestion" , methods=['GET', 'POST'])
def ViewQuestion():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Tests where test_no = %s",([session['current_test_no']],))
        test = cur.fetchone()
        cur.execute("SELECT * FROM Questions where test_no = %s",([session['current_test_no']],))
        questions = cur.fetchall()
        cur.close()
        return render_template("ModifySpecificTest.html", params = params, questions = questions, test = test)
    return render_template("ModifySpecificTest.html", params = params)

#New routes yahan se add kiye hain
@app.route("/UpdateAddQuestion" , methods=['GET', 'POST'])
def UpdateAddQuestion():
    if request.method == 'POST':
        Question = request.form.get("Question")
        Scenario1 = request.form.get("Scenario1")
        Deduction1 = request.form.get("Deduction1")
        Scenario2 = request.form.get("Scenario2")
        Deduction2 = request.form.get("Deduction2")
        Scenario3 = request.form.get("Scenario3")
        Deduction3 = request.form.get("Deduction3")
        Scenario4 = request.form.get("Scenario4")
        Deduction4 = request.form.get("Deduction4")
        Scenario5 = request.form.get("Scenario5")
        Deduction5 = request.form.get("Deduction5")
        operation = request.form.get("operation")  
        test_number = request.form.get("test_number")
        scenario = []
        deduction = []
        if(Scenario1 != ''):
            scenario.append(Scenario1)
            deduction.append(Deduction1)
        if (Scenario2 != ''):
            scenario.append(Scenario2)
            deduction.append(Deduction2)
        if (Scenario3 != ''):
            scenario.append(Scenario3)
            deduction.append(Deduction3)
        if (Scenario4 != ''):
            scenario.append(Scenario4)
            deduction.append(Deduction4)
        if (Scenario5 != ''):
            scenario.append(Scenario5)
            deduction.append(Deduction5)
        count = len(scenario)

        cur = mysql.connection.cursor()
        cur.execute("SELECT question_no FROM Questions where question_no = (select max(question_no) from Questions where test_no = %s)", ([session['current_test_no']],))
        questionNumber = cur.fetchone()
        question_no = questionNumber['question_no'] + 1
        cur.execute("INSERT INTO Questions (question_no, test_no,question_text) values(%s,%s,%s)",([question_no],[session['current_test_no']],[Question],))
        mysql.connection.commit()
        
        for i in range(1, count+1):
            if (deduction[i-1] not in session['list_of_sort_by']):
                Show_In_Sort_By = 0
            else:
                Show_In_Sort_By = 1
            cur.execute("INSERT INTO Scenario (scenario_id, test_no, question_no, scenario_options, deduction,Show_In_Sort_By) values(%s,%s,%s,%s,%s,%s)",([i],[session['current_test_no']],[question_no],[scenario[i-1]],[deduction[i-1]],[Show_In_Sort_By],))
            mysql.connection.commit()
        if ('Departments'  in session):
            Total_Department = list(session['Departments'])
            length_of_departments = len(Total_Department)
            for i in range(1,length_of_departments+1):
                cur.execute("INSERT INTO QuestionDepartments (test_no, question_no,department_name) values(%s,%s,%s)",([session['current_test_no']],[question_no],[Total_Department[i-1]['DepartmentName']],))
                mysql.connection.commit()
            session.pop('Departments')

        cur.execute("SELECT * FROM Tests where test_no = %s",([session['current_test_no']],))
        test = cur.fetchone()
        cur.execute("SELECT * FROM Questions where test_no = %s",([session['current_test_no']],))
        questions = cur.fetchall()

        if (operation == "add question"):
            cur.execute("SELECT DISTINCT(department_name) FROM QuestionDepartments")
            Departments = cur.fetchall()
            cur.execute("SELECT DISTINCT(deduction) FROM Scenario")
            Deductions = cur.fetchall()
            cur.close()
            return render_template("UpdateAddQuestion.html", params = params, test = test, Departments = Departments, Deductions = Deductions)
        elif (operation == "complete update"):
            return render_template("ModifySpecificTest.html", params = params, questions = questions, test = test)


    return render_template("ModifySpecificTest.html", params = params)


@app.route("/IndividualOrCollective", methods=['GET', 'POST'] )
def ViewSpecificTest():
    if('loggedin' in session):
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            test_number = request.form.get("test_number")
            listt = test_number.split(',')
            test_number = listt[0]
            SortBy = listt[1]
            session['current_test_no'] = [test_number]
            cur.execute("SELECT * FROM Admin where admin_id = %s",([session['id']],))
            admin_user = cur.fetchone()
            return render_template("IndividualorCollective.html", params = params, test_number = test_number, admin_user = admin_user, SortByName = SortBy)

        cur.execute("Select * from tests where admin_id = %s" , (session['id'],))
        tests = cur.fetchall()    
        return render_template("ViewTest.html", params = params, tests = tests)
    else:
        return redirect(url_for("AdminLogin"))
    

@app.route("/report_type" , methods=['GET', 'POST'])
def report_type():
    if('loggedin' in session):
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            test_number = request.form.get("test_number")
            operation = request.form.get("operation")
            cur = mysql.connection.cursor()
            if (operation == "Individual Report"):
                # new_update
                cur.execute("Select DISTINCT DEDUCTION FROM Scenario where test_no = %s AND Show_In_Sort_By = 1",([test_number]))
                SortByList = cur.fetchall()
                SortBy = request.form.get("SortBy")
                if (SortBy == "Department"):
                    cur.execute("Select emp_id,emp_name,emp_designation,emp_department from employees where emp_id IN (SELECT EMP_ID FROM ANSWER_RECORDED WHERE test_no = %s) Order By emp_department",([test_number]))
                    employees_data = cur.fetchall()
                    return render_template("Individual_details.html" ,employees_data  = employees_data , test_number = test_number,SortByList = SortByList,SortByName = SortBy)
                elif (SortBy == "Name"):
                    cur.execute("Select emp_id,emp_name,emp_designation,emp_department from employees where emp_id IN (SELECT EMP_ID FROM ANSWER_RECORDED WHERE test_no = %s) Order By emp_name",([test_number]))
                    employees_data = cur.fetchall()
                    return render_template("Individual_details.html" ,employees_data  = employees_data , test_number = test_number,SortByList = SortByList,SortByName = SortBy)
                else:
                    cur.execute("SELECT ANS.emp_id FROM SCENARIO SC JOIN ANSWER_RECORDED ANS ON (SC.TEST_NO = ANS.TEST_NO AND SC.QUESTION_NO = ANS.QUESTION_NO AND SC.SCENARIO_ID = ANS.SCENARIO_ID ) WHERE SC.TEST_NO = %s AND SC.DEDUCTION = %s GROUP BY ANS.emp_id ORDER BY ROUND(COUNT(ANS.SCENARIO_ID)/(SELECT COUNT(SCENARIO_ID) FROM SCENARIO  WHERE TEST_NO = SC.TEST_NO AND DEDUCTION = SC.DEDUCTION)*100,2) DESC",([test_number],[SortBy]))
                    employees_id = cur.fetchall()
                    employees_data = []
                    for id in employees_id:
                        cur.execute("Select emp_id,emp_name,emp_designation,emp_department from employees where emp_id = %s",([id['emp_id']],))
                        data = cur.fetchone()
                        employees_data.append(data)
                    return render_template("Individual_details.html" ,employees_data  = employees_data , test_number = test_number ,SortByList = SortByList,SortByName = SortBy)
                #finish_update
                
                
            elif(operation == "Collective Report"):
                # new_update
                cur.execute("SELECT COUNT(*) AS 'COUNT'FROM EMPLOYEES where emp_id IN (SELECT emp_id FROM ANSWER_RECORDED WHERE test_no = %s)",([test_number]))
                #finish_update
                no_of_employee = cur.fetchone()
                cur.execute("SELECT COUNT(ANS.SCENARIO_ID) AS 'COUNT',(COUNT(DISTINCT SC.SCENARIO_ID, SC.QUESTION_NO, SC.TEST_NO)),ROUND(COUNT(ANS.SCENARIO_ID)/(COUNT(DISTINCT SC.SCENARIO_ID, SC.QUESTION_NO, SC.TEST_NO)*%s)*100,2) AS 'PERCENTAGE',SC.DEDUCTION FROM SCENARIO SC LEFT OUTER JOIN ANSWER_RECORDED ANS ON (SC.TEST_NO = ANS.TEST_NO AND SC.QUESTION_NO = ANS.QUESTION_NO AND SC.SCENARIO_ID = ANS.SCENARIO_ID ) WHERE SC.TEST_NO = %s GROUP BY SC.DEDUCTION", ([no_of_employee['COUNT']],[test_number],))
                GROUP_REPORT = cur.fetchall()
                cur.execute("SELECT * FROM Tests where test_no = %s",([session['current_test_no']],))
                test = cur.fetchone()
                return render_template("Collective_Report.html" , GROUP_REPORT = GROUP_REPORT,test = test)
        cur.execute("Select * from tests where admin_id = %s " , (session['id'],))
        tests = cur.fetchall()
        return render_template("ViewTest.html", params = params, tests = tests)
    else:
        return redirect(url_for("AdminLogin"))

@app.route("/for_refresh", methods=['POST'])
def for_refresh():
    cur = mysql.connection.cursor()
    cur.execute("Select DISTINCT DEDUCTION FROM Scenario where test_no = %s AND Show_In_Sort_By = 1",([session['current_test_no']],))
    SortByList = cur.fetchall()
    SortBy = request.form.get("SortBy")
    if (SortBy == "Department"):
        cur.execute("Select emp_id,emp_name,emp_designation,emp_department from employees where emp_id IN (SELECT EMP_ID FROM ANSWER_RECORDED WHERE test_no = %s) Order By emp_department",([session['current_test_no']]))
        employees_data = cur.fetchall()
        return render_template("Individual_details.html" ,employees_data  = employees_data , test_number = session['current_test_no'][0],SortByList = SortByList,SortByName = SortBy)
    elif (SortBy == "Name"):
        cur.execute("Select emp_id,emp_name,emp_designation,emp_department from employees where emp_id IN (SELECT EMP_ID FROM ANSWER_RECORDED WHERE test_no = %s) Order By emp_name",([session['current_test_no']]))
        employees_data = cur.fetchall()
        return render_template("Individual_details.html" ,employees_data  = employees_data , test_number = session['current_test_no'][0],SortByList = SortByList,SortByName = SortBy)
    else:
        cur.execute("SELECT ANS.emp_id FROM SCENARIO SC JOIN ANSWER_RECORDED ANS ON (SC.TEST_NO = ANS.TEST_NO AND SC.QUESTION_NO = ANS.QUESTION_NO AND SC.SCENARIO_ID = ANS.SCENARIO_ID ) WHERE SC.TEST_NO = %s AND SC.DEDUCTION = %s GROUP BY ANS.emp_id ORDER BY ROUND(COUNT(ANS.SCENARIO_ID)/(SELECT COUNT(SCENARIO_ID) FROM SCENARIO  WHERE TEST_NO = SC.TEST_NO AND DEDUCTION = SC.DEDUCTION)*100,2) DESC",([session['current_test_no']],[SortBy]))
        employees_id = cur.fetchall()
        employees_data = []
        for id in employees_id:
            cur.execute("Select emp_id,emp_name,emp_designation,emp_department from employees where emp_id = %s",([id['emp_id']],))
            data = cur.fetchone()
            employees_data.append(data)
            test_number = session['current_test_no'][0]
        return render_template("Individual_details.html" ,employees_data  = employees_data , test_number = test_number ,SortByList = SortByList, SortByName = SortBy)


@app.route("/Individual_Report" , methods=['GET', 'POST'])
def Individual_Report():
    if('loggedin' in session):
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            
            employee_dat = request.form.get("employee_dat")
            listt = employee_dat.split(',')
            employee_id = int(listt[0])
            employee_name = listt[1]
            employee_designation = listt[2]
            employee_department = listt[3]
            test_number = int(listt[4])
            SortBy = listt[5]
            cur.execute("select t.test_no, t.test_subject, q.question_no, q.question_text, ans.scenario_id,sc.scenario_options,sc.deduction from tests t JOIN questions q ON(t.test_no = q.test_no) JOIN scenario sc ON(sc.test_no = q.test_no AND sc.question_no = q.question_no) JOIN answer_recorded ans ON (ans.test_no = sc.test_no  AND ans.question_no = sc.question_no AND sc.scenario_id = ans.scenario_id) where q.test_no = %s AND emp_id = (SELECT emp_id from employees where emp_name = %s AND emp_designation = %s AND emp_department = %s)", ([test_number],[employee_name],[employee_designation],[employee_department],))
            details = cur.fetchall()
            length_details = len(details)
            cur.execute("Select * from tests where test_no = %s",([test_number]))
            test = cur.fetchone()
            cur.execute("SELECT SC.DEDUCTION,COUNT(ANS.SCENARIO_ID) AS 'COUNT',ROUND(COUNT(ANS.SCENARIO_ID)/(SELECT COUNT(SCENARIO_ID) FROM SCENARIO  WHERE TEST_NO = SC.TEST_NO AND DEDUCTION = SC.DEDUCTION)*100,2) AS 'PERCENTAGE' FROM SCENARIO SC JOIN ANSWER_RECORDED ANS ON (SC.TEST_NO = ANS.TEST_NO AND SC.QUESTION_NO = ANS.QUESTION_NO AND SC.SCENARIO_ID = ANS.SCENARIO_ID ) WHERE SC.TEST_NO = %s AND ANS.emp_id = %s GROUP BY SC.DEDUCTION", ([test_number],[employee_id]))
            Individual_REPORT = cur.fetchall()
            return render_template("Individual_Report.html", test = test,length_details = length_details, details = details,employee_name = employee_name,employee_designation = employee_designation,employee_department = employee_department,Individual_REPORT = Individual_REPORT,SortByName = SortBy)
        cur.execute("Select * from tests where admin_id = %s AND test_no = %s" , (session['id'],))
        tests = cur.fetchall()
        return render_template("ViewTest.html", params = params, tests = tests)
    else:
        return redirect(url_for("AdminLogin"))

@app.route("/SuperAdminSignUp", methods=['GET', 'POST'])
def SuperAdminSignUp():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        passowrd = request.form.get("password")


        cur = mysql.connection.cursor()
        cur.execute("select super_admin_email from superadmin")
        admin_records = cur.fetchall()
        for records in admin_records:
            if records['super_admin_email'] == email:
                message = "This super admin account already exists, please login instead."
                return render_template("SuperAdminSignup.html", params = params, message = message)

        cur.execute("INSERT INTO superadmin(super_admin_name, super_admin_email, super_admin_password) values(%s,%s,%s)",([name],[email],[passowrd]),)
        mysql.connection.commit()
        cur.close()
        message = ''
        return render_template("SuperAdminLogin.html", params = params, message = message)
    else:
        message = ''
        return render_template("SuperAdminSignup.html", params = params, message = message)


@app.route("/SuperAdminLogin", methods=['GET', 'POST'])
def SuperAdminLogin():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM superadmin where super_admin_email = %s AND super_admin_password=%s",([email],[password],))
        super_admin_user = cur.fetchone()
        cur.close()
        if(super_admin_user != None and  len(super_admin_user)>0):
            session['super_loggedin']= True
            session['super_id'] = super_admin_user['super_admin_id']
            session['super_admin_name'] = super_admin_user['super_admin_name']
            return render_template("SuperadminFunctions.html", super_admin_user = super_admin_user, params = params)
        else:
            message = "Invalid Email or Password"
            return render_template("SuperAdminLogin.html", params = params, message = message)

    return render_template("SuperAdminLogin.html", params = params)

# yahan se continue karna hai
@app.route("/SuperAdminTestFunctions", methods=['GET', 'POST'])
def SuperAdminTestFunctions():
    if request.method == 'POST':
        
        text = request.form.get("operation")
        admin_id = session['super_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM SuperAdmin where super_admin_id = %s", ([admin_id],))
        admin = cur.fetchone()

        message = ""        
        if (text == 'Show All Tests'):
            cur.execute("Select t.test_no, t.test_subject, t.admin_id, a.admin_name from Tests t, Admin a where a.admin_id = t.admin_id")
            tests = cur.fetchall()
            if(len(tests)>0):
                message = ''
                return render_template("SuperAdmin_LaunchTest.html", pasams = params, tests = tests, message = message)
            else:
                message = 'There are currently no pending tests.'
                return render_template("SuperAdmin_LaunchTest.html", pasams = params, tests = tests, message = message)
        elif (text == "View Pending Tests"):
            cur.execute("Select t.test_no, t.test_subject, t.admin_id, a.admin_name from Temperory_Tests t, Admin a where a.admin_id = t.admin_id")
            tests = cur.fetchall()
            cur.close()
            if(len(tests)>0):
                message = ''
                return render_template("SuperAdmin_ShowAllTests.html", params = params, tests = tests, message = message)
            else:
                message = 'There are currently no pending tests.'
                return render_template("SuperAdmin_ShowAllTests.html", params = params, tests = tests, message = message)        
                
    if('super_loggedin' in session):
        admin_id = session['super_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM superAdmin where super_admin_id = %s", ([admin_id],))
        super_admin_user = cur.fetchone()
        return render_template("SuperadminFunctions.html", params = params, super_admin_user = super_admin_user)
    elif ('super_loggedin' not in session):
        return redirect(url_for("SuperAdminLogin"))

# for show all test button for admin
@app.route("/SuperAdmin_LaunchTest", methods=['GET', 'POST'])
def SuperAdmin_LaunchTest():
    if('super_loggedin' not in session):
        return redirect(url_for("SuperAdminLogin"))
    
    if request.method == 'POST':
        operationn = request.form.get("operation")
        list = operationn.split(',')
        test_number = list[0]
        operation = list[1]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Tests where test_no = %s",([test_number],))
        test = cur.fetchone()
        cur.execute("SELECT * FROM Questions where test_no = %s",([test_number],))
        questions = cur.fetchall()

        if operation == 'View Test':
            return render_template("SuperAdmin_ShowSpecificTest.html", params = params, questions = questions,test = test)   
        elif operation == 'Approve Test':
            print(1)
    
    return redirect(url_for("SuperAdminTestFunctions"))

@app.route("/SuperAdmin_ShowSpecificQuestion", methods=['GET', 'POST'])
def SuperAdmin_ShowSpecificQuestion():
    if('super_loggedin' not in session):
        return redirect(url_for("SuperAdminLogin"))

    if request.method == 'POST':
        operation = request.form.get("operation")
        list = operation.split()
        test_number = list[0]
        question_number = list[1]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Scenario where question_no = %s AND test_no = %s",([question_number],[test_number],))
        scenarios = cur.fetchall()
        cur.execute("SELECT * FROM Questions where question_no = %s AND test_no = %s ",([question_number],[test_number],))
        question = cur.fetchone()
        cur.execute("SELECT * FROM Tests where test_no = %s",([test_number],))
        test = cur.fetchone()
        return render_template("SuperAdmin_ShowSpecificQuestion.html", params = params, test = test, question = question, scenarios = scenarios)
        
    return redirect(url_for("SuperAdminTestFunctions"))

# 
    
@app.route("/SuperAdmin_ShowAllTests", methods=['GET', 'POST'])
def SuperAdmin_ShowAllTests():
    if('super_loggedin' not in session):
        return redirect(url_for("SuperAdminLogin"))

    if request.method == 'POST':
        operationn = request.form.get("operation")
        list = operationn.split(',')
        test_number = list[0]
        operation = list[1]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Temperory_Tests where test_no = %s",([test_number],))
        test = cur.fetchone()
        cur.execute("SELECT * FROM Temperory_Questions where test_no = %s",([test_number],))
        questions = cur.fetchall()

        if operation == 'View Test':
            return render_template("SuperAdmin_ViewSpecificTest.html", params = params, questions = questions,test = test)   
        elif operation == 'Approve Test':
            cur.execute("INSERT INTO Tests (test_subject,admin_id) values(%s,%s)",([test['test_subject']],[test['admin_id']],))
            mysql.connection.commit()
            for question in questions:
                cur.execute("select max(test_no) as max_test from tests")
                test_num = cur.fetchone()
                cur.execute("INSERT INTO Questions (question_no, test_no,question_text) values(%s,%s,%s)",([question['question_no']],[test_num['max_test']],[question['question_text']],))
                mysql.connection.commit()
                cur.execute("SELECT * FROM Temperory_Scenario where test_no = %s and question_no = %s", ([question['test_no']],[question['question_no']],))
                scenarios = cur.fetchall()
                
                for scenario in scenarios:
                    cur.execute("INSERT INTO Scenario (scenario_id, test_no, question_no, scenario_options, deduction,Show_In_Sort_By) values(%s,%s,%s,%s,%s,%s)",([scenario['scenario_id']],[test_num['max_test']],[scenario['question_no']],[scenario['scenario_options']],[scenario['deduction']],[scenario['Show_In_Sort_By']],))
                    mysql.connection.commit()
                cur.execute("SELECT department_name FROM Temperory_questionDepartments where test_no = %s and question_no = %s",([question['test_no']],[question['question_no']],))
                departments = cur.fetchall()
                
                for department in departments:
                    cur.execute("INSERT INTO QuestionDepartments (test_no, question_no,department_name) values(%s,%s,%s)",([test_num['max_test']],[question['question_no']],[department['department_name']],))
                    mysql.connection.commit()
            
                cur.execute("DELETE FROM Temperory_QuestionDepartments where test_no = %s and question_no = %s",([question['test_no']],[question['question_no']],))
                mysql.connection.commit()
                cur.execute("DELETE FROM Temperory_Scenario where test_no = %s and question_no = %s",([question['test_no']],[question['question_no']],))
                mysql.connection.commit()
            cur.execute("DELETE FROM Temperory_Questions WHERE test_no = %s", [test_number])
            mysql.connection.commit()
            cur.execute("DELETE FROM Temperory_Tests where test_no = %s", [test_number])
            mysql.connection.commit()
            cur.close() 

    return redirect(url_for("SuperAdminTestFunctions"))

@app.route("/SuperAdmin_ViewSpecificQuestion", methods=['GET', 'POST'])
def SuperAdmin_ViewSpecificQuestion():
    if('super_loggedin' not in session):
        return redirect(url_for("SuperAdminLogin"))

    if request.method == 'POST':
        operation = request.form.get("operation")
        list = operation.split()
        test_number = list[0]
        question_number = list[1]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Temperory_Scenario where question_no = %s AND test_no = %s",([question_number],[test_number],))
        scenarios = cur.fetchall()
        cur.execute("SELECT * FROM Temperory_Questions where question_no = %s AND test_no = %s ",([question_number],[test_number],))
        question = cur.fetchone()
        cur.execute("SELECT * FROM Temperory_tests where test_no = %s",([test_number],))
        test = cur.fetchone()
        return render_template("SuperAdmin_ViewSpecificQuestion.html", params = params, test = test, question = question, scenarios = scenarios)
        
    return redirect(url_for("SuperAdminTestFunctions"))

@app.route("/SuperAdmin_LaunchUserTest", methods=['GET', 'POST'])
def SuperAdmin_LaunchUserTest():
    if('super_loggedin' not in session):
        return redirect(url_for("SuperAdminLogin"))

    if request.method == 'POST':
        operation = request.form.get("operation")
        list = operation.split(',')
        test_num = list[0]
        task = list[1]

        if task == 'Launch Complete Test':
            session["launch_test_num"] = test_num
            session["launch_test_type"] = "Complete"

    return redirect(url_for("SuperAdminTestFunctions"))

app.run(debug=True)