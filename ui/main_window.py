# -*- coding: utf-8 -*-
"""
النافذة الرئيسية للتطبيق
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import sys

# إضافة مسار المشروع إلى sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import *
from ui.components.form_components import ArabicLabel, ArabicButton
from ui.add_employee import AddEmployeeWindow
from ui.employees_list import EmployeesListWindow
from ui.employee_profile import EmployeeProfileWindow
from database.database_manager import DatabaseManager

class MainWindow:
    def __init__(self):
        """
        تهيئة النافذة الرئيسية
        """
        # إنشاء النافذة الرئيسية
        self.root = ctk.CTk()
        self.root.title("نظام إدارة شؤون الموظفين والعلاوات السنوية")
        self.root.geometry(f"{DIMENSIONS['window_width']}x{DIMENSIONS['window_height']}")
        self.root.configure(fg_color=COLORS['bg_primary'])
        
        # تطبيق الخط العربي
        self.root.option_add('*Font', get_font('arabic', 'normal'))
        
        # تهيئة قاعدة البيانات
        self.db_manager = DatabaseManager()
        
        # إعداد الواجهة
        self.setup_ui()
        
        # متغيرات النوافذ الفرعية
        self.add_employee_window = None
        self.employees_list_window = None
        self.employee_profile_window = None
    
    def setup_ui(self):
        """
        إعداد واجهة المستخدم
        """
        # إعداد الشبكة الرئيسية
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # الشريط الجانبي
        self.create_sidebar()
        
        # المنطقة الرئيسية
        self.create_main_area()
    
    def create_sidebar(self):
        """
        إنشاء الشريط الجانبي للتنقل
        """
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=DIMENSIONS['sidebar_width'],
            fg_color=COLORS['bg_sidebar'],
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        # عنوان التطبيق
        title_label = ArabicLabel(
            self.sidebar,
            text="نظام إدارة الموظفين",
            style="title"
        )
        title_label.configure(text_color=COLORS['text_white'])
        title_label.pack(pady=30, padx=20)
        
        # أزرار التنقل
        nav_buttons = [
            ("🏠", "الصفحة الرئيسية", self.show_home),
            ("👤", "إضافة موظف جديد", self.show_add_employee),
            ("📋", "قائمة الموظفين", self.show_employees_list),
            ("📊", "الإحصائيات", self.show_statistics),
            ("📅", "الاستحقاقات القادمة", self.show_upcoming_entitlements),
            ("⚙️", "الإعدادات", self.show_settings)
        ]
        
        for icon, text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}  {text}",
                command=command,
                fg_color="transparent",
                hover_color=COLORS['primary_dark'],
                text_color=COLORS['text_white'],
                font=get_font('arabic', 'large'),
                height=50,
                anchor="w"
            )
            btn.pack(pady=5, padx=20, fill="x")
    
    def create_main_area(self):
        """
        إنشاء المنطقة الرئيسية
        """
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=COLORS['bg_secondary'],
            corner_radius=0
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # عرض الصفحة الرئيسية افتراضياً
        self.show_home()
    
    def clear_main_area(self):
        """
        مسح المنطقة الرئيسية
        """
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """
        عرض الصفحة الرئيسية
        """
        self.clear_main_area()
        
        # إطار المحتوى
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # العنوان الرئيسي
        title = ArabicLabel(
            content_frame,
            text="مرحباً بك في نظام إدارة شؤون الموظفين والعلاوات السنوية",
            style="title"
        )
        title.pack(pady=30)
        
        # وصف النظام
        description = ArabicLabel(
            content_frame,
            text="نظام شامل ومتكامل لأتمتة وحوسبة العمليات المعقدة المتعلقة بحساب العلاوات السنوية والترفيعات الوظيفية",
            style="subtitle"
        )
        description.pack(pady=20)
        
        # بطاقات الإحصائيات السريعة
        stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=30)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # الحصول على الإحصائيات
        stats = self.db_manager.get_statistics()
        
        # بطاقة إجمالي الموظفين
        total_card = self.create_stat_card(
            stats_frame,
            "👥",
            "إجمالي الموظفين",
            str(stats.get('total_employees', 0)),
            COLORS['primary']
        )
        total_card.grid(row=0, column=0, padx=10, sticky="ew")
        
        # بطاقة الموظفين التدريسيين
        teaching_count = stats.get('by_category', {}).get('تدريسي', 0)
        teaching_card = self.create_stat_card(
            stats_frame,
            "🎓",
            "الكادر التدريسي",
            str(teaching_count),
            COLORS['success']
        )
        teaching_card.grid(row=0, column=1, padx=10, sticky="ew")
        
        # بطاقة الموظفين الإداريين
        admin_count = stats.get('by_category', {}).get('إداري', 0)
        admin_card = self.create_stat_card(
            stats_frame,
            "💼",
            "الكادر الإداري",
            str(admin_count),
            COLORS['warning']
        )
        admin_card.grid(row=0, column=2, padx=10, sticky="ew")
        
        # أزرار الإجراءات السريعة
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=50)
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # زر إضافة موظف
        add_btn = ArabicButton(
            actions_frame,
            text="👤 إضافة موظف جديد",
            style="primary",
            command=self.show_add_employee,
            height=60,
            font=get_font('arabic', 'large', 'bold')
        )
        add_btn.grid(row=0, column=0, padx=10, sticky="ew")
        
        # زر قائمة الموظفين
        list_btn = ArabicButton(
            actions_frame,
            text="📋 قائمة الموظفين",
            style="secondary",
            command=self.show_employees_list,
            height=60,
            font=get_font('arabic', 'large', 'bold')
        )
        list_btn.grid(row=0, column=1, padx=10, sticky="ew")
        
        # زر الإحصائيات
        stats_btn = ArabicButton(
            actions_frame,
            text="📊 الإحصائيات",
            style="success",
            command=self.show_statistics,
            height=60,
            font=get_font('arabic', 'large', 'bold')
        )
        stats_btn.grid(row=0, column=2, padx=10, sticky="ew")
    
    def create_stat_card(self, parent, icon, title, value, color):
        """
        إنشاء بطاقة إحصائية
        """
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
        
        # الأيقونة
        icon_label = ArabicLabel(card, text=icon, style="title")
        icon_label.configure(text_color=COLORS['text_white'])
        icon_label.pack(pady=(20, 10))
        
        # القيمة
        value_label = ArabicLabel(card, text=value, style="title")
        value_label.configure(text_color=COLORS['text_white'])
        value_label.pack()
        
        # العنوان
        title_label = ArabicLabel(card, text=title, style="normal")
        title_label.configure(text_color=COLORS['text_white'])
        title_label.pack(pady=(5, 20))
        
        return card
    
    def show_add_employee(self):
        """
        عرض نافذة إضافة موظف جديد
        """
        if self.add_employee_window is None or not self.add_employee_window.winfo_exists():
            self.add_employee_window = AddEmployeeWindow(self.root, self.db_manager)
        else:
            self.add_employee_window.focus()
    
    def show_employees_list(self):
        """
        عرض نافذة قائمة الموظفين
        """
        if self.employees_list_window is None or not self.employees_list_window.winfo_exists():
            self.employees_list_window = EmployeesListWindow(self.root, self.db_manager, self.show_employee_profile)
        else:
            self.employees_list_window.focus()
    
    def show_employee_profile(self, employee_id):
        """
        عرض ملف الموظف
        """
        if self.employee_profile_window is None or not self.employee_profile_window.winfo_exists():
            self.employee_profile_window = EmployeeProfileWindow(self.root, self.db_manager, employee_id)
        else:
            self.employee_profile_window.load_employee(employee_id)
            self.employee_profile_window.focus()
    
    def show_statistics(self):
        """
        عرض الإحصائيات
        """
        messagebox.showinfo("قريباً", "ستتوفر هذه الميزة في المرحلة القادمة")
    
    def show_upcoming_entitlements(self):
        """
        عرض الاستحقاقات القادمة
        """
        messagebox.showinfo("قريباً", "ستتوفر هذه الميزة في المرحلة القادمة")
    
    def show_settings(self):
        """
        عرض الإعدادات
        """
        messagebox.showinfo("قريباً", "ستتوفر هذه الميزة في المرحلة القادمة")
    
    def run(self):
        """
        تشغيل التطبيق
        """
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()

