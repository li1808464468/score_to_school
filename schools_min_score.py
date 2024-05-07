import requests
import json
import sys
import os
import pandas as pd

# Configuration settings
province_id = "37"
province_name = "shandong"
want = "软件工程"
years = [2023, 2022, 2021, 2020, 2019]
is_hugescratch = True
is_college_only = True

# Get the current working directory
path = os.getcwd()

# Get province ID if not a digit
if not province_id.isdigit() or province_id == "None":
    if province_id == "None":
        province_id = input("请输入省份名称:")
    print("检测到您未获取您省份的id,正在为你获取")
    back = requests.get("https://static-data.gaokao.cn/www/2.0/config/81004.json")
    all_province = json.loads(back.text)

    for key, value in all_province['data'].items():
        if value['provinceName'] == province_id:
            id = key
            break

    if province_id:
        print(f"{province_id}的ID为:{id}")
        province_id = id
    else:
        print("找不到该省份的ID")
        sys.exit()

# Fetch all school IDs
print("开始获取学校id")
all_school_id = {}
back = requests.get("https://static-data.gaokao.cn/www/2.0/info/linkage.json")
all_school_ids = ((json.loads(back.text)).get("data")).get("school")
for i in range(len(all_school_ids)):
    school_id = all_school_ids[i]["school_id"]
    school_name = all_school_ids[i]["name"]
    all_school_id[school_name] = school_id

# Set up the Excel filename
excel_filename = f"{province_name}_schools_min_score.xlsx"
desired_fields = [
    'school_id', 'special_id', 'min', 'min_section', 'sp_sxk', 'sp_info',
    'level1_name', 'level2_name', 'level3_name', 'spname'
]

# Initialize error tracking and the DataFrame for all data
errors = []
all_data_df = pd.DataFrame()
total_schools = len(all_school_id)
processed_schools = 0

print("开始获取学校对应专业最低分，该过程较慢，请耐心等待...")

# Process each school
for school_name, school_id in all_school_id.items():
    for year in years:
        try:
            response = requests.get(
                f"https://static-data.gaokao.cn/www/2.0/schoolspecialscore/{school_id}/{year}/{province_id}.json")
            response.raise_for_status()
            response_data = response.json()

            if response_data['code'] == '0000' and 'data' in response_data:
                for key, item in response_data['data'].items():
                    filtered_items = [{k: v for k, v in subitem.items() if k in desired_fields} for subitem in item['item']]
                    df = pd.DataFrame(filtered_items)
                    df['school_name'] = school_name
                    df['year'] = year
                    # Ensure that 'school_name' and 'year' are at the front
                    cols = ['school_name', 'year'] + [col for col in df.columns if col not in ['school_name', 'year']]
                    df = df[cols]
                    all_data_df = pd.concat([all_data_df, df], ignore_index=True)
        except Exception as e:
            errors.append(f"{school_name} ({year}): {str(e)}")
            print(f"发生错误：{school_name} ({year}): {str(e)}")

    processed_schools += 1
    progress = (processed_schools / total_schools) * 100
    # Print progress with percentage and school name after each school is processed
    print(f"已处理 {processed_schools}/{total_schools} ({progress:.2f}%): {school_name}")

# Write all data to a single sheet
with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
    # Ensure that 'school_name' and 'year' are at the front in the final DataFrame as well
    final_cols = ['school_name', 'year'] + [col for col in all_data_df.columns if col not in ['school_name', 'year']]
    all_data_df = all_data_df[final_cols]
    all_data_df.to_excel(writer, sheet_name='All Schools', index=False)

print(f"所有数据已成功写入 {excel_filename}")

# Output any errors that occurred
if errors:
    print("部分数据处理过程中发生错误：")
    for error in errors:
        print(error)


