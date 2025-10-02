# -*- coding: utf-8 -*-
"""
اختبار المحرك الذكي للحسابات
"""

import sys
import os
from datetime import datetime, timedelta

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database_manager import DatabaseManager
from models.calculation_engine import CalculationEngine

def test_calculation_engine():
    """اختبار المحرك الذكي للحسابات"""
    
    print("🧪 اختبار المحرك الذكي للحسابات")
    print("=" * 50)
    
    # إنشاء قاعدة البيانات
    db_manager = DatabaseManager()
    calc_engine = CalculationEngine(db_manager)
    
    # الحصول على جميع الموظفين
    employees = db_manager.get_all_employees()
    
    if not employees:
        print("❌ لا يوجد موظفين في قاعدة البيانات")
        print("💡 قم بتشغيل sample_data.py أولاً لإضافة بيانات تجريبية")
        return
    
    print(f"📊 عدد الموظفين: {len(employees)}")
    print()
    
    # اختبار كل موظف
    for i, employee in enumerate(employees[:3], 1):  # اختبار أول 3 موظفين فقط
        print(f"👤 الموظف {i}: {employee['full_name']}")
        print("-" * 30)
        
        try:
            # الحصول على معلومات الاستحقاق
            entitlement_info = calc_engine.get_complete_entitlement_info(employee['id'])
            
            print(f"📍 الوضع الحالي:")
            print(f"   الدرجة: {entitlement_info['current_grade']}")
            print(f"   المرحلة: {entitlement_info['current_stage']}")
            print(f"   الراتب: {entitlement_info['current_salary']:,} دينار")
            print(f"   المؤشر: {entitlement_info['current_indicator']}")
            
            print(f"🎯 الاستحقاق القادم:")
            print(f"   النوع: {entitlement_info['next_entitlement_type']}")
            print(f"   التاريخ: {entitlement_info['next_entitlement_date'].strftime('%d/%m/%Y')}")
            
            if entitlement_info['next_entitlement_type'] != "لا يوجد استحقاق":
                print(f"   الدرجة الجديدة: {entitlement_info['next_grade']}")
                print(f"   المرحلة الجديدة: {entitlement_info['next_stage']}")
                print(f"   الراتب الجديد: {entitlement_info['next_salary']:,} دينار")
                print(f"   المؤشر الجديد: {entitlement_info['updated_indicator']}")
            
            service = entitlement_info['effective_service']
            print(f"⏰ الخدمة الفعلية: {service['years']} سنة، {service['months']} شهر، {service['days']} يوم")
            
            print("✅ تم الاختبار بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في الاختبار: {e}")
        
        print()
    
    # اختبار الاستحقاقات القادمة
    print("📅 اختبار الاستحقاقات القادمة")
    print("-" * 30)
    
    try:
        upcoming = db_manager.get_upcoming_entitlements(365)  # خلال سنة
        
        if upcoming:
            print(f"📊 عدد الاستحقاقات القادمة: {len(upcoming)}")
            
            for entitlement in upcoming[:5]:  # أول 5 استحقاقات
                print(f"👤 {entitlement['employee_name']}")
                print(f"   النوع: {entitlement['entitlement_type']}")
                print(f"   التاريخ: {entitlement['entitlement_date'].strftime('%d/%m/%Y')}")
                print(f"   من: {entitlement['current_grade']}/{entitlement['current_stage']}")
                print(f"   إلى: {entitlement['next_grade']}/{entitlement['next_stage']}")
                print()
        else:
            print("📭 لا توجد استحقاقات قادمة")
            
    except Exception as e:
        print(f"❌ خطأ في اختبار الاستحقاقات القادمة: {e}")
    
    print("🎉 انتهى الاختبار!")

if __name__ == "__main__":
    test_calculation_engine()

