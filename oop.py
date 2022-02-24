import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By


class Tools(object):
    """
    工具类
    """

    def __init__(self):
        pass

    def get_random_seq(self):
        """
        返回随机数
        """
        return f'{random.randint(0, 9999)}', f'{random.randint(0, 999)}', f'{random.randint(0, 999)}'


class CadDriver(object):
    """
    网页模拟发送数据类
    """

    def __init__(self, test_host_url):
        # self.test_host_url = 'http://www.jsons.cn/websocket/'
        self.test_host_url = test_host_url
        self.driver = None
        self.input_address = None  # 选择要测试的websocket地址
        self.input_test_message = None  # 请输入测试信息
        self.button_send_message = None  # 发送信息按钮
        self.button_web_link = None  # websocket连接按钮
        self.output = None  # 输出框

    def wd_init(self):
        """
        初始化
        """
        global driver  # 让浏览器窗口不自动关闭
        self.driver = webdriver.Chrome()
        self.driver.get(self.test_host_url)

    def wd_get_id(self):
        """
        获取控件ID
        """
        self.input_address = self.driver.find_element(By.ID, 'wsaddr')  # 选择要测试的websocket地址
        self.input_test_message = self.driver.find_element(By.ID, 'message')  # 请输入测试信息
        self.button_send_message = self.driver.find_element(By.XPATH,
                                                            '/html/body/div/div/div/div/div/div/form/div/span/button')  # 发送信息按钮
        self.button_web_link = self.driver.find_element(By.CLASS_NAME, 'btn,btn-success')  # websocket连接按钮
        self.output = self.driver.find_element(By.ID, 'output')  # 输出结果
        print(type(self.output))

    def link(self, url):
        """
        ws://221.178.225.58:9906/WebSocket'
        """

        self.input_address.send_keys(url)  # 输入服务器地址
        self.button_web_link.click()  # 点击连接按钮

    def send_message(self, data):
        """
        发送消息
        """
        self.input_test_message.send_keys(json.dumps(data, ensure_ascii=False))  # 发送心跳信息测试
        self.button_send_message.click()  # 点击发送测试信息按钮
        self.input_test_message.clear()  # 清空测试信息栏，以便发送下一条测试信息

    def get_data(self):
        """
        获取每次返回的结果
        """
        print(type(self.output))
        print(self.output.text)
        # print(self.output)

# test0 = CadDriver('aaa')
# test0.get_data()

class TestCall(object):
    def __init__(self):
        self.cadDriver = CadDriver('http://www.jsons.cn/websocket/')  #
        self.tools = Tools()

    def test_init(self):
        self.cadDriver.wd_init()
        self.cadDriver.wd_get_id()

    def link(self):
        """
        # 连接成功，可以开始测试
        """
        url = 'ws://221.178.225.58:9906/WebSocket'
        self.cadDriver.link(url)

    def xin_tiao(self):  # 心跳信息测试
        random_data = self.tools.get_random_seq()  # 调用tools对象中的get_random_seq类方法
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "heartbeat", }
        # print(f'你发送的消息是：\n{dic1}')
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)

    def shi_zhong_he_yan(self):  # 时钟核验
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "synctime", }
        self.cadDriver.send_message(dic1)
        # dic2 = {"seq": seq, "src": src, "dst": dst, "cmd": "synctime", }
        # input_test_message.send_keys(str(dic2))  # 发送时钟核验信息测试
        # button_send_message.click()  # 点击发送测试信息按钮
        # input_test_message.clear()  # 清空测试信息栏，以便发送下一条测试信息
        time.sleep(0.2)

    def zhu_dong_xia_fa_cad(self):  # 调度台CAD主动下发当前时间
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "time",
                " time ": "2021-12-09 08:30:00.123"}
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)

    def zhu_dong_fa_song_chezai(self):  # 车载台主动发送位置请求给CAD
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "querylocation", }
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)

    def hu_jiao_shen_qing(self):  # 呼叫申请
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "rtt", "mode": "emg",
                "ident": "1301",
                "stanum": "3", "carnum": "1021", "drvnum": "0099"}
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)

    def qing_qiu_gui_shu(self):  # 请求归属
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "attach", "assign": "00",
                "dir": "up", "trainnum": "2233"}
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)

    def yu_zhi_duao_xiao_xi(self):  # 发送预制短消息
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "msg", "ident": "1401",
                "SDS": "司机确认"}
        self.cadDriver.send_message(dic1)

    def dian_zi_gong_dan(self):  # 短消息及电子工单
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "msg", "ident": "1601",
                "sender": "190001", "senderName": "行调1", "type": "4", "sds": "注意瞭望"}
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)

    def guang_bo_kong_zhi(self):  # 广播控制
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": " startCPA ",
                "cpatg": "1601"}
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)

    def zi_jian_xin_xi(self):  # 自检信息
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "selftest",
                "type": "powerup",
                "mmiver": "mmi_V1.0", "hostver": "host_V1.0", "summary": "ok", "mmisum": "FF",
                "hostsum": "FF", "handset": "FF"}
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)

    def cheng_ke_dui_jiang(self):  # 乘客对讲控制
        random_data = self.tools.get_random_seq()
        dic1 = {"seq": random_data[0], "src": random_data[1], "dst": random_data[2], "cmd": "pap",
                "reqloc": "0000000000000000",
                "paploc": "0000000000000000", "drvmode": "fao", "truip": "10.11.12.123", "role": "11"}
        self.cadDriver.send_message(dic1)
        time.sleep(0.2)
    def get_output(self):
        self.cadDriver.get_data()
def testall():
    test1 = TestCall()

    test1.test_init()
    test1.link()
    test1.xin_tiao()
    test1.shi_zhong_he_yan()
    test1.zhu_dong_xia_fa_cad()
    test1.zhu_dong_fa_song_chezai()
    test1.hu_jiao_shen_qing()
    test1.qing_qiu_gui_shu()
    test1.yu_zhi_duao_xiao_xi()
    test1.dian_zi_gong_dan()
    test1.guang_bo_kong_zhi()
    test1.zi_jian_xin_xi()
    test1.cheng_ke_dui_jiang()
    time.sleep(3)
    test1.get_output()  # 获取输出结果

if __name__ == '__main__':
    testall()

    # time.sleep(3)


# test1 = Test()
# test1.link()
# # print("请输入要测试的功能：\n")
# # print("1.心跳信息测试\n"
# #       "2.时钟核验测试\n"
# #       "3.调度服务器CAD主动下发当前时间信息\n"
# #       "4.车载台设备主动发送位置请求给CAD\n"
# #       "5.呼叫申请\n"
# #       "6.请求归属\n"
# #       "7.发送预制短消息\n"
# #       "8.短消息及电子工单\n"
# #       "9.广播控制\n"
# #       "10.自检信息\n"
# #       "11.乘客对讲控制\n")
# # x = input('请输入')
# #
# # if x == 1:
# #     test1.xin_tiao()
# # test1.xin_tiao()
# # x = input('请输入序号')
# # if x == 1:
# #     test1.xin_tiao()
# # elif x == 2:
# #     test1.shi_zhong_he_yan()
# # elif x == 3:
# #     test1.zhu_dong_xia_fa_cad()
# # elif x == 4:
# #     test1.zhu_dong_fa_song_chezai()
# # elif x == 5:
# #     test1.hu_jiao_shen_qing()
# # elif x == 6:
# #     test1.qing_qiu_gui_shu()
# # elif x == 7:
# #     test1.yu_zhi_duao_xiao_xi()
# # elif x == 8:
# #     test1.dian_zi_gong_dan()
# # elif x == 9:
# #     test1.guang_bo_kong_zhi()
# # elif x == 10:
# #     test1.zi_jian_xin_xi()
# # elif x == 11:
# #     test1.cheng_ke_dui_jiang()
# test1.xin_tiao()
# test1.shi_zhong_he_yan()
# test1.zhu_dong_xia_fa_cad()
# test1.zhu_dong_fa_song_chezai()
# test1.hu_jiao_shen_qing()
# test1.qing_qiu_gui_shu()
# test1.yu_zhi_duao_xiao_xi()
# test1.dian_zi_gong_dan()
# test1.guang_bo_kong_zhi()
# test1.zi_jian_xin_xi()
# test1.cheng_ke_dui_jiang()
#
# time.sleep(1)
# print(output.text)
#
# # input_test_message_list = [{"seq": seq, "src": src, "dst": dst, "cmd": "heartbeat", },  # 心跳信息测试
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "synctime", },  # 时钟核验测试
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "time",
# #                             " time ": "2021-12-09 08:30:00.123"},
# #                            # 调度服务器CAD主动下发当前的时间信息
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "querylocation", },
# #                            # 车载台设备主动发送位置请求给调度台服务器CAD设备，调度服务器CAD将当前设备的位置信息下发给车载台设备
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "rtt", "mode": "emg", "ident": "1301",
# #                             "stanum": "3", "carnum": "1021", "drvnum": "0099"},
# #                            # 呼叫申请
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "attach", "assign": "00",
# #                             "dir": "up", "trainnum": "2233"},
# #                            # 请求归属
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "msg", "ident": "1401", "SDS": "司机确认"},
# #                            # 发送预制短消息
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "msg", "ident": "1601",
# #                             "sender": "190001", "senderName": "行调1", "type": "4", "sds": "注意瞭望"},
# #                            # 短消息及电子工单
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": " startCPA ", "cpatg": "1601"},
# #                            # 广播控制
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "selftest", "type": "powerup",
# #                             "mmiver": "mmi_V1.0", "hostver": "host_V1.0", "summary": "ok", "mmisum": "FF",
# #                             "hostsum": "FF", "handset": "FF"},
# #                            # 自检信息
# #                            {"seq": seq, "src": src, "dst": dst, "cmd": "pap", "reqloc": "0000000000000000",
# #                             "paploc": "0000000000000000", "drvmode": "fao", "truip": "10.11.12.123", "role": "11"}
# #                            # 乘客对讲控制
# #                            ]
# # for dic in input_test_message_list:  # 遍历列表，发送列表中的测试信息
# #
# #     input_test_message.send_keys(f'{dic}')  # 将dic转化为字符串再进行发送
# #     button_send_message.click()  # 点击发送测试信息按钮
# #     input_test_message.clear()  # 清空测试信息栏，以便发送下一条测试信息
# #
# # time.sleep(1)
# #
# #
# # f = open('test.docx', 'w')
# # output_results = driver.find_elements(By.XPATH, '//*[@id="output"]/div/span[2]')  # 获取服务器回应的信息的文本内容
# # for output_result in output_results:
# #     print(output_result.text)
# #     f.write(f'{output_result.text}'+'\n')
# #
# # f.close()
