from flask import Flask, render_template, redirect, url_for, request, jsonify
import emp_manage as em


app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("emp_chart"))


@app.route("/hr/emp_count")
@app.route("/hr/count")
@app.route("/hr/cnt")
def emp_count():
    result = em.get_emp_count()
    print(result)
    return render_template("hr/count.html", data=result)


# http://localhost:5000/hr/cnt?deptid=50
# http://localhost:5000/hr/cnt/50 <-선택
@app.route("/hr/cnt/<deptid>")
def emp_count_by_deptid(deptid):
    result = em.get_emp_count_by_department_id(deptid)
    print(result)
    return render_template("hr/count.html", data=result)


@app.route("/hr/emp/<emp_id>")
def emp_info(emp_id):
    emp = em.get_emp_info(emp_id)
    return render_template("hr/view.html",
                            data=emp.to_dict())


@app.route("/hr/emp/chart")
def emp_chart():
    num_list = em.get_num_of_emps_by_dept()
    # print(num_list)
    chart_data = []
    for row in num_list:
        chart_data.append(f"{{ from: {row[0]}, to: {row[0]}, value: {row[1]} }}")

    print(','.join(chart_data))
    return render_template("index.html", data=','.join(chart_data))


@app.route("/hr")
def emp_list():
    emps = em.get_all_emps()
    return render_template("hr/list.html", data=emps)


@app.route("/hr/json/<empid>")
def emp_json(empid):
    emp = em.get_emp_info(empid)
    return jsonify(emp.to_dict())


@app.route("/hr/insert", methods=["GET"])
def insert_form():
    dept_list = em.get_dept_info()
    job_list = em.get_job_info()
    manager_list = em.get_manager_info()
    return render_template("hr/insert_form.html",
                           data={"dept_list": dept_list,
                                 "job_list": job_list,
                                 "manager_list": manager_list})


@app.route("/hr/insert", methods=["POST"])
def insert_emp():
    employee_id = int(request.form["employee_id"])
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    hire_date = request.form["hire_date"]
    job_id = request.form["job_id"]
    salary = int(request.form["salary"])
    commission_pct = None
    try :
        commission_pct = eval(request.form["commission_pct"])
    except Exception as e:
        print(e) # commission_pct를 실수형으로 변환할 수 없을 경우

    manager_id = int(request.form["manager_id"])
    department_id = int(request.form["department_id"])
    em.insert_emp(employee_id=employee_id, first_name=first_name, last_name=last_name,
                  email=email, phone_number=phone_number, hire_date=hire_date, job_id=job_id,
                  salary=salary, commission_pct=commission_pct, manager_id=manager_id,
                  department_id=department_id)
    return redirect("/hr")


@app.route("/hr/delete/<int:emp_id>")
def delete_emp(emp_id):
    em.delete_emp(emp_id)
    return redirect("/hr")


@app.route("/hr/update/<int:emp_id>", methods=["GET"])
def update_form(emp_id):
    dept_list = em.get_dept_info()
    job_list = em.get_job_info()
    manager_list = em.get_manager_info()
    emp = em.get_emp_info(emp_id)
    return render_template("hr/update_form.html",
                           data={"dept_list": dept_list,
                                 "job_list": job_list,
                                 "manager_list": manager_list,
                                 "emp": emp.to_dict()})


@app.route("/hr/update", methods=["POST"])
def update_emp():
    employee_id = int(request.form["employee_id"])
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    hire_date = request.form["hire_date"]
    job_id = request.form["job_id"]
    salary = int(eval(request.form["salary"]))
    commission_pct = float(request.form["commission_pct"])
    manager_id = int(request.form["manager_id"])
    department_id = int(request.form["department_id"])
    emp = em.Employees(employee_id, first_name, last_name, email,
                       phone_number, hire_date, job_id, salary,
                       commission_pct, manager_id, department_id)
    em.update_emp(emp)
    return redirect("/hr")


# 이 코드는 파일의 맨 아래에 두세요.
if __name__ == "__main__":
    app.debug = True
    app.run(port=80)
    # app.run(host="0.0.0.0", port=80)