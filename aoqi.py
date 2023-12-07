import requests
import logging
import json
from colorlog import ColoredFormatter


class Aoqi():
    def __init__(self):
        self.urls = ["https://service.100bt.com/aqsy_wxmp_sign/sign_in.jsonp",
                     "https://service.100bt.com/aqsy_wxmp_sign/user_info.jsonp"]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                          "like Gecko)"
                          "Chrome/119.0.0.0 Mobile Safari/537.36 Edg/119.0.0.0",
            "Host": "service.100bt.com",
            "Referer": "https://aqsy.100bt.com/",

        }

    def get_cookies(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            return config
        except FileNotFoundError as e:
            return 0

    def main(self):
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)-8s%(reset)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info("获取配置文件")
        config = self.get_cookies()
        if config == 0:
            logger.error("获取配置文件失败，请检查config.json文件是否存在")
            return
        logger.info("获取配置文件成功")
        logger.info("开始签到!")
        users = config.keys()
        count, total = 0, len(users)
        try:
            for user in users:
                cookies = {"BT_SESSION": config[user]["BT_SESSION"],
                           "BT_AUTO_0701-aqsy-qiandao": config[user]["BT_AUTO_0701-aqsy-qiandao"]}
                sign_in, user_info = self.urls[0], self.urls[1]
                try:
                    res = requests.get(url=sign_in, headers=self.headers, cookies=cookies)
                    msg = res.json()["jsonResult"]["message"]
                    logger.info(f"{user}: {msg}")
                except Exception as e:
                    logger.error(e)
                try:
                    res = requests.get(url=user_info, headers=self.headers, cookies=cookies)
                    signInTotal = res.json()["jsonResult"]["data"]["signInTotal"]
                    logger.info(f"{user}签到成功，签到次数：{signInTotal}")
                    count += 1
                except Exception as e:
                    logger.error(e)

        except Exception as e:
            logger.error(e)
            return
        logger.info(f"签到完成，共签到{total}人，签到成功{count}人")


if __name__ == '__main__':
    aoqi = Aoqi()
    aoqi.main()
