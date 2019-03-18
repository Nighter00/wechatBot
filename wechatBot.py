#coding:utf-8
from wxpy import *
import os
import cv2

# 初始化机器人，扫码登陆
bot = Bot(cache_path=True)
my_friend = bot.friends().search('某某')[0]
# 发送文本给好友
#my_friend.send('Hello WeChat!')
#my_friend.send('我是机器人')
#bot.self.add()
#bot.self.accept()
#bot.self.send('兄弟')


def face(name):
    print('正在处理')

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    count = 0
    img = cv2.imread(name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        count += 1
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)
        font = cv2.FONT_HERSHEY_SIMPLEX

        roi_gray = gray[y:y + h / 2, x:x + w]
        roi_color = img[y:y + h / 2, x:x + w]

    cv2.imwrite("face_detected_1.jpg", img)  # 保存已经生成好的图片
    print(count)
    return count  # 返回人脸总数

@bot.register(Friend,PICTURE)
def face_msg(msg):
    image_name = msg.file_name
    friend = msg.chat
    print(msg.chat)
    print('接收图片')
    # face(image_name)
    msg.get_file('' + msg.file_name)
    count = face(image_name)
    if (count == 0):
        msg.reply(u'未检测到人脸')
    else:
        msg.reply_image("face_detected_1.jpg")
        msg.reply(u"检测到%d张人脸"%count)
    os.remove(image_name)
    os.remove("face_detected_1.jpg")


# 获取所有类型的消息（好友消息、群聊、公众号，不包括任何自己发送的消息）
# 并将获得的消息打印到控制台
@bot.register()
def print_others(msg):
    print(msg)

@bot.register(Friend, TEXT)
def reply_friend_msg(msg):
    print(msg)
    print(msg.file_name)
    msg.reply('我现在有事不在，请稍后联系')
# 回复 my_friend 发送的消息
@bot.register(my_friend)
def reply_my_friend(msg):
    return 'received: {}'.format(msg.text)


# 回复发送给自己的消息，可以使用这个方法来进行测试机器人而不影响到他人
@bot.register(bot.self, except_self=False)
def reply_self(msg):
    return 'received: {} ({})'.format(msg.text, msg.type)

# 打印出所有群聊中@自己的文本消息，并自动回复相同内容
# 这条注册消息是我们构建群聊机器人的基础
@bot.register(Group, TEXT)
def print_group_msg(msg):
    if msg.is_at:
        print(msg)
    #msg.reply(msg.text)

# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 接受好友请求
    new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send('哈哈，我自动接受了你的好友请求')
embed()
