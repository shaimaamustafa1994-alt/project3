# -*- coding: utf-8 -*-
"""
نافذة ملف الموظف الشخصي
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import sys

# إضافة مسار المشروع إلى sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import *
from ui.components.form_components import *
from models.employee import Employee
from database.salary_data import get_salary
from models.calculation_engine import CalculationEngine

class EmployeeProfileWindow(ctk.CTkToplevel):
    def __init__(self, parent, db_manager, employee_id):
        """
        تهيئة نافذة ملف الموظف
        """
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.employee_id = employee_id
        self.employee = None
        
        # إعدادات النافذة
        self.title("ملف الموظف")
        self.geometry("1000x800")
        self.configure(fg_color=COLORS['bg_primary'])
        
        # جعل النافذة في المقدمة
        self.transient(parent)
        self.grab_set()
        
        # إعداد الواجهة
        self.setup_ui()
        
        # تحميل بيانات الموظف
        self.load_employee(employee_id)
    
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
        
        # قسم الرأس
        self.create_header_section()
        
        # قسم المؤشرات الرئيسية
        self.create_metrics_section()
        
        # قسم السجلات التاريخية
        self.create_history_section()
    
    def create_header_section(self):
        """
        إنشاء قسم الرأس
        """
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_card'])
        header_frame.pack(fill="x", pady=20)
        
        # إعداد الشبكة
        header_frame.grid_columnconfigure(1, weight=1)
        
        # إطار الصورة
        photo_frame = ctk.CTkFrame(header_frame, width=150, height=150, fg_color=COLORS['light_gray'])
        photo_frame.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="n")
        photo_frame.grid_propagate(False)
        
        # صورة الموظف (افتراضية)
        self.photo_label = ArabicLabel(photo_frame, text="👤", style="title")
        self.photo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # زر تحميل الصورة
        upload_btn = ArabicButton(
            header_frame,
            text="📷 تحميل صورة",
            style="secondary",
            command=self.upload_photo,
            width=120,
            height=30
        )
        upload_btn.grid(row=3, column=0, padx=20, pady=(0, 20))
        
        # معلومات الموظف الأساسية
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="ew", padx=20, pady=20)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # اسم الموظف
        self.name_label = ArabicLabel(info_frame, text="", style="title")
        self.name_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=10)
        
        # الصنف الوظيفي
        ArabicLabel(info_frame, text="الصنف الوظيفي:", style="normal").grid(
            row=1, column=0, sticky="e", padx=(0, 10), pady=5
        )
        self.category_label = ArabicLabel(info_frame, text="", style="heading")
        self.category_label.grid(row=1, column=1, sticky="w", pady=5)
        
        # العنوان الوظيفي
        ArabicLabel(info_frame, text="العنوان الوظيفي:", style="normal").grid(
            row=2, column=0, sticky="e", padx=(0, 10), pady=5
        )
        self.title_label = ArabicLabel(info_frame, text="", style="heading")
        self.title_label.grid(row=2, column=1, sticky="w", pady=5)
        
        # الشهادة العلمية
        ArabicLabel(info_frame, text="الشهادة العلمية:", style="normal").grid(
            row=3, column=0, sticky="e", padx=(0, 10), pady=5
        )
        self.degree_label = ArabicLabel(info_frame, text="", style="heading")
        self.degree_label.grid(row=3, column=1, sticky="w", pady=5)
        
        # مؤشر الحالة
        self.status_label = ArabicLabel(info_frame, text="🟢 في الخدمة", style="normal")
        self.status_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)
        
        # زر التعديل
        edit_btn = ArabicButton(
            header_frame,
            text="✏️ تعديل البيانات الأساسية",
            style="primary",
            command=self.edit_basic_info,
            height=40
        )
        edit_btn.grid(row=1, column=1, sticky="e", padx=20, pady=5)
    
    def create_metrics_section(self):
        """
        إنشاء قسم المؤشرات الرئيسية
        """
        metrics_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=20)
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # بطاقة الدرجة والمرحلة الحالية
        self.current_card = InfoCard(
            metrics_frame,
            title="الدرجة والمرحلة الحالية",
            value="",
            icon="🏆",
            style="primary"
        )
        self.current_card.grid(row=0, column=0, padx=10, sticky="ew")
        
        # بطاقة الاستحقاق القادم
        self.next_card = InfoCard(
            metrics_frame,
            title="الاستحقاق القادم",
            value="",
            icon="📅",
            style="success"
        )
        self.next_card.grid(row=0, column=1, padx=10, sticky="ew")
        
        # بطاقة الخدمة الفعلية
        self.service_card = InfoCard(
            metrics_frame,
            title="الخدمة الفعلية",
            value="",
            icon="⏰",
            style="warning"
        )
        self.service_card.grid(row=0, column=2, padx=10, sticky="ew")
    
    def create_history_section(self):
        """
        إنشاء قسم السجلات التاريخية
        """
        history_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_card'])
        history_frame.pack(fill="x", pady=20)
        
        # عنوان القسم
        ArabicLabel(history_frame, text="السجلات التاريخية", style="subtitle").pack(pady=20)
        
        # نظام التبويبات
        self.tabview = ctk.CTkTabview(history_frame, height=300)
        self.tabview.pack(fill="x", padx=20, pady=20)
        
        # تبويب المسار الوظيفي
        self.career_tab = self.tabview.add("المسار الوظيفي")
        self.create_career_timeline()
        
        # تبويب الأحداث المهنية
        self.events_tab = self.tabview.add("الأحداث المهنية")
        self.create_events_list()
    
    def create_career_timeline(self):
        """
        إنشاء الخط الزمني للمسار الوظيفي
        """
        timeline_frame = ctk.CTkScrollableFrame(self.career_tab, height=250)
        timeline_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # سيتم ملء هذا القسم بالبيانات الفعلية عند تحميل الموظف
        self.timeline_frame = timeline_frame
        
        # رسالة افتراضية
        placeholder_label = ArabicLabel(
            timeline_frame,
            text="سيتم عرض المسار الوظيفي هنا في المرحلة القادمة",
            style="secondary"
        )
        placeholder_label.pack(pady=50)
    
    def create_events_list(self):
        """
        إنشاء قائمة الأحداث المهنية
        """
        events_frame = ctk.CTkScrollableFrame(self.events_tab, height=250)
        events_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # سيتم ملء هذا القسم بالبيانات الفعلية عند تحميل الموظف
        self.events_frame = events_frame
        
        # رسالة افتراضية
        placeholder_label = ArabicLabel(
            events_frame,
            text="سيتم عرض الأحداث المهنية هنا في المرحلة القادمة",
            style="secondary"
        )
        placeholder_label.pack(pady=50)
    
    def load_employee(self, employee_id):
        """
        تحميل بيانات الموظف
        """
        try:
            # الحصول على بيانات الموظف
            employee_data = self.db_manager.get_employee_by_id(employee_id)
            
            if not employee_data:
                messagebox.showerror("خطأ", "لم يتم العثور على الموظف")
                self.destroy()
                return
            
            # إنشاء كائن الموظف
            self.employee = Employee(employee_data)
            self.employee_id = employee_id
            
            # تحديث الواجهة
            self.update_ui()
        
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل بيانات الموظف:\n{str(e)}")
    
    def update_ui(self):
        """
        تحديث واجهة المستخدم ببيانات الموظف
        """
        if not self.employee:
            return
        
        # تحديث قسم الرأس
        self.name_label.configure(text=self.employee.full_name)
        self.category_label.configure(text=self.employee.job_category)
        self.title_label.configure(text=self.employee.job_title)
        self.degree_label.configure(text=self.employee.academic_degree)
        
        # تحديث المؤشرات الرئيسية باستخدام المحرك الذكي
        self.update_cards_with_engine()
        
        # تحديث عنوان النافذة
        self.title(f"ملف الموظف - {self.employee.full_name}")
    
    def update_cards_with_engine(self):
        """
        تحديث البطاقات باستخدام المحرك الذكي للحسابات
        """
        try:
            # إنشاء المحرك الذكي
            calc_engine = CalculationEngine(self.db_manager)
            
            # الحصول على معلومات الاستحقاق الكاملة
            entitlement_info = calc_engine.get_complete_entitlement_info(self.employee_id)
            
            # تحديث بطاقة الدرجة والمرحلة الحالية
            current_info = f"الدرجة {entitlement_info['current_grade']} - المرحلة {entitlement_info['current_stage']}\n"
            current_info += f"الراتب: {entitlement_info['current_salary']:,} دينار\n"
            current_info += f"تاريخ آخر استحقاق: {entitlement_info['last_entitlement_date'].strftime('%d/%m/%Y')}\n"
            current_info += f"المؤشر: {entitlement_info['current_indicator']}"
            self.current_card.update_value(current_info)
            
            # تحديث بطاقة الاستحقاق القادم
            next_info = f"{entitlement_info['next_entitlement_type']}\n"
            if entitlement_info['next_entitlement_type'] != "لا يوجد استحقاق":
                next_info += f"الدرجة {entitlement_info['next_grade']} - المرحلة {entitlement_info['next_stage']}\n"
                next_info += f"الراتب: {entitlement_info['next_salary']:,} دينار\n"
                next_info += f"التاريخ: {entitlement_info['next_entitlement_date'].strftime('%d/%m/%Y')}\n"
                next_info += f"المؤشر الجديد: {entitlement_info['updated_indicator']}"
            else:
                next_info += "وصل الموظف للحد الأقصى"
            self.next_card.update_value(next_info)
            
            # تحديث بطاقة الخدمة الفعلية
            service = entitlement_info['effective_service']
            service_info = f"{service['years']} سنة، {service['months']} شهر، {service['days']} يوم"
            self.service_card.update_value(service_info)
            
        except Exception as e:
            print(f"خطأ في تحديث البطاقات: {e}")
            # في حالة الخطأ، استخدم الطريقة القديمة
            self.update_cards_fallback()
    
    def update_cards_fallback(self):
        """
        تحديث البطاقات بالطريقة القديمة (في حالة فشل المحرك الذكي)
        """
        # الدرجة والمرحلة الحالية
        current_info = f"{self.employee.get_grade_stage_text()}\n"
        current_info += f"الراتب: {self.employee.get_current_salary_text()}\n"
        current_info += f"تاريخ الاستحقاق: {self.employee.last_entitlement_date.strftime('%d/%m/%Y')}"
        self.current_card.update_value(current_info)
        
        # الاستحقاق القادم
        next_type = self.employee.get_next_entitlement_type()
        next_grade, next_stage, next_salary = self.employee._calculate_next_position(next_type)
        next_info = f"{next_type}\n"
        next_info += f"الدرجة {next_grade} - المرحلة {next_stage}\n"
        next_info += f"الراتب: {next_salary:,} دينار\n"
        next_info += "التاريخ: قريباً"
        self.next_card.update_value(next_info)
        
        # الخدمة الفعلية
        self.service_card.update_value(self.employee.get_service_duration_text())
    
    def upload_photo(self):
        """
        تحميل صورة الموظف
        """
        file_path = filedialog.askopenfilename(
            title="اختر صورة الموظف",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # تحميل وتغيير حجم الصورة
                image = Image.open(file_path)
                image = image.resize((120, 120), Image.Resampling.LANCZOS)
                
                # تحويل إلى PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # تحديث التسمية
                self.photo_label.configure(image=photo, text="")
                self.photo_label.image = photo  # الاحتفاظ بمرجع
                
                # حفظ مسار الصورة في قاعدة البيانات
                self.db_manager.update_employee(self.employee_id, {'photo_path': file_path})
                
                messagebox.showinfo("نجح", "تم تحميل الصورة بنجاح")
            
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في تحميل الصورة:\n{str(e)}")
    
    def edit_basic_info(self):
        """
        تعديل البيانات الأساسية
        """
        messagebox.showinfo("قريباً", "ستتوفر ميزة تعديل البيانات في المرحلة القادمة")
    
    def refresh_data(self):
        """
        تحديث البيانات
        """
        if self.employee_id:
            self.load_employee(self.employee_id)
