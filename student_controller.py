from course_center_db import Student, Payment
from peewee import DoesNotExist, IntegrityError

class StudentService:
    @staticmethod    
    def create_student(name, phone, grade_id, section, reg_date):        
        try:
            student = Student.create(                
                name=name,
                phone=phone,
                grade_id=grade_id,
                section=section,
                reg_date=reg_date
            )
            return True, "تم تسجيل الطالب بنجاح"
        except DoesNotExist:
            return False, "الطالب المحدد غير موجود"
        except Exception as e:
            return False, f"خطأ تكرار بيانات"
        
    @staticmethod
    def student_update(student_id, name, phone, grade_id, section, reg_date):
        
        try:
            student = Student.get(Student.id == student_id)                        
            student.name = name            
            student.phone = phone            
            student.grade_id = grade_id  # سيتم تحويله تلقائياً لكائن Grade
            student.section = section
            student.reg_date = reg_date
            student.save()
            return True, "تم تحديث بيانات الطالب بنجاح"
        except DoesNotExist:
            return False, "الطالب غير موجود"
        except IntegrityError as e:
            return False, f"حدث خطأ أثناء التحديث"
    
    @staticmethod    
    def student_delete(student_id):
        try:
            student = Student.get(Student.id == student_id)
            if Payment.select().where(Payment.student_id == student_id).exists():                
                return False, "لا يمكن حذف الطالب لوجود دفعات مالية مسجلة له"
            else:
                student.delete_instance()
                return True, "تم حذف الطالب بنجاح"
        except DoesNotExist:
            return False, "الطالب غير موجود"
        except IntegrityError as e:
            return False, f"خطأ في قاعدة البيانات: {str(e)}"    