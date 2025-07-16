# # from .db_connection import get_connection

# # def fetch_employees():
# #     conn = get_connection()
# #     cur = conn.cursor()
# #     cur.execute("SELECT name, role, department FROM employees")
# #     rows = cur.fetchall()
# #     cur.close()
# #     conn.close()
# #     return rows

# # def fetch_teams():
# #     conn = get_connection()
# #     cur = conn.cursor()
# #     cur.execute("SELECT name, lead, members FROM teams")
# #     rows = cur.fetchall()
# #     cur.close()
# #     conn.close()
# #     return rows

# # def fetch_policies(policy_type):
# #     conn = get_connection()
# #     cur = conn.cursor()
# #     cur.execute("SELECT title, content FROM company_policies WHERE type = %s", (policy_type,))
# #     rows = cur.fetchall()
# #     cur.close()
# #     conn.close()
# #     return rows

# from .db_connection import get_connection
# import datetime

# def get_employees_by_department(dept_name):
#     try:
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             SELECT name FROM employees 
#             WHERE LOWER(department) = LOWER(%s)
#         """, (dept_name,))
#         rows = cur.fetchall()
#         cur.close()
#         conn.close()
#         return [r[0] for r in rows]
#     except Exception as e:
#         print(f"❌ DB Error (department): {e}")
#         return []

# def get_employees_by_birth_month(month_name):
#     try:
#         # month_num = list(calendar.month_name).index(month_name.capitalize())
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("""
#             SELECT name FROM employees 
#             WHERE TO_CHAR(DOB, 'Month') ILIKE %s
#         """, (month_name + '%',))
#         rows = cur.fetchall()
#         cur.close()
#         conn.close()
#         return [r[0] for r in rows]
#     except Exception as e:
#         print(f"❌ DB Error (birth month): {e}")
#         return []

# def get_total_employees():
#     try:
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT COUNT(*) FROM employees")
#         count = cur.fetchone()[0]
#         cur.close()
#         conn.close()
#         return count
#     except Exception as e:
#         print(f"❌ DB Error (total): {e}")
#         return 0

from .db_connection import get_connection
import calendar
import datetime

def get_employees_by_department(department):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM employees WHERE LOWER(department) = LOWER(%s)", (department,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [row[0] for row in rows]
    except Exception as e:
        print("❌ DB Error (department):", e)
        return []

def get_employees_by_birth_month(month_name):
    try:
        month_num = list(calendar.month_name).index(month_name.capitalize())
        conn = get_connection()
        cur = conn.cursor()
        query = "SELECT name FROM employees WHERE EXTRACT(MONTH FROM dob) = %s"
        cur.execute(query, (month_num,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [row[0] for row in rows]
    except ValueError:
        return []
    except Exception as e:
        print("❌ DB Error (birth_month):", e)
        return []

def get_upcoming_birthdays(days_ahead=7):
    try:
        conn = get_connection()
        cur = conn.cursor()
        today = datetime.date.today()
        end_date = today + datetime.timedelta(days=days_ahead)

        query = """
        SELECT name, dob FROM employees
        WHERE TO_CHAR(dob, 'MM-DD') BETWEEN TO_CHAR(%s, 'MM-DD') AND TO_CHAR(%s, 'MM-DD')
        """
        cur.execute(query, (today, end_date))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [f"{name} - {dob.strftime('%d %b')}" for name, dob in rows]
    except Exception as e:
        print("❌ DB Error (upcoming_birthdays):", e)
        return []

def get_total_employees():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM employees")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return count
    except Exception as e:
        print("❌ DB Error (count):", e)
        return 0
