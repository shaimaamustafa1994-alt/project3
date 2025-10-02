# -*- coding: utf-8 -*-
"""
إعدادات التصميم والألوان العصرية الكلاسيكية
"""

import customtkinter as ctk

# إعدادات التصميم العامة
ctk.set_appearance_mode("light")  # وضع فاتح
ctk.set_default_color_theme("blue")  # اللون الأساسي أزرق

# الألوان العصرية الكلاسيكية
COLORS = {
    # الألوان الأساسية
    'primary': '#2E86AB',        # أزرق أساسي
    'primary_dark': '#1B5E7A',   # أزرق داكن
    'primary_light': '#A8DADC',  # أزرق فاتح
    
    # الألوان الثانوية
    'secondary': '#457B9D',      # أزرق رمادي
    'accent': '#F1FAEE',         # أبيض مائل للأزرق
    'success': '#2D6A4F',        # أخضر للنجاح
    'warning': '#F77F00',        # برتقالي للتحذير
    'danger': '#D62828',         # أحمر للخطر
    
    # الألوان المحايدة
    'white': '#FFFFFF',
    'light_gray': '#F8F9FA',
    'gray': '#6C757D',
    'dark_gray': '#495057',
    'black': '#212529',
    
    # ألوان الخلفية
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F8F9FA',
    'bg_card': '#FFFFFF',
    'bg_sidebar': '#2E86AB',
    
    # ألوان النصوص
    'text_primary': '#212529',
    'text_secondary': '#6C757D',
    'text_white': '#FFFFFF',
    'text_muted': '#ADB5BD'
}

# أحجام الخطوط
FONT_SIZES = {
    'title': 24,        # العناوين الرئيسية
    'subtitle': 20,     # العناوين الفرعية
    'heading': 18,      # عناوين الأقسام
    'large': 16,        # النصوص الكبيرة
    'normal': 14,       # النصوص العادية
    'small': 12,        # النصوص الصغيرة
    'tiny': 10          # النصوص الدقيقة
}

# الخطوط
FONTS = {
    'arabic': ('Cairo', 'Tajawal', 'Arial Unicode MS', 'Tahoma'),
    'english': ('Segoe UI', 'Arial', 'Helvetica'),
    'numbers': ('Consolas', 'Monaco', 'Courier New')
}

# أبعاد العناصر
DIMENSIONS = {
    'window_width': 1400,
    'window_height': 900,
    'sidebar_width': 280,
    'header_height': 80,
    'button_height': 45,
    'input_height': 40,
    'card_padding': 20,
    'section_spacing': 30,
    'element_spacing': 15
}

# أنماط الأزرار
BUTTON_STYLES = {
    'primary': {
        'fg_color': COLORS['primary'],
        'hover_color': COLORS['primary_dark'],
        'text_color': COLORS['white'],
        'font': (FONTS['arabic'][0], FONT_SIZES['normal'], 'bold'),
        'height': DIMENSIONS['button_height'],
        'corner_radius': 8
    },
    'secondary': {
        'fg_color': COLORS['gray'],
        'hover_color': COLORS['dark_gray'],
        'text_color': COLORS['white'],
        'font': (FONTS['arabic'][0], FONT_SIZES['normal']),
        'height': DIMENSIONS['button_height'],
        'corner_radius': 8
    },
    'success': {
        'fg_color': COLORS['success'],
        'hover_color': '#1E4A35',
        'text_color': COLORS['white'],
        'font': (FONTS['arabic'][0], FONT_SIZES['normal'], 'bold'),
        'height': DIMENSIONS['button_height'],
        'corner_radius': 8
    },
    'danger': {
        'fg_color': COLORS['danger'],
        'hover_color': '#B02A2A',
        'text_color': COLORS['white'],
        'font': (FONTS['arabic'][0], FONT_SIZES['normal'], 'bold'),
        'height': DIMENSIONS['button_height'],
        'corner_radius': 8
    }
}

# أنماط حقول الإدخال
INPUT_STYLES = {
    'default': {
        'height': DIMENSIONS['input_height'],
        'font': (FONTS['arabic'][0], FONT_SIZES['normal']),
        'corner_radius': 6,
        'border_width': 1,
        'fg_color': COLORS['white'],
        'border_color': COLORS['gray'],
        'text_color': COLORS['text_primary']
    }
}

# أنماط التسميات
LABEL_STYLES = {
    'title': {
        'font': (FONTS['arabic'][0], FONT_SIZES['title'], 'bold'),
        'text_color': COLORS['text_primary']
    },
    'subtitle': {
        'font': (FONTS['arabic'][0], FONT_SIZES['subtitle'], 'bold'),
        'text_color': COLORS['text_primary']
    },
    'heading': {
        'font': (FONTS['arabic'][0], FONT_SIZES['heading'], 'bold'),
        'text_color': COLORS['text_primary']
    },
    'normal': {
        'font': (FONTS['arabic'][0], FONT_SIZES['normal']),
        'text_color': COLORS['text_primary']
    },
    'secondary': {
        'font': (FONTS['arabic'][0], FONT_SIZES['normal']),
        'text_color': COLORS['text_secondary']
    }
}

# أنماط البطاقات
CARD_STYLES = {
    'default': {
        'fg_color': COLORS['bg_card'],
        'corner_radius': 12,
        'border_width': 1,
        'border_color': COLORS['light_gray']
    },
    'primary': {
        'fg_color': COLORS['primary_light'],
        'corner_radius': 12,
        'border_width': 0
    },
    'success': {
        'fg_color': '#E8F5E8',
        'corner_radius': 12,
        'border_width': 0
    },
    'warning': {
        'fg_color': '#FFF3CD',
        'corner_radius': 12,
        'border_width': 0
    }
}

def get_font(font_type: str = 'arabic', size: str = 'normal', weight: str = 'normal') -> tuple:
    """
    الحصول على خط مخصص
    """
    font_family = FONTS.get(font_type, FONTS['arabic'])[0]
    font_size = FONT_SIZES.get(size, FONT_SIZES['normal'])
    
    if weight == 'bold':
        return (font_family, font_size, 'bold')
    else:
        return (font_family, font_size)

def apply_rtl_layout():
    """
    تطبيق تخطيط RTL للغة العربية
    """
    # سيتم تطبيق هذا في الإصدارات المستقبلية
    pass

