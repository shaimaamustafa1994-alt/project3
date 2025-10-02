# -*- coding: utf-8 -*-
"""
نافذة قائمة الموظفين
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
import os
import sys

# إضافة مسار المشروع إلى sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import *
from ui.components.form_components import *
from database.salary_data import JOB_CATEGORIES
from models.employee import Employee

class EmployeesListWindow(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, show_profile_callback):
        """
        تهيئة نافذة قائمة الموظفين
        """
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.show_profile_callback = show_profile_callback
        self.employees_data = []
        
        # إعدادات النافذة
        self.title("قائمة الموظفين")
        self.geometry("1200x700")
        self.configure(fg_color=COLORS['bg_primary'])
        
        # جعل النافذة في المقدمة
        self.transient(parent)
        self.grab_set()
        
        # إعداد الواجهة
        self.setup_ui()
        
        # تحميل البيانات
        self.load_employees()
    
    def setup_ui(self):
        """
        إعداد واجهة المستخدم
        """
        # إطار رئيسي
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # العنوان
        title_label = ArabicLabel(
            main_frame,
            text="قائمة الموظفين",
            style="title"
        )
        title_label.pack(pady=20)
        
        # إطار البحث والفلترة
        self.create_search_filter(main_frame)
        
        # إطار الجدول
        self.create_table(main_frame)
        
        # إطار الأزرار
        self.create_action_buttons(main_frame)
    
    def create_search_filter(self, parent):
        """
        إنشاء إطار البحث والفلترة
        """
        filter_frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'])
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        # إعداد الشبكة
        filter_frame.grid_columnconfigure(1, weight=1)
        
        # حقل البحث
        ArabicLabel(filter_frame, text="البحث:", style="normal").grid(
            row=0, column=0, padx=10, pady=15, sticky="e"
        )
        
        self.search_entry = ArabicEntry(filter_frame, placeholder="ابحث عن موظف...")
        self.search_entry.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # فلتر الصنف الوظيفي
        ArabicLabel(filter_frame, text="الصنف:", style="normal").grid(
            row=0, column=2, padx=10, pady=15, sticky="e"
        )
        
        self.category_filter = ArabicComboBox(
            filter_frame,
            values=["الكل"] + JOB_CATEGORIES,
            width=150,
            command=self.on_filter_change
        )
        self.category_filter.grid(row=0, column=3, padx=10, pady=15)
        self.category_filter.set("الكل")
        
        # زر التحديث
        refresh_btn = ArabicButton(
            filter_frame,
            text="🔄 تحديث",
            style="primary",
            command=self.load_employees,
            width=100
        )
        refresh_btn.grid(row=0, column=4, padx=10, pady=15)
    
    def create_table(self, parent):
        """
        إنشاء جدول الموظفين
        """
        # إطار الجدول
        table_frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_card'])
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # إنشاء Treeview للجدول
        columns = (
            "id", "name", "job_title", "category", "grade_stage", 
            "next_event", "next_date", "service_duration"
        )
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # تعريف العناوين
        headers = {
            "id": "الرقم",
            "name": "اسم الموظف",
            "job_title": "العنوان الوظيفي",
            "category": "الصنف",
            "grade_stage": "الدرجة/المرحلة",
            "next_event": "الحدث القادم",
            "next_date": "تاريخ الاستحقاق",
            "service_duration": "الخدمة الفعلية"
        }
        
        # إعداد العناوين والأعمدة
        for col in columns:
            self.tree.heading(col, text=headers[col], anchor="center")
            self.tree.column(col, width=120, anchor="center")
        
        # تخصيص عرض الأعمدة
        self.tree.column("id", width=60)
        self.tree.column("name", width=200)
        self.tree.column("job_title", width=150)
        self.tree.column("category", width=100)
        self.tree.column("grade_stage", width=120)
        self.tree.column("next_event", width=100)
        self.tree.column("next_date", width=120)
        self.tree.column("service_duration", width=150)
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # تخطيط الجدول
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # ربط الأحداث
        self.tree.bind("<Double-1>", self.on_row_double_click)
    
    def create_action_buttons(self, parent):
        """
        إنشاء أزرار الإجراءات
        """
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=10)
        buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # زر عرض الملف
        view_btn = ArabicButton(
            buttons_frame,
            text="👁️ عرض ملف الموظف",
            style="primary",
            command=self.view_employee_profile,
            height=45
        )
        view_btn.grid(row=0, column=0, padx=10, sticky="ew")
        
        # زر تعديل البيانات
        edit_btn = ArabicButton(
            buttons_frame,
            text="✏️ تعديل البيانات",
            style="secondary",
            command=self.edit_employee,
            height=45
        )
        edit_btn.grid(row=0, column=1, padx=10, sticky="ew")
        
        # زر حذف الموظف
        delete_btn = ArabicButton(
            buttons_frame,
            text="🗑️ حذف الموظف",
            style="danger",
            command=self.delete_employee,
            height=45
        )
        delete_btn.grid(row=0, column=2, padx=10, sticky="ew")
    
    def load_employees(self):
        """
        تحميل بيانات الموظفين
        """
        try:
            # مسح البيانات الحالية
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # الحصول على البيانات من قاعدة البيانات
            self.employees_data = self.db_manager.get_all_employees()
            
            # عرض البيانات في الجدول
            for emp_data in self.employees_data:
                employee = Employee(emp_data)
                
                # حساب الاستحقاق القادم (مبسط للمرحلة الأولى)
                next_entitlement = employee.get_next_entitlement_type()
                next_date = "قريباً"  # سيتم حسابه في المرحلة الثانية
                
                # إدراج البيانات في الجدول
                self.tree.insert("", "end", values=(
                    employee.id,
                    employee.full_name,
                    employee.job_title,
                    employee.job_category,
                    employee.get_grade_stage_text(),
                    next_entitlement,
                    next_date,
                    employee.get_service_duration_text()
                ))
        
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل بيانات الموظفين:\n{str(e)}")
    
    def on_search_change(self, event=None):
        """
        عند تغيير نص البحث
        """
        search_text = self.search_entry.get().strip()
        self.filter_employees(search_text=search_text)
    
    def on_filter_change(self, value=None):
        """
        عند تغيير فلتر الصنف
        """
        category = self.category_filter.get()
        if category == "الكل":
            category = None
        self.filter_employees(category=category)
    
    def filter_employees(self, search_text="", category=None):
        """
        فلترة الموظفين
        """
        # مسح الجدول
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # تطبيق الفلاتر
        for emp_data in self.employees_data:
            employee = Employee(emp_data)
            
            # فلتر البحث
            if search_text and search_text.lower() not in employee.full_name.lower():
                continue
            
            # فلتر الصنف
            if category and employee.job_category != category:
                continue
            
            # عرض الموظف
            next_entitlement = employee.get_next_entitlement_type()
            next_date = "قريباً"
            
            self.tree.insert("", "end", values=(
                employee.id,
                employee.full_name,
                employee.job_title,
                employee.job_category,
                employee.get_grade_stage_text(),
                next_entitlement,
                next_date,
                employee.get_service_duration_text()
            ))
    
    def get_selected_employee_id(self):
        """
        الحصول على معرف الموظف المحدد
        """
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار موظف من القائمة")
            return None
        
        item = self.tree.item(selection[0])
        return item['values'][0]  # معرف الموظف
    
    def on_row_double_click(self, event):
        """
        عند النقر المزدوج على صف
        """
        self.view_employee_profile()
    
    def view_employee_profile(self):
        """
        عرض ملف الموظف
        """
        employee_id = self.get_selected_employee_id()
        if employee_id:
            self.show_profile_callback(employee_id)
    
    def edit_employee(self):
        """
        تعديل بيانات الموظف
        """
        employee_id = self.get_selected_employee_id()
        if employee_id:
            messagebox.showinfo("قريباً", "ستتوفر ميزة التعديل في المرحلة القادمة")
    
    def delete_employee(self):
        """
        حذف الموظف
        """
        employee_id = self.get_selected_employee_id()
        if not employee_id:
            return
        
        # تأكيد الحذف
        result = messagebox.askyesno(
            "تأكيد الحذف",
            "هل أنت متأكد من حذف هذا الموظف؟\nلا يمكن التراجع عن هذا الإجراء."
        )
        
        if result:
            try:
                success = self.db_manager.delete_employee(employee_id)
                if success:
                    messagebox.showinfo("نجح", "تم حذف الموظف بنجاح")
                    self.load_employees()  # إعادة تحميل القائمة
                else:
                    messagebox.showerror("خطأ", "فشل في حذف الموظف")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء حذف الموظف:\n{str(e)}")

