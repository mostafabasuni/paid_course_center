def monthly_payments(year, month):
        from collections import defaultdict
        

        summaries = defaultdict(lambda: {'due': Decimal('0.00'), 'paid': Decimal('0.00')})

        # حساب المستحقات من جدول StudentCourse
        student_courses = StudentCourse.select().join(Course).where(
            (StudentCourse.reg_date.year <= year) &
            ((StudentCourse.reg_date.month <= month) | (StudentCourse.reg_date.year < year))
        )

        for sc in student_courses:
            summaries[sc.student.id]['due'] += sc.course.monthly_fee

        # حساب المدفوعات من جدول Payment
        payments = Payment.select().where(
            (Payment.payment_date.year == year) & (Payment.payment_date.month == month)
        )

        for payment in payments:
            summaries[payment.student.id]['paid'] += payment.amount

        # تحديث أو إنشاء سجل شهري
        for student_id, data in summaries.items():
            msp, created = MonthlyStudentPayment.get_or_create(
                student=student_id, year=year, month=month,
                defaults={
                    'total_due': data['due'],
                    'total_paid': data['paid'],
                    'is_paid': data['paid'] >= data['due']
                }
            )
            if not created:
                msp.total_due = data['due']
                msp.total_paid = data['paid']
                msp.is_paid = data['paid'] >= data['due']
                msp.save()