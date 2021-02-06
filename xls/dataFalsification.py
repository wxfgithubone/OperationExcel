#!/usr/bin/env python3
# -*-coding:utf-8 -*-
"""
@Author: 王小飞
@File  : dataFalsification.py
@Time  : 2021/1/14 17:10
@Tool  : PyCharm
"""
from faker import Faker

"""伪造数据"""
china_fake = Faker("zh_CN")  # 修改本地化区域参数
us_fake = Faker("en_US")

print(china_fake.name())  # 生成一个姓名
print(china_fake.last_name())  # 姓
print(china_fake.first_name())  # 名
print(china_fake.phone_number())  # 生成号码
print(china_fake.user_name())  # 生成用户名
print(china_fake.password())  # 生成密码
print(china_fake.email())  # 生成邮箱
print(china_fake.phonenumber_prefix())  # 生成运营商号段，前三位
print(china_fake.country())  # 生成一个国家名
print(china_fake.city())  # 生成一个城市名
print(china_fake.city_suffix())  # 城市后缀
print(china_fake.address())  # 生成地址
print(china_fake.street_address())  # 生成街道地址
print(china_fake.street_name())  # 生成街道名称
print(china_fake.postcode())  # 生成邮编
print(china_fake.latitude())  # 生成维度
print(china_fake.longitude())  # 生成经度
print(china_fake.ean8())  # 生成8位条形码
print(china_fake.ean13())  # 生成13位条形码
print(china_fake.hex_color())  # 生成16进制表示的颜色
print(china_fake.rgb_css_color())  # 生成css用的rgb色
print(china_fake.rgb_color())  # 表示rgb色的字符串
print(china_fake.color_name())  # 生成颜色名
print(china_fake.safe_hex_color())  # 生成安全16进制颜色
print(china_fake.safe_color_name())  # 安全颜色名
print(china_fake.company())  # 生成公司名
print(china_fake.company_suffix())  # 公司名后缀
print(china_fake.credit_card_number(card_type=None))  # 生成卡号
print(china_fake.credit_card_provider(card_type=None))  # 卡的提供者
print(china_fake.credit_card_security_code(card_type=None))  # 卡的安全密码
print(china_fake.credit_card_expire())  # 卡的有效期
print(china_fake.credit_card_full(card_type=None))  # 完整的卡信息
print(china_fake.currency_code())  # 生成货币代码
print(china_fake.time(pattern="%H:%M:%S"))  # 生成随机的时间
print(china_fake.date(pattern="%Y-%m-%d"))  # 生成随机的日期
print(china_fake.date(pattern="%Y-%m-%d") + " " + china_fake.time(pattern="%H:%M:%S"))  # 随机的日期加时间
print(china_fake.file_name(category="image", extension="png"))  # 生成文件名（指定文件类型和后缀名）
print(china_fake.file_name())  # 随机生成各类型文件
print(china_fake.file_extension(category=None))  # 生成文件后缀
print(china_fake.mime_type(category=None))  # 生成文件类型
print(china_fake.ipv4(network=False))  # 生成IPV4地址
print(china_fake.ipv6(network=False))  # 生成IPV6地址
print(china_fake.uri_path(deep=None))  # 生成uri路径
print(china_fake.uri_extension())  # 生成uri扩展名
print(china_fake.uri())  # 生成uri
print(china_fake.url())  # 生成url
print(china_fake.image_url(width=None, height=None))  # 生成图片url
print(china_fake.user_agent())  # 生成User-Agent
print(china_fake.safe_email())  # 生成安全邮箱
print(china_fake.free_email())  # 生成免费邮箱
print(china_fake.company_email())  # 生成公司邮箱
print(china_fake.job())  # 生成工作职位
print(china_fake.words(nb=3))  # 生成3个字
print(china_fake.text(max_nb_chars=200))  # 生成一百字的文章
print(china_fake.paragraph(nb_sentences=4, variable_nb_sentences=True))  # 随机生成一段文字
print(china_fake.paragraphs(nb=3))  # 随机生成几段文字
print(china_fake.word())  # 生成随机的字
print(china_fake.sentences(nb=3))  # 随机生成几个句子
print(china_fake.binary(length=10))  # 随机二进制字符串，可指定长度
print(china_fake.md5(raw_output=False))  # 随机md5，16进制字符串
print(china_fake.sha1(raw_output=False))  # 随机sha1，16进制字符串
print(china_fake.sha256(raw_output=False))  # 随机sha265，16进制字符串
print(china_fake.boolean(chance_of_getting_true=50))  # 随机真假值(得到True的几率是50%)
print(china_fake.null_boolean())  # 随机真假值和null
print(china_fake.uuid4())  # 随机uuid
print(china_fake.profile(fields=None, sex=None))  # 人物描述信息：姓名、性别、地址、公司等
print(china_fake.ssn())  # 随机生成身份证号(18位)
# ------------python数据----------
print(china_fake.pyint())  # 生成整数
print(china_fake.pyfloat(left_digits=None, right_digits=None, positive=False))  # 生成浮点数
print(china_fake.pydecimal(left_digits=None, right_digits=None, positive=False))  # 随机高精度数
print(china_fake.pystr(min_chars=None, max_chars=200))  # 随机字符串，可指定长度
print(china_fake.pybool())  # 随机bool值
print(china_fake.pyiterable(nb_elements=5, variable_nb_elements=True))  # 随机的可迭代对象
print(china_fake.pylist(nb_elements=5, variable_nb_elements=True))  # 随机的列表
print(china_fake.pydict(nb_elements=5, variable_nb_elements=True))  # 随机的字典
print(china_fake.pytuple(nb_elements=5, variable_nb_elements=True))  # 随机的元祖
print(china_fake.pyset(nb_elements=5, variable_nb_elements=True))  # 随机的集合
# -----------浏览器伪造-----------
print(china_fake.internet_explorer())  # IE
print(china_fake.opera())  # opera
print(china_fake.chrome())  # chrome
print(china_fake.firefox())  # Firefox
print(china_fake.safari())  # Safari

print(china_fake.pystr(min_chars=None, max_chars=100))  # 随机字符串，可指定长度
