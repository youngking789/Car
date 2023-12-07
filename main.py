import cv2
import pygame
import btn
import file
import get_carder
import Right
import sql
import sys
# 0已入库 1已出库 2未入库成功


def window():  # 窗口
    pygame.init()  # 初始化Pygame
    pygame.display.set_caption('智能停车场车牌识别计费系统')  # 设置窗口名字
    screen = pygame.display.set_mode((1000, 484))  # 创建窗口
    background = (135, 206, 235)  # 背景颜色
    screen.fill(background)  # 设置背景颜色

    button_wid = 150  # 按钮宽度
    button_he = 65  # 按钮高度
    button_color = (176, 23, 31)  # 按钮颜色
    button_x = 490  # 按钮x轴
    button_y = 422  # 按钮y轴
    text_color = (255, 255, 255)  # 字体颜色
    text_x = 535  # 文字x轴
    text_y = 440  # 文字y轴

    button_wid2 = 120
    button_he2 = 55
    button_color2 = (255, 128, 0)
    button_x2 = 870
    button_y2 = 425
    text_color2 = (255, 255, 255)
    text_x2 = 890
    text_y2 = 440

    allCar = 5  # 共有车位
    img_size = (640, 485)  # 摄像头大小
    imgxy = (0, 0)  # 视频坐标
    r = Right.right(screen, background)  # 实例化对象

    try:
        cap = cv2.VideoCapture(0)  # 创建摄像头
    except:
        print('没有摄像头')
    while True:
        img = file.file('img/temp.jpg').readwrite(cap)
        img = pygame.transform.scale(img, img_size)  # 设置图片大小
        screen.blit(img, imgxy)  # 绘制视频画面,blit函数将image绘制在screen上,参数是x,y坐标
        button1 = btn.button(screen, button_wid, button_he, button_color, button_x, button_y, text_color, text_x, text_y)
        button2 = btn.button(screen, button_wid2, button_he2, button_color2, button_x2, button_y2, text_color2, text_x2, text_y2)
        for event in pygame.event.get():  # 获取鼠标动作
            if event.type == pygame.QUIT:  # 如果点击删除就退出
                cap.release()  # 释放摄像头
                cv2.destroyAllWindows()
                pygame.quit()  # 退出窗口
                sql.Sql().close()  # 关闭游标
                # exit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 如果是点击
                x, y = event.pos  # 获取当前鼠标的x,y轴
                if button_x + button_wid >= x >= button_x and button_y + button_he >= y >= button_y:  # 判断x,y轴在不在框里
                    file.file('img/get.png').readwrite(cap)  # 截取一帧图片截到文件里
                    get_carder.get_carder('img/get.png', background).get_car(allCar, screen)  # 获取图片中的车牌
                elif button_x2 + button_wid >= x >= button_x2 and button_y2 + button_he2 >= y >= button_y2:
                    r.stat()
        r.top_font((255, 255, 255), 700, 40, allCar)  # 定义文字  颜色，坐标，共有车位，背景颜色
        r.line()  # 定义线条
        r.font('车号\t\t\t\t\t时间', (255, 255, 255), 720, 90, 20)
        r.sel()  # 查询出停车场内车辆
        r.down()  # 停车时间最长的
        r.money()  # 计算停车费
        r.yujin()  #
        button1.button('识别', 30)  # 调用button函数
        button2.button('收入统计', 20)  # 按钮2
        pygame.display.update()  # 更新屏幕


if __name__ == '__main__':
    window()
