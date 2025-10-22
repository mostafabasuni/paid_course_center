from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QLineEdit, QToolButton
from peewee import fn
from peewee import DoesNotExist
import sys
import os
from decimal import Decimal
from datetime import datetime
from peewee import JOIN
from peewee import fn
import subprocess
import pymysql
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextDocument
from num2words import num2words   # لتحويل الأرقام إلى حروف
from PyQt5.QtWidgets import QLineEdit



from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPageLayout, QPageSize
from PyQt5.QtGui import QPageLayout, QPageSize

from course_center_db import User, Student, Teacher, Grade, Course, Enrollment, Payment, TeacherAccount, TeacherStudent,  StudentMonthlyInvoice, Attendance, Permission # استيراد الجداول من Peewee
from user_controller import UserManager  # استيراد وحدة التحكم للمستخدم
from grade_controller import GradeService  # استيراد وحدة التحكم للصفوف 
from teacher_controller import TeacherService  # استيراد وحدة التحكم للمدرسين
from course_controller import CourseService  # استيراد وحدة التحكم للمقررات
from student_controller import StudentService  # استيراد وحدة التحكم للطلاب
from enrollment_controller import EnrollmentService  # استيراد وحدة التحكم للتسجيل في المقررات
from payment_controller import PaymentService  # استيراد وحدة التحكم للمدفوعات
from attendance_controller import AttendanceService  # استيراد وحدة التحكم لسجل الغيات

# ⚡ إعدادات قاعدة البيانات ⚡
DB_NAME = "course_center"
DB_USER = "root"
DB_PASS = ""          # ضع كلمة مرور MySQL إن وجدت
DB_HOST = "localhost"
BACKUP_DIR = "course_center_archive_2025_1"  # مجلد النسخة الاحتياطية
TABLES_TO_CLEAR = ["Enrollment","Payment", "StudentMonthlyInvoice", "Attendance", "TeacherAccount", "TeacherStudent" ]  # الجداول التي سيتم تفريغها


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('paid_course_center.ui', self)  # تحميل ملف التصميم
        self.tabWidget.tabBar().setVisible(False)
        self.user_manager = UserManager()
        self.teacher_manager = TeacherService()  # إنشاء مثيل من خدمة المعلم
        self.student_manager = StudentService()  # إنشاء مثيل من خدمة الطالب
        self.enrollment_manager = EnrollmentService()  # إنشاء مثيل من خدمة التسجيل
        self.attendance_manager = AttendanceService()  # إنشاء مثيل من خدمة الغياب
        

        self.permission_checkboxes = [
        self.checkBox_15,  # user_tab
        self.checkBox_16,  # teacher_tab
        self.checkBox_17,  # grade_tab
        self.checkBox_18,  # course_tab
        self.checkBox_19,  # student_tab
        self.checkBox_20,  # enrollment_tab
        self.checkBox_21,  # student_account_tab
        self.checkBox_22,  # student_stat_tab
        self.checkBox_23,  # teacher_account_tab
        self.checkBox_24,  # attendance_tab
        self.checkBox_25,  # management_tab
        self.checkBox_26,  # permission_tab
        ]
        
        self.nav_buttons = [
        self.pushButton,
        self.pushButton_2,
        self.pushButton_3,
        self.pushButton_4,
        self.pushButton_5,
        self.pushButton_6,
        self.pushButton_7,
        self.pushButton_8,
        self.pushButton_9,
        self.pushButton_55, 
        self.pushButton_56,  
        self.pushButton_57,         
        ]
        
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit_2.setDate(QDate.currentDate())
        self.dateEdit_7.setDate(QDate.currentDate())        
        
        self.set_day_name()
        self.user_load()
        self.permission_apply()
        self.teacher_load()
        self.grade_load()
        self.course_load()
        self.student_load()
        self.user_combo_refresh()
        self.teacher_combo_refresh()
        self.student_combo_refresh()
        self.grade_combo_refresh()
        self.payment_type_combo_refresh()        
        #self.teacher_received_table()  # تحميل حسابات المدرسين عند بدء التطبيق              
        self.fill_months_combobox(self.comboBox_10, self.comboBox_21, self.comboBox_25, self.comboBox_26, self.comboBox_29, self.comboBox_30)
        self.absence_table_load()        
        self.password_setup()  # إعداد خاصية إظهار/إخفاء كلمة المرور
        
    
        
        self.tableWidget.itemClicked.connect(self.user_table_select)
        self.tableWidget_2.itemClicked.connect(self.teacher_table_select)
        self.tableWidget_3.itemClicked.connect(self.grade_table_select)
        self.tableWidget_4.itemClicked.connect(self.course_table_select)
        self.tableWidget_5.itemClicked.connect(self.student_table_select)
        self.tableWidget_13.itemClicked.connect(self.absence_table_select)
        
        
        self.pushButton.clicked.connect(self.user_tab_open) 
        self.pushButton_2.clicked.connect(self.teacher_tab_open)
        self.pushButton_3.clicked.connect(self.course_tab_open)        
        self.pushButton_4.clicked.connect(self.grade_tab_open)
        self.pushButton_5.clicked.connect(self.student_tab_open)
        self.pushButton_6.clicked.connect(self.course_enrollment_tab_open)
        self.pushButton_7.clicked.connect(self.student_account_tab_open)
        self.pushButton_8.clicked.connect(self.student_stat_tab_open)
        self.pushButton_9.clicked.connect(self.teacher_account_tab_open)
        self.pushButton_10.clicked.connect(self.permission_save)
        self.pushButton_11.clicked.connect(self.user_form_clear) 
        self.pushButton_12.clicked.connect(self.user_creation)
        self.pushButton_13.clicked.connect(self.user_update)
        self.pushButton_14.clicked.connect(self.user_delete)
        self.pushButton_15.clicked.connect(self.login)
        self.pushButton_16.clicked.connect(self.permission_toggle)
        self.pushButton_17.clicked.connect(self.teacher_form_clear)
        self.pushButton_18.clicked.connect(self.teacher_creation)
        self.pushButton_19.clicked.connect(self.teacher_update)
        self.pushButton_20.clicked.connect(self.teacher_delete)
        self.pushButton_22.clicked.connect(self.course_form_clear)
        self.pushButton_23.clicked.connect(self.course_creation)
        self.pushButton_24.clicked.connect(self.course_update)
        self.pushButton_25.clicked.connect(self.course_delete)        
        self.pushButton_27.clicked.connect(self.grade_form_clear)
        self.pushButton_28.clicked.connect(self.grade_creation)
        self.pushButton_29.clicked.connect(self.grade_update)
        self.pushButton_30.clicked.connect(self.grade_delete)
        self.pushButton_32.clicked.connect(self.student_search)
        self.pushButton_33.clicked.connect(self.student_form_clear)
        self.pushButton_34.clicked.connect(self.student_creation)
        self.pushButton_35.clicked.connect(self.student_update)
        self.pushButton_36.clicked.connect(self.student_delete)
        self.pushButton_37.clicked.connect(self.grade_search)
        self.pushButton_39.clicked.connect(self.course_enrollment_form_clear)
        self.pushButton_40.clicked.connect(self.course_enrollment)
        self.pushButton_41.clicked.connect(self.student_enrollment_display)
        self.pushButton_42.clicked.connect(self.course_enrollment_delete)
        self.pushButton_43.clicked.connect(self.payment_form_clear)
        self.pushButton_44.clicked.connect(self.monthly_payments)
        self.pushButton_45.clicked.connect(self.print_student_receipt)        
        self.pushButton_48.clicked.connect(self.teacher_received)        
        self.pushButton_49.clicked.connect(self.teacher_no_received)
        self.pushButton_49.setToolTip("مدرسين لم يستلموا مستحقاتهم")
        self.pushButton_50.clicked.connect(self.teacher_received_table)
        self.pushButton_50.setToolTip("مدرسين استلموا مستحقاتهم")
        self.pushButton_51.clicked.connect(self.student_paid_all_debt)
        self.pushButton_52.clicked.connect(self.student_no_paid)
        self.pushButton_53.clicked.connect(self.student_debt)
        self.pushButton_55.clicked.connect(self.attendance_tab_open)
        self.pushButton_56.clicked.connect(self.permission_tab_open)
        self.pushButton_57.clicked.connect(self.management_tab_open)
        self.pushButton_58.clicked.connect(self.update_withdrawn_student)
        self.pushButton_59.clicked.connect(self.attendance_form_clear)
        self.pushButton_60.clicked.connect(self.student_absence_add)
        self.pushButton_61.clicked.connect(self.absence_update)
        self.pushButton_62.clicked.connect(self.absence_delete)
        self.pushButton_63.clicked.connect(self.absence_search)
        self.pushButton_64.clicked.connect(self.management_form_clear)
        self.pushButton_65.clicked.connect(self.student_stat)
        self.pushButton_66.clicked.connect(self.total_income)
        self.pushButton_69.clicked.connect(self.logout)
        self.pushButton_70.clicked.connect(self.start_backup_and_clear)
        self.pushButton_71.clicked.connect(self.print_teacher_receipt)
        
        self.pushButton.clicked.connect(lambda: self.highlight_active_button(self.pushButton))
        self.pushButton_2.clicked.connect(lambda: self.highlight_active_button(self.pushButton_2))
        self.pushButton_3.clicked.connect(lambda: self.highlight_active_button(self.pushButton_3))
        self.pushButton_4.clicked.connect(lambda: self.highlight_active_button(self.pushButton_4))
        self.pushButton_5.clicked.connect(lambda: self.highlight_active_button(self.pushButton_5))
        self.pushButton_6.clicked.connect(lambda: self.highlight_active_button(self.pushButton_6))
        self.pushButton_7.clicked.connect(lambda: self.highlight_active_button(self.pushButton_7))
        self.pushButton_8.clicked.connect(lambda: self.highlight_active_button(self.pushButton_8))
        self.pushButton_9.clicked.connect(lambda: self.highlight_active_button(self.pushButton_9))
        self.pushButton_55.clicked.connect(lambda: self.highlight_active_button(self.pushButton_55))
        self.pushButton_56.clicked.connect(lambda: self.highlight_active_button(self.pushButton_56))
        self.pushButton_57.clicked.connect(lambda: self.highlight_active_button(self.pushButton_57))

        
        self.comboBox.activated.connect(self.permission_show)
        self.comboBox_5.activated.connect(self.linedit_23_refresh)
        self.comboBox_9.activated.connect(self.teacher_info)
        self.comboBox_15.activated.connect(self.refresh_student_info)
        self.comboBox_18.activated.connect(self.get_student_info)
        self.comboBox_19.activated.connect(self.course_info)
        self.comboBox_27.activated.connect(self.student_absence_info)
        self.comboBox_30.activated.connect(self.absence_table_load)        
        
        self.checkBox_2.stateChanged.connect(self.withdrawn_page_open)    
        self.dateEdit_7.dateChanged.connect(self.set_day_name)
    
    def set_day_name(self):
        # خريطة أيام الأسبوع من إنجليزي → عربي
        days_map = {
            "Saturday": "السبت",
            "Sunday": "الأحد",
            "Monday": "الاثنين",
            "Tuesday": "الثلاثاء",
            "Wednesday": "الأربعاء",
            "Thursday": "الخميس",
            "Friday": "الجمعة"
        }

        # نجيب التاريخ من dateEdit
        date = self.dateEdit_7.date()
        day_name_en = date.toString("dddd")
        day_name_ar = days_map.get(day_name_en, day_name_en)

        # نطبع اليوم داخل QLineEdit
        self.lineEdit_48.setText(day_name_ar)
    
    def password_setup(self):
        self.lineEdit_7.setEchoMode(QLineEdit.Password)
        # إنشاء زر العين (داخل حقل الباسورد)
        self.eye_button = QToolButton(self.lineEdit_7)
        self.eye_button.setText("👁️")  # أيقونة نصية بدون صور
        self.eye_button.setCursor(QtCore.Qt.PointingHandCursor)
        # ضبط موقع الزر داخل الـ QLineEdit
        frame_width = self.lineEdit_7.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        self.eye_button.setStyleSheet("border: none; padding: 0px;")
        button_size = self.eye_button.sizeHint()
        self.eye_button.setFixedSize(button_size)
        # تحريك الزر إلى الطرف الأيمن داخل الحقل
        self.lineEdit_7.setTextMargins(0, 0, button_size.width() + frame_width, 0)
        self.eye_button.move(self.lineEdit_7.rect().right() - button_size.width() - frame_width, (self.lineEdit_7.rect().height() - button_size.height()) // 2)
        # ربط الضغط على العين بوظيفة الإظهار/الإخفاء
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        # التأكد أن الزر يبقى في مكانه عند تغيير حجم النافذة
        self.lineEdit_7.textChanged.connect(self.adjust_eye_position)
    
    def adjust_eye_position(self):
        """تحديث موقع الزر عند تغيير حجم الحقل"""
        frame_width = self.lineEdit_7.style().pixelMetric(QtWidgets.QStyle.PM_DefaultFrameWidth)
        button_size = self.eye_button.sizeHint()
        self.eye_button.move(self.lineEdit_7.rect().right() - button_size.width() - frame_width,
                             (self.lineEdit_7.rect().height() - button_size.height()) // 2)

    def toggle_password_visibility(self):
        """تبديل إظهار/إخفاء كلمة المرور"""
        if self.lineEdit_7.echoMode() == QLineEdit.Password:
            self.lineEdit_7.setEchoMode(QLineEdit.Normal)
            self.eye_button.setText("🙈")
        else:
            self.lineEdit_7.setEchoMode(QLineEdit.Password)
            self.eye_button.setText("👁️")
    
    
            
    def login(self):
        self.groupBox.setEnabled(True)
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_9.setEnabled(False)
        self.pushButton_55.setEnabled(False)
        self.pushButton_56.setEnabled(False)
        self.pushButton_57.setEnabled(False)
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        if not all([username, password]):        
            QtWidgets.QMessageBox.warning(self, "بيانات ناقصة", "يرجى ملء جميع الحقول.")
            return
        success, result = self.user_manager.login(username, password)
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", f"مرحبًا {result.username}!")
            permissions = self.user_manager.get_permissions()
            for p in permissions:
                if p.user_tab:
                    self.pushButton.setEnabled(True)
                if p.teacher_tab:
                    self.pushButton_2.setEnabled(True)
                if p.grade_tab:                
                    self.pushButton_3.setEnabled(True)
                if p.course_tab:
                    self.pushButton_4.setEnabled(True)
                if p.student_tab:
                    self.pushButton_5.setEnabled(True)
                if p.enrollment_tab:
                    self.pushButton_6.setEnabled(True)
                if p.student_account_tab:
                    self.pushButton_7.setEnabled(True)
                if p.student_stat_tab:
                    self.pushButton_8.setEnabled(True)
                if p.teacher_account_tab:
                    self.pushButton_9.setEnabled(True)
                if p.attendance_tab:
                    self.pushButton_55.setEnabled(True)
                if p.management_tab:
                    self.pushButton_57.setEnabled(True)
                if p.permission_tab:
                    self.pushButton_56.setEnabled(True)
            # يمكنك هنا تفعيل التبويبات أو إظهار الصفحة التالية
            self.lineEdit.clear()
            self.lineEdit_2.clear()
        else:
            QtWidgets.QMessageBox.warning(self, "فشل", result)    
            
    def logout(self):
        self.user_manager.logged_user = None                
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_9.setEnabled(False)
        self.pushButton_55.setEnabled(False)
        self.pushButton_56.setEnabled(False)
        self.pushButton_57.setEnabled(False)        
        self.groupBox.setEnabled(False)
        self.highlight_active_button(None)
        self.tabWidget.setCurrentIndex(0)  # العودة إلى صفحة تسجيل الدخول        
        
    # ===================== User =========================
    def user_tab_open(self):
        self.tabWidget.setCurrentIndex(1)
        
    def user_creation(self):
        fullname = self.lineEdit_4.text().strip()
        username = self.lineEdit_6.text().strip()
        password = self.lineEdit_7.text().strip()
        job = self.lineEdit_5.text().strip()
        phone = self.lineEdit_8.text().strip()
        is_admin = self.checkBox.isChecked()
        if not all([fullname, username, password, job, phone]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        success, message = UserManager.create_user(fullname, username, password, job, phone, is_admin)
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", message)
            self.user_form_clear()  # مسح النموذج
            self.user_load()  # إعادة تحميل المستخدمين بعد الإضافة
        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)

    def user_update(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار مستخدم من الجدول")
            return
        user_id = int(self.tableWidget.item(selected_row, 0).text())
        fullname = self.lineEdit_4.text().strip()
        job = self.lineEdit_5.text().strip()
        username = self.lineEdit_6.text().strip()
        password = self.lineEdit_7.text().strip()
        phone = self.lineEdit_8.text().strip()
        is_admin = self.checkBox.isChecked()
        if not all([fullname, username, job, phone]):
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار مستخدم من الجدول.")
            return
        reply = QtWidgets.QMessageBox.question(
        self,
        "تأكيد تحديث بيانات",
        "هل أنت متأكد من تحديث بيانات هذا المستخدم؟",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)    
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = self.user_manager.update_user(user_id, fullname, job, username, password, phone, is_admin)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.user_form_clear()
                self.user_load()
            else:
                QtWidgets.QMessageBox.critical(self, "خطأ", message)
    
    def user_combo_refresh(self):
        self.comboBox.clear()
        self.comboBox.addItem("اختر مستخدم")
        for user in User.select():
            self.comboBox.addItem(user.fullname)
            
            
        
    def user_delete(self):
        if self.lineEdit_4.text() == "":
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار مستخدم من الجدول.")
            return
        selected_row = self.tableWidget.currentRow()        
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار مستخدم من الجدول")
            return
        user_id = int(self.tableWidget.item(selected_row, 0).text())
        reply = QtWidgets.QMessageBox.question(
        self,
        "تأكيد الحذف",
        "هل أنت متأكد من حذف هذا المستخدم؟",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)    
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = self.user_manager.delete_user(user_id)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.user_load()
                self.user_form_clear()
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", message)            
    
    def user_load(self):
        self.tableWidget.setRowCount(0)
        for row_index, user in enumerate(User.select()):
            self.tableWidget.insertRow(row_index)
            self.tableWidget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(user.id)))
            self.tableWidget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(user.fullname))
            self.tableWidget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(user.job)))
            self.tableWidget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(user.phone))
            self.tableWidget.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(user.username)))
            self.tableWidget.setItem(row_index, 5, QtWidgets.QTableWidgetItem("نعم" if user.is_admin else "لا"))
            self.tableWidget.setItem(row_index, 6, QtWidgets.QTableWidgetItem(user.created_at.strftime("%Y-%m-%d")))
        self.tableWidget.resizeColumnsToContents()
        
    def user_table_select(self):        
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار مستخدم من الجدول")
            return

        user_id = int(self.tableWidget.item(selected_row, 0).text())
        user = User.get_by_id(user_id)
        self.lineEdit_3.setText(str(user.id))
        self.lineEdit_4.setText(user.fullname)        
        self.lineEdit_5.setText(user.job)
        self.lineEdit_8.setText(user.phone)
        self.lineEdit_6.setText(user.username)
        self.checkBox.setChecked(user.is_admin)
        self.dateEdit.setDate(QDate.fromString(user.created_at.strftime("%Y-%m-%d"), "yyyy-MM-dd"))        
    
    def user_form_clear(self):
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.checkBox.setChecked(False)
        self.tableWidget.clearSelection() # مسح التحديد في الجدول        
    # ===================== End User =========================        
    # ===================== teacher ==========================        
    def teacher_tab_open(self):
        self.tabWidget.setCurrentIndex(2)
    
    def teacher_creation(self):
        name = self.lineEdit_9.text().strip()
        phone = self.lineEdit_10.text().strip()
        specialization = self.lineEdit_11.text().strip()
        share_percent = self.lineEdit_13.text().strip()        
        if not all([name, phone, specialization, share_percent]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        success, message = TeacherService.create_teacher(name, phone, specialization, share_percent)
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", message)
            self.teacher_form_clear()  # مسح النموذج
            self.teacher_load()  # إعادة تحميل المستخدمين بعد الإضافة
        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)

    def teacher_update(self):
        selected_row = self.tableWidget_2.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار معلم من الجدول")
            return

        teacher_id = int(self.tableWidget_2.item(selected_row, 0).text())
        name = self.lineEdit_9.text().strip()
        phone = self.lineEdit_10.text().strip()
        specialization = self.lineEdit_11.text().strip()
        share_percent = self.lineEdit_13.text().strip()
        if not all([name, phone, specialization, share_percent]):
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار معلم من الجدول.")
            return
        reply = QtWidgets.QMessageBox.question(
        self,
        "تأكيد تحديث بيانات",
        "هل أنت متأكد من تحديث بيانات هذا المعلم؟",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)    
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = self.teacher_manager.update_teacher(teacher_id, name, phone, specialization, share_percent)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.teacher_load()
            else:
                QtWidgets.QMessageBox.critical(self, "خطأ", message)
        
        
    def teacher_delete(self):
        if self.lineEdit_9.text() == "":
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار معلم من الجدول.")
            return
        selected_row = self.tableWidget_2.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار معلم من الجدول")
            return

        teacher_id = int(self.tableWidget_2.item(selected_row, 0).text())
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد الحذف",
            "هل أنت متأكد من حذف هذا المعلم؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = self.teacher_manager.delete_teacher(teacher_id)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.teacher_load()
                self.teacher_form_clear()
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", message)            
    
    def teacher_load(self):
        self.tableWidget_2.setRowCount(0)
        for row_index, teacher in enumerate(Teacher.select()):
            self.tableWidget_2.insertRow(row_index)
            self.tableWidget_2.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(teacher.id)))
            self.tableWidget_2.setItem(row_index, 1, QtWidgets.QTableWidgetItem(teacher.name))
            self.tableWidget_2.setItem(row_index, 2, QtWidgets.QTableWidgetItem(teacher.phone))
            self.tableWidget_2.setItem(row_index, 3, QtWidgets.QTableWidgetItem(teacher.specialization))
            self.tableWidget_2.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(teacher.share_percent) + " %"))
            t = TeacherAccount.get_or_none(TeacherAccount.teacher_id == teacher.id)
            if t:
                self.tableWidget_2.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(t.student_count)))
                self.tableWidget_2.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(t.income)))
            else:
                self.tableWidget_2.setItem(row_index, 5, QtWidgets.QTableWidgetItem("0"))
                self.tableWidget_2.setItem(row_index, 6, QtWidgets.QTableWidgetItem("0"))
                
        self.tableWidget_2.resizeColumnsToContents()
        
    def teacher_table_select(self):
        selected_row = int(self.tableWidget_2.currentRow())        
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار معلم من الجدول")
            return

        teacher_id = int(self.tableWidget_2.item(selected_row, 0).text())        
        try:
            teacher = Teacher.get_by_id(teacher_id)
            t_account = TeacherAccount.get_or_none(TeacherAccount.teacher_id == teacher.id)
            self.lineEdit_9.setText(teacher.name)
            self.lineEdit_10.setText(teacher.phone)
            self.lineEdit_11.setText(teacher.specialization)
            self.lineEdit_13.setText(str(teacher.share_percent) + " %")
            if t_account:
                self.lineEdit_14.setText(str(t_account.student_count))
                self.lineEdit_15.setText(str(t_account.income))
            else:
                self.lineEdit_14.setText("0")
                self.lineEdit_15.setText("0.00")
        except DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "المعلم غير موجود")
    
    def teacher_form_clear(self):
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()
        self.lineEdit_11.clear()
        self.lineEdit_13.clear()
        self.lineEdit_14.clear()
        self.lineEdit_15.clear()
        self.tableWidget_2.clearSelection() # مسح التحديد في الجدول
    
    def teacher_account_tab_open(self):
        self.tabWidget.setCurrentIndex(9)
        self.stackedWidget.setCurrentIndex(0)
    
    
    def teacher_info(self):
        teacher_name = self.comboBox_9.currentText()
        month = self.comboBox_10.currentText()
        if not all([teacher_name, month]):
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار المعلم والشهر.")
            return
        
        try:
            teacher = Teacher.get(Teacher.name == teacher_name)                
            teacher_id = teacher.id
            self.lineEdit_37.setText(teacher.phone)
            self.lineEdit_16.setText(teacher.specialization)
            self.lineEdit_40.setText(str(teacher.share_percent) + " %")
            #self.lineEdit_41.setText(str(teacher.student_count))
            #self.lineEdit_42.setText(str(teacher.income))
            self.dateEdit_5.setDate(QDate.currentDate())
            
        except DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "المعلم غير موجود")
        self.teacher_student_count(teacher_id, month)
        self.teacher_student_name(teacher_id, month)

    def teacher_student_count(self, teacher_id, month):
        
        try:
            # استعلام Peewee مع join و ORDER BY
            query = (
                Enrollment
                .select(
                    Grade.level,
                    Grade.name,
                    fn.COUNT(Enrollment.id).alias('student_count'),
                    fn.SUM(Enrollment.course_price).alias('total_price')
                )
                .join(Grade, on=(Enrollment.grade_id == Grade.id))
                .where(
                    (Enrollment.teacher_id == teacher_id) & 
                    (Enrollment.month == month)
                )
                .group_by(Grade.level, Grade.name)
                .order_by(Grade.level, Grade.name)
            )
            if not query:
                self.tableWidget_11.setRowCount(0)
                self.lineEdit_41.setText("0")
                self.lineEdit_42.setText("0")
                return
            else:
                total_student = 0  # متغير لتجميع عدد الطلاب
                total_income = 0
                teacher = Teacher.get_by_id(teacher_id)
                self.tableWidget_11.setRowCount(0)
                for i, row in enumerate(query):
                    g = row.grade_id            # هذا كائن Grade
                    self.tableWidget_11.insertRow(i)
                    self.tableWidget_11.setItem(i, 0, QtWidgets.QTableWidgetItem(str(g.level)))
                    self.tableWidget_11.setItem(i, 1, QtWidgets.QTableWidgetItem(str(g.name)))
                    self.tableWidget_11.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row.student_count)))
                    total_student += row.student_count  # نجمع                    
                    if row.total_price:  # نتأكد أن القيمة ليست None
                        total_income += row.total_price

                # حساب حصيلة المدرس بناءً على نسبته
                teacher_income = (teacher.share_percent / 100) * total_income

                # إضافة صف المجموع الكلي
                summary_row = self.tableWidget_11.rowCount()
                self.tableWidget_11.insertRow(summary_row)
                self.tableWidget_11.setItem(summary_row, 0, QtWidgets.QTableWidgetItem("إجمالي"))
                self.tableWidget_11.setItem(summary_row, 1, QtWidgets.QTableWidgetItem(""))
                self.tableWidget_11.setItem(summary_row, 2, QtWidgets.QTableWidgetItem(str(total_student)))
                self.tableWidget_11.resizeColumnsToContents()
                self.lineEdit_41.setText(str(total_student))  # عدد الطلاب الكلي
                self.lineEdit_42.setText(str(round(teacher_income, 2)))  # حصيلة المدرس
                
        except Teacher.DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "المعلم غير موجود")

    def teacher_received(self):
        self.stackedWidget.setCurrentIndex(0)
        user_id = self.user_manager.get_logged_user_id()
        teacher_name = self.comboBox_9.currentText()
        income = self.lineEdit_42.text().strip()
        month = self.comboBox_10.currentText().strip()
        student_count = self.lineEdit_41.text().strip()
        date = self.dateEdit_5.date().toPyDate()
        if not all([income, month, student_count]):
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول وخاصة تحديد الشهر.")
            return
        
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد استلام المستحفات",
            "هل أنت متأكد من تسليم المعلم مستحقاته لهذا الشهر؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
        
            try:
                teacher = Teacher.get(Teacher.name == teacher_name)
                
                success, message = self.teacher_manager.update_teacher_account(teacher.id, month, date, user_id)
                if success:
                    QtWidgets.QMessageBox.information(self, "نجاح", message)
                    self.teacher_received_table()
                    #self.teacher_load()  # إعادة تحميل المعلمين بعد الإضافة
                else:
                    QtWidgets.QMessageBox.critical(self, "خطأ", message)
            except DoesNotExist:
                QtWidgets.QMessageBox.warning(self, "خطأ", "المعلم غير موجود")
        
    
    def teacher_no_received(self):
        self.stackedWidget.setCurrentIndex(1)
        month = self.comboBox_10.currentText().strip()
        if not month:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر.")
            return
        query = TeacherAccount.select().where (            
            (TeacherAccount.month == month) 
            & (TeacherAccount.status == False))
        
        self.tableWidget_10.setRowCount(0)  # مسح الجدول قبل التحميل
        for row_index, teacher in enumerate(query):
            t = Teacher.get(id=teacher.teacher_id)
            self.tableWidget_10.insertRow(row_index)
            self.tableWidget_10.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(t.id)))
            self.tableWidget_10.setItem(row_index, 1, QtWidgets.QTableWidgetItem(t.name))
            self.tableWidget_10.setItem(row_index, 2, QtWidgets.QTableWidgetItem(t.phone))
            self.tableWidget_10.setItem(row_index, 3, QtWidgets.QTableWidgetItem(t.specialization))
            self.tableWidget_10.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(t.share_percent) + " %"))
            self.tableWidget_10.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(teacher.student_count)))
            self.tableWidget_10.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(teacher.income)))
            self.tableWidget_10.setItem(row_index, 7, QtWidgets.QTableWidgetItem(month))
            self.tableWidget_10.setItem(row_index, 8, QtWidgets.QTableWidgetItem("لا"))
        self.tableWidget_10.resizeColumnsToContents()  # ضبط عرض الأعمدة تلقائيًا
        
    

    def teacher_student_name(self, teacher_id, month):
        self.stackedWidget.setCurrentIndex(2)

        try:
            query = (
                Enrollment
                .select(Enrollment, Student, Grade)
                .join(Student, on=(Enrollment.student_id == Student.id))
                .switch(Enrollment)
                .join(Grade, on=(Enrollment.grade_id == Grade.id))
                .where(
                    (Enrollment.teacher_id == teacher_id) &
                    (Enrollment.month == month)
                )
                .order_by(Grade.level, Grade.name, Student.name)
            )

            # تفريغ الجدول دائمًا قبل الملء
            self.tableWidget_12.setRowCount(0)

            if query.count() == 0:
                QtWidgets.QMessageBox.warning(self, "تنبيه", "لا يوجد طلاب مسجلين لهذا المعلم في هذا الشهر.")
                return
            
            # جلب بيانات المدرس لمعرفة النسبة
            teacher = Teacher.get_by_id(teacher_id)
            
            for i, row in enumerate(query):
                st = row.student_id   # كائن Student
                gr = row.grade_id     # كائن Grade
                # حساب نصيب المدرس من هذا الطالب
                teacher_share = row.course_price * (teacher.share_percent / 100)
                self.tableWidget_12.insertRow(i)
                # عدل ترتيب الأعمدة حسب تصميم جدولك
                self.tableWidget_12.setItem(i, 0, QtWidgets.QTableWidgetItem(str(st.id)))
                self.tableWidget_12.setItem(i, 1, QtWidgets.QTableWidgetItem(st.name))
                self.tableWidget_12.setItem(i, 2, QtWidgets.QTableWidgetItem(st.phone or ""))
                self.tableWidget_12.setItem(i, 3, QtWidgets.QTableWidgetItem(gr.level))
                self.tableWidget_12.setItem(i, 4, QtWidgets.QTableWidgetItem(gr.name))
                self.tableWidget_12.setItem(i, 5, QtWidgets.QTableWidgetItem(str(row.course_price)))   # سعر الكورس للطالب
                self.tableWidget_12.setItem(i, 6, QtWidgets.QTableWidgetItem(str(round(teacher_share, 2))))  # نصيب المدرس
                
            self.tableWidget_12.resizeColumnsToContents()

        except Teacher.DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "المعلم غير موجود")                     
                    
    
    def teacher_received_table(self):
        self.stackedWidget.setCurrentIndex(0)
        month = self.comboBox_10.currentText().strip()
        if not month:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر.")
            return
        t_accounts = TeacherAccount.select().where((TeacherAccount.month == month) & (TeacherAccount.status == True)).order_by(TeacherAccount.date.desc())
        self.tableWidget_8.setRowCount(0)
        
        for row_index, account in enumerate(t_accounts):
            self.tableWidget_8.insertRow(row_index)
            self.tableWidget_8.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(account.id)))
            self.tableWidget_8.setItem(row_index, 1, QtWidgets.QTableWidgetItem(Teacher.get(Teacher.id == account.teacher_id).name))
            self.tableWidget_8.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(account.student_count)))
            self.tableWidget_8.setItem(row_index, 3, QtWidgets.QTableWidgetItem(str(account.income)))
            self.tableWidget_8.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(account.month)))            
            item = QtWidgets.QTableWidgetItem("نعم") if account.status == True else QtWidgets.QTableWidgetItem("لا")
            self.tableWidget_8.setItem(row_index, 5, QtWidgets.QTableWidgetItem(item.text()))
            self.tableWidget_8.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(account.date)))
            self.tableWidget_8.setItem(row_index, 7, QtWidgets.QTableWidgetItem(str(User.get(User.id == account.user_id).fullname)))
        self.tableWidget_8.resizeColumnsToContents()  # ضبط عرض الأعمدة تلقائيًا
        
            
    # ===================== End teacher =========================
    
    # ===================== Grade =========================
    def grade_tab_open(self):
        self.tabWidget.setCurrentIndex(3)
    
    def grade_creation(self):
        name = self.lineEdit_21.text().strip()        
        level = self.lineEdit_20.text().strip()
        term = self.lineEdit_19.text().strip()
        academic_year = self.lineEdit_18.text().strip()
        
        
        if not all([name, level, term, academic_year]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        
        success, message = GradeService.create_grade(self, name, level, term, academic_year)
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", message)
            self.grade_form_clear()    
            self.grade_load()  # إعادة تحميل  الصفوف بعد الإضافة
            self.grade_combo_refresh()
        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)
            
    def grade_update(self):
        selected_row = self.tableWidget_3.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار صف من الجدول")
            return

        grade_id = int(self.tableWidget_3.item(selected_row, 0).text())
        name = self.lineEdit_21.text().strip()
        level = self.lineEdit_20.text().strip()
        term = self.lineEdit_19.text().strip()
        academic_year = self.lineEdit_18.text().strip()        
        if not all([name, level, term, academic_year]):
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار صف من الجدول.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد تحديث بيانات",
            "هل أنت متأكد من تحديث بيانات هذا الصف ؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = GradeService.update_grade(self, grade_id, name, level, term, academic_year)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.grade_load()
            else:
                QtWidgets.QMessageBox.critical(self, "خطأ", message)
    
    def grade_delete(self):
        selected_row = self.tableWidget_3.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار صف من الجدول")
            return
        if self.lineEdit_21.text() == "":
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار صف من الجدول.")
            return
        grade_id = int(self.tableWidget_3.item(selected_row, 0).text())
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد الحذف",
            "هل أنت متأكد من حذف هذا الصف ؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = GradeService.delete_grade(self, grade_id)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.grade_load()
                self.grade_form_clear()
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", message)
    
    def grade_search(self):
        grade = self.comboBox_11.currentText().strip()
        level = self.comboBox_12.currentText().strip()
        section = self.spinBox_3.value()
        if not all([grade, level, section]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        grade_id = Grade.select().where(
            (Grade.name == grade) 
            & (Grade.level == level)).get().id if grade and level else None
        grade = Student.select().where((Student.grade_id == grade_id) & (Student.section == section)) 
        self.tableWidget_5.setRowCount(0)
        for row_index, student in enumerate(grade):
            self.tableWidget_5.insertRow(row_index)
            self.tableWidget_5.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(student.id)))
            self.tableWidget_5.setItem(row_index, 1, QtWidgets.QTableWidgetItem(student.name))
            self.tableWidget_5.setItem(row_index, 2, QtWidgets.QTableWidgetItem(student.phone or ""))
            g = Grade.get_by_id(student.grade_id)
            self.tableWidget_5.setItem(row_index, 3, QtWidgets.QTableWidgetItem(g.name))
            self.tableWidget_5.setItem(row_index, 4, QtWidgets.QTableWidgetItem(g.level))
            self.tableWidget_5.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(student.section)))
            self.tableWidget_5.setItem(row_index, 6, QtWidgets.QTableWidgetItem(student.reg_date.strftime("%Y-%m-%d")))            
        self.tableWidget_5.resizeColumnsToContents()
            

    def grade_load(self):
        self.tableWidget_3.setRowCount(0)
        for row_index, grade in enumerate(Grade.select()):            
            self.tableWidget_3.insertRow(row_index)
            self.tableWidget_3.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(grade.id)))
            self.tableWidget_3.setItem(row_index, 1, QtWidgets.QTableWidgetItem(grade.academic_year))
            self.tableWidget_3.setItem(row_index, 2, QtWidgets.QTableWidgetItem(grade.term))
            self.tableWidget_3.setItem(row_index, 3, QtWidgets.QTableWidgetItem(grade.level))
            self.tableWidget_3.setItem(row_index, 4, QtWidgets.QTableWidgetItem(grade.name))
        self.tableWidget_3.resizeColumnsToContents()
    
    def grade_table_select(self):
        selected_row = self.tableWidget_3.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار درجة من الجدول")
            return

        grade_id = int(self.tableWidget_3.item(selected_row, 0).text())
        try:
            grade = Grade.get_by_id(grade_id)
            self.lineEdit_21.setText(grade.name)
            self.lineEdit_20.setText(grade.level)
            self.lineEdit_19.setText(str(grade.term))
            self.lineEdit_18.setText(grade.academic_year)            
        except DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "الدرجة غير موجودة")
            
    def grade_form_clear(self):
        self.lineEdit_21.clear()
        self.lineEdit_20.clear()
        self.lineEdit_19.clear()
        self.lineEdit_18.clear()
        self.tableWidget_3.clearSelection() # مسح التحديد في الجدول
        

# ===================== End Grade =========================
# ===================== Course =========================
    def course_tab_open(self):
        self.tabWidget.setCurrentIndex(4)
    
    def course_creation(self):
        course_name = self.lineEdit_17.text().strip()
        price = self.lineEdit_24.text().strip()
        teacher = self.comboBox_5.currentText().strip()
        grade = self.comboBox_4.currentText().strip()
        level = self.comboBox_3.currentText().strip()
        term = self.comboBox_2.currentText().strip() 
        
        if not all([course_name, price, teacher, grade, level, term]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return      
        
        price = Decimal(price) if price else Decimal('0.00')  # تحويل السعر إلى Decimal
        grade_id = Grade.select().where(
            (Grade.name == grade) & 
            (Grade.level == level) & 
            (Grade.term == term)            
        ).first().id if grade and level and term else None        
        teacher_id = Teacher.select().where(Teacher.name == teacher).first().id if teacher else None        
        success, message = CourseService.create_course(course_name, grade_id, teacher_id, price)
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", message)
            self.course_form_clear()
            self.course_load()  # إعادة تحميل المقررات بعد الإضافة
            self.grade_combo_refresh()  # تحديث الـ Comboboxes بعد الإضافة
        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)

    def course_update(self):
        selected_row = self.tableWidget_4.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار مقرر من الجدول")
            return
        course_id = int(self.tableWidget_4.item(selected_row, 0).text())
        course_name = self.lineEdit_17.text().strip()
        price = self.lineEdit_24.text().strip()
        teacher = self.comboBox_5.currentText().strip()
        grade = self.comboBox_4.currentText().strip()
        level = self.comboBox_3.currentText().strip()
        term = self.comboBox_2.currentText().strip()
        if not all([course_name, price, teacher, grade, level, term]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار مقرر من الجدول.")
            return
        price = Decimal(price) if price else Decimal('0.00')  # تحويل السعر إلى Decimal
        grade_id = Grade.select().where(
            (Grade.name == grade) & 
            (Grade.level == level) & 
            (Grade.term == term)            
        ).first().id if grade and level and term else None        
        teacher_id = Teacher.select().where(Teacher.name == teacher).first().id if teacher else None
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد تحديث بيانات",
            "هل أنت متأكد من تحديث بيانات هذه المادة ؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = CourseService.update_course(course_id, course_name, grade_id, teacher_id, price)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.course_load()
            else:
                QtWidgets.QMessageBox.critical(self, "خطأ", message)
                
        
    def course_delete(self):
        if self.lineEdit_17.text() == "" and self.lineEdit_24.text() == "":
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار مقرر من الجدول.")
            return
        selected_row = self.tableWidget_4.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار مقرر من الجدول")
            return
        course_id = int(self.tableWidget_4.item(selected_row, 0).text())
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد الحذف",
            "هل أنت متأكد من حذف هذا المقرر ؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = CourseService.delete_course(course_id)       
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.course_load()
                self.course_form_clear()    
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", message)
            
        
        
    
    def course_load(self):        
        self.tableWidget_4.setRowCount(0)
        for row_index, course in enumerate(Course.select()):
            self.tableWidget_4.insertRow(row_index)
            grade = Grade.get_by_id(course.grade_id) if course.grade_id else None
            teacher = Teacher.get_by_id(course.teacher_id) if course.teacher_id else None
            self.tableWidget_4.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(course.id)))
            self.tableWidget_4.setItem(row_index, 1, QtWidgets.QTableWidgetItem(course.name))
            self.tableWidget_4.setItem(row_index, 2, QtWidgets.QTableWidgetItem(grade.term if grade else ""))
            self.tableWidget_4.setItem(row_index, 3, QtWidgets.QTableWidgetItem(grade.level if grade else ""))
            self.tableWidget_4.setItem(row_index, 4, QtWidgets.QTableWidgetItem(grade.name if grade else ""))            
            self.tableWidget_4.setItem(row_index, 5, QtWidgets.QTableWidgetItem(teacher.name if teacher else ""))
            self.tableWidget_4.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(course.price)))
        self.tableWidget_4.resizeColumnsToContents()
        
    def course_table_select(self):
        selected_row = self.tableWidget_4.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار مقرر من الجدول")
            return
        course_id = int(self.tableWidget_4.item(selected_row, 0).text())
        try:
            course = Course.get_by_id(course_id)
            self.lineEdit_17.setText(course.name)
            self.lineEdit_24.setText(str(course.price))
            grade = Grade.get_by_id(course.grade_id) if course.grade_id else None
            teacher = Teacher.get_by_id(course.teacher_id) if course.teacher_id else None  
            if grade:
                self.comboBox_4.setCurrentText(grade.name)
                self.comboBox_3.setCurrentText(grade.level)
                self.comboBox_2.setCurrentText(grade.term)
            else:
                self.comboBox_4.setCurrentIndex(-1)
                self.comboBox_3.setCurrentIndex(-1)
                self.comboBox_2.setCurrentIndex(-1)
            if teacher:
                self.comboBox_5.setCurrentText(teacher.name)
                self.lineEdit_23.setText(teacher.specialization)
            else:
                self.comboBox_5.setCurrentIndex(-1)
        except DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "المقرر غير موجود")
            
    
    def course_form_clear(self):
        self.lineEdit_17.clear()
        self.lineEdit_24.clear()
        self.comboBox_5.setCurrentIndex(-1)
        self.comboBox_4.setCurrentIndex(-1)
        self.comboBox_3.setCurrentIndex(-1)
        self.comboBox_2.setCurrentIndex(-1)
        self.tableWidget_4.clearSelection() # مسح التحديد في الجدول
    
    def course_info(self):
        teacher_name = self.comboBox_19.currentText().strip()
        teacher = Teacher.select().where(Teacher.name == teacher_name).first() if teacher_name else None
        if teacher:
            teacher_id = teacher.id
            self.lineEdit_32.setText(str(teacher.specialization))
            course = Course.select().where(Course.teacher_id == teacher_id).first()
            if course:
                self.lineEdit_33.setText(str(course.name))
                self.lineEdit_31.setText(str(course.price))
            
        else:
            self.lineEdit_32.clear()
            self.lineEdit_33.clear()
            self.lineEdit_31.clear()
        
    def withdrawn_page_open(self):
        self.stackedWidget_3.setCurrentIndex(1)
        student_name = self.comboBox_15.currentText().strip()
        month = self.comboBox_26.currentText().strip()
        if not all([student_name, month]):
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار الطالب والشهر")
            return
        
        student = Student.select().where(Student.name == student_name).first()
        if not student:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "الطالب غير موجود.")
            return
        enrollments = Enrollment.select().where((Enrollment.student_id == student.id) &( Enrollment.month == month))

        if enrollments.count() == 0:
            QtWidgets.QMessageBox.warning(self, "تنبيه", f"لا توجد تسجيلات للطالب : {student.name} في شهر {month}.")
            self.tableWidget_17.setRowCount(0)
            self.lineEdit_38.clear()
            return        

        self.tableWidget_17.setRowCount(0)        
        for row_index, enrollment in enumerate(enrollments):
            course = enrollment.course_id
            teacher = course.teacher_id  # بافتراض أن جدول Course يحتوي على حقل teacher            
            
            self.tableWidget_17.insertRow(row_index)
            self.tableWidget_17.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(enrollment.id)))
            self.tableWidget_17.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(student.id)))
            self.tableWidget_17.setItem(row_index, 2, QtWidgets.QTableWidgetItem(course.name))
            self.tableWidget_17.setItem(row_index, 3, QtWidgets.QTableWidgetItem(teacher.name))
            self.tableWidget_17.setItem(row_index, 4, QtWidgets.QTableWidgetItem(''))           
        self.tableWidget_17.resizeColumnsToContents()        

    
    def update_withdrawn_student(self):
        try:
            # تحقق أن المستخدم اختار الطالب وأن الجدول فيه بيانات
            if self.tableWidget_17.rowCount() == 0:
                QtWidgets.QMessageBox.warning(self, "خطأ", "لا توجد بيانات لتحديثها.")
                return

            # تحقق من حالة checkbox
            is_withdrawn = self.checkBox_2.isChecked()
            total_due = 0
            center_share = 0

            for row in range(self.tableWidget_17.rowCount()):
                enrollment_id_item = self.tableWidget_17.item(row, 0)
                attendance_item = self.tableWidget_17.item(row, 4)

                if not enrollment_id_item or not attendance_item:
                    continue

                enrollment_id = int(enrollment_id_item.text())
                attendance_count = int(attendance_item.text())

                # جلب السجل من قاعدة البيانات
                enrollment = Enrollment.get_by_id(enrollment_id)
                center_share = enrollment.center_share or Decimal('0.00')
                # تحديث عدد الحصص
                enrollment.attendance_count = attendance_count
                month = enrollment.month
                # تحديث حالة الانسحاب
                if is_withdrawn:
                    enrollment.withdrawn = True

                # حساب السعر الفعلي (بناءً على عدد الحصص/إجمالي الحصص 8 مثلاً)
                per_class_price = enrollment.course_id.price / 8
                new_price = per_class_price * attendance_count
                total_due += new_price
                enrollment.course_price = new_price
                enrollment.center_share = center_share * Decimal(attendance_count / 8)  # نفترض أن المركز يأخذ 8%
                center_share += enrollment.center_share
                enrollment.save()

                # تحديث فاتورة المدرس
                teacher_id = enrollment.teacher_id
                teacher = Teacher.get_by_id(teacher_id) if teacher_id else None
                t_account, created = TeacherAccount.get_or_create(
                teacher_id=teacher.id,
                month=month)
                if not created:
                    absence_fee = 8 - attendance_count
                    teacher_deduction = absence_fee * per_class_price * (teacher.share_percent / 100) if teacher else 0
                    t_account.income -= teacher_deduction
                    t_account.save()
                
                # تحديث فاتورة الطالب
                invoice, created = StudentMonthlyInvoice.get_or_create(
                    student_id=enrollment.student_id.id,
                    month=enrollment.month,
                    defaults={
                        'total_due': new_price,
                        'total_paid': 0,
                        'remain': new_price
                    }
                )

                if not created:
                    # نعيد حساب المستحق حسب جميع تسجيلاته لهذا الشهر
                    total_due = (
                        Enrollment
                        .select(fn.SUM(Enrollment.course_price))
                        .where(
                            (Enrollment.student_id == enrollment.student_id) &
                            (Enrollment.month == enrollment.month)
                        )
                        .scalar()
                    ) or 0

                    invoice.total_due = total_due
                    invoice.remain = total_due - invoice.total_paid
                    invoice.save()
            payment = Payment.select().where(
                (Payment.student_id == enrollment.student_id) & (Payment.month == enrollment.month)).first()
            if payment:
                paid_amount = payment.amount                
                if paid_amount > total_due:
                    cash_back = paid_amount - total_due
                    payment.cash_back = cash_back
                payment.amount = total_due              
                payment.center_share = center_share
                payment.save()
            # تحديث الحقل في الواجهة
            self.lineEdit_38.setText(str(total_due))
            QtWidgets.QMessageBox.information(self, "نجاح", "تم تحديث حساب الطالب بنجاح.")
            self.checkBox_2.setChecked(False)  # إعادة تعيين حالة checkbox

        except Exception as e:
            print("Error:", e)
            QtWidgets.QMessageBox.critical(self, "خطأ", f"حدث خطأ: {e}")

            
        
# ===================== End Course =========================
# ===================== Student =========================
    def student_tab_open(self):
        self.tabWidget.setCurrentIndex(5)
        self.pushButton_35.setEnabled(False)
        self.pushButton_36.setEnabled(False)
    
    def student_creation(self):
        name = self.lineEdit_25.text().strip()
        phone = self.lineEdit_26.text().strip()
        grade = self.comboBox_11.currentText().strip()
        level = self.comboBox_12.currentText().strip()
        section = self.spinBox_3.value()
        reg_date = self.dateEdit_2.date().toPyDate()
        
        if not all([name, phone, grade, level, section, reg_date]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        grade_id = Grade.select().where(
            (Grade.name == grade) & 
            (Grade.level == level)            
        ).first().id if grade and level else None        
        success, message = self.student_manager.create_student(name, phone, grade_id, section, reg_date)    
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", message)
            self.student_form_clear()
            self.student_load()  # إعادة تحميل الطلاب بعد الإضافة
            self.student_combo_refresh()
        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)
            
    def student_update(self):
        selected_row = self.tableWidget_5.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار طالب من الجدول")
            return 
        student_id = int(self.tableWidget_5.item(selected_row, 0).text())
        name = self.lineEdit_25.text().strip()
        phone = self.lineEdit_26.text().strip()
        grade = self.comboBox_11.currentText().strip()
        level = self.comboBox_12.currentText().strip()
        section = self.spinBox_3.value()
        reg_date = self.dateEdit_2.date().toPyDate()
        if not all([name, phone, grade, level, section, reg_date]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار طالب من الجدول.")
            return
        grade_id = Grade.select().where(
            (Grade.name == grade) & 
            (Grade.level == level)
        ).first().id if grade and level else None        
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد تحديث بيانات",
            f"هل أنت متأكد من تحديث بيانات الطالب \n {self.tableWidget_5.item(selected_row, 1).text()} ؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = self.student_manager.student_update(student_id, name, phone, grade_id, section, reg_date)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.student_load()
            else:
                QtWidgets.QMessageBox.critical(self, "خطأ", message)
        self.pushButton_35.setEnabled(False)
        self.pushButton_36.setEnabled(False)
                
    def student_delete(self):
        if self.lineEdit_25.text() == "" :
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار طالب من الجدول.")
            return
        selected_row = self.tableWidget_5.currentRow() 
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار طالب من الجدول")
            return 
        student_id = int(self.tableWidget_5.item(selected_row, 0).text())
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد الحذف",
            "هل أنت متأكد من حذف هذا الطالب ؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = self.student_manager.student_delete(student_id)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.student_load()
                self.student_form_clear()
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", message)
        self.pushButton_35.setEnabled(False)
        self.pushButton_36.setEnabled(False)
        
    def student_search(self):
        
        student_name = self.lineEdit_27.text().strip()
        phone = self.lineEdit_28.text().strip()
        if not student_name and not phone:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم الطالب أو رقم الهاتف للبحث.")
            return
        if student_name:
            student_id = Student.get(Student.name.contains(student_name)).id
        if phone:
            student_id = Student.get(Student.phone == phone).id
            
        student = Student.select().where(Student.id == student_id).first() if student_id else None
        if not student:
            QtWidgets.QMessageBox.warning(self, "خطأ", "الطالب غير موجود.")
            return

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        self.tableWidget_5.setItem(0, 0, QtWidgets.QTableWidgetItem(str(student.id)))
        self.tableWidget_5.setItem(0, 1, QtWidgets.QTableWidgetItem(student.name))
        self.tableWidget_5.setItem(0, 2, QtWidgets.QTableWidgetItem(student.phone))
        grade = Grade.get_by_id(student.grade_id) if student.grade_id else None
        self.tableWidget_5.setItem(0, 3, QtWidgets.QTableWidgetItem(grade.name if grade else ""))
        self.tableWidget_5.setItem(0, 4, QtWidgets.QTableWidgetItem(grade.level if grade else ""))
        self.tableWidget_5.setItem(0, 5, QtWidgets.QTableWidgetItem(str(student.section)))            
        self.tableWidget_5.setItem(0, 6, QtWidgets.QTableWidgetItem(student.reg_date.strftime("%Y-%m-%d")))            
        self.tableWidget_5.resizeColumnsToContents()
        
    def student_load(self):
        self.tableWidget_5.setRowCount(0)
        for row_index, student in enumerate(Student.select()):
            self.tableWidget_5.insertRow(row_index)
            grade = Grade.get_by_id(student.grade_id) if student.grade_id else None
            self.tableWidget_5.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(student.id)))
            self.tableWidget_5.setItem(row_index, 1, QtWidgets.QTableWidgetItem(student.name))
            self.tableWidget_5.setItem(row_index, 2, QtWidgets.QTableWidgetItem(student.phone))
            self.tableWidget_5.setItem(row_index, 3, QtWidgets.QTableWidgetItem(grade.name if grade else ""))
            self.tableWidget_5.setItem(row_index, 4, QtWidgets.QTableWidgetItem(grade.level if grade else ""))
            self.tableWidget_5.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(student.section)))            
            self.tableWidget_5.setItem(row_index, 6, QtWidgets.QTableWidgetItem(student.reg_date.strftime("%Y-%m-%d")))            
        self.tableWidget_5.resizeColumnsToContents()
        
    def student_table_select(self):
        self.pushButton_35.setEnabled(True)
        self.pushButton_36.setEnabled(True)
        selected_row = self.tableWidget_5.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار طالب من الجدول")
            return
        student_id = int(self.tableWidget_5.item(selected_row, 0).text())
        try:
            student = Student.get_by_id(student_id)
            self.lineEdit_25.setText(student.name)
            self.lineEdit_26.setText(student.phone)
            grade = Grade.get_by_id(student.grade_id) if student.grade_id else None
            if grade:
                self.comboBox_11.setCurrentText(grade.name)
                self.comboBox_12.setCurrentText(grade.level)    
            else:
                self.comboBox_11.setCurrentIndex(-1)
                self.comboBox_12.setCurrentIndex(-1)
            self.spinBox_3.setValue(student.section)
            self.dateEdit_2.setDate(QDate.fromString(student.reg_date.strftime("%Y-%m-%d"), "yyyy-MM-dd"))
        except DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "الطالب غير موجود")
    
    def student_form_clear(self):
        self.lineEdit_25.clear()
        self.lineEdit_26.clear()
        self.comboBox_11.setCurrentIndex(-1)
        self.comboBox_12.setCurrentIndex(-1)
        self.spinBox_3.setValue(1)
        self.dateEdit_2.setDate(QDate.currentDate())
        self.tableWidget_5.clearSelection() # مسح التحديد في الجدول
    
    def refresh_student_info(self):
        self.stackedWidget_3.setCurrentIndex(0)
        student_name = self.comboBox_15.currentText()
        month = self.comboBox_26.currentText()
        if student_name:
            try:
                student = Student.get(Student.name == student_name)
                student_id = student.id
                grade_id = student.grade_id                
                grade = Grade.get_by_id(grade_id) if grade_id else None                
                self.lineEdit_30.setText(student.phone)
                self.dateEdit_3.setDate(QDate.fromString(student.reg_date.strftime("%Y-%m-%d"), "yyyy-MM-dd"))
                self.spinBox_4.setValue(student.section)
                if grade:
                    self.comboBox_13.setCurrentText(grade.name)
                    self.comboBox_14.setCurrentText(grade.level)
                    self.student_enrollment_display()
                else:
                    self.comboBox_13.setCurrentIndex(-1)
                    self.comboBox_14.setCurrentIndex(-1)
                    self.comboBox_15.setCurrentIndex(-1)
            except DoesNotExist:
                self.lineEdit_30.clear()
                self.dateEdit_3.setDate(QDate.currentDate())
                self.spinBox_4.setValue(1)
                QtWidgets.QMessageBox.warning(self, "خطأ", "الطالب غير موجود")                    

    def get_student_info(self):        
        student_name = self.comboBox_18.currentText().strip()        
        month = self.comboBox_21.currentText().strip()
        if not all([student_name, month]):
            #QtWidgets.QMessageBox.warning(self, "خطأ", "الرجاء إدخال اسم الطالب والشهر")
            return
        student = Student.get(Student.name == student_name)
        st_info = StudentMonthlyInvoice.select().where((StudentMonthlyInvoice.student_id == student.id) & (StudentMonthlyInvoice.month == month)).first()
        if not st_info:
            self.lineEdit_35.clear()
            self.lineEdit_36.setText('0.00')
            self.lineEdit_39.setText('0.00')
            self.lineEdit_57.setText('0.00')
            self.comboBox_20.setCurrentIndex(0)
            self.tableWidget_7.setRowCount(0)
            QtWidgets.QMessageBox.warning(self, "تنبيه", f" الطالب : {student.name}  لم يسجل في أي مقرر في شهر {month}.")
            return
        self.lineEdit_34.setText(student.phone)
        self.lineEdit_35.setText(str(st_info.course_count))
        if st_info.remain < 0:
            self.lineEdit_57.setText(str(-st_info.remain))
            self.lineEdit_39.setText('0.00')
        else:
            self.lineEdit_36.setText(str(st_info.remain))
            self.lineEdit_57.setText('0.00')        
        self.spinBox_5.setValue(student.section if student else 1)
        self.dateEdit_4.setDate(QDate.currentDate())
        grade = Grade.get_by_id(student.grade_id) if student.grade_id else None
        self.comboBox_16.setCurrentText(grade.name if grade else "")
        self.comboBox_17.setCurrentText(grade.level if grade else "")
        self.payment_table_load(student, month)
        
    def student_account_tab_open(self):
        self.tabWidget.setCurrentIndex(7)
        self.stackedWidget_2.setCurrentIndex(0)
    
    
    def student_stat_tab_open(self):
        self.tabWidget.setCurrentIndex(8)
    
    def student_paid_all_debt(self):
        self.tableWidget_9.setRowCount(0)
        month = self.comboBox_25.currentText().strip()
        if not month:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر.")
            return
        student = StudentMonthlyInvoice.select().where(
            (StudentMonthlyInvoice.month == month) & 
            (StudentMonthlyInvoice.remain == 0)                        
        )
        if student.count() == 0:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "لايوجد")            
            return        
        for row_index, s in enumerate(student):
            student_info = Student.get_by_id(s.student_id)
            grade = Grade.get_by_id(student_info.grade_id) if student_info.grade_id else None
            self.tableWidget_9.insertRow(row_index)
            self.tableWidget_9.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(student_info.id)))
            self.tableWidget_9.setItem(row_index, 1, QtWidgets.QTableWidgetItem(student_info.name))
            self.tableWidget_9.setItem(row_index, 2, QtWidgets.QTableWidgetItem(student_info.phone))
            self.tableWidget_9.setItem(row_index, 3, QtWidgets.QTableWidgetItem(grade.name))
            self.tableWidget_9.setItem(row_index, 4, QtWidgets.QTableWidgetItem(grade.level))
            self.tableWidget_9.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(s.course_count)))
            self.tableWidget_9.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(s.total_due)))            
            self.tableWidget_9.setItem(row_index, 7, QtWidgets.QTableWidgetItem(s.month))
            self.tableWidget_9.setItem(row_index, 8, QtWidgets.QTableWidgetItem(str(s.total_paid)))
            self.tableWidget_9.setItem(row_index, 9, QtWidgets.QTableWidgetItem(str(s.remain)))
        self.tableWidget_9.resizeColumnsToContents()  # ضبط عرض الأعمدة تلقائيًا
        
    
    
    def student_debt(self):
        self.tableWidget_9.setRowCount(0)
        month = self.comboBox_25.currentText().strip()
        if not month:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر.")
            return
        student = StudentMonthlyInvoice.select().where(
            (StudentMonthlyInvoice.month == month) & 
            (StudentMonthlyInvoice.total_paid > 0) &
            (StudentMonthlyInvoice.remain > 0)            
        )
        if student.count() == 0:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "لايوجد")            
            return        
        for row_index, s in enumerate(student):
            student_info = Student.get_by_id(s.student_id)
            grade = Grade.get_by_id(student_info.grade_id) if student_info.grade_id else None
            self.tableWidget_9.insertRow(row_index)
            self.tableWidget_9.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(student_info.id)))
            self.tableWidget_9.setItem(row_index, 1, QtWidgets.QTableWidgetItem(student_info.name))
            self.tableWidget_9.setItem(row_index, 2, QtWidgets.QTableWidgetItem(student_info.phone))
            self.tableWidget_9.setItem(row_index, 3, QtWidgets.QTableWidgetItem(grade.name))
            self.tableWidget_9.setItem(row_index, 4, QtWidgets.QTableWidgetItem(grade.level))
            self.tableWidget_9.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(s.course_count)))
            self.tableWidget_9.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(s.total_due)))            
            self.tableWidget_9.setItem(row_index, 7, QtWidgets.QTableWidgetItem(s.month))
            self.tableWidget_9.setItem(row_index, 8, QtWidgets.QTableWidgetItem(str(s.total_paid)))
            self.tableWidget_9.setItem(row_index, 9, QtWidgets.QTableWidgetItem(str(s.remain)))
        self.tableWidget_9.resizeColumnsToContents()  # ضبط عرض الأعمدة تلقائيًا
        
    
    def student_no_paid(self):
        self.tableWidget_9.setRowCount(0)
        month = self.comboBox_25.currentText().strip()
        if not month:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر.")
            return
        student = StudentMonthlyInvoice.select().where(
            (StudentMonthlyInvoice.month == month) & 
            (StudentMonthlyInvoice.total_paid == 0)             
        )
        if student.count() == 0:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "لايوجد")            
            return        
        for row_index, s in enumerate(student):
            student_info = Student.get_by_id(s.student_id)
            grade = Grade.get_by_id(student_info.grade_id) if student_info.grade_id else None
            self.tableWidget_9.insertRow(row_index)
            self.tableWidget_9.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(student_info.id)))
            self.tableWidget_9.setItem(row_index, 1, QtWidgets.QTableWidgetItem(student_info.name))
            self.tableWidget_9.setItem(row_index, 2, QtWidgets.QTableWidgetItem(student_info.phone))
            self.tableWidget_9.setItem(row_index, 3, QtWidgets.QTableWidgetItem(grade.name))
            self.tableWidget_9.setItem(row_index, 4, QtWidgets.QTableWidgetItem(grade.level))
            self.tableWidget_9.setItem(row_index, 5, QtWidgets.QTableWidgetItem(str(s.course_count)))
            self.tableWidget_9.setItem(row_index, 6, QtWidgets.QTableWidgetItem(str(s.total_due)))            
            self.tableWidget_9.setItem(row_index, 7, QtWidgets.QTableWidgetItem(s.month))
            self.tableWidget_9.setItem(row_index, 8, QtWidgets.QTableWidgetItem(str(s.total_paid)))
            self.tableWidget_9.setItem(row_index, 9, QtWidgets.QTableWidgetItem(str(s.remain)))
        self.tableWidget_9.resizeColumnsToContents()  # ضبط عرض الأعمدة تلقائيًا
    
    def student_absence_info(self):
        student_name = self.comboBox_27.currentText().strip()
        month = self.comboBox_30.currentText().strip()
        if not student_name:
            return
        student = Student.get(Student.name == student_name)
        enrollments = Enrollment.select().where((Enrollment.student_id == student.id) &( Enrollment.month == month))
        if enrollments.count() == 0:            
            QtWidgets.QMessageBox.warning(self, "تنبيه", f"لا توجد تسجيلات للطالب : {student.name} في شهر {month}.")
        grade = Grade.get_by_id(student.grade_id)        
        teachers = (
            Teacher
            .select()
            .join(TeacherStudent, on=(TeacherStudent.teacher_id == Teacher.id))
            .where((TeacherStudent.student_id == student.id) & (TeacherStudent.month == month))
        )      
        self.lineEdit_47.setText(student.phone)
        self.spinBox_7.setValue(student.section)
        self.lineEdit_51.setText(grade.level)
        self.lineEdit_50.setText(grade.name)
        self.lineEdit_52.clear()
        self.comboBox_28.clear()
        for t in teachers:            
            self.comboBox_28.addItem(t.name)
            
    
    def student_absence_add(self):        
        student_name = self.comboBox_27.currentText().strip()
        teacher_name = self.comboBox_28.currentText().strip()
        date = self.dateEdit_7.date().toPyDate()
        day = self.lineEdit_48.text().strip()
        if not all([student_name, teacher_name, date, day]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        student = Student.get(Student.name == student_name)
        grade = Grade.get_by_id(student.grade_id)        
        teacher = Teacher.get(Teacher.name == teacher_name)
        course = Course.get(Course.teacher_id == teacher.id)  
        success, message = self.attendance_manager.add_absence(student.id, course.id, teacher.id, grade.id, date, day)
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", message)
            self.absence_table_load()
            self.attendance_form_clear()
            
        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)
    
        
    def absence_update(self):
        selected_row = self.tableWidget_13.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار مقرر من الجدول")
            return
        absence_id = int(self.tableWidget_13.item(selected_row, 0).text())
        student_name = self.comboBox_27.currentText().strip()
        student = Student.get(Student.name == student_name)
        grade = Grade.get_by_id(student.grade_id)
        teacher_name = self.comboBox_28.currentText()
        teacher = Teacher.get(Teacher.name == teacher_name)
        course = Course.get(Course.teacher_id == teacher.id)
        date = self.dateEdit_7.date().toPyDate()
        day = self.lineEdit_48.text()
        if not all([absence_id, student_name, teacher_name, date, day]):        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        success, message = self.attendance_manager.update_absence(absence_id, student.id, course.id, teacher.id, grade.id, date, day)
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", message)
            self.absence_table_load()

        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)
    
    def absence_delete(self):
        selected_row = self.tableWidget_13.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار صف من الجدول")
            return
        absence_id = int(self.tableWidget_13.item(selected_row, 0).text())        
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد الحذف",
            "هل أنت متأكد من حذف هذا الغياب ؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
        
            success, message = self.attendance_manager.delete_absence(absence_id)
            if success: 
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.absence_table_load()

            else:
                QtWidgets.QMessageBox.critical(self, "خطأ", message)
        
    def absence_search(self):
        student_name = self.lineEdit_29.text().strip()
        phone = self.lineEdit_45.text().strip()
        if not student_name and not phone:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم الطالب أو رقم الهاتف للبحث.")
            return
        if student_name:
            student_id = Student.get(Student.name.contains(student_name)).id
        if phone:
            student_id = Student.get(Student.phone == phone).id
        if student_id:
            absences = Attendance.select().where(Attendance.student_id == student_id)            
            if absences:
                self.tableWidget_13.setRowCount(0)
                for i, absence in enumerate(absences):
                    student = Student.get_by_id(absence.student_id)
                    teacher = Teacher.get_by_id(absence.teacher_id)
                    grade = Grade.get_by_id(absence.grade_id)
                    course = Course.get_by_id(absence.course_id)
                    self.tableWidget_13.insertRow(i)
                    self.tableWidget_13.setItem(i, 0, QtWidgets.QTableWidgetItem(str(absence.id)))
                    self.tableWidget_13.setItem(i, 1, QtWidgets.QTableWidgetItem(student.name))
                    self.tableWidget_13.setItem(i, 2, QtWidgets.QTableWidgetItem(student.phone))
                    self.tableWidget_13.setItem(i, 3, QtWidgets.QTableWidgetItem(grade.level))
                    self.tableWidget_13.setItem(i, 4, QtWidgets.QTableWidgetItem(grade.name))
                    self.tableWidget_13.setItem(i, 5, QtWidgets.QTableWidgetItem(teacher.name))
                    self.tableWidget_13.setItem(i, 6, QtWidgets.QTableWidgetItem(course.name))
                    self.tableWidget_13.setItem(i, 7, QtWidgets.QTableWidgetItem(absence.absence_day))
                    self.tableWidget_13.setItem(i, 8, QtWidgets.QTableWidgetItem(str(absence.absence_date)))
                self.tableWidget_13.resizeColumnsToContents()
                self.lineEdit_59.setText(str(absences.count()))

            else:
                QtWidgets.QMessageBox.critical(self, "رسالة", "لا يوجد غياب لهذا الطالب")

            
    def absence_table_select(self):
        self.comboBox_28.clear()
        teachers = Teacher.select()
        for teacher in teachers:
            self.comboBox_28.addItem(teacher.name)
        
        selected_row = self.tableWidget_13.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار مقرر من الجدول")
            return
        absence_id = int(self.tableWidget_13.item(selected_row, 0).text())
        try:
            absence = Attendance.get_by_id(absence_id)
            student_id = absence.student_id
            student= Student.get_by_id(student_id)
            teacher_id = absence.teacher_id
            teacher = Teacher.get_by_id(teacher_id)
            grade_id = absence.grade_id
            grade = Grade.get_by_id(grade_id)            
            if absence:
                self.lineEdit_48.setText(absence.absence_day) 
                self.dateEdit_7.setDate(absence.absence_date)
            if student:
                self.comboBox_27.setCurrentText(student.name)
                self.lineEdit_47.setText(str(student.phone))
                self.spinBox_7.setValue(student.section)
            else:
                self.comboBox_27.setCurrentIndex(-1)
                self.lineEdit_47.clear()
                self.spinBox_7.setValue(1)                
            if teacher:            
                self.comboBox_28.setCurrentText(teacher.name)                
            else:
                self.comboBox_28.setCurrentIndex(-1)
            if grade:
                self.lineEdit_50.setText(grade.name)
                self.lineEdit_51.setText(grade.level)            
            course_name = self.tableWidget_13.item(selected_row, 6).text()
            self.lineEdit_52.setText(course_name)
        except DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "الغياب غير موجود")
            
    
            
    def absence_table_load(self):
        self.tableWidget_13.setRowCount(0)
        months = {"يناير":1, "فبراير":2, "مارس":3, "أبريل":4, "مايو":5, "يونيو":6,
                        "يوليو":7, "أغسطس":8, "سبتمبر":9, "أكتوبر":10, "نوفمبر":11, "ديسمبر":12}
        month = self.comboBox_30.currentText().strip()        
        month_as_num = months.get(month)        
        absences = (
            Attendance
            .select()
            .where(fn.MONTH(Attendance.absence_date) == month_as_num)
        )
        for i, absence in enumerate(absences):
            student = Student.get_by_id(absence.student_id)
            teacher = Teacher.get_by_id(absence.teacher_id)
            grade = Grade.get_by_id(absence.grade_id)
            course = Course.get_by_id(absence.course_id)
            self.tableWidget_13.insertRow(i)
            self.tableWidget_13.setItem(i, 0, QtWidgets.QTableWidgetItem(str(absence.id)))
            self.tableWidget_13.setItem(i, 1, QtWidgets.QTableWidgetItem(student.name))
            self.tableWidget_13.setItem(i, 2, QtWidgets.QTableWidgetItem(student.phone))
            self.tableWidget_13.setItem(i, 3, QtWidgets.QTableWidgetItem(grade.level))
            self.tableWidget_13.setItem(i, 4, QtWidgets.QTableWidgetItem(grade.name))
            self.tableWidget_13.setItem(i, 5, QtWidgets.QTableWidgetItem(teacher.name))
            self.tableWidget_13.setItem(i, 6, QtWidgets.QTableWidgetItem(course.name))
            self.tableWidget_13.setItem(i, 7, QtWidgets.QTableWidgetItem(absence.absence_day))
            self.tableWidget_13.setItem(i, 8, QtWidgets.QTableWidgetItem(str(absence.absence_date)))
        self.tableWidget_13.resizeColumnsToContents()
    
        
    def attendance_form_clear(self):
        self.dateEdit_7.setDate(QDate.currentDate())
        self.comboBox_27.setCurrentIndex(-1)
        self.comboBox_28.setCurrentIndex(-1)
        self.lineEdit_29.clear()        
        self.lineEdit_45.clear()
        self.lineEdit_47.clear()
        self.lineEdit_51.clear()
        self.lineEdit_51.clear()
        self.lineEdit_52.clear()
        self.lineEdit_59.clear()
        self.spinBox_7.setValue(1)
        self.absence_table_load()
        

        
# ===================== End Student =========================
# ===================== Enrollment Course ===================

    def course_enrollment_tab_open(self):
        self.tabWidget.setCurrentIndex(6)

    def course_enrollment(self):
        late_reg = 1 if self.checkBox_4.isChecked() else 0
        attendance_hours = int(self.lineEdit_60.text() or "0")
        if attendance_hours == 0 and late_reg == 1:
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى إدخال عدد ساعات الحضور أو اختيار تسجيل متأخر.")
            return
        user_id = self.user_manager.get_logged_user_id()        
        student_name = self.comboBox_15.currentText().strip()
        student_id = Student.select().where(Student.name == student_name).first().id if student_name else None        
        grade_name = self.comboBox_13.currentText().strip()
        grade_level = self.comboBox_14.currentText().strip()        
        month = self.comboBox_26.currentText().strip()
        
        grade_id = Grade.select().where(
            (Grade.name == grade_name) & 
            (Grade.level == grade_level)).first().id if grade_name and grade_level else None        
        course_name = self.lineEdit_33.text().strip()
        course = Course.select().where((Course.name == course_name) & (Course.grade_id == grade_id)).first() if course_name and grade_id else None
        course_price = course.price if course else 0.0
        teacher_name = self.comboBox_19.currentText().strip()
        teacher_id = Teacher.select().where(Teacher.name == teacher_name).first().id if teacher_name else None        
        if not all([student_id, grade_id, course_name, teacher_id, month]):
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        if course_name and teacher_id and grade_id:
            course = Course.select().where(
                (Course.name == course_name) &
                (Course.teacher_id == teacher_id) &
                (Course.grade_id == grade_id)).first()
            if course:
                course_id = course.id                
            else:                
                QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار مقرر لنفس المرحلة التعليمية.")
                return
        
        success, message = self.enrollment_manager.create_enrollment(student_id, teacher_id, grade_id, course_id, month, course_price, late_reg, attendance_hours, user_id)
        if success:            
            QtWidgets.QMessageBox.information(self, "نجاح", message)
            self.enrollment_course_table_fill()  # إعادة ملء جدول التسجيلات بعد الإضافة            
            student = Student.select().where(Student.id == student_id).first()
            #self.lineEdit_38.setText(str(student.amount_due) if student else "0.00")
            self.lineEdit_60.setText("0")
            self.checkBox_4.setChecked(False)
        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)
            
            
    def student_enrollment_display(self):
        student_name = self.comboBox_15.currentText().strip()
        month = self.comboBox_26.currentText().strip()
        if not all([student_name, month]):
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار الطالب والشهر")
            return
        
        student = Student.select().where(Student.name == student_name).first()
        if not student:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "الطالب غير موجود.")
            return
        enrollments = Enrollment.select().where((Enrollment.student_id == student.id) &( Enrollment.month == month))

        if enrollments.count() == 0:            
            QtWidgets.QMessageBox.warning(self, "تنبيه", f"لا توجد تسجيلات للطالب : {student.name} في شهر {month}.")
            self.tableWidget_6.setRowCount(0)
            self.lineEdit_38.clear()
            return
        self.tableWidget_6.setRowCount(0)        
        for row_index, enrollment in enumerate(enrollments):
            course = enrollment.course_id
            teacher = course.teacher_id  # بافتراض أن جدول Course يحتوي على حقل teacher            
            
            self.tableWidget_6.insertRow(row_index)
            self.tableWidget_6.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(enrollment.id)))
            self.tableWidget_6.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(student.id)))
            self.tableWidget_6.setItem(row_index, 2, QtWidgets.QTableWidgetItem(course.name))
            self.tableWidget_6.setItem(row_index, 3, QtWidgets.QTableWidgetItem(teacher.name))
            self.tableWidget_6.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(course.price)))            
        self.tableWidget_6.resizeColumnsToContents()        
        st_invoice = StudentMonthlyInvoice.get_or_none((StudentMonthlyInvoice.student_id == student.id) & (StudentMonthlyInvoice.month == month))       
        self.lineEdit_38.setText(str(st_invoice.total_due) if st_invoice else "0.00")
    
    def course_enrollment_delete(self):
        selected_row = self.tableWidget_6.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار سجل من الجدول")
            return 
        enrollment_id = int(self.tableWidget_6.item(selected_row, 0).text())
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد الحذف",
            "هل أنت متأكد من حذف هذا التسجيل ؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            success, message = self.enrollment_manager.delete_enrollment(enrollment_id)
            if success:
                QtWidgets.QMessageBox.information(self, "نجاح", message)
                self.enrollment_course_table_fill()
            else:
                QtWidgets.QMessageBox.warning(self, "خطأ", message)
                
    
    
    def course_enrollment_form_clear(self):
        self.lineEdit_30.clear()
        self.lineEdit_31.clear()
        self.lineEdit_32.clear()
        self.lineEdit_33.clear()
        self.lineEdit_38.clear()
        self.comboBox_13.setCurrentIndex(-1)        
        self.comboBox_14.setCurrentIndex(-1)
        self.comboBox_15.setCurrentIndex(-1)
        self.comboBox_19.setCurrentIndex(-1)
        self.dateEdit_3.setDate(QDate.currentDate())
        self.tableWidget_6.setRowCount(0)
    
    def enrollment_course_table_fill(self):
        student_name = self.comboBox_15.currentText().strip()
        month = self.comboBox_26.currentText().strip()
        student = Student.select().where(Student.name == student_name).first() if student_name else None
        if not student:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "الطالب غير موجود.")
            return

        enrollments = Enrollment.select().where(
            (Enrollment.student_id == student.id) &
            (Enrollment.month == month))

        if enrollments.count() == 0:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "لا توجد تسجيلات لهذا الطالب.")            
            return        

        self.tableWidget_6.setRowCount(0)        
        for row_index, enrollment in enumerate(enrollments):
            course = enrollment.course_id
            teacher = course.teacher_id  # بافتراض أن جدول Course يحتوي على حقل teacher            
            
            self.tableWidget_6.insertRow(row_index)
            self.tableWidget_6.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(enrollment.id)))
            self.tableWidget_6.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(student.id)))
            self.tableWidget_6.setItem(row_index, 2, QtWidgets.QTableWidgetItem(course.name))
            self.tableWidget_6.setItem(row_index, 3, QtWidgets.QTableWidgetItem(teacher.name))
            self.tableWidget_6.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(course.price)))            
        self.tableWidget_6.resizeColumnsToContents()
        st_invoice = StudentMonthlyInvoice.get_or_none((StudentMonthlyInvoice.student_id == student.id) & (StudentMonthlyInvoice.month == month))        
        self.lineEdit_38.setText(str(st_invoice.total_due) if st_invoice else "0.00")
                
# ===================== Enrollment Course ===================
    def teacher_combo_refresh(self):
        
        self.comboBox_5.clear()
        self.comboBox_9.clear()
        self.comboBox_19.clear()        
        self.comboBox_28.clear() 
        for teacher in Teacher.select():            
            self.comboBox_5.addItem(teacher.name)
            self.comboBox_9.addItem(teacher.name)            
            self.comboBox_19.addItem(teacher.name)            
            self.comboBox_28.addItem(teacher.name)
        self.comboBox_5.setCurrentIndex(-1)
        self.comboBox_9.setCurrentIndex(-1)
        self.comboBox_19.setCurrentIndex(-1)
    
    def student_combo_refresh(self):
        self.comboBox_18.blockSignals(True)    
        self.comboBox_15.clear()
        self.comboBox_18.clear()
        self.comboBox_27.clear()
        for student in Student.select():
            self.comboBox_15.addItem(student.name)
            self.comboBox_18.addItem(student.name)
            self.comboBox_27.addItem(student.name)
        self.comboBox_15.setCurrentIndex(-1)
        self.comboBox_18.setCurrentIndex(-1)
        self.comboBox_27.setCurrentIndex(-1)
        self.comboBox_18.blockSignals(False)
    
    def grade_combo_refresh(self):    
        # تحميل الصفوف في Combobox
        grades = Grade.select(fn.DISTINCT(Grade.name)).where(Grade.name.is_null(False))
        self.comboBox_4.clear()
        self.comboBox_8.clear()        
        self.comboBox_11.clear()
        self.comboBox_13.clear()
        self.comboBox_16.clear()
        for grade in grades: #Grade.select():            
            self.comboBox_4.addItem(grade.name)
            self.comboBox_8.addItem(grade.name)
            self.comboBox_11.addItem(grade.name)
            self.comboBox_13.addItem(grade.name)
            self.comboBox_16.addItem(grade.name)

        levels = Grade.select(fn.DISTINCT(Grade.level)).where(Grade.level.is_null(False))
        self.comboBox_3.clear()
        self.comboBox_7.clear()
        self.comboBox_12.clear()
        self.comboBox_14.clear()
        self.comboBox_17.clear()
        for grade in levels:
            self.comboBox_3.addItem(grade.level)
            self.comboBox_7.addItem(grade.level)
            self.comboBox_12.addItem(grade.level)
            self.comboBox_14.addItem(grade.level)
            self.comboBox_17.addItem(grade.level)        
            
        terms = Grade.select(fn.DISTINCT(Grade.term)).where(Grade.level.is_null(False))
        self.comboBox_2.clear()
        self.comboBox_6.clear()        
        for grade in terms:
            self.comboBox_2.addItem(grade.term)
            self.comboBox_6.addItem(grade.term)        
        
    def payment_type_combo_refresh(self):    
        self.comboBox_20.clear()
        self.comboBox_20.addItem("نقدي")
        self.comboBox_20.addItem("فيزا")
        self.comboBox_20.setCurrentIndex(0)
        
        

    def fill_months_combobox(self, *comboboxes):
        # قائمة الأشهر
        months = [
            "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
            "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
        ]
        
        manths_map = {
            "January": "يناير",
            "February": "فبراير",
            "March": "مارس",
            "April": "أبريل",
            "May": "مايو",
            "June": "يونيو",
            "July": "يوليو", 
            "August": "أغسطس",
            "September": "سبتمبر",
            "October": "أكتوبر",
            "November": "نوفمبر",
            "December": "ديسمبر"
        }
        current_month_en = datetime.now().strftime("%B")
        current_month_ar = manths_map[current_month_en]
        # الحصول على فهرس الشهر الحالي داخل القائمة
        current_index = months.index(current_month_ar)
        # تعبئة كل كومبوبوكس يتم تمريره
        for combo in comboboxes:
            combo.clear()
            combo.addItems(months)
            combo.setCurrentIndex(current_index)  # بدون اختيار افتراضي


    def linedit_23_refresh(self):
        selected_teacher = self.comboBox_5.currentText()
        if selected_teacher:
            try:
                teacher = Teacher.get(Teacher.name == selected_teacher)
                self.lineEdit_23.setText(teacher.specialization)
            except DoesNotExist:
                self.lineEdit_23.clear()
        else:
            self.lineEdit_23.clear()

    def monthly_payments(self):
        user_id = self.user_manager.get_logged_user_id()
        student_name = self.comboBox_18.currentText().strip()
        if not student_name:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "يرجى اختيار طالب من القائمة")
            return
        student = Student.get(Student.name == student_name)
        student_id = student.id
        amount_due = Decimal(self.lineEdit_36.text().strip())
        amount_paid = Decimal(self.lineEdit_39.text().strip())
        paid_type = self.comboBox_20.currentText().strip()
        payment_date = self.dateEdit_4.date().toPyDate()
        month = self.comboBox_21.currentText().strip()
        center_share = Enrollment.select(fn.SUM(Enrollment.center_share)).where((Enrollment.student_id == student_id) & (Enrollment.month == month)).scalar() or 0.00
        st_invoice = StudentMonthlyInvoice.get_or_none((StudentMonthlyInvoice.student_id == student_id) & (StudentMonthlyInvoice.month == month))
        center_share = (
            Decimal(center_share) * 
            (Decimal(amount_paid) / Decimal(st_invoice.total_due))
            ) if st_invoice and st_invoice.total_due > 0 else Decimal("0.00")
        if amount_paid <= 0:
            QtWidgets.QMessageBox.warning(self, "خطأ", "المبلغ المدفوع يجب أن يكون أكبر من صفر.")
            return
        if not all([student_id, amount_due, amount_paid, paid_type, payment_date, month]):
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول.")
            return
        
        success, message = PaymentService.create_payment(
            student_id, amount_due, amount_paid, center_share, paid_type, payment_date, month, user_id)
        if success:
            QtWidgets.QMessageBox.information(self, "نجاح", message)                                    
            self.payment_table_load(student, month)
            self.lineEdit_36.setText(str(Decimal(amount_due) - Decimal(amount_paid)))
            self.lineEdit_39.setText('0.00')
            self.lineEdit_57.setText('0.00')
            self.comboBox_20.setCurrentIndex(0)
        else:
            QtWidgets.QMessageBox.critical(self, "خطأ", message)            

    def payment_form_clear(self):
        
        self.lineEdit_34.clear()
        self.lineEdit_35.clear()
        self.lineEdit_36.setText('0.00')
        self.lineEdit_39.setText('0.00')
        self.lineEdit_57.setText('0.00')
        self.comboBox_16.setCurrentIndex(-1)
        self.comboBox_17.setCurrentIndex(-1)
        self.comboBox_18.setCurrentIndex(-1)
        self.comboBox_20.setCurrentIndex(0)        
        self.dateEdit_4.setDate(QDate.currentDate())
        self.tableWidget_7.setRowCount(0)
        
    def payment_table_load(self, student, month):
        self.stackedWidget_2.setCurrentIndex(0)
        self.tableWidget_7.setRowCount(0)
        # student_name = self.comboBox_18.currentText().strip()        
        # student = Student.get(Student.name == student_name)
        payments = Payment.select().where((Payment.student_id == student.id) & (Payment.month == month))                
        if payments.count() == 0:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "لا توجد مدفوعات لهذا الطالب.")
            return
        for row_index, payment in enumerate(payments):
            self.tableWidget_7.insertRow(row_index)
            self.tableWidget_7.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(student.id)))
            self.tableWidget_7.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(student.name)))
            self.tableWidget_7.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(student.phone)))
            self.tableWidget_7.setItem(row_index, 3, QtWidgets.QTableWidgetItem(payment.month))
            self.tableWidget_7.setItem(row_index, 4, QtWidgets.QTableWidgetItem(str(payment.amount)))
            self.tableWidget_7.setItem(row_index, 5, QtWidgets.QTableWidgetItem(payment.payment_date.strftime("%Y-%m-%d")))
            self.tableWidget_7.setItem(row_index, 6, QtWidgets.QTableWidgetItem(payment.paid_type))   
        self.tableWidget_7.resizeColumnsToContents()
        

    # =============================== Attendance ======================    
    
    def attendance_tab_open(self):
        self.tabWidget.setCurrentIndex(10)
        
    
    # =============================== End Attendance ==================
    
    # =============================== Management ======================
    
    def management_tab_open(self):
        self.tabWidget.setCurrentIndex(11)
        
    def student_stat(self):
        month = self.comboBox_29.currentText()
        if not month:        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر.")
            return
        
        try: # استعلام عدد الطلاب المسجلين في السنتر
            student_count = Student.select().count()
            self.lineEdit_53.setText(str(student_count))
        
        
            # استعلام Peewee مع join و ORDER BY
            query = (
                TeacherStudent
                .select(
                    Grade.level,
                    Grade.name,
                    fn.COUNT(TeacherStudent.id).alias('student_count')
                )
                .join(Grade, on=(TeacherStudent.grade_id == Grade.id))
                .where(                    
                    (TeacherStudent.month == month)
                )
                .group_by(Grade.level, Grade.name)
                .order_by(Grade.level, Grade.name)
            )
            if not query:
                self.tableWidget_16.setRowCount(0)
                
                return
            else:
                total = 0  # متغير لتجميع عدد الطلاب
                self.tableWidget_16.setRowCount(0)
                for i, row in enumerate(query):
                    g = row.grade_id            # هذا كائن Grade
                    self.tableWidget_16.insertRow(i)
                    self.tableWidget_16.setItem(i, 0, QtWidgets.QTableWidgetItem(str(g.level)))
                    self.tableWidget_16.setItem(i, 1, QtWidgets.QTableWidgetItem(str(g.name)))
                    self.tableWidget_16.setItem(i, 2, QtWidgets.QTableWidgetItem(str(row.student_count)))
                    total += row.student_count  # نجمع

                # إضافة صف المجموع الكلي
                summary_row = self.tableWidget_16.rowCount()
                self.tableWidget_16.insertRow(summary_row)
                self.tableWidget_16.setItem(summary_row, 0, QtWidgets.QTableWidgetItem("إجمالي"))
                self.tableWidget_16.setItem(summary_row, 1, QtWidgets.QTableWidgetItem(""))
                self.tableWidget_16.setItem(summary_row, 2, QtWidgets.QTableWidgetItem(str(total)))
                self.tableWidget_16.resizeColumnsToContents()
        except Teacher.DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", "لا يوجد تسجيل لهذا الشهر")
            
    def total_income(self):
        month = self.comboBox_29.currentText()
        if not month:        
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر.")
            return
        try:
            amount_due = StudentMonthlyInvoice.select(fn.SUM(StudentMonthlyInvoice.total_due)).where(StudentMonthlyInvoice.month == month).scalar() or 0.00
            total_income = StudentMonthlyInvoice.select(fn.SUM(StudentMonthlyInvoice.total_paid)).where(StudentMonthlyInvoice.month == month).scalar() or 0.00
            remain = (StudentMonthlyInvoice.select(fn.SUM(StudentMonthlyInvoice.remain))
                    .where((StudentMonthlyInvoice.remain > 0) & (StudentMonthlyInvoice.month == month)).scalar() or 0.00)
            cash_back = (StudentMonthlyInvoice.select(fn.SUM(StudentMonthlyInvoice.remain))
                    .where((StudentMonthlyInvoice.remain < 0) & (StudentMonthlyInvoice.month == month)).scalar() or 0.00)
            center_share = Payment.select(fn.SUM(Payment.center_share)).where(Payment.month == month).scalar() or 0.00
            teacher_income = TeacherAccount.select(fn.SUM(TeacherAccount.income)).where(TeacherAccount.month == month).scalar() or 0.00
            center_income = Decimal(amount_due) - Decimal(teacher_income)            
            net_income = Decimal(total_income) + Decimal(cash_back)
            
            self.lineEdit_54.setText(str(amount_due))
            self.lineEdit_61.setText(str(center_income))
            self.lineEdit_62.setText(str(teacher_income))
                        
            self.lineEdit_55.setText(str(total_income))
            self.lineEdit_56.setText(str(-cash_back))
            self.lineEdit_58.setText(str(net_income))            
            self.lineEdit_63.setText(str(remain))
            self.lineEdit_64.setText(str(center_share))
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "خطأ", f"حدث خطأ أثناء الحساب: {str(e)}")
    
    def management_form_clear(self):
        self.lineEdit_53.clear()
        self.lineEdit_54.clear()
        self.lineEdit_55.clear()
        self.lineEdit_56.clear()
        self.lineEdit_58.clear()
        self.lineEdit_61.clear()
        self.lineEdit_62.clear()
        self.lineEdit_63.clear()
        self.lineEdit_64.clear()
        self.tableWidget_16.setRowCount(0)
    
    # =============================== End Management ==================
    
    # =============================== Permissions ==================
    def permission_tab_open(self):
        self.tabWidget.setCurrentIndex(12)
        
    def permission_save(self):
        user_name = self.comboBox.currentText()
        if user_name == "اختر مستخدم":
            QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار مستخدم من القائمة")
            return
        try:
            user = User.get(User.fullname == user_name)
            
            if user.is_admin:
                user_tab =1
                teacher_tab =1
                grade_tab =1
                course_tab =1
                student_tab =1
                enrollment_tab =1
                student_account_tab =1
                student_stat_tab =1
                teacher_account_tab =1
                attendance_tab =1
                management_tab =1
                permission_tab =1
            else:
                user_tab =1 if self.checkBox_15.isChecked() else 0                
                teacher_tab =1 if self.checkBox_16.isChecked() else 0
                grade_tab =1 if self.checkBox_17.isChecked() else 0
                course_tab =1 if self.checkBox_18.isChecked() else 0
                student_tab =1 if self.checkBox_19.isChecked() else 0
                enrollment_tab =1 if self.checkBox_20.isChecked() else 0
                student_account_tab =1 if self.checkBox_21.isChecked() else 0
                student_stat_tab =1 if self.checkBox_22.isChecked() else 0
                teacher_account_tab =1 if self.checkBox_23.isChecked() else 0
                attendance_tab =1 if self.checkBox_24.isChecked() else 0
                management_tab =1 if self.checkBox_25.isChecked() else 0
                permission_tab =1 if self.checkBox_26.isChecked() else 0
                
            permission, created = Permission.get_or_create(
                user_id=user.id,
                defaults={
                    "user_tab": user_tab,
                    "teacher_tab": teacher_tab,
                    "grade_tab": grade_tab,
                    "course_tab": course_tab,
                    "student_tab": student_tab,
                    "enrollment_tab": enrollment_tab,
                    "student_account_tab": student_account_tab,
                    "student_stat_tab": student_stat_tab,
                    "teacher_account_tab": teacher_account_tab,
                    "attendance_tab": attendance_tab,
                    "management_tab": management_tab,
                    "permission_tab": permission_tab
                }
            )
            
            
            if not created:
                permission.user_tab = user_tab
                permission.teacher_tab = teacher_tab
                permission.grade_tab = grade_tab
                permission.course_tab = course_tab
                permission.student_tab = student_tab
                permission.enrollment_tab = enrollment_tab
                permission.student_account_tab = student_account_tab
                permission.student_stat_tab = student_stat_tab
                permission.teacher_account_tab = teacher_account_tab
                permission.attendance_tab = attendance_tab
                permission.management_tab = management_tab
                permission.permission_tab = permission_tab
                permission.save()

            QtWidgets.QMessageBox.information(self, "تم", "تم حفظ الصلاحيات بنجاح")

        except User.DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "خطأ", f"المستخدم '{user_name}' غير موجود")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "خطأ", f"فشل في الحفظ:\n{e}")


    def permission_apply(self):        
        if not self.user_manager.logged_user:
            return

        try:
            permission = Permission.get(Permission.user == self.user_manager.logged_user)

            self.pushButton.setEnabled(permission.users_tab)
            self.pushButton_2.setEnabled(permission.teacher_tab)
            self.pushButton_3.setEnabled(permission.course_tab)
            self.pushButton_4.setEnabled(permission.grade_tab)
            self.pushButton_5.setEnabled(permission.student_tab)
            self.pushButton_6.setEnabled(permission.enrollment_tab)
            self.pushButton_7.setEnabled(permission.student_account_tab)
            self.pushButton_8.setEnabled(permission.student_stat_tab)
            self.pushButton_9.setEnabled(permission.teacher_account_tab)
            self.pushButton_55.setEnabled(permission.attendance_tab)
            self.pushButton_57.setEnabled(permission.management_tab)
            self.pushButton_56.setEnabled(permission.permission_tab)          

        except Permission.DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "لا توجد صلاحيات محددة لهذا المستخدم")


    def permission_toggle(self):
        # هل جميع الصلاحيات مفعلة؟
        self.comboBox.setCurrentIndex(0)  # إعادة تعيين اختيار المستخدم
        all_checked = all(cb.isChecked() for cb in self.permission_checkboxes)

        for cb in self.permission_checkboxes:
            cb.setChecked(not all_checked)
            
    def permission_show(self):
        user_name = self.comboBox.currentText()
        if not user_name or user_name == "اختر مستخدم":
            return
        try:
            user = User.get(User.fullname == user_name)
            permission = Permission.get(Permission.user_id == user.id)

            self.checkBox_15.setChecked(permission.user_tab)
            self.checkBox_16.setChecked(permission.teacher_tab)
            self.checkBox_17.setChecked(permission.course_tab)
            self.checkBox_18.setChecked(permission.grade_tab)
            self.checkBox_19.setChecked(permission.student_tab)
            self.checkBox_20.setChecked(permission.enrollment_tab)
            self.checkBox_21.setChecked(permission.student_account_tab)
            self.checkBox_22.setChecked(permission.student_stat_tab)
            self.checkBox_23.setChecked(permission.teacher_account_tab)
            self.checkBox_24.setChecked(permission.attendance_tab)
            self.checkBox_25.setChecked(permission.management_tab)
            self.checkBox_26.setChecked(permission.permission_tab)           
            
        except Permission.DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "لا توجد صلاحيات محددة لهذا المستخدم")
            for cb in self.permission_checkboxes:
                cb.setChecked(False)
        except User.DoesNotExist:
            QtWidgets.QMessageBox.warning(self, "تنبيه", "المستخدم غير موجود")
    
    # =============================== End Permissions ==================
    
    # =============================== Update database =========================
    
    def start_backup_and_clear(self):
        """إنشاء نسخة احتياطية من قاعدة البيانات ثم تفريغ الجداول المحددة"""
        reply = QtWidgets.QMessageBox.question(
            self,
            "تأكيد العملية",
            "⚠️ سيتم إنشاء نسخة احتياطية من قاعدة البيانات ثم تفريغ الجداول المحددة.\nهل أنت متأكد؟",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )

        if reply == QtWidgets.QMessageBox.Yes:
            if self.backup_database():
                self.clear_tables()
            else:
                QtWidgets.QMessageBox.critical(
                self,
                "خطأ",
                "فشل النسخ الاحتياطي! لم يتم حذف أي بيانات."
            )    
    def backup_database(self):
        try:
            # مجلد النسخ الاحتياطية
            backup_dir = r"D:\course_center\backups"
            os.makedirs(backup_dir, exist_ok=True)

            # اسم الملف بتاريخ اليوم والوقت
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{now}.sql")
            # أمر النسخ الاحتياطي
            dump_cmd = [
                "mysqldump",
                f"-u{DB_USER}",
                f"-p{DB_PASS}" if DB_PASS else "",
                DB_NAME
            ]

            # إنشاء النسخة
            with open(backup_file, "w", encoding="utf-8") as f:
                result = subprocess.run(
                    [arg for arg in dump_cmd if arg],  # تجاهل العناصر الفارغة
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True
                )

            if result.returncode == 0:
                QtWidgets.QMessageBox.information(
                    self,
                    "نجاح",
                    f"تم إنشاء النسخة الاحتياطية بنجاح:\n{backup_file}"
                )
                return True
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    "خطأ",
                    f"فشل النسخ الاحتياطي:\n{result.stderr}"
                )
                return False

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "خطأ", f"حدث استثناء:\n{str(e)}")
            return False
    

    def clear_tables(self):
        try:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME, charset='utf8mb4')
            cur = conn.cursor()
            cur.execute("SET FOREIGN_KEY_CHECKS=0;")
            for table in TABLES_TO_CLEAR:
                cur.execute(f"TRUNCATE TABLE `{table}`;")
            cur.execute("SET FOREIGN_KEY_CHECKS=1;")
            conn.commit()
            cur.close()
            conn.close()

            QtWidgets.QMessageBox.information(
                self, "نجاح", f"تم تفريغ الجداول بنجاح:\n{', '.join(TABLES_TO_CLEAR)}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "خطأ في التفريغ", f"حدث خطأ: {e}")
            
    # =============================== End Update database =========================
    
    # =============================== Printing =========================    
    
    def print_settings(self):
        try:
            printer = QPrinter(QPrinter.HighResolution)
            
            # إعداد حجم الورق والاتجاه (محدث)
            page_layout = QPageLayout()
            page_layout.setPageSize(QPageSize(QPageSize.A5))  # يمكنك تغيير الحجم حسب الحاجة
            page_layout.setOrientation(QPageLayout.Portrait)  # أو QPageLayout.Landscape
            printer.setPageLayout(page_layout)
            
            print_dialog = QPrintDialog(printer, self)
            
            if print_dialog.exec_() == QPrintDialog.Accepted:
                document = QTextDocument()
                document.setDefaultStyleSheet("""
                    body { direction: rtl; font-family: Arial; margin: 30px; }
                    table { width: 100%; border-collapse: collapse; direction: rtl; }
                """)
                if self.tabWidget.currentIndex() == 7:
                    document.setHtml(self.student_grades_print())
                elif self.tabWidget.currentIndex() == 5:
                    document.setHtml(self.class_names_print())
                else:
                    document.setHtml(self.class_grades_print())
                document.print_(printer)
                
                QtWidgets.QMessageBox.information(self, "نجاح", "تم إرسال التقرير إلى الطابعة")
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الطباعة: {str(e)}")
            
    
    def _amount_to_words_ar(self, amount):
        """
        تحويل قيمة عشرية (Decimal أو float) إلى نص عربي مع جنيه/قرش.
        مثال: 350.75 -> "ثلاثمائة وخمسون جنيه و خمسة وسبعون قرش"
        """
        amt = Decimal(amount).quantize(Decimal('0.01'))
        int_part = int(amt)
        frac = int((amt - int_part) * 100)
        words = num2words(int_part, lang='ar')
        words = f"{words} جنيه"
        if frac:
            frac_words = num2words(frac, lang='ar')
            words = f"{words} و {frac_words} قرش"
        return words


    # تحويل الأرقام إلى عربية
    def convert_to_arabic_numbers(self, number):
        english_numbers = "0123456789"
        arabic_numbers = "٠١٢٣٤٥٦٧٨٩"
        number_str = str(number)
        converted = ""
        for char in number_str:
            if char in english_numbers:
                converted += arabic_numbers[english_numbers.index(char)]
            else:
                converted += char
        return converted

    def print_student_receipt(self):
        try:
            # 1) اختيار الطالب من واجهتك
            student_name = self.comboBox_18.currentText().strip()
            month = self.comboBox_21.currentText().strip()
            if not student_name:
                QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار طالب من القائمة.")
                return
            if not month:
                QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر من القائمة.")
                return
            
            # 2) جلب الكائنات من قاعدة البيانات 
            try:
                student = Student.get(Student.name == student_name)
            except Student.DoesNotExist:
                QtWidgets.QMessageBox.warning(self, "خطأ", "الطالب غير موجود.")
                return

            payment = (Payment.select()
                    .where((Payment.student_id == student.id) & (Payment.month == month))
                    .order_by(Payment.id.desc())
                    .first())
            user = User.get(User.id == payment.user_id) if payment else None
            if not payment:
                QtWidgets.QMessageBox.warning(self, "خطأ", "لا توجد دفعات لهذا الطالب.")
                return

            # 3) إعداد القيم مع تحويل الأرقام إلى عربية
            month = payment.month or ""
            amount_dec = Decimal(payment.amount)            
            
            # تحويل المبلغ إلى أرقام عربية
            amount_str = f"{amount_dec:,.2f}"
            amount_str_arabic = self.convert_to_arabic_numbers(amount_str)
            
            # فصل التاريخ والوقت وإضافة مسافة بينهما
            current_datetime = datetime.now()
            date_english = current_datetime.strftime("%d/%m/%Y")
            time_english = current_datetime.strftime("%H:%M")
            
            date_arabic = self.convert_to_arabic_numbers(date_english)
            time_arabic = self.convert_to_arabic_numbers(time_english)
            
            # دمج التاريخ والوقت بمسافة كبيرة بينهما
            date_time_arabic = f"{date_arabic}&nbsp;&nbsp;&nbsp;&nbsp;{time_arabic}"
        
            amount_words = self._amount_to_words_ar(amount_dec)

        
            # 4) إنشاء HTML للإيصال بتنسيق محسّن
            font_settings = {
                'header_font': 'Arial',  # خط العناوين الرئيسية
                'header_size': '12pt',
                'label_font': 'Arial',  # خط التسميات
                'label_size': '20pt',
                'body_font': 'Times New Roman',  # خط النص العادي
                'body_size': '16pt',                
                'signature_font': 'Arial',
                'signature_size': '16pt'
            }
                    
            html = f"""
            <!doctype html>
            <html dir="rtl" lang="ar">
            <head>
            <meta charset="utf-8">
            <style>
            body {{
                    font-family: {font_settings['body_font']};
                    font-size: {font_settings['body_size']};
                    margin: 0;
                    padding: 20px;
                    direction: rtl;
                }}
            .header {{
                font-family: '{font_settings['header_font']}';
                font-size: {font_settings['header_size']};
                
                }}
            .label {{
                text-align: center;
                margin-bottom: 30px;
                }}
            .label h1 {{
                font-family: '{font_settings['label_font']}';
                font-size: {font_settings['label_size']};                
                }}
            .container {{
                margin-bottom: 20px;                
                padding: 15px;                
                font-family: '{font_settings['body_font']}';
                font-size: {font_settings['body_size']};
                }}
            .footer {{
                    margin-top: 30px;
                    text-align: center;
                    float: left;
                    font-family: '{font_settings['signature_font']}';
                    font-size: {font_settings['signature_size']};
                }}
            </style>
            </head>
            <body>
                <div class="header">
                    <p> مركز النور لتعليم اللغات و الحاسب الآلي </p>
                    <p style = "margin-right: 150px;"> إدارة الأستاذ/ محمد عبدالعزيز </p>
                    <p style = "margin-right: 10px;"> 01068888888 - 01268888888 </p>
                <\div>
                <div class="label">
                    <h1>إيصال استلام نقدية</h1>
                </div>
            
                <div class="container">
                    <p><strong>:  التاريخ </strong> &nbsp;  {date_time_arabic}</p>
                    <p><strong>:  اسم الطالب </strong> {student.name} &nbsp;</p>
                    <p><strong>:  الشهر </strong> {month} &nbsp;</p>
                    <p><strong>:  المبلغ </strong> &nbsp;  {amount_str_arabic}  جنيه </p>
                    <p><strong>:  المبلغ كتابة </strong> {amount_words} &nbsp; فقط لاغير </p>
                </div>
            
                <div class="footer">
                    <p><strong>:  اسم المستلم </strong> {user.fullname} &nbsp; </p> 
                    <p><strong> توقيع المستلم </strong></p>
                </div>
            </body>
            </html>
    
            """

            # 5) إعداد الطابعة (A5) والطباعة
            printer = QPrinter(QPrinter.HighResolution)
            
            # تحديد حجم الصفحة إلى A5
            try:
                printer.setPageSize(QPrinter.A5)
            except Exception:
                try:
                    from PyQt5.QtPrintSupport import QPrinter as _P
                    printer.setPageSize(_P.A5)
                except Exception:
                    pass

            printer.setOrientation(QPrinter.Portrait)
            
            # تحسين إعدادات الطباعة
            printer.setPageMargins(6, 6, 3, 6, QPrinter.Millimeter)
            printer.setFullPage(False)

            # إظهار مربع اختيار الطابعة
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                doc = QTextDocument()
                doc.setHtml(html)
                
                # ضبط هوامش المستند
                doc.setDocumentMargin(5)
                
                # اطبع المستند مباشرة إلى الطابعة المحددة
                doc.print_(printer)
                QtWidgets.QMessageBox.information(self, "نجاح", "تم إرسال الإيصال للطابعة بنجاح.")
            else:
                QtWidgets.QMessageBox.information(self, "ملغي", "تم إلغاء عملية الطباعة.")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "خطأ أثناء الطباعة", str(e))
            
    def print_teacher_receipt(self):
        try:
            # 1) اختيار المدرس من واجهتك
            teacher_name = self.comboBox_9.currentText().strip()
            month = self.comboBox_10.currentText().strip()
            if not teacher_name:
                QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار مدرس من القائمة.")
                return
            if not month:
                QtWidgets.QMessageBox.warning(self, "خطأ", "يرجى اختيار الشهر من القائمة.")
                return
            
            # 2) جلب الكائنات من قاعدة البيانات 
            try:
                teacher = Teacher.get(Teacher.name == teacher_name)
            except Student.DoesNotExist:
                QtWidgets.QMessageBox.warning(self, "خطأ", "المدرس غير موجود.")
                return
            # 3) إعداد القيم مع تحويل الأرقام إلى عربية
            
            amount = Decimal(self.lineEdit_42.text().strip())    
            
            # تحويل المبلغ إلى أرقام عربية
            amount_str = f"{amount:,.2f}"
            amount_str_arabic = self.convert_to_arabic_numbers(amount_str)
            
            # فصل التاريخ والوقت وإضافة مسافة بينهما
            current_datetime = datetime.now()
            date_english = current_datetime.strftime("%d/%m/%Y")
            time_english = current_datetime.strftime("%H:%M")
            
            date_arabic = self.convert_to_arabic_numbers(date_english)
            time_arabic = self.convert_to_arabic_numbers(time_english)
            
            # دمج التاريخ والوقت بمسافة كبيرة بينهما
            date_time_arabic = f"{date_arabic}&nbsp;&nbsp;&nbsp;&nbsp;{time_arabic}"
        
            amount_words = self._amount_to_words_ar(amount)

        
            # 4) إنشاء HTML للإيصال بتنسيق محسّن
            font_settings = {
                'header_font': 'Arial',  # خط العناوين الرئيسية
                'header_size': '12pt',
                'label_font': 'Arial',  # خط التسميات
                'label_size': '20pt',
                'body_font': 'Times New Roman',  # خط النص العادي
                'body_size': '16pt',                
                'signature_font': 'Arial',
                'signature_size': '16pt'
            }
                    
            html = f"""
            <!doctype html>
            <html dir="rtl" lang="ar">
            <head>
            <meta charset="utf-8">
            <style>
            body {{
                    font-family: {font_settings['body_font']};
                    font-size: {font_settings['body_size']};
                    margin: 0;
                    padding: 20px;
                    direction: rtl;
                }}
            .header {{
                font-family: '{font_settings['header_font']}';
                font-size: {font_settings['header_size']};
                
                }}
            .label {{
                text-align: center;
                margin-bottom: 30px;
                }}
            .label h1 {{
                font-family: '{font_settings['label_font']}';
                font-size: {font_settings['label_size']};                
                }}
            .container {{
                margin-bottom: 20px;                
                padding: 15px;                
                font-family: '{font_settings['body_font']}';
                font-size: {font_settings['body_size']};
                }}
            .footer {{
                    margin-top: 30px;
                    text-align: center;
                    float: left;
                    font-family: '{font_settings['signature_font']}';
                    font-size: {font_settings['signature_size']};
                }}
            </style>
            </head>
            <body>
                <div class="header">
                    <p> مركز النور لتعليم اللغات و الحاسب الآلي </p>
                    <p style = "margin-right: 150px;"> إدارة الأستاذ/ محمد عبدالعزيز </p>
                    <p style = "margin-right: 10px;"> 01068888888 - 01268888888 </p>
                <\div>
                <div class="label">
                    <h1>إيصال استلام نقدية</h1>
                </div>
            
                <div class="container">
                    <p><strong>:  التاريخ </strong> &nbsp;  {date_time_arabic}</p>
                    <p><strong>:   استلمت أنا الأستاذ </strong> {teacher.name} &nbsp;</p>
                    <p><strong>:  المبلغ </strong> &nbsp;  {amount_str_arabic}  جنيه </p>
                    <p><strong>:  المبلغ كتابة </strong> {amount_words} &nbsp; فقط لاغير </p>
                    <p><strong>:  وذلك عن شهر </strong> {month} &nbsp;</p>                    
                </div>            
                <div class="footer">                    
                    <p><strong> توقيع المستلم </strong></p>
                </div>
            </body>
            </html>
    
            """

            # 5) إعداد الطابعة (A5) والطباعة
            printer = QPrinter(QPrinter.HighResolution)
            
            # تحديد حجم الصفحة إلى A5
            try:
                printer.setPageSize(QPrinter.A5)
            except Exception:
                try:
                    from PyQt5.QtPrintSupport import QPrinter as _P
                    printer.setPageSize(_P.A5)
                except Exception:
                    pass

            printer.setOrientation(QPrinter.Portrait)
            
            # تحسين إعدادات الطباعة
            printer.setPageMargins(6, 6, 3, 6, QPrinter.Millimeter)
            printer.setFullPage(False)

            # إظهار مربع اختيار الطابعة
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                doc = QTextDocument()
                doc.setHtml(html)
                
                # ضبط هوامش المستند
                doc.setDocumentMargin(5)
                
                # اطبع المستند مباشرة إلى الطابعة المحددة
                doc.print_(printer)
                QtWidgets.QMessageBox.information(self, "نجاح", "تم إرسال الإيصال للطابعة بنجاح.")
            else:
                QtWidgets.QMessageBox.information(self, "ملغي", "تم إلغاء عملية الطباعة.")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "خطأ أثناء الطباعة", str(e))
    
    # =============================== End Printing =========================
    
    def highlight_active_button(self, active_button):
        for btn in self.nav_buttons:
            if btn == active_button:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0078d7;
                        color: white;
                        font-family: 'Arial';
                        font-size: 14pt;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: none;                        
                        font-family: 'Arial';
                        font-size: 14pt;
                        font-weight: bold;
                    }
                """)

    
def main():
    app = QtWidgets.QApplication(sys.argv)
    Window = Main()
    Window.show()
    app.exec_()
if __name__ == '__main__':
    main()
    
        