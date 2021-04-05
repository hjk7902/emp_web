import cx_Oracle as oci

oracle_dsn = oci.makedsn(host="localhost", port=1521, sid="xe")
conn = oci.connect(dsn=oracle_dsn, user="hr", password="hr")


class Employees:
    def __init__(self,
                 employee_id, first_name, last_name, email,
                 phone_number, hire_date, job_id, salary=None, commission_pct=None,
                 manager_id=None, department_id=None):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.hire_date = hire_date
        self.job_id = job_id
        self.salary = salary
        self.commission_pct = commission_pct
        self.manager_id = manager_id
        self.department_id = department_id

    def __str__(self):
        return f"{self.employee_id}, {self.first_name}, {self.last_name}, " \
               f"{self.email}, {self.phone_number}, {self.hire_date}, " \
               f"{self.job_id}, {self.salary}, {self.commission_pct}, " \
               f"{self.manager_id}, {self.department_id}"

    def to_dict(self):
        return {"employee_id": self.employee_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "hire_date": self.hire_date,
                "job_id": self.job_id,
                "salary": self.salary,
                "commission_pct": self.commission_pct,
                "manager_id": self.manager_id,
                "department_id": self.department_id}


def get_emp_count():
    sql = "select count(*) from emps"
    cursor = conn.cursor()
    cursor.execute(sql)
    count = cursor.fetchone()
    return count


def get_emp_count_by_department_id(deptid):
    sql = "select count(*) from emps where department_id=:deptid"
    cursor = conn.cursor()
    cursor.execute(sql, {"deptid":deptid})
    count = cursor.fetchone()
    return count


def get_emp_info(emp_id):
    sql = "select employee_id, first_name, last_name, " \
          "email, phone_number, to_char(hire_date, 'YYYY-MM-DD'), " \
          "job_id, salary, commission_pct, " \
          "manager_id, department_id " \
          "from emps " \
          "where employee_id=:emp_id"
    cursor = conn.cursor()
    cursor.execute(sql, {"emp_id":emp_id})
    emp_info = cursor.fetchone()
    # print(emp_info) # 데이터베이스에서 조회한 데이터는 튜플 형식
    emp = Employees(*emp_info) # 튜플 언패킹해서 생성자에 전달
    # print(emp)  # __str__() 함수가 실행됨
    # print(emp.to_dict()) # 딕셔너리 객체를 출력해봄
    # return emp_info # 튜플 형식으로 반환하고 싶을 겨웅
    return emp  # 객체로 반환하고 싶을 경우


def get_num_of_emps_by_dept():
    sql = "select nvl(department_id, '0'), count(*) from emps group by department_id"
    cursor = conn.cursor()
    cursor.execute(sql)
    num_list = cursor.fetchall()
    return num_list


def get_all_emps():
    sql = "select employee_id, first_name, last_name, " \
          "email, phone_number, to_char(hire_date, 'YYYY-MM-DD'), " \
          "job_id, salary, commission_pct, " \
          "manager_id, department_id " \
          "from emps" # 모든 사원의 모든 열 정보 조회
    cursor = conn.cursor()
    cursor.execute(sql)
    emp_list = []
    for emp in cursor:
        emp_list.append(Employees(*emp))

    # print(emp_list)
    return emp_list
    # emp_list = cursor.fetchall()
    # emps = []
    # for data in emp_list:
    #     emp = Employees(*data)
    #     emps.append(emp)
    # # print(emp_list)
    # return emps


def insert_emp(**kwargs):
    print(kwargs)
    sql = "insert into emps values " \
          "(:employee_id, :first_name, :last_name, :email," \
          ":phone_number, to_date(:hire_date, 'YYYY-MM-DD'), " \
          ":job_id, :salary, :commission_pct, " \
          ":manager_id, :department_id)"
    cursor = conn.cursor()

    if kwargs["commission_pct"] is None:
        sql = "insert into emps values " \
              "(:employee_id, :first_name, :last_name, :email," \
              ":phone_number, to_date(:hire_date, 'YYYY-MM-DD'), " \
              ":job_id, :salary, null, " \
              ":manager_id, :department_id)"
        cursor.execute(sql, {"employee_id": kwargs["employee_id"],
                             "first_name": kwargs["first_name"],
                             "last_name": kwargs["last_name"],
                             "email": kwargs["email"],
                             "phone_number": kwargs["phone_number"],
                             "hire_date": kwargs["hire_date"],
                             "job_id": kwargs["job_id"],
                             "salary": kwargs["salary"],
                             "manager_id": kwargs["manager_id"],
                             "department_id": kwargs["department_id"]
                             })
        conn.commit()
        return

    if kwargs["commission_pct"] >= 1.0:
        raise ValueError("보너스율은 1보다 작아야 합니다.")

    cursor.execute(sql, {"employee_id": kwargs["employee_id"],
                         "first_name": kwargs["first_name"],
                         "last_name": kwargs["last_name"],
                         "email": kwargs["email"],
                         "phone_number": kwargs["phone_number"],
                         "hire_date": kwargs["hire_date"],
                         "job_id": kwargs["job_id"],
                         "salary": kwargs["salary"],
                         "commission_pct": kwargs["commission_pct"],
                         "manager_id": kwargs["manager_id"],
                         "department_id": kwargs["department_id"]
                         })
    conn.commit()


def get_dept_info():
    sql = "select department_name, department_id from departments"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_job_info():
    sql = "select job_title, job_id from jobs"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_manager_info():
    sql = "select first_name || ' ' || last_name as name, employee_id " \
          "from emps"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def delete_emp(emp_id):
    sql = "delete from emps where employee_id=:employee_id"
    cursor = conn.cursor()
    cursor.execute(sql, {"employee_id": emp_id})
    conn.commit()


def update_emp(emp):
    sql = "update emps set " \
          "first_name=:first_name, last_name=:last_name, " \
          "email=:email, phone_number=:phone_number, " \
          "hire_date=to_date(:hire_date, 'YYYY-MM-DD'), " \
          "job_id=:job_id, salary=:salary, commission_pct=:commission_pct, " \
          "manager_id=:manager_id, department_id=:department_id " \
          "where employee_id=:employee_id"
    cursor = conn.cursor()
    print(emp.to_dict())
    cursor.execute(sql, emp.to_dict())
    conn.commit()