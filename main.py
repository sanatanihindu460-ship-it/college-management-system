import json
from pathlib import Path
from abc import ABC,abstractmethod

database="college_data.json"
data={"students":[],"teachers":[]}

if Path(database).exists():
    with open(database,"r") as f:
        content=f.read()
        if content:
            data=json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)
while True:
    class Persons(ABC):

        @abstractmethod
        def get_roles(self):
            pass

        
        @abstractmethod
        def register(self):
            pass


        @abstractmethod
        def show_details(self):
            pass

        @abstractmethod
        def valid_email(email): 
            if ("@" in email) and ("." in email):
                return True
            else:
                return False


    class Student(Persons):

        def get_roles(self):
            return "Student"

        def register(self):
            name=input("Enter the name here: ")
            age=int(input("Enter the age of the student: "))
            email=input("Enter the email of the student: ")
            roll_no=int(input("Enter the roll number of the student: "))

            if not Persons.valid_email(email):
                print("Invalid Email")
                return

            for i in data["students"]:
                if i["Roll_No"] == roll_no:
                    print("Student already exist...")
                    return

            data["students"].append({
                "Name":name,
                "Age" :age,
                "Email":email,
                "Roll_No":roll_no,
                "Grades":{}
            })
            save()
            print(f"Student {name} registered successfully...")

        def show_details(self):
            roll_no=int(input("Enter the roll number of the student: "))
            for i in data["students"]:
                if i["Roll_No"]==roll_no:
                    print(f"Name: {i["Name"]}")
                    print(f"Age: {i["Age"]}")
                    print(f"Email: {i["Email"]}")
                    print(f"Roll No: {i["Roll_No"]}")
                    print(f"Grades: {i["Grades"]}")


        def add_grades(self):
            roll_no=int(input("Enter the roll number of student you want to add grades for: "))
            for i in data["students"]:
                if i["Roll_No"]==roll_no:
                    data_num=int(input("Enter the number of subjects you want to add grades for: "))
                    for j in  range(data_num):
                        sub=input("Enter the subject name: ")
                        marks=int(input("Enter the grade of that subject: "))
                        i["Grades"][sub]=marks
                    save()
                    break
            else:
                print("Student not found...")
                return

        def update_grades(self):
            roll_no=int(input("Enter the roll number of student you want to update grades for: "))
            for i in data["students"]:
                if i["Roll_No"]==roll_no:
                    while True:
                        sub=input("Enter the subject name: ")
                        marks=int(input("Enter the grade of that subject: "))
                        i["Grades"][sub]=marks
                        save()
                        while True:
                            y_n=input("Do you want to update more (Y/N): ")
                            if y_n not in "YyNn":
                                print("Input not recognized...")
                                continue
                            elif y_n in "Nn":
                                break
                        break
                    break
            else:
                print("Student not found...")
                return
                        

        def valid_email(email):
            pass




    class Teacher(Persons):

        def get_roles(self):
            return "Teacher"

        def register(self):
            name=input("Enter the name here: ")
            age=int(input("Enter the age of the teacher: "))
            email=input("Enter the email of the teacher: ")
            Id=int(input("Enter the ID of the teacher: "))
            dep=input("Enter the department of the teacher: ")
            salary=int(input("Enter the salary of the teacher: "))

            if not Persons.valid_email(email):
                print("Invalid Email")
                return

            for i in data["teachers"]:
                if i["Id"] == Id:
                    print("Teacher already exist...")
                    return

            data["teachers"].append({
                "Name":name,
                "Age" :age,
                "Email":email,
                "Id":Id,
                "Department":dep,
                "Salary":salary
            })
            save()
            print(f"Teacher {name} registered successfully...")
        
        def show_details(self):
            Id=int(input("Enter the ID of the teacher: "))
            for i in data["teachers"]:
                if i["Id"] == Id:
                    print(f"Name: {i["Name"]}")
                    print(f"Age: {i["Age"]}")
                    print(f"Email: {i["Email"]}")
                    print(f"ID: {i["Id"]}")
                    print(f"Department: {i["Department"]}")
                    print(f"Salary: {i["Salary"]}")
            else:
                print("Teacher not found...")

        def update_salary(self):
            while True:
                Id=int(input("Enter the ID of the teacher: "))
                for i in data["teachers"]:
                            if i["Id"] == Id:
                                upt_salary=int(input("Enter the updated salary of the teacher: "))
                                i["Salary"]=upt_salary
                                save()
                else:
                    print("Teacher not found...")
                while True:
                    y_n=input("Do you want to update more (Y/N): ")
                    if y_n not in "YyNn":
                        print("Input not recognized...")
                        continue
                    elif y_n in "Nn":
                        break
                break

        def valid_email(email):
            pass


    s1=Student()
    t1=Teacher()

    print("\n")
    print("Press 1 to register a student ")
    print("Press 2 to register a teacher ")
    print("Press 3 to add or update grades of the student ")
    print("Press 4 to update salary of the teacher ")
    print("Press 5 to show teacher details ")
    print("Press 6 to show student details ")
    choice=int(input("Enter the option you want to perform\n"))


    if choice==1:
        s1.register()

    elif choice==2:
        t1.register()

    elif choice==3:
        print("Enter 1 to add grades")
        print("Enter 2 to update grades")
        choice_1=int(input("Enter your choice: "))
        if choice_1==1:
            s1.add_grades()
        elif choice_1==2:
            s1.update_grades()
        else:
            print("Invalid choice...")

    elif choice==4:
        t1.update_salary()

    elif choice==5:
        t1.show_details()

    elif choice==6:
        s1.show_details()

    else:
        print("Invalid option")
    
    y_n=input("Do you want to update more (Y/N): ")
    if y_n in "Nn":
        break

    
print("Thank You for visiting us...")
