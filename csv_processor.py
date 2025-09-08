import pandas as pd
from tqdm import tqdm
import xlsxwriter
import os

def process_csv_to_filtered_excel(
    input_file: str,
    filter_column: str,
    filter_value: str,
    output_prefix: str = "filtered_output",
    chunk_size: int = 100000,
    excel_limit: int = 1048576
):
    """
    อ่านไฟล์ CSV ขนาดใหญ่ กรองข้อมูลตามเงื่อนไข และบันทึกเป็น Excel หลายไฟล์
    """
    
    print(f"🚀 เริ่มประมวลผลไฟล์: {input_file}")
    print(f"📋 กรองคอลัมน์: {filter_column} = '{filter_value}'")
    
    part_count = 1
    total_filtered_rows = 0
    current_file_rows = 0
    workbook = None
    worksheet = None
    header_written = False
    output_files = []
    
    def create_new_excel_file():
        nonlocal workbook, worksheet, header_written, current_file_rows, part_count
        if workbook:
            workbook.close()
        output_file = f"{output_prefix}_part{part_count}.xlsx"
        workbook = xlsxwriter.Workbook(output_file)
        worksheet = workbook.add_worksheet()
        header_written = False
        current_file_rows = 0
        part_count += 1
        output_files.append(output_file)
        return output_file
    
    current_output_file = create_new_excel_file()
    
    try:
        csv_reader = pd.read_csv(input_file, chunksize=chunk_size, dtype=str)
        
        for chunk_num, chunk in enumerate(tqdm(csv_reader, desc="Processing chunks", unit="chunk")):
            if filter_column not in chunk.columns:
                continue
            
            df_filtered = chunk[chunk[filter_column] == filter_value]
            
            if df_filtered.empty:
                continue
            
            if not header_written:
                for col_num, col_name in enumerate(df_filtered.columns):
                    worksheet.write(0, col_num, col_name)
                header_written = True
                current_file_rows = 1
            
            for _, row in df_filtered.iterrows():
                if current_file_rows >= excel_limit:
                    current_output_file = create_new_excel_file()
                    for col_num, col_name in enumerate(df_filtered.columns):
                        worksheet.write(0, col_num, col_name)
                    header_written = True
                    current_file_rows = 1
                row_data = [str(x) if pd.notna(x) else "" for x in row.values]
                worksheet.write_row(current_file_rows, 0, row_data)
                current_file_rows += 1
                total_filtered_rows += 1
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return [], 0
    
    finally:
        if workbook:
            workbook.close()
    
    return output_files, total_filtered_rows
