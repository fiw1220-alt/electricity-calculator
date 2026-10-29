import streamlit as st

def simple_electricity_calc(appliance_text, days_per_month, unit_price):
    if not appliance_text or appliance_text.strip() == "":
        return "⚠️ กรุณากรอกข้อมูลเครื่องใช้ไฟฟ้าอย่างน้อย 1 รายการ"

    lines = appliance_text.strip().split("\n")
    total_kwh_month = 0.0
    appliance_summary = []

    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        
        if len(parts) != 4:
            return f"⚠️ ข้อมูลบรรทัดที่ {index} ไม่ถูกต้อง (รูปแบบ: ชื่อ, วัตต์, จำนวน, ชั่วโมง)"

        try:
            name = parts[0]
            watts = float(parts[1])
            qty = int(parts[2])
            hours = float(parts[3])
        except ValueError:
            return f"⚠️ ข้อมูลตัวเลขในบรรทัดที่ {index} ไม่ถูกต้อง"

        kwh_month = (watts * qty * hours * days_per_month) / 1000.0
        total_kwh_month += kwh_month

        appliance_summary.append(f"{index}. **{name}** ➡️ ใช้ไฟ {kwh_month:.2f} หน่วย/เดือน")

    total_cost = total_kwh_month * unit_price

    if total_kwh_month <= 150:
        status = "🟢 ระดับประหยัด (Low) 😁"
    elif total_kwh_month <= 400:
        status = "🟡 ระดับปานกลาง (Moderate) 🙂"
    else:
        status = "🔴 ระดับสูง (High) ☠️"

    report = f"""### 📆 สรุปค่าไฟฟ้า ({days_per_month} วัน)
**ระดับการใช้ไฟ:** {status}

#### 🔌 ปริมาณการใช้ไฟแต่ละอุปกรณ์
{chr(10).join(appliance_summary)}

---
#### 💰 สรุปค่าใช้จ่าย
* **หน่วยไฟฟ้ารวม:** `{total_kwh_month:,.2f}` หน่วย (kWh)
* **ราคาไฟที่กำหนด:** `{unit_price:,.2f}` บาท/หน่วย
* 🧾 **รวมค่าไฟฟ้าที่ต้องจ่าย:** **`{total_cost:,.2f}` บาท**
"""
    return report

# ---------------- การจัดหน้าเว็บ UI ด้วย Streamlit ----------------
st.set_page_config(page_title="Simple Electricity Calculator", page_icon="⚡", layout="wide")
st.title("⚡ โปรแกรมคำนวณค่าไฟแบบง่าย (Simple Electricity Calculator)⚡")
st.markdown("รูปแบบการกรอก: **`ชื่ออุปกรณ์, กำลังวัตต์(W), จำนวนเครื่อง, ชั่วโมงที่ใช้ต่อวัน`**")

default_appliances = "แอร์ 12000 BTU, 1200, 1, 8\nพัดลม, 50, 2, 8\nหลอดไฟ, 10, 4, 6"

col1, col2 = st.columns(2) # แบ่งหน้าจอเป็น 2 ฝั่ง ซ้าย-ขวา

with col1:
    app_input = st.text_area("รายการเครื่องใช้ไฟฟ้า", value=default_appliances, height=150)
    days_input = st.slider("จำนวนวันในรอบบิล", min_value=1, max_value=31, value=30)
    price_input = st.number_input("ค่าไฟ (บาท/หน่วย)", value=4.50, step=0.1)
    calc_btn = st.button("🚀 คำนวณค่าไฟ 🚀", type="primary")

with col2:
    st.markdown("### ผลลัพธ์การคำนวณ")
    if calc_btn:
        result = simple_electricity_calc(app_input, days_input, price_input)
        st.markdown(result)
