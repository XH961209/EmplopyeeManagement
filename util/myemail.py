import smtplib
from email.mime.text import MIMEText


def send_email(receivers, subject, content):
    mail_host = 'smtp.qq.com'
    mail_user = '3024693372@qq.com'
    mail_pass = 'dxvwvdhtikvddfec'
    sender = '3024693372@qq.com'

    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = subject
    # 发送方信息
    message['From'] = sender

    # 登录并发送邮件
    try:
        smtp_obj = smtplib.SMTP()
        # 连接到服务器
        smtp_obj.connect(mail_host, 587)
        # 登录到服务器
        smtp_obj.login(mail_user, mail_pass)
        # 发送
        smtp_obj.sendmail(sender, receivers, message.as_string())
        # 退出
        smtp_obj.quit()
    except smtplib.SMTPException as e:
        raise e


if __name__ == "__main__":
    send_email(["21210240375@m.fudan.edu.cn"], "您的密码", "123")
