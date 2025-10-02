# -*- coding: utf-8 -*-
"""
بيانات تجريبية لاختبار النظام
"""

from datetime import date, timedelta
from database.database_manager import DatabaseManager

def create_sample_data():
    """
    إنشاء بيانات تجريبية للنظام
    """
    db = DatabaseManager()
    
    # بيانات موظفين تجريبية
    sample_employees = [
        {
            'full_name': 'أحمد محمد علي حسن',
            'start_date': (date.today() - timedelta(days=1825)).strftime('%Y-%m-%d'),  # 5 سنوات
            'last_entitlement_date': (date.today() - timedelta(days=365)).strftime('%Y-%m-%d'),  # سنة واحدة
            'academic_degree': 'ماجستير',
            'job_category': 'تدريسي',
            'job_title': 'مدرس مساعد',
            'current_grade': 7,
            'current_stage': 3,
            'tracking_indicator': '4/3',
            'notes': 'موظف متميز في الأداء'
        },
        {
            'full_name': 'فاطمة عبد الله محمود',
            'start_date': (date.today() - timedelta(days=2920)).strftime('%Y-%m-%d'),  # 8 سنوات
            'last_entitlement_date': (date.today() - timedelta(days=180)).strftime('%Y-%m-%d'),  # 6 أشهر
            'academic_degree': 'بكالوريوس',
            'job_category': 'إداري',
            'job_title': 'موظف إداري أول',
            'current_grade': 5,
            'current_stage': 2,
            'tracking_indicator': '5/2',
            'notes': 'موظفة ملتزمة ودقيقة'
        },
        {
            'full_name': 'محمد سعد الدين يوسف',
            'start_date': (date.today() - timedelta(days=3650)).strftime('%Y-%m-%d'),  # 10 سنوات
            'last_entitlement_date': (date.today() - timedelta(days=90)).strftime('%Y-%m-%d'),  # 3 أشهر
            'academic_degree': 'دكتوراه',
            'job_category': 'تدريسي',
            'job_title': 'أستاذ مساعد',
            'current_grade': 3,
            'current_stage': 5,
            'tracking_indicator': '5/4',
            'notes': 'حاصل على عدة كتب شكر'
        },
        {
            'full_name': 'سارة أحمد محمد علي',
            'start_date': (date.today() - timedelta(days=1460)).strftime('%Y-%m-%d'),  # 4 سنوات
            'last_entitlement_date': (date.today() - timedelta(days=270)).strftime('%Y-%m-%d'),  # 9 أشهر
            'academic_degree': 'دبلوم',
            'job_category': 'فني',
            'job_title': 'فني مختبر',
            'current_grade': 8,
            'current_stage': 4,
            'tracking_indicator': '4/2',
            'notes': 'خبرة عملية ممتازة'
        },
        {
            'full_name': 'عمر خالد عبد الرحمن',
            'start_date': (date.today() - timedelta(days=730)).strftime('%Y-%m-%d'),  # سنتان
            'last_entitlement_date': (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'),  # شهر واحد
            'academic_degree': 'ماجستير',
            'job_category': 'إداري',
            'job_title': 'رئيس قسم',
            'current_grade': 6,
            'current_stage': 1,
            'tracking_indicator': '4/1',
            'notes': 'موظف جديد نسبياً'
        }
    ]
    
    print("إنشاء بيانات تجريبية...")
    
    for emp_data in sample_employees:
        try:
            employee_id = db.add_employee(emp_data)
            print(f"تم إضافة الموظف: {emp_data['full_name']} (ID: {employee_id})")
        except Exception as e:
            print(f"خطأ في إضافة الموظف {emp_data['full_name']}: {str(e)}")
    
    print("تم الانتهاء من إنشاء البيانات التجريبية!")

if __name__ == "__main__":
    create_sample_data()

