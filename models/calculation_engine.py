# -*- coding: utf-8 -*-
"""
المحرك الذكي للحسابات (Intelligent Calculation Engine)
يقوم بحساب العلاوات والترفيعات بناءً على القواعد المعقدة للنظام
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Tuple, Optional
import logging

class CalculationEngine:
    """المحرك الذكي لحساب العلاوات والترفيعات"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
        
        # قواعد الترفيع حسب الدرجة
        self.promotion_rules = {
            # الدرجات 6-10: تحتاج 4 سنوات (3 علاوات + 1 ترفيع)
            10: {'years_for_promotion': 4, 'allowances_before_promotion': 3},
            9: {'years_for_promotion': 4, 'allowances_before_promotion': 3},
            8: {'years_for_promotion': 4, 'allowances_before_promotion': 3},
            7: {'years_for_promotion': 4, 'allowances_before_promotion': 3},
            6: {'years_for_promotion': 4, 'allowances_before_promotion': 3},
            
            # الدرجات 2-5: تحتاج 5 سنوات (4 علاوات + 1 ترفيع)
            5: {'years_for_promotion': 5, 'allowances_before_promotion': 4},
            4: {'years_for_promotion': 5, 'allowances_before_promotion': 4},
            3: {'years_for_promotion': 5, 'allowances_before_promotion': 4},
            2: {'years_for_promotion': 5, 'allowances_before_promotion': 4},
            
            # الدرجة الأولى: لا يوجد ترفيع، فقط علاوات حتى المرحلة 11
            1: {'years_for_promotion': None, 'allowances_before_promotion': None}
        }
    
    def parse_tracking_indicator(self, indicator: str) -> Tuple[int, int]:
        """تحليل مؤشر تتبع العلاوة (مثل '4/3' إلى (4, 3))"""
        try:
            parts = indicator.split('/')
            if len(parts) != 2:
                raise ValueError(f"مؤشر غير صحيح: {indicator}")
            
            total = int(parts[0])
            current = int(parts[1])
            
            return total, current
        except (ValueError, IndexError) as e:
            self.logger.error(f"خطأ في تحليل المؤشر {indicator}: {e}")
            raise ValueError(f"مؤشر تتبع العلاوة غير صحيح: {indicator}")
    
    def create_tracking_indicator(self, total: int, current: int) -> str:
        """إنشاء مؤشر تتبع العلاوة"""
        return f"{total}/{current}"
    
    def get_next_entitlement_type(self, employee_data: Dict) -> str:
        """تحديد نوع الاستحقاق القادم (علاوة أو ترفيع)"""
        grade = employee_data['current_grade']
        stage = employee_data['current_stage']
        tracking_indicator = employee_data['tracking_indicator']
        
        # حالة خاصة: الدرجة الأولى
        if grade == 1:
            if stage >= 11:
                return "لا يوجد استحقاق"  # وصل لأقصى مرحلة
            return "علاوة"
        
        # حالة خاصة: الترفيع السريع للدبلوم من الدرجة 8/5
        if (grade == 8 and stage == 5 and 
            employee_data.get('degree') == 'دبلوم' and
            self._is_first_entitlement(employee_data)):
            return "ترفيع"
        
        # تحليل مؤشر التتبع
        try:
            total, current = self.parse_tracking_indicator(tracking_indicator)
            
            # إذا وصل المؤشر لنهايته، الاستحقاق القادم ترفيع
            if current >= total:
                return "ترفيع"
            else:
                return "علاوة"
                
        except ValueError:
            self.logger.error(f"مؤشر تتبع غير صحيح للموظف {employee_data.get('id', 'غير معروف')}")
            return "علاوة"  # افتراضي
    
    def _is_first_entitlement(self, employee_data: Dict) -> bool:
        """التحقق من كون هذا أول استحقاق للموظف"""
        # يمكن تحسين هذا بالتحقق من سجل المسار الوظيفي
        start_date = datetime.strptime(employee_data['start_date'], '%Y-%m-%d')
        last_entitlement = datetime.strptime(employee_data['last_entitlement_date'], '%Y-%m-%d')
        
        # إذا كان تاريخ آخر استحقاق هو نفس تاريخ المباشرة، فهذا أول استحقاق
        return start_date.date() == last_entitlement.date()
    
    def calculate_base_period_months(self, employee_data: Dict) -> int:
        """حساب المدة الأساسية بالأشهر (افتراضياً 12 شهر)"""
        return 12
    
    def get_professional_events_impact(self, employee_id: int, 
                                     since_date: datetime) -> int:
        """حساب تأثير الأحداث المهنية على المدة بالأشهر"""
        # سيتم تطوير هذا في المرحلة الثالثة
        # حالياً نعيد 0 (لا يوجد تأثير)
        return 0
    
    def calculate_next_entitlement_date(self, employee_data: Dict) -> datetime:
        """حساب تاريخ الاستحقاق القادم"""
        try:
            # نقطة الانطلاق: تاريخ آخر استحقاق
            last_entitlement = datetime.strptime(
                employee_data['last_entitlement_date'], '%Y-%m-%d'
            )
            
            # المدة الأساسية (12 شهر)
            base_months = self.calculate_base_period_months(employee_data)
            
            # تأثير الأحداث المهنية (سيتم تطويره في المرحلة الثالثة)
            events_impact = self.get_professional_events_impact(
                employee_data['id'], last_entitlement
            )
            
            # المدة النهائية
            total_months = base_months + events_impact
            
            # حساب التاريخ الجديد
            next_date = last_entitlement + relativedelta(months=total_months)
            
            return next_date
            
        except Exception as e:
            self.logger.error(f"خطأ في حساب تاريخ الاستحقاق للموظف {employee_data.get('id')}: {e}")
            # في حالة الخطأ، نعيد تاريخ افتراضي
            return datetime.now() + relativedelta(months=12)
    
    def get_next_grade_stage(self, employee_data: Dict, 
                           entitlement_type: str) -> Tuple[int, int]:
        """حساب الدرجة والمرحلة القادمة"""
        current_grade = employee_data['current_grade']
        current_stage = employee_data['current_stage']
        
        if entitlement_type == "علاوة":
            # العلاوة: زيادة المرحلة بـ 1
            new_grade = current_grade
            new_stage = current_stage + 1
            
            # التحقق من عدم تجاوز الحد الأقصى للمراحل
            if current_grade == 1 and new_stage > 11:
                new_stage = 11  # الحد الأقصى للدرجة الأولى
            elif current_grade > 1 and new_stage > 11:
                new_stage = 11  # الحد الأقصى للدرجات الأخرى
                
        elif entitlement_type == "ترفيع":
            # الترفيع: تقليل الدرجة بـ 1 وإعادة المرحلة إلى 1
            new_grade = current_grade - 1
            new_stage = 1
            
            # التحقق من عدم تجاوز الحد الأدنى للدرجات
            if new_grade < 1:
                new_grade = 1
                new_stage = current_stage  # لا تغيير
                
        else:
            # لا يوجد استحقاق
            new_grade = current_grade
            new_stage = current_stage
        
        return new_grade, new_stage
    
    def get_salary_for_grade_stage(self, grade: int, stage: int) -> int:
        """الحصول على الراتب للدرجة والمرحلة المحددة"""
        try:
            salary_data = self.db_manager.get_salary_for_grade_stage(grade, stage)
            return salary_data['salary'] if salary_data else 0
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على الراتب للدرجة {grade} المرحلة {stage}: {e}")
            return 0
    
    def update_tracking_indicator(self, employee_data: Dict, 
                                entitlement_type: str) -> str:
        """تحديث مؤشر تتبع العلاوة بعد الاستحقاق"""
        current_indicator = employee_data['tracking_indicator']
        grade = employee_data['current_grade']
        
        try:
            total, current = self.parse_tracking_indicator(current_indicator)
            
            if entitlement_type == "علاوة":
                # زيادة المؤشر الحالي
                new_current = current + 1
                new_indicator = self.create_tracking_indicator(total, new_current)
                
            elif entitlement_type == "ترفيع":
                # إعادة تعيين المؤشر للدرجة الجديدة
                new_grade = grade - 1
                if new_grade in self.promotion_rules:
                    rule = self.promotion_rules[new_grade]
                    if rule['years_for_promotion'] is not None:
                        new_total = rule['years_for_promotion']
                        new_indicator = self.create_tracking_indicator(new_total, 1)
                    else:
                        # الدرجة الأولى: مؤشر خاص
                        new_indicator = "11/1"
                else:
                    new_indicator = current_indicator  # لا تغيير
            else:
                new_indicator = current_indicator  # لا تغيير
                
            return new_indicator
            
        except ValueError:
            self.logger.error(f"خطأ في تحديث مؤشر التتبع: {current_indicator}")
            return current_indicator
    
    def calculate_effective_service(self, employee_data: Dict) -> Dict[str, int]:
        """حساب الخدمة الفعلية (بالسنوات والأشهر والأيام)"""
        try:
            start_date = datetime.strptime(employee_data['start_date'], '%Y-%m-%d')
            current_date = datetime.now()
            
            # حساب الفرق
            diff = relativedelta(current_date, start_date)
            
            # في المستقبل، سنطرح فترات الإجازات الطويلة
            # حالياً نحسب الخدمة الكاملة
            
            return {
                'years': diff.years,
                'months': diff.months,
                'days': diff.days
            }
            
        except Exception as e:
            self.logger.error(f"خطأ في حساب الخدمة الفعلية للموظف {employee_data.get('id')}: {e}")
            return {'years': 0, 'months': 0, 'days': 0}
    
    def get_complete_entitlement_info(self, employee_id: int) -> Dict:
        """الحصول على معلومات الاستحقاق الكاملة للموظف"""
        try:
            # الحصول على بيانات الموظف
            employee_data = self.db_manager.get_employee_by_id(employee_id)
            if not employee_data:
                raise ValueError(f"الموظف غير موجود: {employee_id}")
            
            # تحديد نوع الاستحقاق القادم
            entitlement_type = self.get_next_entitlement_type(employee_data)
            
            # حساب تاريخ الاستحقاق القادم
            next_date = self.calculate_next_entitlement_date(employee_data)
            
            # حساب الدرجة والمرحلة القادمة
            next_grade, next_stage = self.get_next_grade_stage(
                employee_data, entitlement_type
            )
            
            # حساب الراتب الحالي والقادم
            current_salary = self.get_salary_for_grade_stage(
                employee_data['current_grade'], employee_data['current_stage']
            )
            next_salary = self.get_salary_for_grade_stage(next_grade, next_stage)
            
            # حساب الخدمة الفعلية
            effective_service = self.calculate_effective_service(employee_data)
            
            # تحديث مؤشر التتبع (للعرض فقط، لا يتم حفظه)
            updated_indicator = self.update_tracking_indicator(
                employee_data, entitlement_type
            )
            
            return {
                'employee_id': employee_id,
                'current_grade': employee_data['current_grade'],
                'current_stage': employee_data['current_stage'],
                'current_salary': current_salary,
                'current_indicator': employee_data['tracking_indicator'],
                
                'next_entitlement_type': entitlement_type,
                'next_entitlement_date': next_date,
                'next_grade': next_grade,
                'next_stage': next_stage,
                'next_salary': next_salary,
                'updated_indicator': updated_indicator,
                
                'effective_service': effective_service,
                'last_entitlement_date': datetime.strptime(
                    employee_data['last_entitlement_date'], '%Y-%m-%d'
                )
            }
            
        except Exception as e:
            self.logger.error(f"خطأ في حساب معلومات الاستحقاق للموظف {employee_id}: {e}")
            raise
    
    def process_entitlement(self, employee_id: int) -> Dict:
        """معالجة استحقاق الموظف وتحديث بياناته"""
        try:
            # الحصول على معلومات الاستحقاق
            entitlement_info = self.get_complete_entitlement_info(employee_id)
            
            if entitlement_info['next_entitlement_type'] == "لا يوجد استحقاق":
                return {
                    'success': False,
                    'message': 'الموظف وصل للحد الأقصى ولا يوجد استحقاقات قادمة'
                }
            
            # تحديث بيانات الموظف
            update_data = {
                'grade': entitlement_info['next_grade'],
                'stage': entitlement_info['next_stage'],
                'tracking_indicator': entitlement_info['updated_indicator'],
                'last_entitlement_date': datetime.now().strftime('%Y-%m-%d')
            }
            
            # تحديث قاعدة البيانات
            success = self.db_manager.update_employee(employee_id, update_data)
            
            if success:
                # إضافة سجل في المسار الوظيفي
                career_record = {
                    'employee_id': employee_id,
                    'event_type': entitlement_info['next_entitlement_type'],
                    'event_date': datetime.now().strftime('%Y-%m-%d'),
                    'from_grade': entitlement_info['current_grade'],
                    'from_stage': entitlement_info['current_stage'],
                    'to_grade': entitlement_info['next_grade'],
                    'to_stage': entitlement_info['next_stage'],
                    'from_salary': entitlement_info['current_salary'],
                    'to_salary': entitlement_info['next_salary'],
                    'description': f"{entitlement_info['next_entitlement_type']}: من الدرجة {entitlement_info['current_grade']}/{entitlement_info['current_stage']} إلى {entitlement_info['next_grade']}/{entitlement_info['next_stage']}"
                }
                
                self.db_manager.add_career_record(career_record)
                
                return {
                    'success': True,
                    'message': f"تم منح {entitlement_info['next_entitlement_type']} بنجاح",
                    'entitlement_info': entitlement_info
                }
            else:
                return {
                    'success': False,
                    'message': 'فشل في تحديث بيانات الموظف'
                }
                
        except Exception as e:
            self.logger.error(f"خطأ في معالجة استحقاق الموظف {employee_id}: {e}")
            return {
                'success': False,
                'message': f'خطأ في المعالجة: {str(e)}'
            }

