
"""


派遣资源定位
region=(597, 899, 150, 150)

首页活动定位第一行第一列
region=(18, 210, 123, 150)
第一行第二列
region=(172, 210, 123, 150)
region=(326, 210, 123, 150)
region=(480, 210, 123, 150)

x差值：154


第二行第一列
region=(18, 410, 123, 150)
region=(172, 410, 123, 150)
region=(326, 410, 123, 150)
region=(480, 410, 123, 150)
region=(633, 410, 123, 150)
region=(783, 410, 123, 150)

y差值：200


第三行第一列
region=(18, 610, 123, 150)
region=(172, 610, 123, 150)
region=(326, 610, 123, 150)
region=(480, 610, 123, 150)
region=(633, 610, 123, 150)
region=(783, 610, 123, 150)

"""

# x_list = [18,172,326,480,633,783]
# y_list = [210,410,610]
# for y in y_list:
#     for x in x_list:
#         # 过滤点击空白区域
#         if y == y_list[0] and x is x_list[4]:
#             print(f"跳过（{x, y}）")
#             break
#         else:
#             print(x, y, 123, 150)



# for x in range(10):
#     for y in range(10):
#         if y == 1:
#             break
#         else:
#             print(f'x:{x},y:{y}')


huodong = {
            "page_path": "../page_png/armoury_page_inner.png",
            "lb_path" : "../page_png/armoury_page_lb.png",
            "mf_path" : "../page_png/armoury_lb_mf.png",
            "yb_path" : "../page_png/armoury_lb_yb.png",
            "page_name" : "锦囊妙计",
            "region_page" : (850, 1780, 180, 180),
            "region_lb" : (940, 435, 120, 120),
            "region_mf" : (780, 750, 230, 100),
            "region_yb" : (780, 1028, 230, 100)
        }

print(type(huodong["region_mf"]))
print(huodong["region_mf"][0])

#
# region_one = ((18, 210, 123, 150),(172, 210, 123, 150),(326, 210, 123, 150),(480, 210, 123, 150))
# region_two = ((18, 410, 123, 150),(172, 410, 123, 150),(326, 410, 123, 150),(480, 410, 123, 150),(633, 410, 123, 150),(783, 410, 123, 150))
#
# region_three = ((18, 610, 123, 150),(172, 610, 123, 150),(326, 610, 123, 150),(480, 610, 123, 150),(633, 610, 123, 150),(783, 610, 123, 150))
# print(region_three)
# for region in region_three:
#     print(region)
#
