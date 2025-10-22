from course_center_db import Teacher, TeacherAccount
from peewee import DoesNotExist

class TeacherService:
    def __init__(self):
        pass

    @staticmethod
    def create_teacher(name, phone, specialization, share_percent):
        try:            
            teacher = Teacher.create(
                name=name, 
                phone=phone, 
                specialization=specialization, 
                share_percent=share_percent)        
            return True, "تم حفظ المدرس بنجاح"        
        except Exception as e:
            return False, f"خطأ تكرار بيانات"
        
        
        
    def update_teacher(self, id, name, phone, specialization, share_percent):
        try:
            teacher = Teacher.get(Teacher.id == id)            
            teacher.name = name
            teacher.phone = phone
            teacher.specialization = specialization
            teacher.share_percent = share_percent            
            teacher.save()
            return True, "تم تحديث بيانات المعلم بنجاح"
        except Teacher.DoesNotExist:
            return False, "المعلم غير موجود"
        except Exception as e:
            return False, f"حدث خطأ أثناء التحديث: {str(e)}"

    def delete_teacher(self, id):
        try:
            teacher = Teacher.get_by_id(id)
            teacher.delete_instance()
            return True, "تم حذف المدرس بنجاح"
        except Teacher.DoesNotExist:
            return False, "المدرس غير موجود"
        except Exception as e:
            return False, "لا يمكن حذف المدرس لارتباطه بسجلات أخرى"
    
    def update_teacher_account(self, teacher_id, month, date, user_id):
        t = Teacher.get_by_id(teacher_id)
        try:
            teacher = TeacherAccount.select().where(
                (TeacherAccount.teacher_id == teacher_id) & 
                (TeacherAccount.month == month)
            ).get()

            if teacher.status == 1:  # استلم بالفعل
                return False, f"المدرس : {t.name}\nاستلم مستحقاته لهذا الشهر بالفعل"

            # تحديث البيانات إذا ما استلمش
            teacher.date = date
            teacher.status = 1  # تم التحصيل
            teacher.user_id = user_id
            teacher.save()

            return True, "تم تحديث بيانات المستحقات بنجاح"

        except DoesNotExist:
            return False, f"لا يوجد حساب مستحقات مسجل للمدرس {t.name} لهذا الشهر"
        except Exception as e:
            return False, f"حدث خطأ أثناء حفظ حساب المدرس: {str(e)}"
