from django.shortcuts import render,HttpResponse,redirect
from appwrite.query import Query
from django.contrib import messages
from . import data as db
import json 
from django.http import JsonResponse
from pprint import pprint





import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

    
# function to handle user logout
def logout(request):
    data = {'logOut': True}
    return render(request, 'home.html', data)



def home(request):
    return render(request,"home.html",{"home":True})


def admin(request):
    return redirect('teachers')
                  

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        data = db.getDocument(os.getenv('db_id'), os.getenv('teacher_details_col_id'))
        # print(data)
        
        for user in data:
            # print (user)
            if user["Username"] == username and user["Password"] == password:
                data={}
                data['username'] = username
                data['password'] = password
                data['saveLogin'] = True
                if user["is_admin"]:
                    data["data"]= db.getDocument(os.getenv('db_id'), os.getenv('teacher_details_col_id'),
                                      [Query.not_equal("Username", ["admin"])])
    
    
                    return render(request, "manage_teachers.html",data)
                else:
                    timetable= db.getDocument(os.getenv('db_id'), os.getenv('timetable_col_id'), [Query.equal("TeacherUsername",[username]),Query.limit(100)])
        
                    table={}
                    for day in timetable:
                        # print(day)
                        key=day['Day']+"_"+str(day['Hour'])
                        table[key]={
                                        "Subject":day['Subject'],
                                        "TeacherUsername":day['TeacherUsername'],
                                        "ClassId":day['ClassId'],
                                        }
                        
                    
                                        
                    
                
                
                    data["timetable"]=table
                    return render(request,"user/schedule.html",data)
    
                    return render(request, 'user/schedule.html',data)
        
        # If no user with matching credentials is found
        messages.error(request, 'Login Failed ! Please Check Your Credentials...')
        return render(request,'login.html',{'user':request.POST.get('user'),'home':True})
    
    user=request.GET.get('user')
    return render(request, 'login.html', {'user': user,"home":True})

        
    

def manageteachers(request):

    if request.method == 'POST':
        if "addteacher" in request.POST:
            data={"Name": request.POST.get("name"),
                  "Department":request.POST.get("department"),
                  "Phoneno":int(request.POST.get("phoneno")), 
                  "Username": request.POST.get("username"),
                  "Password":request.POST.get("password")
                  }
            result=db.addDocument(os.getenv('db_id'), os.getenv('teacher_details_col_id'),data)
            if not result:
                # print(result)
                messages.error(request,"Error! Username Already Exists")
                data={"docid": request.POST.get("docid"),
                  "Name": request.POST.get("name"),
                  "Department":request.POST.get("department"),
                  "Phoneno":int(request.POST.get("phoneno")), 
                  "Username": request.POST.get("username"),
                  "Password":request.POST.get("password")
                  }
                return render(request,"add_teachers.html",{"data":data})
                
            else:
                messages.success(request,"Added Successfully")
               
                
        # to save the edited data
        elif "saveButton" in request.POST:
            data={"Name": request.POST.get("name"),
                  "Department":request.POST.get("department"),
                  "Phoneno":int(request.POST.get("phoneno")), 
                  "Username": request.POST.get("username"),
                  "Password":request.POST.get("password")
                  }
            result=db.updateDocument(os.getenv('db_id'), os.getenv('teacher_details_col_id'),request.POST.get("docid"),data)
            if not result:
                messages.error(request,"Error! Username Already Exists")
                data={"docid": request.POST.get("docid"),
                  "Name": request.POST.get("name"),
                  "Department":request.POST.get("department"),
                  "Phoneno":int(request.POST.get("phoneno")), 
                  "Username": request.POST.get("username"),
                  "Password":request.POST.get("password")
                  }
                return render(request,"view_teacher.html",{"data":data})
            else:
                messages.success(request,"Updated Successfully")
             
        # to delete teacher
        elif "delete" in request.POST:
            
            result=db.deleteDocument(os.getenv('db_id'), os.getenv('teacher_details_col_id'),request.POST.get("docid"))
            if not result:
                messages.error(request,"Could not Delete")
            else:
                messages.success(request,"Deleted Successfully")
            
        else:  
            return render(request, 'add_teachers.html')
        
    
    data = db.getDocument(os.getenv('db_id'), os.getenv('teacher_details_col_id'),
                                      [Query.not_equal("Username", ["admin"])])
    
    
    return render(request, "manage_teachers.html",{"data":data})



def teacherdetails(request):
    if request.method == 'POST':
        data={"docid": request.POST.get("docid"),
              "Name": request.POST.get("name"),
                  "Department":request.POST.get("department"),
                  "Phoneno":int(request.POST.get("phoneno")), 
                  "Username": request.POST.get("username"),
                  "Password":request.POST.get("password")
                  }
        return render(request,"view_teacher.html",{"data":data})
    return redirect("teacherdetails")



def manageclass(request):
    if request.method == 'POST':
        if "saveclass" in request.POST:
            data={
                  "Department":request.POST.get("department"),
                  "Year":request.POST.get("year"),
                  "ClassId":request.POST.get("year")+request.POST.get("department"),
                  }
            result=db.addDocument(os.getenv('db_id'), os.getenv('class_col_id'),data)
            if not result:
                messages.error(request,"did not add")
            else:
                messages.success(request,"Added Successfully")
                
    data = db.getDocument(os.getenv('db_id'), os.getenv('class_col_id'))
                                    
    return  render(request,"man_class.html",{"data":data})
 
 
def manage(request):
    if request.method =="POST":
        classid=request.POST.get("classid")
        data = db.getDocument(os.getenv('db_id'), os.getenv('students_col_id'),[Query.equal("ClassId",[classid])])
        return render(request, "manage_students.html",{"data":data,"classid":classid})
    
    data = db.getDocument(os.getenv('db_id'), os.getenv('class_col_id'))
    return  render(request,"man_class.html",{"data":data})
    

def students(request):
    classid=request.GET.get("classid")
    if request.method == 'POST':
        classid=request.POST.get("classid")
        # print("hear",classid)
        
        if "addstudent" in request.POST:
            data={"Regno": request.POST.get("Regno"),
                  "Rollno":request.POST.get("Rollno"),
                  "Name":request.POST.get("Name"), 
                  "Phoneno": int(request.POST.get("Phoneno")),
                  "ClassId":request.POST.get("classid")
                  }
            result=db.addDocument(os.getenv('db_id'), os.getenv('students_col_id'),data)
            print(result)
            if not result:
                messages.error(request,"Error! Reg No or Roll No Already Exists")
                data={"classid": request.POST.get("classid"),
                      "Regno": request.POST.get("Regno"),
                  "Rollno":int(request.POST.get("Rollno")),
                  "Name":request.POST.get("Name"), 
                  "Phoneno": int(request.POST.get("Phoneno")),
                  }
                return render(request,"add_student.html",{"data":data})
                
            else:
                messages.success(request,"Added Successfully")
               
                
        # to save the edited data
        elif "savebtn" in request.POST:
            data={"Regno": request.POST.get("Regno"),
                  "Rollno":request.POST.get("Rollno"),
                  "Name":request.POST.get("Name"), 
                  "Phoneno": int(request.POST.get("Phoneno")),
                  "ClassId":request.POST.get("classid")
                  }
            print(data)
            result=db.updateDocument(os.getenv('db_id'), os.getenv('students_col_id'),request.POST.get("docid"),data)
            if not result:
                messages.error(request,"Error! Reg No or Roll No Already Exists")
                data={"classid": request.POST.get("classid"),
                      "Regno": request.POST.get("Regno"),
                  "Rollno":int(request.POST.get("Rollno")),
                  "Name":request.POST.get("Name"), 
                  "Phoneno": int(request.POST.get("Phoneno")),
                  }
                return render(request,"view_student.html",{"data":data})
            else:
                messages.success(request,"Updated Successfully")
             
        # # to delete teacher
        elif "delete" in request.POST:
            
            result=db.deleteDocument(os.getenv('db_id'), os.getenv('students_col_id'),request.POST.get("docid"))
            if not result:
                messages.error(request,"Could not Delete")
            else:
                messages.success(request,"Deleted Successfully")
            
        else:  
            return render(request, 'add_student.html',{"data":{"classid": classid}})
        
    # print(classid)
    if classid is None or classid=="":
        return redirect('manage')
    data = db.getDocument(os.getenv('db_id'), os.getenv('students_col_id'),[Query.equal("ClassId",[classid])])
    

    
    return render(request, "manage_students.html",{"data":data,"classid":classid})
    



def subjects(request):
    
    
    if request.method == 'POST':
        if "savesub" in request.POST:
            data={
                  "Subject":request.POST.get("subject"),
                  "Username":request.POST.get("teacher"),
                  "ClassId":request.POST.get("classid"),
                  }
            
            result=db.addDocument(os.getenv('db_id'), os.getenv('subjects_col_id'),data)
            if not result:
                messages.error(request,"Failed Adding Subjects")
            else:
                messages.success(request,"Added Successfully")
        
        if "updatebtn" in request.POST:
            data={
                  "Subject":request.POST.get("subject"),
                  "Username":request.POST.get("teacher"),
                  "ClassId":request.POST.get("classid"),
                  }
            result=db.updateDocument(os.getenv('db_id'), os.getenv('subjects_col_id'),request.POST.get("docid"),data)
            
            if not result:
                messages.error(request,"Failed Updating")
                
            else:
                messages.success(request,"Updated Successfully")
        
        elif "deletebtn" in request.POST:
            
            result=db.deleteDocument(os.getenv('db_id'), os.getenv('subjects_col_id'),request.POST.get("docid"))
            if not result:
                messages.error(request,"Could not Delete")
            else:
                messages.success(request,"Deleted Successfully")
            
    
    
    teacher = db.getDocument(os.getenv('db_id'), os.getenv('teacher_details_col_id'),
                                      [Query.not_equal("Username", ["admin"])])
    
    data = db.getDocument(os.getenv('db_id'), os.getenv('subjects_col_id'),[Query.equal("ClassId",[request.POST.get("classid")])])
    
    
    
    return render(request,"subjects.html",{"data":data,"teacher":teacher,"classid":request.POST.get("classid")})


def studentdetails(request):
    if request.method == 'POST':
        data={"docid": request.POST.get("docid"),
              "Regno":request.POST.get("Regno"),
              "Rollno":request.POST.get("Rollno"),
                  "Name":request.POST.get("Name"), 
                  "Phoneno":request.POST.get("Phoneno"),
                  "classid":request.POST.get("classid"),
                  }
        return render(request,"view_students.html",{"data":data})
    return redirect("studentdetails")


def timetable(request):
    
    subjects = db.getDocument(os.getenv('db_id'), os.getenv('subjects_col_id'),[Query.equal("ClassId",[request.POST.get("classid")])])
    teachers= db.getDocument(os.getenv('db_id'), os.getenv('teacher_details_col_id'), [Query.not_equal("Username", ["admin"])])
    timetable= db.getDocument(os.getenv('db_id'), os.getenv('timetable_col_id'), [Query.equal("ClassId",[request.POST.get("classid")]),Query.limit(100)])
    
    table={}
    for day in timetable:
        # print(day)
        key=day['Day']+"_"+str(day['Hour'])
        table[key]={
                           "Subject":day['Subject'],
                           "TeacherUsername":day['TeacherUsername']
                           }
        
    
                          
    
    print(table)
    return render(request,"timetables.html",{"subjects":subjects,"teachers":teachers,"timetable":table,"ClassId":request.POST.get("classid")})


# user below ************************************************************

def schedule(request):
    if request.method == "POST":
        timetable= db.getDocument(os.getenv('db_id'), os.getenv('timetable_col_id'), [Query.equal("TeacherUsername",[request.POST.get("username")]),Query.limit(100)])
        
        table={}
        for day in timetable:
            # print(day)
            key=day['Day']+"_"+str(day['Hour'])
            table[key]={
                            "Subject":day['Subject'],
                            "TeacherUsername":day['TeacherUsername'],
                            "ClassId":day['ClassId'],
                            }
            
        
                            
        
    
    
        data={"username":request.POST.get("username"),"timetable":table}
        return render(request,"user/schedule.html",data)
    return redirect("logout")



def attendence(request):
    if request.method == "POST":
        username=request.POST.get("username")
        
        if "takeAttendance" in request.POST:
            date=request.POST.get("date")
            hour=request.POST.get("hour")
            ClassId=request.POST.get("class")
            subject=request.POST.get("subject")
            
            students= db.getDocument(os.getenv('db_id'), os.getenv('students_col_id'),[Query.equal("ClassId",[ClassId])])
            
            data={
                "date": date,
                "hour": hour,
                "ClassId": ClassId,
                "subject": subject,
                "students": students,
                "username":username
            }
            
            return render(request, "user/take_attendance.html",data)
            
            
        # classes = db.getDocument(os.getenv('db_id'), os.getenv('class_col_id'))
        subjects= db.getDocument(os.getenv('db_id'), os.getenv('subjects_col_id'),[Query.equal("Username",[username])])
      
        
        
        return render(request, "user/attendence.html",{"subjects":subjects,"username":username})
    return redirect("logout")




def attendencereport(request):
    if request.method == "POST":
        username=request.POST.get("username")
        # classes = db.getDocument(os.getenv('db_id'), os.getenv('class_col_id'))
        subjects= db.getDocument(os.getenv('db_id'), os.getenv('subjects_col_id'),[Query.equal("Username",[username])])
        data = db.getDocument(os.getenv('db_id'), os.getenv('attendence_col_id'))
        
        # print(subjects)
        # print(classes)
        
        return render(request,"user/attendence_report.html",{"username":username,"data":data,"classes":subjects,"subjects":subjects})
    return redirect("logout")






# AJAX Method below   ************************************************************************************************


def saveImportedStudent(request):
    # Your view logic here
    # return render(request, 'mobile.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            students = data.get('students')
          
            
            # Process the data here
        
            print(f"Msg: {students}")
            
            
            notupdateCount=0
            for student in students:
                data={"Regno": student["Regno"],
                  "Rollno":str(student["Rollno"]),
                  "Name":student["Name"], 
                  "Phoneno": int(student["Phoneno"]),
                  "ClassId":student["ClassId"]
                  }
                result=db.addDocument(os.getenv('db_id'), os.getenv('students_col_id'),data)
                
                
                if not result:
                    notupdateCount+=1
    
            res=True

            if notupdateCount==0:
                # Respond with a success message
                return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
            return JsonResponse({'status': 'error', 'message': f'{notupdateCount} students not added'}, status=400)
        
        except json.JSONDecodeError:
           
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



def viewattendence(request):
    data=db.getDocument(os.getenv('db_id'), os.getenv('attendence_col_id'),[Query.equal("ClassId",[request.POST.get("classid")])])
    return render(request,"view_attendence.html",{"data":data})



def saveTimetable(request):
    # Your view logic here
    # return render(request, 'mobile.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            ClassId = data.get('ClassId')
            timeTable = data.get('timeTable')
          
            
            # Process the data here
        
            print(f"ClassId: {ClassId}")
            
            for Day,value in timeTable.items():
                for Hour in range(0, len(value)):
                    Subject=value[Hour]['subject']
                    TeacherUsername=value[Hour]['teacher']
                    h=value[Hour]['hour']
                    
                    saveDay={
                        "Day":Day,
                        "Hour":h,
                        "ClassId":ClassId,
                        "Subject":Subject,
                        "TeacherUsername":TeacherUsername
                    }
                    
                    db.addDocument(os.getenv('db_id'), os.getenv('timetable_col_id'),saveDay)
                    
                    
                    
                    
            # pprint(timeTable)
            
            
            
    
            res=True

            if res:
                # Respond with a success message
                return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
            return JsonResponse({'status': 'error', 'message': f'{res} students not added'}, status=400)
        
        except json.JSONDecodeError:
           
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def saveAttendence(request):
    # Your view logic here
    # return render(request, 'mobile.html')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            data = data.get('data')
            
            for each in data:
                res=db.addDocument(os.getenv('db_id'), os.getenv('attendence_col_id'),each)
                if not res:
                    return JsonResponse({'status': 'error', 'message': 'Error'}, status=400)
          
    
            res=True

            if res:
                # Respond with a success message
                return JsonResponse({'status': 'success', 'message': 'Data received successfully'})
            return JsonResponse({'status': 'error', 'message': f'{res}'}, status=400)
        
        except json.JSONDecodeError:
           
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

