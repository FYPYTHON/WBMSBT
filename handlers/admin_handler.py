#coding=utf-8
import hashlib
from handlers.base_handler import BaseHandler
from json import dumps as json_dumps
from method.generate_verify_image import generate_verify_image
import re
import base64
import random
import weblog
class verifyCode(BaseHandler):
    def get(self):
        pass

    def post(self):
        fg_color=random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        try:
            mstream, strs = generate_verify_image(save_img=False,fg_color=fg_color, font_type="method/Arial.ttf")
            # self.write(simplejson.dumps({'code': 0, 'img': stream.getvalue().encode('base64')}))
            # self.set_cookie("code", strs)
            self.set_secure_cookie("code", strs)
            weblog.info("%s , imgage code:%s",self._request_summary(),strs)
            # img = mstream.getvalue().encode('base64')
            img = base64.b64encode(mstream.getvalue()).decode()
            return self.write(json_dumps({'code': strs, 'img': img}))
        except:
            weblog.exception("verify image code error")
            return

