from course_center_db import Attendance
from peewee import DoesNotExist

class AttendanceService:
    @staticmethod
    def add_absence(student_id, course_id, teacher_id, grade_id ,date, day):
        try:
            attendance = Attendance.create(                
                student_id=student_id,
                course_id=course_id,
                teacher_id=teacher_id,                
                grade_id=grade_id,
                absence_date=date,
                absence_day=day                
            )
            return True, "تم إضافة الغياب بنجاح"
        except DoesNotExist:
            return False, "الطالب أو المدرس غير موجود"
        except Exception as e:
            return False, f"خطأ تكرار بيانات"

    @staticmethod
    def update_absence(absence_id, student_id, course_id, teacher_id, grade_id ,date, day):
        try:
            Attendance.update(                
                student_id=student_id,
                course_id=course_id,
                teacher_id=teacher_id,                
                grade_id=grade_id,
                absence_date=date,
                absence_day=day                
            ).where(Attendance.id == absence_id).execute()
            return True, "تم تحديث الغياب بنجاح"
        except DoesNotExist:
            return False, "الطالب أو المدرس غير موجود"
    
    @staticmethod
    def delete_absence(absence_id):
        try:
            absence = Attendance.get_by_id(absence_id)
            absence.delete_instance()            
            return True, "تم حذف الغياب بنجاح"
        except DoesNotExist:
            return False, "الغياب غير موجود"
        