from course_center_db import Enrollment, Course, StudentMonthlyInvoice, TeacherStudent, TeacherAccount
from decimal import Decimal
from decimal import Decimal, ROUND_HALF_UP

class EnrollmentService:
    def __init__(self):
        pass
    
    def create_enrollment(self, student_id, teacher_id, grade_id, course_id, month, course_price, late_reg, attendance_count, user_id):
        # التحقق من وجود تسجيل مسبق لنفس الطالب في نفس المقرر
        existing = Enrollment.select().where(
            (Enrollment.student_id == student_id) &
            (Enrollment.course_id == course_id) &
            (Enrollment.month == month)
        ).first()

        if existing:
            return False, "الطالب مسجل بالفعل في هذا المقرر."

        try:
            course = Course.get_by_id(course_id)
            teacher = course.teacher_id
            if late_reg:
                course_price = (Decimal(attendance_count) * course.price / Decimal(8)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else:
                course_price = course.price
            center_share = (course_price - (course_price * Decimal(teacher.share_percent) / Decimal(100))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # إنشاء تسجيل جديد
            enrollment = Enrollment.create(
                student_id=student_id,
                teacher_id=teacher_id,
                grade_id=grade_id,
                course_id=course_id,
                month=month,
                course_price=course_price,
                late_registration=late_reg,
                center_share=center_share,
                attendance_count=attendance_count,
                user_id=user_id
            )
            # تحديث حساب المدرس          
                
            teacher = course.teacher_id
            t_account, created = TeacherAccount.get_or_create(
                teacher_id=teacher.id,
                month=month,                
                defaults={
                    'income': course_price * Decimal(teacher.share_percent / 100),
                    'student_count': 1
                }
            )
            if not created:
                t_account.income += course_price * Decimal(teacher.share_percent / 100)
                t_account.student_count += 1
                t_account.save()

            # تحديث الفاتورة الشهرية للطالب                       
                
            st_monthly_invoice, created = StudentMonthlyInvoice.get_or_create(
                student_id=student_id,
                month=month,
                defaults={
                    'course_count': 1,
                    'total_due': course_price,
                    'total_paid': 0,
                    'remain': course_price
                }
            )

            if not created:
                st_monthly_invoice.course_count += 1                
                st_monthly_invoice.total_due += course_price
                st_monthly_invoice.remain += course_price
                st_monthly_invoice.save()

            # ربط الطالب بالمدرس
            TeacherStudent.get_or_create(
                teacher_id=teacher_id,
                student_id=student_id,
                grade_id=grade_id,
                month=month
            )

            return True, "تم تسجيل الطالب بنجاح."

        except Exception as e:
            print("Error:", e)
            return False, "حدث خطأ أثناء التسجيل لعدم وجود بعض البيانات أو لسبب آخر"

    def delete_enrollment(self, enrollment_id):
        try:
            enrollment = Enrollment.get_by_id(enrollment_id)
            course = enrollment.course_id
            teacher = enrollment.teacher_id # بافتراض أن جدول Course يحتوي على حقل teacher_id
            student = enrollment.student_id
            month = enrollment.month
            t_account = TeacherAccount.get(
                (TeacherAccount.teacher_id == teacher.id) & (TeacherAccount.month == month))
            st_account = StudentMonthlyInvoice.get(
                (StudentMonthlyInvoice.student_id == student.id) & (StudentMonthlyInvoice.month == month))
            t_account.student_count -= 1
            t_account.income -= enrollment.course_price * Decimal(teacher.share_percent / 100)  # تحديث المبلغ المستحق على المدرس
            st_account.course_count -= 1
            st_account.remain -= enrollment.course_price  # تحديث المبلغ المتبقي على الطالب
            st_account.total_due -= enrollment.course_price  # تحديث المبلغ المستحق على الطالب
            # حذف العلاقة TeacherStudent
            TeacherStudent.delete().where(
                (TeacherStudent.teacher_id == teacher.id) & 
                (TeacherStudent.student_id == student.id)
            ).execute()            
            st_account.save()
            t_account.save()
            enrollment.delete_instance()
            return True, "تم حذف التسجيل بنجاح."
        except Enrollment.DoesNotExist:
            return False, "التسجيل غير موجود."
        except Exception as e:
            print("Error:", e)
            return False, "حدث خطأ أثناء حذف التسجيل."
        
