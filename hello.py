from uiautomation import WindowControl  # 引入uiautomation库中的WindowControl类，用来进行图像识别和模拟操作
from openai import OpenAI

client = OpenAI(api_key="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")

# 绑定微信主窗口
wx = WindowControl(
    Name='微信',
    searchDepth=1
)
# 切换窗口
wx.ListControl()
wx.SwitchToThisWindow()
# 寻找会话控件绑定
hw = wx.ListControl(Name='会话')
# 死循环接收消息
while True:
    # 从查找未读消息,通过用户列表右上角的未读信息角标判断是否存在
    we = hw.TextControl(searchDepth=4)
    # 死循环维持，没有超时报错
    while not we.Exists():
        pass
    if we.Name:
        we.Click(simulateMove=False)
        last_msg = wx.ListControl(Name='消息').GetChildren()[-1].Name
        print('1')
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": last_msg}],
            stream=True,
        )
        print('2')
        result = ""
        for chunk in stream:
            answer = chunk.choices[0].delta.content
            print(answer)
            if answer is not None:
                result += answer
            else:
                print(result, end="")
                print(wx)
                wx.SendKeys(text = result, waitTime=1)
                wx.SendKeys('{Enter}', waitTime=1)
                wx.ButtonControl(searchDepth=4, Name="聊天").Click()
        print('3')
