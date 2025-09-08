import streamlit as st
import os
from csv_processor import process_csv_to_filtered_excel

st.set_page_config(page_title="CSV to Excel Filter", layout="wide")
st.title("🚀 CSV Filter & Export to Excel")

uploaded_file = st.file_uploader("📂 เลือกไฟล์ CSV", type=["csv", "txt"])

filter_col = "SPL_D_SCCD_SA1234_SGMD"
filter_val = "Regional Management 4 (North)"

# filter_col = st.text_input("📝 ชื่อคอลัมน์ที่ต้องการกรอง", "")
# filter_val = st.text_input("🎯 ค่าที่ต้องการกรอง", "")
output_prefix = st.text_input("📁 Prefix ของไฟล์ผลลัพธ์", "filtered_output")

if st.button("▶️ เริ่มประมวลผล") and uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("⏳ กำลังประมวลผล..."):
        output_files, total_rows = process_csv_to_filtered_excel(
            input_file=uploaded_file.name,
            filter_column=filter_col,
            filter_value=filter_val,
            output_prefix=output_prefix,
            chunk_size=100000,
            excel_limit=1048576
        )
    
    if output_files:
        st.success(f"✅ เสร็จสิ้น! พบข้อมูล {total_rows:,} แถว")
        for file in output_files:
            with open(file, "rb") as f:
                st.download_button(
                    label=f"⬇️ ดาวน์โหลด {os.path.basename(file)}",
                    data=f,
                    file_name=os.path.basename(file),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.error("❌ ไม่พบข้อมูลที่ตรงเงื่อนไข หรือเกิดข้อผิดพลาด")
