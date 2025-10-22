from course_center_db import Payment, StudentMonthlyInvoice

class PaymentService:
    def __init__(self):
        pass
    
    def create_payment(student_id, amount_due, amount_paid, center_share, paid_type, payment_date, month, user_id):
        try:
            payment = Payment(
                student_id=student_id,
                amount=amount_paid,
                paid_type=paid_type,
                payment_date=payment_date,
                center_share=center_share,
                month=month,
                user_id=user_id
            )
            payment.save()
            
            studentpayment, created = StudentMonthlyInvoice.get_or_create(
            student_id=student_id,
            month=month,
            defaults={
                'total_due': amount_due,
                'total_paid': amount_paid,
                'remain': amount_due - amount_paid
            }
        )

            # إذا كان السجل موجود بالفعل، عدل القيم ثم احفظ
            if not created:                
                studentpayment.total_paid += amount_paid
                studentpayment.remain = studentpayment.total_due - studentpayment.total_paid
                studentpayment.save()

            return True, "عملية الدفع تمت بنجاح"
        except Exception as e:
            return False, f"خطأ في عملية الدفع  : {str(e)}"
    