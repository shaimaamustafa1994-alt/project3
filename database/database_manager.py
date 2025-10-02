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

