# -*- coding: utf-8 -*-
"""
مكونات النماذج المخصصة للتطبيق
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, date
import tkinter as tk
from config.theme import *

class ArabicLabel(ctk.CTkLabel):
    """
    تسمية مخصصة للنصوص العربية
    """
    def __init__(self, parent, text="", style="normal", **kwargs):
        style_config = LABEL_STYLES.get(style, LABEL_STYLES['normal'])
        
        super().__init__(
            parent,
            text=text,
            **style_config,
            **kwargs
        )

class ArabicEntry(ctk.CTkEntry):
    """
    حقل إدخال مخصص للنصوص العربية
    """
    def __init__(self, parent, placeholder="", **kwargs):
        style_config = INPUT_STYLES['default'].copy()
        style_config.update(kwargs)
        
        super().__init__(
            parent,
            placeholder_text=placeholder,
            **style_config
        )
        
        # تطبيق محاذاة RTL للنصوص العربية
        self.configure(justify='right')

class ArabicComboBox(ctk.CTkComboBox):
    """
    قائمة منسدلة مخصصة للنصوص العربية
    """
    def __init__(self, parent, values=[], **kwargs):
        style_config = {
            'height': DIMENSIONS['input_height'],
            'font': get_font('arabic', 'normal'),
            'corner_radius': 6,
            'border_width': 1,
            'fg_color': COLORS['white'],
            'border_color': COLORS['gray'],
            'text_color': COLORS['text_primary'],
            'dropdown_font': get_font('arabic', 'normal')
        }
        style_config.update(kwargs)
        
        super().__init__(
            parent,
            values=values,
            **style_config
        )
        
        # تطبيق محاذاة RTL
        self.configure(justify='right')

class DatePicker(ctk.CTkFrame):
    """
    منتقي التاريخ المخصص
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # إعداد الشبكة
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # قوائم اليوم والشهر والسنة
        self.day_var = tk.StringVar(value="1")
        self.month_var = tk.StringVar(value="1")
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        
        # قائمة الأيام
        days = [str(i) for i in range(1, 32)]
        self.day_combo = ArabicComboBox(self, values=days, variable=self.day_var, width=80)
        self.day_combo.grid(row=0, column=2, padx=2, sticky="ew")
        
        # قائمة الشهور
        months = [
            "1", "2", "3", "4", "5", "6",
            "7", "8", "9", "10", "11", "12"
        ]
        self.month_combo = ArabicComboBox(self, values=months, variable=self.month_var, width=80)
        self.month_combo.grid(row=0, column=1, padx=2, sticky="ew")
        
        # قائمة السنوات
        current_year = datetime.now().year
        years = [str(i) for i in range(current_year - 50, current_year + 10)]
        self.year_combo = ArabicComboBox(self, values=years, variable=self.year_var, width=100)
        self.year_combo.grid(row=0, column=0, padx=2, sticky="ew")
    
    def get_date(self) -> date:
        """
        الحصول على التاريخ المحدد
        """
        try:
            day = int(self.day_var.get())
            month = int(self.month_var.get())
            year = int(self.year_var.get())
            return date(year, month, day)
        except ValueError:
            return date.today()
    
    def set_date(self, selected_date: date):
        """
        تعيين التاريخ
        """
        self.day_var.set(str(selected_date.day))
        self.month_var.set(str(selected_date.month))
        self.year_var.set(str(selected_date.year))

class ArabicButton(ctk.CTkButton):
    """
    زر مخصص للنصوص العربية
    """
    def __init__(self, parent, text="", style="primary", **kwargs):
        style_config = BUTTON_STYLES.get(style, BUTTON_STYLES['primary']).copy()
        style_config.update(kwargs)
        
        super().__init__(
            parent,
            text=text,
            **style_config
        )

class FormField(ctk.CTkFrame):
    """
    حقل نموذج كامل مع تسمية وحقل إدخال
    """
    def __init__(self, parent, label_text="", field_type="entry", **kwargs):
        super().__init__(parent, fg_color="transparent")
        
        # إعداد الشبكة
        self.grid_columnconfigure(1, weight=1)
        
        # التسمية
        self.label = ArabicLabel(self, text=label_text, style="normal")
        self.label.grid(row=0, column=0, sticky="e", padx=(0, 10))
        
        # حقل الإدخال حسب النوع
        if field_type == "entry":
            self.field = ArabicEntry(self, **kwargs)
        elif field_type == "combobox":
            values = kwargs.pop('values', [])
            self.field = ArabicComboBox(self, values=values, **kwargs)
        elif field_type == "date":
            self.field = DatePicker(self, **kwargs)
        elif field_type == "text":
            self.field = ctk.CTkTextbox(self, height=100, **kwargs)
        
        self.field.grid(row=0, column=1, sticky="ew", pady=5)
    
    def get_value(self):
        """
        الحصول على قيمة الحقل
        """
        if hasattr(self.field, 'get_date'):  # DatePicker
            return self.field.get_date()
        elif hasattr(self.field, 'get'):
            return self.field.get()
        else:
            return ""
    
    def set_value(self, value):
        """
        تعيين قيمة الحقل
        """
        if hasattr(self.field, 'set_date'):  # DatePicker
            self.field.set_date(value)
        elif hasattr(self.field, 'set'):
            self.field.set(value)

class InfoCard(ctk.CTkFrame):
    """
    بطاقة معلومات مع أيقونة وعنوان وقيمة
    """
    def __init__(self, parent, title="", value="", icon="📊", style="default", **kwargs):
        style_config = CARD_STYLES.get(style, CARD_STYLES['default']).copy()
        style_config.update(kwargs)
        
        super().__init__(parent, **style_config)
        
        # إعداد الشبكة
        self.grid_columnconfigure(1, weight=1)
        
        # الأيقونة
        self.icon_label = ArabicLabel(self, text=icon, style="heading")
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=15, pady=15, sticky="w")
        
        # العنوان
        self.title_label = ArabicLabel(self, text=title, style="normal")
        self.title_label.grid(row=0, column=1, sticky="ew", padx=10, pady=(15, 5))
        
        # القيمة
        self.value_label = ArabicLabel(self, text=value, style="heading")
        self.value_label.grid(row=1, column=1, sticky="ew", padx=10, pady=(0, 15))
    
    def update_value(self, new_value):
        """
        تحديث القيمة
        """
        self.value_label.configure(text=new_value)

class SearchFilter(ctk.CTkFrame):
    """
    مكون البحث والفلترة
    """
    def __init__(self, parent, on_search=None, on_filter=None, filter_options=[], **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_search = on_search
        self.on_filter = on_filter
        
        # إعداد الشبكة
        self.grid_columnconfigure(1, weight=1)
        
        # حقل البحث
        ArabicLabel(self, text="البحث:", style="normal").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.search_entry = ArabicEntry(self, placeholder="ابحث عن موظف...")
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        
        # فلتر الصنف الوظيفي
        if filter_options:
            ArabicLabel(self, text="الصنف:", style="normal").grid(row=0, column=2, padx=10, pady=10, sticky="e")
            
            self.filter_combo = ArabicComboBox(self, values=["الكل"] + filter_options, width=150)
            self.filter_combo.grid(row=0, column=3, padx=10, pady=10)
            self.filter_combo.set("الكل")
            self.filter_combo.configure(command=self._on_filter_change)
    
    def _on_search_change(self, event=None):
        """
        عند تغيير نص البحث
        """
        if self.on_search:
            self.on_search(self.search_entry.get())
    
    def _on_filter_change(self, value=None):
        """
        عند تغيير الفلتر
        """
        if self.on_filter:
            selected = self.filter_combo.get()
            if selected == "الكل":
                selected = None
            self.on_filter(selected)

