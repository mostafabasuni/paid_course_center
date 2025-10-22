from peewee import *
import datetime

# الاتصال بقاعدة البيانات (SQLite في هذا المثال، يمكنك تغييرها إلى MySQL)
db = MySQLDatabase('course_center', user='root', password='', host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=100)  # يُفضل أن تُخزّن كلمة السر مُشفّرة
    fullname = CharField(max_length=100)
    phone = CharField(max_length=20, null=True, unique=True)  # يجب أن يكون فريدًا
    job = CharField(max_length=50)  # مثل admin, staff, viewer
    is_admin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.date.today)

class Management(BaseModel):
    prime_st_account = IntegerField(default=0)  # عدد طلاب المرحلة الابتدائية المسجلي
    prep_st_account = IntegerField(default=0)  # عدد طلاب المرحلة الإعدادية المسجلين
    sec_st_account = IntegerField(default=0)  # عدد طلاب المرحلة الثانوية المسجلين
    outcome = DecimalField(max_digits=14, decimal_places=2, default=0.0)  # النتيجة المالية
    share_percent = DecimalField(max_digits=5, decimal_places=2, default=0.0)  # نسبة من رسوم الكورس

    

class Grade(BaseModel):
    name = CharField()                # اسم واضح مثل "الصف الأول الابتدائي"    
    level = CharField(null=True)       # المرحلة (ابتدائي/متوسط/ثانوي)
    term = CharField(null=True)     # الفصل الدراسي (الأول - الثاني.)
    academic_year = CharField()
    class Meta:
        indexes = (
            # منع تكرار نفس الصف والمستوى والترم والسنة
            (('name', 'level', 'term', 'academic_year'), True),
        )


class Student(BaseModel):
    name = CharField(max_length=100)
    phone = CharField(max_length=20, null=True, unique=True)  # يجب أن يكون فريدًا
    grade_id = ForeignKeyField(Grade, field=Grade.id, backref='students') 
    section = IntegerField(null=True)  # الفصل (1, 2, 3, إلخ.)
    reg_date = DateTimeField(default=datetime.date.today)


class Teacher(BaseModel):
    name = CharField(max_length=100)
    phone = CharField(max_length=20, null=True, unique=True)  # يجب أن يكون فريدًا
    specialization = CharField(max_length=100, null=True)
    share_percent = DecimalField(max_digits=5, decimal_places=2, default=0.0)  # نسبة من رسوم الكورس


class TeacherAccount(BaseModel):
    teacher_id = ForeignKeyField(Teacher, backref='teacher_accounts', on_delete='RESTRICT')
    income = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    month = CharField(max_length=15, null=True)  # الشهر الذي تم فيه الحساب
    student_count = IntegerField(default=0)  # عدد الطلاب المسجلين لدى المعلم في هذا الشهر
    status = BooleanField(default=False)  # حالة الحساب (استلم أو لم يستلم بعد)
    date = DateField(default=datetime.date.today)  # تاريخ الحساب
    user = ForeignKeyField(User, null=True, backref='teacher_accounts')


class Course(BaseModel):
    name = CharField(max_length=100)
    grade_id = ForeignKeyField(Grade, backref='courses', on_delete='RESTRICT')
    teacher_id = ForeignKeyField(Teacher, backref='courses', on_delete='RESTRICT', null=True)
    price = DecimalField(max_digits=10, decimal_places=2)       
    class Meta:
        indexes = (
            # منع تكرار نفس اسم الكورس مع نفس الصف والمعلم
            (('name', 'grade_id', 'teacher_id'), True),
        )


class TeacherStudent(BaseModel):
    teacher_id = ForeignKeyField(Teacher, backref='teacher_grades', on_delete='RESTRICT')
    student_id = ForeignKeyField(Student, backref='teacher_students',on_update='CASCADE', on_delete='RESTRICT')
    grade_id = ForeignKeyField(Grade, backref='teacher_students', on_update='CASCADE', on_delete='RESTRICT')
    month = CharField(max_length=15, null=True)  # الشهر الذي تم فيه التسجيل


class Enrollment(BaseModel):
    student_id = ForeignKeyField(Student, backref='enrollments', on_delete='RESTRICT')
    teacher_id = ForeignKeyField(Teacher, backref='enrollments', on_delete='RESTRICT')
    grade_id = ForeignKeyField(Grade, backref='enrollments', on_delete='RESTRICT')
    course_id = ForeignKeyField(Course, backref='enrollments', on_delete='RESTRICT')        
    month = CharField(max_length=15, null=True)  # الشهر الذي تم فيه التسجيل
    course_price = DecimalField(max_digits=10, decimal_places=2, default=0.0)  # سعر الكورس وقت التسجيل
    late_registration = BooleanField(default=False)  # تسجيل متأخر أم لا
    withdrawn = BooleanField(default=False)  # انسحب أم لا
    center_share = DecimalField(max_digits=10, decimal_places=2, default=0.0)  # حصة المركز من هذا المبلغ
    attendance_count = IntegerField(default=0)  # عدد الحصص التي حضرها الطالب في هذا الكورس
    user_id = ForeignKeyField(User, null=True, backref='enrollments')
    
    
    

class Payment(BaseModel):
    student_id = ForeignKeyField(Student, backref='payments', on_delete='RESTRICT')
    amount = DecimalField(max_digits=10, decimal_places=2, default=0.0)  # المبلغ المدفوع
    cash_back = DecimalField(max_digits=10, decimal_places=2, default=0.0)  # الباقي إن وجد
    center_share = DecimalField(max_digits=10, decimal_places=2, default=0.0)  # حصة المركز من هذا المبلغ
    paid_type = CharField(choices=["نقدي", "فيزا"], default="نقدي")
    payment_date = DateField(default=datetime.date.today)
    month = CharField(max_length=15, null=True)  # الشهر الذي تم فيه الدفع
    user = ForeignKeyField(User, null=True, backref='payments')

class StudentMonthlyInvoice(BaseModel):
    student_id = ForeignKeyField(Student, backref='monthly_invoices', on_delete='RESTRICT')    
    month = CharField(max_length=15, null=True)  # الشهر الذي تم فيه الفاتورة    
    total_due = DecimalField(max_digits=10, decimal_places=2)
    total_paid = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    remain = DecimalField(max_digits=10, decimal_places=2, default=0.0)
    course_count = IntegerField(default=0)  # عدد الكورسات المسجل فيها الطالب
    
class Attendance(BaseModel):
    student_id = ForeignKeyField(Student, backref='attendances', on_delete='RESTRICT')
    course_id = ForeignKeyField(Course, backref='attendances', on_delete='RESTRICT')    
    teacher_id = ForeignKeyField(Teacher, backref='attendances', on_delete='RESTRICT')
    grade_id = ForeignKeyField(Grade, backref='attendances', on_delete='RESTRICT')
    absence_date = DateField(null=True)  # تاريخ الغياب إذا كان غائبًا    
    absence_day = CharField(max_length=15, null=True)
    class Meta:
        indexes = (
            # منع تكرار نفس الطالب في نفس الكورس في نفس اليوم
            (('student_id', 'course_id', 'absence_date'), True),
        )


class Permission(BaseModel):
    user_id = ForeignKeyField(User, backref='permissions', on_update='CASCADE', on_delete='RESTRICT')
    user_tab = BooleanField()
    teacher_tab = BooleanField()
    grade_tab = BooleanField()
    course_tab = BooleanField()    
    student_tab = BooleanField()
    enrollment_tab = BooleanField()
    student_account_tab = BooleanField()
    student_stat_tab = BooleanField()
    teacher_account_tab = BooleanField()    
    attendance_tab = BooleanField()
    management_tab = BooleanField()
    permission_tab = BooleanField()
    
db.connect()
db.create_tables([User, Management, Grade, Student,
                Teacher, TeacherAccount,
                Course, TeacherStudent,
                Enrollment, Payment,
                StudentMonthlyInvoice,
                Attendance, Permission])


# try:    
#     db.execute_sql('''
#         ALTER TABLE course
#         ADD CONSTRAINT unique_course_fields UNIQUE (name, grade_id, teacher_id);
#     ''')
#     print("تم إضافة القيد UNIQUE بنجاح.")
# except Exception as e:
#     print(f"حدث خطأ: {e}")
# finally:
#     db.close()