import time
import uuid
from aip import AipOcr
import file
import sql
import Right
import pygame


class get_carder:
    def __init__(self, img_file, background):
        self.img_file = img_file
        self.background = background

    def get_car(self, allCar, screen):  # 获取车牌
        file.file('conf/log.txt').log()  # 调用log函数
        APP_ID, API_KEY, SECRET_KEY = file.file('conf/conf.ini').cof()  # 调用cof函数
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)  # 配置百度aip
        image = file.file(self.img_file).get_file_content()  # 读取图片二进制数据
        res = client.licensePlate(image)  # 解析图片二进制
        s = sql.Sql()
        r = Right.right(screen, self.background)
        if 'words_result' in res.keys():
            res_image = res['words_result']['number']
            res_color = res['words_result']['color']
            print('-----------------')
            print('车牌:', res_image)
            print('颜色:', res_color)
            print('-----------------')
            count = s.select('select count(*) from vehicle')[0][0]  # 查询有几条数据
            exist = s.select(f'select 车牌号 from vehicle where 车牌号 = \'{res_image}\'')  # 如果在库中返回0
            if exist == 0:  # 判断这个车是出库还是入库，存在就出库，不存在就入库
                if count != allCar:  # 没有到最大停车数
                    mysql = f'insert into vehicle values(\'{uuid.uuid1()}\',\'{res_image}\',now(),0,0)'  # 插入到实时的停车场信息表里
                    mysql2 = f"insert into information values(\'{uuid.uuid1()}\',\'{res_image}\',now(),\'1111-11-11 11:11:11\',0,0)"  # 插入到历史表
                    if s.insert(mysql) > 0 and s.insert(mysql2) > 0:  # 判断插入成功没有
                        q = s.select(f"select DATE_FORMAT(入库时间,'%Y-%m-%d %H:%i:%s') from vehicle where 车牌号 = \'{res_image}\'")  # 查询出时间
                        r.enterCarInfo(res_image, q[0][0])  # 将时间和车牌号输出到界面
                        print('入库成功')
                else:  # 停满了车
                    mysql2 = f"insert into information values(\'{uuid.uuid1()}\',\'{res_image}\',now(),\'1111-11-11 11:11:11\',0,2)"  # 插入到历史表记录
                    s.insert(mysql2)
                    t = time.localtime()  # 获取当前时间
                    r.maxInfo(res_image, time.strftime('%Y-%m-%d %H:%M:%S', t))  # 输出车牌号和当前时间
                    print('车位已满')
            else:  # 如果是出库
                mysql1 = f"select 停车费用,DATE_FORMAT(入库时间,'%Y-%m-%d %H:%i:%s') from vehicle where 车牌号 = \'{exist[0][0]}\'"  # 查询停车费用和时间
                value = s.select(mysql1)  # 执行sql语句
                m = value[0][0]  # 费用
                t = value[0][1]  # 时间
                mysql2 = f'update information set 出库时间 = now(),停车状态 = 1 where 车牌号 = \'{exist[0][0]}\''  # 更新历史表中的出库时间
                s.update(mysql2)
                mysql3 = f'delete from vehicle where 车牌号 = \'{exist[0][0]}\''  # 在实时表中删除数据
                if s.delete(mysql3) > 0:
                    r.outCarInfo(exist[0][0], t, m)  # 绘制信息在界面
                    print('出库成功')
        else:
            r.nullInfo()
            print('未识别到车牌')

