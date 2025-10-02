# -*- coding: utf-8 -*-
"""
نموذج الموظف - يحتوي على منطق العمل الخاص بالموظفين
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from database.salary_data import get_salary, get_allowance_amount, get_promotion_years, get_max_stage

class Employee:
    def __init__(self, employee_data: Dict):
        """
        تهيئة كائن الموظف
        """
        self.id = employee_data.get('id')
        self.full_name = employee_data['full_name']
        self.start_date = self._parse_date(employee_data['start_date'])
        self.last_entitlement_date = self._parse_date(employee_data['last_entitlement_date'])
        self.academic_degree = employee_data['academic_degree']
        self.job_category = employee_data['job_category']
        self.job_title = employee_data['job_title']
        self.current_grade = int(employee_data['current_grade'])
        self.current_stage = int(employee_data['current_stage'])
        self.tracking_indicator = employee_data['tracking_indicator']
        self.photo_path = employee_data.get('photo_path')
        self.status = employee_data.get('status', 'نشط')
        self.notes = employee_data.get('notes', '')
        
        # حساب البيانات المشتقة
        self.current_salary = get_salary(self.current_grade, self.current_stage)
        self.allowance_amount = get_allowance_amount(self.current_grade)
    
    def _parse_date(self, date_str):
        """
        تحويل النص إلى تاريخ
        """
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                try:
                    return datetime.strptime(date_str, '%d/%m/%Y').date()
                except ValueError:
                    return date.today()
        elif isinstance(date_str, date):
            return date_str
        else:
            return date.today()
    
    def get_service_duration(self) -> Tuple[int, int, int]:
        """
        حساب مدة الخدمة الفعلية (سنوات، أشهر، أيام)
        """
        today = date.today()
        delta = today - self.start_date
        
        years = delta.days // 365
        remaining_days = delta.days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        
        return years, months, days
    
    def get_service_duration_text(self) -> str:
        """
        الحصول على نص مدة الخدمة
        """
        years, months, days = self.get_service_duration()
        return f"{years} سنة، {months} شهر، {days} يوم"
    
    def get_current_salary_text(self) -> str:
        """
        الحصول على نص الراتب الحالي
        """
        return f"{self.current_salary:,} دينار"
    
    def get_grade_stage_text(self) -> str:
        """
        الحصول على نص الدرجة والمرحلة
        """
        return f"الدرجة {self.current_grade} - المرحلة {self.current_stage}"
    
    def parse_tracking_indicator(self) -> Tuple[int, int]:
        """
        تحليل مؤشر تتبع العلاوة
        """
        try:
            parts = self.tracking_indicator.split('/')
            total = int(parts[0])
            current = int(parts[1])
            return total, current
        except:
            return 4, 1  # قيمة افتراضية
    
    def get_next_entitlement_type(self) -> str:
        """
        تحديد نوع الاستحقاق القادم (علاوة أو ترفيع)
        """
        total, current = self.parse_tracking_indicator()
        
        # إذا وصل إلى النهاية، فالاستحقاق القادم ترفيع
        if current >= total:
            return "ترفيع"
        else:
            return "علاوة"
    
    def calculate_next_entitlement(self, professional_events: List[Dict] = None) -> Dict:
        """
        حساب الاستحقاق القادم مع تأثير الأحداث المهنية
        """
        # البدء من تاريخ آخر استحقاق
        base_date = self.last_entitlement_date
        
        # المدة الأساسية (12 شهر)
        base_months = 12
        
        # حساب تأثير الأحداث المهنية
        total_impact = 0
        if professional_events:
            for event in professional_events:
                event_date = self._parse_date(event['event_date'])
                # فقط الأحداث بعد تاريخ آخر استحقاق
                if event_date >= base_date:
                    total_impact += event.get('impact_months', 0)
        
        # المدة النهائية
        final_months = base_months + total_impact
        
        # حساب تاريخ الاستحقاق القادم
        next_date = base_date + timedelta(days=final_months * 30)  # تقريبي
        
        # تحديد نوع الاستحقاق
        entitlement_type = self.get_next_entitlement_type()
        
        # حساب الدرجة والمرحلة القادمة
        next_grade, next_stage, next_salary = self._calculate_next_position(entitlement_type)
        
        return {
            'type': entitlement_type,
            'date': next_date,
            'next_grade': next_grade,
            'next_stage': next_stage,
            'next_salary': next_salary,
            'total_impact_months': total_impact
        }
    
    def _calculate_next_position(self, entitlement_type: str) -> Tuple[int, int, float]:
        """
        حساب الدرجة والمرحلة والراتب القادم
        """
        if entitlement_type == "علاوة":
            # نفس الدرجة، مرحلة أعلى
            next_grade = self.current_grade
            next_stage = min(self.current_stage + 1, get_max_stage(self.current_grade))
            next_salary = get_salary(next_grade, next_stage)
        else:  # ترفيع
            # درجة أعلى، مرحلة 1
            next_grade = max(1, self.current_grade - 1)  # الدرجات تقل بالترفيع
            next_stage = 1
            next_salary = get_salary(next_grade, next_stage)
        
        return next_grade, next_stage, next_salary
    
    def update_tracking_indicator_after_entitlement(self, entitlement_type: str) -> str:
        """
        تحديث مؤشر التتبع بعد الحصول على استحقاق
        """
        total, current = self.parse_tracking_indicator()
        
        if entitlement_type == "علاوة":
            # زيادة العداد الحالي
            new_current = current + 1
            if new_current > total:
                new_current = total
            return f"{total}/{new_current}"
        else:  # ترفيع
            # إعادة تعيين المؤشر حسب الدرجة الجديدة
            next_grade = max(1, self.current_grade - 1)
            promotion_years = get_promotion_years(next_grade)
            
            if promotion_years == 4:
                return "4/1"
            elif promotion_years == 5:
                return "5/1"
            else:  # الدرجة الأولى
                return "11/1"
    
    def to_dict(self) -> Dict:
        """
        تحويل الكائن إلى قاموس
        """
        return {
            'id': self.id,
            'full_name': self.full_name,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else '',
            'last_entitlement_date': self.last_entitlement_date.strftime('%Y-%m-%d') if self.last_entitlement_date else '',
            'academic_degree': self.academic_degree,
            'job_category': self.job_category,
            'job_title': self.job_title,
            'current_grade': self.current_grade,
            'current_stage': self.current_stage,
            'tracking_indicator': self.tracking_indicator,
            'photo_path': self.photo_path,
            'status': self.status,
            'notes': self.notes,
            'current_salary': self.current_salary,
            'allowance_amount': self.allowance_amount
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """
        إنشاء كائن موظف من قاموس
        """
        return cls(data)
    
    def get_entitlement_info_with_engine(self, db_manager):
        """
        الحصول على معلومات الاستحقاق باستخدام المحرك الذكي
        """
        from .calculation_engine import CalculationEngine
        
        calc_engine = CalculationEngine(db_manager)
        return calc_engine.get_complete_entitlement_info(self.id)
    
    def process_entitlement_with_engine(self, db_manager):
        """
        معالجة الاستحقاق باستخدام المحرك الذكي
        """
        from .calculation_engine import CalculationEngine
        
        calc_engine = CalculationEngine(db_manager)
        return calc_engine.process_entitlement(self.id)
