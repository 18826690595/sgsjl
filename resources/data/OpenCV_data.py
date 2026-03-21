import csv
import os

header = ['账号', '密码', "登录状态", "VIP奖励", "好有日常", "世界聊天", "竞技场", "斗塔", "名将招募", "商店购买", "军团任务", "野外", "征战", "领取任务奖励", "助战", "活动", "退出登录"]
output_path = os.path.join(os.path.dirname(__file__), 'user_info.csv')

# 读取现有数据
rows = []
if os.path.exists(output_path):
    with open(output_path, 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if rows and rows[0] != header:  # 检查表头是否匹配
            rows.insert(0, header)

# 查找并更新指定账号
account_to_update = '202508001'
updated = False
ow[header.index('账号')]
# print(rows[1:])
for row in rows[1:]:  # 跳过表头
    # print(row)
    for r in row:
        print(r)
    # print(row[header.index('账号')])
# for row in rows[1:]:  # 跳过表头
#     if row[header.index('账号')] == account_to_update:
#         row[header.index('登录状态')] = '已登录'
#         updated = True
#         break
#
# # 如果账号不存在，添加新行
# if not updated:
#     new_row = [account_to_update, '密码'] + [''] * (len(header) - 2)
#     new_row[header.index('登录状态')] = '已登录'
#     rows.append(new_row)
#
# # 写入更新后的数据
# with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
#     writer = csv.writer(f)
#     writer.writerows(rows)



