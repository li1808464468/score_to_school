import requests
import csv
import json

# all_school_id = {}
# back = requests.get("https://static-data.gaokao.cn/www/2.0/info/linkage.json")
# all_school_ids = ((json.loads(back.text)).get("data")).get("school")
# print(len(all_school_ids))


# # 指定CSV文件名
# csv_file = "schools.csv"
# # 初始化csv_columns为空列表
# csv_columns = []
#
# pageIndex = 1
# # 打开CSV文件准备写入
# with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
#     writer = None
#
#     while True:
#         # API的URL
#         url = "https://api.zjzw.cn/gh5/api"
#         # 请求体，根据您的JSON配置
#         payload = {
#             "ad_show": 2,
#             "admissions": "",
#             "f211": "",
#             "f985": "",
#             "is_doublehigh": "",
#             "is_dual_class": "",
#             "keyword": "",
#             "local_province_id": 11,
#             "local_type_id": "",
#             "nature": "",
#             "page": pageIndex,
#             "province_id": "",
#             "school_type": "",
#             "signsafe": "11ed708352dea7d9674d2574949a814b",
#             "size": 30,
#             "sort": "eol_rank",
#             "sorttype": "asc",
#             "spe_ids": "",
#             "type": "",
#             "uri": "apidata/api/gkv3/school/lists"
#         }
#         headers = {
#             'User-Agent': 'PostmanRuntime-ApipostRuntime/1.1.0',
#         }
#         # 发送POST请求
#         response = requests.post(url, json=payload, headers=headers)
#
#         # 检查响应代码
#         if response.status_code == 200:
#             response_json = response.json()
#             # 请求成功，处理响应
#             print("Success:", response_json)
#
#             # 检查data字段是否包含item键
#             if 'item' in response_json['data']:
#                 items = response_json['data']['item']
#                 print("Item中的条数:", len(items))
#
#                 # 如果csv_columns为空，则从第一批项目中获取它们
#                 if not csv_columns:
#                     csv_columns = items[0].keys() if items else []
#                     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#                     writer.writeheader()
#
#                 # 写入CSV
#                 for item in items:
#                     writer.writerow(item)
#                 print(f"数据已追加到 {csv_file} 中")
#
#             else:
#                 # 如果data字段不包含item键，则认为没有更多数据可以获取
#                 print("No more items to retrieve.")
#                 break
#
#         else:
#             # 请求失败，处理错误
#             print("Error:", response.status_code)
#             break
#
#         pageIndex += 1  # 递增页码以获取下一页数据
#
#         # 这里可以添加一个条件来判断何时停止循环，例如：
#         # if pageIndex > MAX_PAGE_INDEX:
#         #     break
