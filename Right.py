import datetime

import pygame
import sql
import matplotlib.pyplot as plt


class right:
    def __init__(self, screen, background):
        self.screen = screen  # 窗体
        self.mysql = sql.Sql()  # 实例化sql类
        self.background = background

    def font(self, text, color, x, y, size):  # 文字
        font = pygame.font.Font('C:/Windows/Fonts/simsun.ttc', size)  # 字体大小
        t = font.render(text, True, color)  # 文字 颜色
        self.screen.blit(t, (x, y))  # 绘制文字

    def top_font(self, color, x, y, have_che):  # 顶部文字
        s = 'select count(*) from vehicle'  # sql语句
        a = self.mysql.select(s)  # 执行查询语句
        chewei = have_che - a[0][0]  # 剩余车位
        pygame.draw.rect(self.screen, self.background, (700, 40, 300, 20))  # 绘画矩形框覆盖
        right.font(self, f'共有车位：{have_che}，剩余车位：{chewei}', color, x, y, 20)  # 输出文字

    def line(self):
        start_pos = 660, 80  # 起点
        end_pos = 970, 80  # 终点
        color = (255, 0, 0)  # 定义颜色
        pygame.draw.line(self.screen, color, start_pos, end_pos)  # 绘制直线

    def sel(self):
        s = "select 车牌号,DATE_FORMAT(入库时间,'%Y-%m-%d %H:%i:%s') from vehicle"  # sql语句
        a = self.mysql.select(s)  # 执行查询操作
        x = 700  # 车辆信息x轴
        y = 100  # 车辆信息y轴
        pygame.draw.rect(self.screen, self.background, (700, 120, 300, 120))  # 绘画矩形框覆盖
        if a != 0:  # 如果有信息就输出
            for i in a:  # 遍历循环出信息
                text = f'{i[0]}\t\t\t{i[1]}'  # 输出文字
                y += 20  # 每行加20间距
                right.font(self, text, (255, 255, 255), x, y, 15)  # 绘制文字
        else:  # 如果没信息则什么都不做
            pass

    def down(self):
        s = 'select 车牌号,timestampdiff(hour,入库时间,now()) from vehicle ORDER BY 入库时间 asc limit 1'  # 查询出车牌号停车时间
        jieguo = self.mysql.select(s)  # 执行sql语句
        pygame.draw.rect(self.screen, self.background, (650, 265, 200, 45))  # 绘制矩形框覆盖文字
        if jieguo != 0:  # 如果有值：
            text1 = f'停车时间最长车辆：{jieguo[0][0]}'
            text2 = f'停车时间：{jieguo[0][1]}小时'
            right.font(self, text1, (255, 255, 255), 650, 270, 15)
            right.font(self, text2, (255, 255, 255), 702, 290, 15)
        pygame.draw.rect(self.screen, (255, 0, 0), (650, 320, 340, 100), 1)  # 绘制矩形线条框

    def enterCarInfo(self, car, time):  # 入库车辆信息
        pygame.draw.rect(self.screen, self.background, (651, 321, 338, 98))  # 绘制矩形框
        text1 = '入库车辆信息'
        text2 = f'车牌号:{car}'
        text3 = '有空余车位,可以进入停车场'
        text4 = f'进入停车场时间:{time}'
        color = (255, 0, 0)
        right.font(self, text1, color, 660, 330, 15)
        right.font(self, text2, color, 740, 350, 15)
        right.font(self, text3, color, 730, 370, 15)
        right.font(self, text4, color, 700, 390, 15)

    def outCarInfo(self, car, time, m):  # 出库车辆信息
        pygame.draw.rect(self.screen, self.background, (651, 321, 338, 98))  # 绘制矩形框
        text1 = '出库车辆信息'
        text2 = f'车牌号:{car}'
        text3 = f'停车费:{m}元'
        text4 = f'进入停车场时间:{time}'
        color = (255, 0, 0)
        right.font(self, text1, color, 660, 330, 15)
        right.font(self, text2, color, 740, 350, 15)
        right.font(self, text3, color, 730, 370, 15)
        right.font(self, text4, color, 700, 390, 15)

    def maxInfo(self, car, time):  # 出库车辆信息
        pygame.draw.rect(self.screen, self.background, (651, 321, 338, 98))  # 绘制矩形框
        text1 = '车辆信息'
        text2 = f'车牌号:{car}'
        text3 = '车位已满，入库失败'
        text4 = f'进入停车场时间:{time}'
        color = (255, 0, 0)
        right.font(self, text1, color, 660, 330, 15)
        right.font(self, text2, color, 740, 350, 15)
        right.font(self, text3, color, 730, 370, 15)
        right.font(self, text4, color, 700, 390, 15)

    def nullInfo(self):
        pygame.draw.rect(self.screen, self.background, (651, 321, 338, 98))  # 绘制矩形框
        text1 = '未识别到车牌'
        color = (255, 0, 0)
        right.font(self, text1, color, 730, 350, 30)

    def money(self):  # 计费规则 小于30分钟0元，小于2小时4元，超过两小时每小时3块，封顶70
        s = 'select 车牌号 from vehicle;'
        value = self.mysql.select(s)
        if value != 0:
            for chepai in value:
                s = f'select timestampdiff(minute,入库时间,now()) from vehicle where 车牌号 = \'{chepai[0]}\''
                t = self.mysql.select(s)[0][0]
                if t < 30:
                    v = '0'
                elif 30 < t < 120:
                    v = '4'
                elif 120 < t < 1440:
                    v = '3 * (timestampdiff(hour,入库时间,now())-1)+4'
                else:
                    v = '70'
                s = f'update vehicle set 停车费用 = {v} where 车牌号 = \'{chepai[0]}\''
                s1 = f'update information set 停车费用 = {v} where 车牌号 = \'{chepai[0]}\''
                self.mysql.update(s)
                self.mysql.update(s1)

    def stat(self):
        month = datetime.datetime.today().month
        x_data = [f'{i}月' for i in range(month-3, month)]
        y_data = []
        for i in range(month - 3, month):
            s = f"select 停车费用 from information where MONTH(出库时间) = {i} and 停车状态 = 1"
            y = self.mysql.select(s)
            if y != 0:
                y_data.append(sum(y[0]))
            else:
                y_data.append(y)
        plt.rcParams["font.sans-serif"] = ["SimSun"]
        plt.rcParams["axes.unicode_minus"] = False
        # 画图，plt.bar()可以画柱状图
        for i in range(len(x_data)):
            plt.bar(x_data[i], y_data[i])
        # 设置图片名称
        plt.title(f"停车场{x_data[0]}---{x_data[-1]}的数据统计")
        # 设置x轴标签名
        plt.xlabel("月份")
        # 设置y轴标签名
        plt.ylabel("停车费用")
        # 显示
        plt.show()

    def yujin(self):
        dt = datetime.datetime.now().weekday()+1
        if dt == 0:
            pygame.draw.rect(self.screen, (255, 255, 0), (0, 1, 640, 50))
            text = '根据数据分析,明天可能出现车位紧张的情况,请提前做好调度!'
            color = (255, 0, 0)
            x = 5
            y = 12
            size = 23
            right.font(self, text, color, x, y, size)
