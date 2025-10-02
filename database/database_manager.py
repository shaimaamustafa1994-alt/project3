# -*- coding: utf-8 -*-
"""
مدير قاعدة البيانات - إدارة جميع العمليات المتعلقة بقاعدة البيانات
"""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import json

class DatabaseManager:
    def __init__(self, db_path: str = "employees.db"):
        """
        تهيئة مدير قاعدة البيانات
        """
        self.db_path = db_path
        self.init_database()
        self.create_salary_scale_table()
    
    def get_connection(self):
        """
        الحصول على اتصال بقاعدة البيانات
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
        return conn
    
    def init_database(self):
        """
        إنشاء جداول قاعدة البيانات
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول الموظفين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                start_date DATE NOT NULL,
                last_entitlement_date DATE NOT NULL,
                academic_degree TEXT NOT NULL,
                job_category TEXT NOT NULL,
                job_title TEXT NOT NULL,
                current_grade INTEGER NOT NULL,
                current_stage INTEGER NOT NULL,
                tracking_indicator TEXT NOT NULL,
                photo_path TEXT,
                status TEXT DEFAULT 'نشط',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الأحداث المهنية
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS professional_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                event_date DATE NOT NULL,
                document_number TEXT,
                document_date DATE,
                description TEXT,
                impact_months INTEGER DEFAULT 0,
                start_date DATE,
                end_date DATE,
                is_active BOOLEAN DEFAULT 1,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # جدول المسار الوظيفي (العلاوات والترفيعات)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS career_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                event_date DATE NOT NULL,
                from_grade INTEGER,
                from_stage INTEGER,
                to_grade INTEGER NOT NULL,
                to_stage INTEGER NOT NULL,
                from_salary REAL,
                to_salary REAL,
                related_events TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # جدول الإعدادات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT NOT NULL,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_employee(self, employee_data: Dict) -> int:
        """
        إضافة موظف جديد
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO employees (
                full_name, start_date, last_entitlement_date, academic_degree,
                job_category, job_title, current_grade, current_stage,
                tracking_indicator, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            employee_data['full_name'],
            employee_data['start_date'],
            employee_data['last_entitlement_date'],
            employee_data['academic_degree'],
            employee_data['job_category'],
            employee_data['job_title'],
            employee_data['current_grade'],
            employee_data['current_stage'],
            employee_data['tracking_indicator'],
            employee_data.get('notes', '')
        ))
        
        employee_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return employee_id
    
    def get_all_employees(self, filters: Dict = None) -> List[Dict]:
        """
        الحصول على جميع الموظفين مع إمكانية الفلترة
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM employees WHERE status = 'نشط'"
        params = []
        
        if filters:
            if filters.get('job_category'):
                query += " AND job_category = ?"
                params.append(filters['job_category'])
            
            if filters.get('search_name'):
                query += " AND full_name LIKE ?"
                params.append(f"%{filters['search_name']}%")
        
        query += " ORDER BY full_name"
        
        cursor.execute(query, params)
        employees = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return employees
    
    def get_employee_by_id(self, employee_id: int) -> Optional[Dict]:
        """
        الحصول على موظف بالمعرف
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
        employee = cursor.fetchone()
        
        conn.close()
        
        if employee:
            return dict(employee)
        return None
    
    def update_employee(self, employee_id: int, employee_data: Dict) -> bool:
        """
        تحديث بيانات موظف
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # بناء استعلام التحديث ديناميكياً
        fields = []
        values = []
        
        for key, value in employee_data.items():
            if key != 'id':
                fields.append(f"{key} = ?")
                values.append(value)
        
        if not fields:
            return False
        
        values.append(datetime.now())
        values.append(employee_id)
        
        query = f"UPDATE employees SET {', '.join(fields)}, updated_at = ? WHERE id = ?"
        
        cursor.execute(query, values)
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    def delete_employee(self, employee_id: int) -> bool:
        """
        حذف موظف (تعطيل فقط)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE employees SET status = 'محذوف', updated_at = ? WHERE id = ?",
            (datetime.now(), employee_id)
        )
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def add_professional_event(self, event_data: Dict) -> int:
        """
        إضافة حدث مهني
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO professional_events (
                employee_id, event_type, event_date, document_number,
                document_date, description, impact_months, start_date,
                end_date, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_data['employee_id'],
            event_data['event_type'],
            event_data['event_date'],
            event_data.get('document_number'),
            event_data.get('document_date'),
            event_data.get('description', ''),
            event_data.get('impact_months', 0),
            event_data.get('start_date'),
            event_data.get('end_date'),
            event_data.get('notes', '')
        ))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return event_id
    
    def get_employee_events(self, employee_id: int) -> List[Dict]:
        """
        الحصول على أحداث موظف معين
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM professional_events 
            WHERE employee_id = ? AND is_active = 1
            ORDER BY event_date DESC
        ''', (employee_id,))
        
        events = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return events
    
    def get_employee_career_history(self, employee_id: int) -> List[Dict]:
        """
        الحصول على المسار الوظيفي لموظف
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM career_history 
            WHERE employee_id = ?
            ORDER BY event_date DESC
        ''', (employee_id,))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return history
    
    def add_career_event(self, career_data: Dict) -> int:
        """
        إضافة حدث في المسار الوظيفي
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO career_history (
                employee_id, event_type, event_date, from_grade, from_stage,
                to_grade, to_stage, from_salary, to_salary, related_events, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            career_data['employee_id'],
            career_data['event_type'],
            career_data['event_date'],
            career_data.get('from_grade'),
            career_data.get('from_stage'),
            career_data['to_grade'],
            career_data['to_stage'],
            career_data.get('from_salary'),
            career_data['to_salary'],
            career_data.get('related_events', ''),
            career_data.get('notes', '')
        ))
        
        career_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return career_id
    
    def get_statistics(self) -> Dict:
        """
        الحصول على إحصائيات النظام
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # إجمالي الموظفين
        cursor.execute("SELECT COUNT(*) as total FROM employees WHERE status = 'نشط'")
        stats['total_employees'] = cursor.fetchone()['total']
        
        # إحصائيات حسب الصنف الوظيفي
        cursor.execute('''
            SELECT job_category, COUNT(*) as count 
            FROM employees WHERE status = 'نشط'
            GROUP BY job_category
        ''')
        stats['by_category'] = {row['job_category']: row['count'] for row in cursor.fetchall()}
        
        # إحصائيات حسب الشهادة
        cursor.execute('''
            SELECT academic_degree, COUNT(*) as count 
            FROM employees WHERE status = 'نشط'
            GROUP BY academic_degree
        ''')
        stats['by_degree'] = {row['academic_degree']: row['count'] for row in cursor.fetchall()}
        
        conn.close()
        return stats
    
    def get_salary_for_grade_stage(self, grade: int, stage: int) -> Optional[Dict]:
        """
        الحصول على الراتب للدرجة والمرحلة المحددة
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT salary FROM salary_scale 
            WHERE grade = ? AND stage = ?
        """, (grade, stage))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {'salary': row['salary']}
        return None
    
    def add_career_record(self, record_data: Dict) -> int:
        """
        إضافة سجل في المسار الوظيفي (مرادف لـ add_career_event)
        """
        return self.add_career_event(record_data)
    
    def get_career_history(self, employee_id: int) -> List[Dict]:
        """
        الحصول على المسار الوظيفي للموظف (مرادف لـ get_career_events)
        """
        return self.get_career_events(employee_id)
    
    def get_upcoming_entitlements(self, days_ahead: int = 30) -> List[Dict]:
        """
        الحصول على الاستحقاقات القادمة خلال فترة محددة
        """
        from models.calculation_engine import CalculationEngine
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # الحصول على جميع الموظفين النشطين
        cursor.execute("SELECT id FROM employees WHERE status = 'نشط'")
        employee_ids = [row['id'] for row in cursor.fetchall()]
        
        conn.close()
        
        # حساب الاستحقاقات لكل موظف
        calc_engine = CalculationEngine(self)
        upcoming = []
        
        from datetime import datetime, timedelta
        target_date = datetime.now() + timedelta(days=days_ahead)
        
        for emp_id in employee_ids:
            try:
                entitlement_info = calc_engine.get_complete_entitlement_info(emp_id)
                
                # التحقق من كون الاستحقاق خلال الفترة المحددة
                if entitlement_info['next_entitlement_date'] <= target_date:
                    upcoming.append({
                        'employee_id': emp_id,
                        'employee_name': self.get_employee_by_id(emp_id)['full_name'],
                        'entitlement_type': entitlement_info['next_entitlement_type'],
                        'entitlement_date': entitlement_info['next_entitlement_date'],
                        'current_grade': entitlement_info['current_grade'],
                        'current_stage': entitlement_info['current_stage'],
                        'next_grade': entitlement_info['next_grade'],
                        'next_stage': entitlement_info['next_stage']
                    })
            except Exception as e:
                print(f"خطأ في حساب استحقاق الموظف {emp_id}: {e}")
                continue
        
        # ترتيب حسب تاريخ الاستحقاق
        upcoming.sort(key=lambda x: x['entitlement_date'])
        
        return upcoming
    
    def create_salary_scale_table(self):
        """
        إنشاء جدول سلم الرواتب
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # إنشاء الجدول
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salary_scale (
                grade INTEGER,
                stage INTEGER,
                salary INTEGER,
                PRIMARY KEY (grade, stage)
            )
        ''')
        
        # التحقق من وجود البيانات
        cursor.execute("SELECT COUNT(*) FROM salary_scale")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # إدراج بيانات سلم الرواتب
            salary_data = [
                # الدرجة الأولى
                (1, 1, 910000), (1, 2, 930000), (1, 3, 950000), (1, 4, 970000), (1, 5, 990000),
                (1, 6, 1010000), (1, 7, 1030000), (1, 8, 1050000), (1, 9, 1070000), (1, 10, 1090000), (1, 11, 1110000),
                
                # الدرجة الثانية
                (2, 1, 723000), (2, 2, 740000), (2, 3, 757000), (2, 4, 774000), (2, 5, 791000),
                (2, 6, 808000), (2, 7, 825000), (2, 8, 842000), (2, 9, 859000), (2, 10, 876000), (2, 11, 893000),
                
                # الدرجة الثالثة
                (3, 1, 600000), (3, 2, 610000), (3, 3, 620000), (3, 4, 630000), (3, 5, 640000),
                (3, 6, 650000), (3, 7, 660000), (3, 8, 670000), (3, 9, 680000), (3, 10, 690000), (3, 11, 700000),
                
                # الدرجة الرابعة
                (4, 1, 509000), (4, 2, 517000), (4, 3, 525000), (4, 4, 533000), (4, 5, 541000),
                (4, 6, 549000), (4, 7, 557000), (4, 8, 565000), (4, 9, 573000), (4, 10, 581000), (4, 11, 589000),
                
                # الدرجة الخامسة
                (5, 1, 429000), (5, 2, 435000), (5, 3, 441000), (5, 4, 447000), (5, 5, 453000),
                (5, 6, 459000), (5, 7, 465000), (5, 8, 471000), (5, 9, 477000), (5, 10, 483000), (5, 11, 489000),
                
                # الدرجة السادسة
                (6, 1, 362000), (6, 2, 368000), (6, 3, 374000), (6, 4, 380000), (6, 5, 386000),
                (6, 6, 392000), (6, 7, 398000), (6, 8, 404000), (6, 9, 410000), (6, 10, 416000), (6, 11, 422000),
                
                # الدرجة السابعة
                (7, 1, 296000), (7, 2, 302000), (7, 3, 308000), (7, 4, 314000), (7, 5, 320000),
                (7, 6, 326000), (7, 7, 332000), (7, 8, 338000), (7, 9, 344000), (7, 10, 350000), (7, 11, 356000),
                
                # الدرجة الثامنة
                (8, 1, 260000), (8, 2, 263000), (8, 3, 266000), (8, 4, 269000), (8, 5, 272000),
                (8, 6, 275000), (8, 7, 278000), (8, 8, 281000), (8, 9, 284000), (8, 10, 287000), (8, 11, 290000),
                
                # الدرجة التاسعة
                (9, 1, 210000), (9, 2, 213000), (9, 3, 216000), (9, 4, 219000), (9, 5, 222000),
                (9, 6, 225000), (9, 7, 228000), (9, 8, 231000), (9, 9, 234000), (9, 10, 237000), (9, 11, 240000),
                
                # الدرجة العاشرة
                (10, 1, 170000), (10, 2, 173000), (10, 3, 176000), (10, 4, 179000), (10, 5, 182000),
                (10, 6, 185000), (10, 7, 188000), (10, 8, 191000), (10, 9, 194000), (10, 10, 197000), (10, 11, 200000),
            ]
            
            cursor.executemany("INSERT INTO salary_scale (grade, stage, salary) VALUES (?, ?, ?)", salary_data)
            conn.commit()
        
        conn.close()
