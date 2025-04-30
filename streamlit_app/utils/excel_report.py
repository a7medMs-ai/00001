import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import datetime

def generate_excel_report(data, website_name):
    df = pd.DataFrame(data)
    
    # تنسيق متقدم
    filename = f"website_{website_name}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for lang, group in df.groupby('language'):
            lang_df = group[[
                'url', 
                'title', 
                'word_count', 
                'segments', 
                'has_media'
            ]]
            
            lang_df.to_excel(writer, sheet_name=lang.upper(), index=False)
            worksheet = writer.sheets[lang.upper()]
            
            # إضافة التنسيقات المهنية
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
            
            for cell in worksheet["1:1"]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center")
            
            # إضافة الإجماليات
            last_row = len(lang_df) + 2
            worksheet[f'A{last_row}'] = 'TOTAL'
            worksheet[f'C{last_row}'] = lang_df['word_count'].sum()
            worksheet[f'D{last_row}'] = lang_df['segments'].sum()
            
            # تثبيت العناوين
            worksheet.freeze_panes = 'A2'
    
    return filename
