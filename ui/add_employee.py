# -*- coding: utf-8 -*-
"""
نافذة إضافة موظف جديد
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import date
import os
import sys

# إضافة مسار المشروع إلى sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import *
from ui.components.form_components import *
from database.salary_data import ACADEMIC_DEGREES, JOB_CATEGORIES, TRACKING_INDICATORS
from models.employee import Employee

class AddEmployeeWindow(ctk.CTkToplevel):
    def __init__(self, parent, db_manager):
        """
        تهيئة نافذة إضافة موظف جديد
        """
        super().__init__(parent)
        
        self.db_manager = db_manager
        
        # إعدادات النافذة
        self.title("إضافة موظف جديد")
        self.geometry("800x700")
        self.configure(fg_color=COLORS['bg_primary'])
        self.resizable(False, False)
        
        # جعل النافذة في المقدمة
        self.transient(parent)
        self.grab_set()
        
        # إعداد الواجهة
        self.setup_ui()
    
    def setup_ui(self):
        """
        إعداد واجهة المستخدم
        """
        # إطار التمرير الرئيسي
        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS['bg_primary']
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # العنوان
        title_label = ArabicLabel(
            self.main_frame,
            text="إضافة موظف جديد",
            style="title"
        )
        title_label.pack(pady=20)
        
        # إطار النموذج
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_card'])
        self.form_frame.pack(fill="x", padx=20, pady=10)
        
        # إعداد الشبكة للنموذج
        self.form_frame.grid_columnconfigure(1, weight=1)
        
        # إنشاء حقول النموذج
        self.create_form_fields()
        
        # أزرار الإجراءات
        self.create_action_buttons()
    
    def create_form_fields(self):
        """
        إنشاء حقول النموذج
        """
        row = 0
        
        # الاسم الرباعي واللقب
        self.name_field = FormField(
            self.form_frame,
            label_text="الاسم الرباعي واللقب:",
            field_type="entry",
            placeholder="أدخل الاسم الكامل للموظف"
        )
        self.name_field.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        row += 1
        
        # تاريخ المباشرة بالوظيفة
        ArabicLabel(self.form_frame, text="تاريخ المباشرة بالوظيفة:", style="normal").grid(
            row=row, column=0, sticky="e", padx=(20, 10), pady=10
        )
        self.start_date_picker = DatePicker(self.form_frame)
        self.start_date_picker.grid(row=row, column=1, sticky="ew", padx=(0, 20), pady=10)
        row += 1
        
        # تاريخ آخر استحقاق للعلاوة
        ArabicLabel(self.form_frame, text="تاريخ آخر استحقاق للعلاوة:", style="normal").grid(
            row=row, column=0, sticky="e", padx=(20, 10), pady=10
        )
        self.last_entitlement_picker = DatePicker(self.form_frame)
        self.last_entitlement_picker.grid(row=row, column=1, sticky="ew", padx=(0, 20), pady=10)
        row += 1
        
        # الشهادة العلمية
        self.degree_field = FormField(
            self.form_frame,
            label_text="الشهادة العلمية:",
            field_type="combobox",
            values=ACADEMIC_DEGREES
        )
        self.degree_field.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        row += 1
        
        # صنف الوظيفة
        self.category_field = FormField(
            self.form_frame,
            label_text="صنف الوظيفة:",
            field_type="combobox",
            values=JOB_CATEGORIES
        )
        self.category_field.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        row += 1
        
        # العنوان الوظيفي
        self.title_field = FormField(
            self.form_frame,
            label_text="العنوان الوظيفي:",
            field_type="entry",
            placeholder="مثال: مدرس، موظف إداري، فني"
        )
        self.title_field.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        row += 1
        
        # الدرجة الوظيفية
        self.grade_field = FormField(
            self.form_frame,
            label_text="الدرجة الوظيفية:",
            field_type="combobox",
            values=[str(i) for i in range(1, 11)]
        )
        self.grade_field.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        row += 1
        
        # المرحلة الوظيفية
        self.stage_field = FormField(
            self.form_frame,
            label_text="المرحلة الوظيفية:",
            field_type="combobox",
            values=[str(i) for i in range(1, 12)]
        )
        self.stage_field.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        row += 1
        
        # مؤشر تتبع العلاوة
        self.indicator_field = FormField(
            self.form_frame,
            label_text="مؤشر تتبع العلاوة:",
            field_type="combobox",
            values=TRACKING_INDICATORS
        )
        self.indicator_field.grid(row=row, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        row += 1
        
        # ملاحظات
        ArabicLabel(self.form_frame, text="ملاحظات:", style="normal").grid(
            row=row, column=0, sticky="ne", padx=(20, 10), pady=10
        )
        self.notes_field = ctk.CTkTextbox(
            self.form_frame,
            height=80,
            font=get_font('arabic', 'normal')
        )
        self.notes_field.grid(row=row, column=1, sticky="ew", padx=(0, 20), pady=10)
        row += 1
    
    def create_action_buttons(self):
        """
        إنشاء أزرار الإجراءات
        """
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # زر الحفظ
        save_btn = ArabicButton(
            buttons_frame,
            text="💾 حفظ الموظف",
            style="success",
            command=self.save_employee,
            height=50,
            font=get_font('arabic', 'large', 'bold')
        )
        save_btn.grid(row=0, column=0, padx=10, sticky="ew")
        
        # زر الإلغاء
        cancel_btn = ArabicButton(
            buttons_frame,
            text="❌ إلغاء",
            style="danger",
            command=self.destroy,
            height=50,
            font=get_font('arabic', 'large', 'bold')
        )
        cancel_btn.grid(row=0, column=1, padx=10, sticky="ew")
    
    def validate_form(self) -> bool:
        """
        التحقق من صحة بيانات النموذج
        """
        # التحقق من الحقول المطلوبة
        if not self.name_field.get_value().strip():
            messagebox.showerror("خطأ", "يرجى إدخال اسم الموظف")
            return False
        
        if not self.degree_field.get_value():
            messagebox.showerror("خطأ", "يرجى اختيار الشهادة العلمية")
            return False
        
        if not self.category_field.get_value():
            messagebox.showerror("خطأ", "يرجى اختيار صنف الوظيفة")
            return False
        
        if not self.title_field.get_value().strip():
            messagebox.showerror("خطأ", "يرجى إدخال العنوان الوظيفي")
            return False
        
        if not self.grade_field.get_value():
            messagebox.showerror("خطأ", "يرجى اختيار الدرجة الوظيفية")
            return False
        
        if not self.stage_field.get_value():
            messagebox.showerror("خطأ", "يرجى اختيار المرحلة الوظيفية")
            return False
        
        if not self.indicator_field.get_value():
            messagebox.showerror("خطأ", "يرجى اختيار مؤشر تتبع العلاوة")
            return False
        
        # التحقق من صحة التواريخ
        start_date = self.start_date_picker.get_date()
        last_entitlement_date = self.last_entitlement_picker.get_date()
        
        if last_entitlement_date < start_date:
            messagebox.showerror("خطأ", "تاريخ آخر استحقاق لا يمكن أن يكون قبل تاريخ المباشرة")
            return False
        
        return True
    
    def save_employee(self):
        """
        حفظ بيانات الموظف الجديد
        """
        if not self.validate_form():
            return
        
        try:
            # جمع بيانات الموظف
            employee_data = {
                'full_name': self.name_field.get_value().strip(),
                'start_date': self.start_date_picker.get_date().strftime('%Y-%m-%d'),
                'last_entitlement_date': self.last_entitlement_picker.get_date().strftime('%Y-%m-%d'),
                'academic_degree': self.degree_field.get_value(),
                'job_category': self.category_field.get_value(),
                'job_title': self.title_field.get_value().strip(),
                'current_grade': int(self.grade_field.get_value()),
                'current_stage': int(self.stage_field.get_value()),
                'tracking_indicator': self.indicator_field.get_value(),
                'notes': self.notes_field.get("1.0", "end-1c")
            }
            
            # حفظ في قاعدة البيانات
            employee_id = self.db_manager.add_employee(employee_data)
            
            if employee_id:
                messagebox.showinfo("نجح", f"تم حفظ الموظف بنجاح\nرقم الموظف: {employee_id}")
                self.clear_form()
            else:
                messagebox.showerror("خطأ", "فشل في حفظ بيانات الموظف")
        
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ البيانات:\n{str(e)}")
    
    def clear_form(self):
        """
        مسح النموذج
        """
        # مسح الحقول النصية
        self.name_field.field.delete(0, 'end')
        self.title_field.field.delete(0, 'end')
        
        # إعادة تعيين القوائم المنسدلة
        self.degree_field.field.set("")
        self.category_field.field.set("")
        self.grade_field.field.set("")
        self.stage_field.field.set("")
        self.indicator_field.field.set("")
        
        # إعادة تعيين التواريخ
        today = date.today()
        self.start_date_picker.set_date(today)
        self.last_entitlement_picker.set_date(today)
        
        # مسح الملاحظات
        self.notes_field.delete("1.0", "end")

