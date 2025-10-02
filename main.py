#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة شؤون الموظفين والعلاوات السنوية
الملف الرئيسي لتشغيل التطبيق

المرحلة الأولى: البنية الأساسية
- قاعدة بيانات SQLite محلية متكاملة
- واجهة إضافة موظف جديد
- واجهة عرض قائمة الموظفين مع الفلترة
- ملف الموظف الأساسي
- التصميم العصري بألوان كلاسيكية وخطوط كبيرة
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

# إضافة مسار المشروع إلى sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def check_dependencies():
    """
    التحقق من توفر المكتبات المطلوبة
    """
    required_packages = [
        'customtkinter',
        'PIL',
        'sqlite3'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'sqlite3':
                import sqlite3
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        error_msg = "المكتبات التالية غير مثبتة:\n"
        error_msg += "\n".join(f"- {pkg}" for pkg in missing_packages)
        error_msg += "\n\nيرجى تثبيتها باستخدام:\n"
        error_msg += "pip install -r requirements.txt"
        
        # إنشاء نافذة خطأ بسيطة
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("مكتبات مفقودة", error_msg)
        root.destroy()
        return False
    
    return True

def main():
    """
    الدالة الرئيسية لتشغيل التطبيق
    """
    # التحقق من المكتبات
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # استيراد وتشغيل التطبيق
        from ui.main_window import MainWindow
        
        # إنشاء وتشغيل التطبيق
        app = MainWindow()
        app.run()
    
    except Exception as e:
        # إنشاء نافذة خطأ
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "خطأ في التطبيق",
            f"حدث خطأ أثناء تشغيل التطبيق:\n\n{str(e)}\n\nيرجى التأكد من تثبيت جميع المكتبات المطلوبة."
        )
        root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    main()

