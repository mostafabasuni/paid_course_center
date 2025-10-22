from course_center_db import Course
from peewee import DoesNotExist

class CourseService:
    @staticmethod
    def create_course(name, grade_id, teacher_id, price):
        try:
            course = Course.create(                
                name=name,
                grade_id=grade_id,
                teacher_id=teacher_id,
                price=price
            )
            return True, "تم إنشاء المادة الدراسية بنجاح"
        except DoesNotExist:
            return False, "المدرس أو الصف غير موجود"
        except Exception as e:
            return False, f"خطأ تكرار بيانات"

    @staticmethod
    def get_all_courses():
        return Course.select()

    
    @staticmethod
    def update_course(course_id, course_name, grade_id, teacher_id, price):
        try:
            # التحقق من وجود المادة الدراسية
            course = Course.get(Course.id == course_id)
            # تحديث البيانات        
            course.name = course_name
            course.grade_id = grade_id
            course.teacher_id = teacher_id
            course.price = price
            course.save()
            
            return True, "تم تحديث المادة الدراسية بنجاح"
        
        except DoesNotExist:
            return False, "المادة أو الصف أو المدرس غير موجود"
        except Exception as e:
            return False, "حدث خطأ أثناء التحديث"

    @staticmethod
    def delete_course(course_id):
        try:            
            course = Course.get_by_id(course_id)
            course.delete_instance()
            return True, "تم حذف المادة بنجاح"
        except Course.DoesNotExist:
            return False, "المادة غير موجودة"
        except Exception as e:
            return False, f"حدث خطأ أثناء الحذف: {str(e)}"
    
    