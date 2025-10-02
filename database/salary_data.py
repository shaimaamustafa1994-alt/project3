# -*- coding: utf-8 -*-
"""
جدول الرواتب المعتمد للنظام
يحتوي على جميع الدرجات والمراحل الوظيفية مع الرواتب ومقدار العلاوات
"""

# جدول الرواتب الأساسي (بالآلاف الدنانير)
SALARY_TABLE = {
    1: {  # الدرجة الأولى
        'promotion_years': 0,  # لا يوجد ترفيع
        'allowance_amount': 20000,
        'stages': {
            1: 910, 2: 930, 3: 950, 4: 970, 5: 990,
            6: 1010, 7: 1030, 8: 1050, 9: 1070, 10: 1090, 11: 1110
        }
    },
    2: {  # الدرجة الثانية
        'promotion_years': 5,
        'allowance_amount': 17000,
        'stages': {
            1: 723, 2: 740, 3: 757, 4: 774, 5: 791,
            6: 808, 7: 825, 8: 842, 9: 859, 10: 876, 11: 893
        }
    },
    3: {  # الدرجة الثالثة
        'promotion_years': 5,
        'allowance_amount': 10000,
        'stages': {
            1: 600, 2: 610, 3: 620, 4: 630, 5: 640,
            6: 650, 7: 660, 8: 670, 9: 680, 10: 690, 11: 700
        }
    },
    4: {  # الدرجة الرابعة
        'promotion_years': 5,
        'allowance_amount': 8000,
        'stages': {
            1: 509, 2: 517, 3: 525, 4: 533, 5: 541,
            6: 549, 7: 557, 8: 565, 9: 573, 10: 581, 11: 589
        }
    },
    5: {  # الدرجة الخامسة
        'promotion_years': 5,
        'allowance_amount': 6000,
        'stages': {
            1: 429, 2: 435, 3: 441, 4: 447, 5: 453,
            6: 459, 7: 465, 8: 471, 9: 477, 10: 483, 11: 489
        }
    },
    6: {  # الدرجة السادسة
        'promotion_years': 4,
        'allowance_amount': 6000,
        'stages': {
            1: 362, 2: 368, 3: 374, 4: 380, 5: 386,
            6: 392, 7: 398, 8: 404, 9: 410, 10: 416, 11: 422
        }
    },
    7: {  # الدرجة السابعة
        'promotion_years': 4,
        'allowance_amount': 6000,
        'stages': {
            1: 296, 2: 302, 3: 308, 4: 314, 5: 320,
            6: 326, 7: 332, 8: 338, 9: 344, 10: 350, 11: 356
        }
    },
    8: {  # الدرجة الثامنة
        'promotion_years': 4,
        'allowance_amount': 3000,
        'stages': {
            1: 260, 2: 263, 3: 266, 4: 269, 5: 272,
            6: 275, 7: 278, 8: 281, 9: 284, 10: 287, 11: 290
        }
    },
    9: {  # الدرجة التاسعة
        'promotion_years': 4,
        'allowance_amount': 3000,
        'stages': {
            1: 210, 2: 213, 3: 216, 4: 219, 5: 222,
            6: 225, 7: 228, 8: 231, 9: 234, 10: 237, 11: 240
        }
    },
    10: {  # الدرجة العاشرة
        'promotion_years': 4,
        'allowance_amount': 3000,
        'stages': {
            1: 170, 2: 173, 3: 176, 4: 179, 5: 182,
            6: 185, 7: 188, 8: 191, 9: 194, 10: 197, 11: 200
        }
    }
}

# قائمة الشهادات العلمية
ACADEMIC_DEGREES = [
    "دكتوراه",
    "ماجستير", 
    "دبلوم عالي",
    "بكالوريوس",
    "دبلوم",
    "إعدادية",
    "أخرى"
]

# أصناف الوظائف
JOB_CATEGORIES = [
    "تدريسي",
    "إداري", 
    "فني"
]

# مؤشرات تتبع العلاوة
TRACKING_INDICATORS = [
    "4/1", "4/2", "4/3", "4/4",
    "5/1", "5/2", "5/3", "5/4", "5/5"
]

def get_salary(grade, stage):
    """
    الحصول على الراتب لدرجة ومرحلة معينة
    """
    if grade in SALARY_TABLE and stage in SALARY_TABLE[grade]['stages']:
        return SALARY_TABLE[grade]['stages'][stage]
    return 0

def get_allowance_amount(grade):
    """
    الحصول على مقدار العلاوة لدرجة معينة
    """
    if grade in SALARY_TABLE:
        return SALARY_TABLE[grade]['allowance_amount']
    return 0

def get_promotion_years(grade):
    """
    الحصول على عدد السنوات المطلوبة للترفيع لدرجة معينة
    """
    if grade in SALARY_TABLE:
        return SALARY_TABLE[grade]['promotion_years']
    return 0

def get_max_stage(grade):
    """
    الحصول على أقصى مرحلة لدرجة معينة
    """
    if grade in SALARY_TABLE:
        return max(SALARY_TABLE[grade]['stages'].keys())
    return 0

