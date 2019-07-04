# coding: utf-8
"""
author:zs1621
source:https://github.com/zs1621/tornado-redis-session
python3 must chang grammar
"""

import uuid
import hmac
import ujson
import hashlib
import redis
import weblog


class SessionData(dict):
	def __init__(self, session_id, hmac_key):
		self.session_id = session_id
		self.hmac_key = hmac_key

	# @property
	# def sid(self):
	# 	return self.session_id
	#
	# @x.setter
	# def sid(self, value):
	# 	self.session_id = value


class Session(SessionData):
	def __init__(self, session_manager, request_handler):

		self.session_manager = session_manager
		self.request_handler = request_handler

		try:
			current_session = session_manager.get(request_handler)
		except InvalidSessionException:
			current_session = session_manager.get()
		for key, data in current_session.items():
			self[key] = data
		self.session_id = current_session.session_id
		self.hmac_key = current_session.hmac_key
	
	def save(self):
		# print(self.request_handler, self)
		self.session_manager.set(self.request_handler, self)


class SessionManager(object):
	def __init__(self, secret, store_options, session_timeout):
		self.secret = secret
		self.session_timeout = session_timeout
		try:
			if store_options['redis_pass']:
				self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'], password=store_options['redis_pass'])
			else:
				self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'])
		except Exception as e:
			weblog.exception(e)

	def _fetch(self, session_id):
		try:
			session_data = raw_data = self.redis.get(session_id)
			if raw_data is not None:
				self.redis.setex(session_id, self.session_timeout, raw_data)
				session_data = ujson.loads(raw_data)

			# if type(session_data) == type({}):
			if isinstance(session_data, type({})):
				return session_data
			else:
				return {}
		except IOError:
			return {}

	def get(self, request_handler=None):
		if request_handler is None:
			session_id = None
			hmac_key = None
		else:
			session_id = request_handler.get_secure_cookie("session_id")
			hmac_key = request_handler.get_secure_cookie("verification")
		# print("session get:", request_handler, session_id, hmac_key)

		if session_id is None:
			session_exists = False
			session_id = self._generate_id()
			hmac_key = self._generate_hmac(session_id)
		else:
			session_exists = True
		check_hmac = self._generate_hmac(session_id)
		if hmac_key != check_hmac:
			raise InvalidSessionException()

		session = SessionData(session_id, hmac_key)

		if session_exists:
			session_data = self._fetch(session_id)
			for key, data in session_data.items():
				session[key] = data
		return session
	
	def set(self, request_handler, session):
		request_handler.set_secure_cookie("session_id", session.session_id)
		request_handler.set_secure_cookie("verification", session.hmac_key)

		session_data = ujson.dumps(dict(session.items()))

		self.redis.setex(session.session_id, self.session_timeout, session_data)

	def _generate_id(self):
		secret = self.secret
		if isinstance(secret, (bytes, bytearray)):
			secret = secret.decode('utf-8')
		new_id = hashlib.sha256(bytes(secret + str(uuid.uuid4()), encoding='utf-8'))
		return new_id.hexdigest()

	def _generate_hmac(self, session_id):
		if isinstance(session_id, str):
			session_id = bytes(session_id,encoding='utf-8')
		secret = self.secret
		if isinstance(secret, str):
			secret = bytes(secret, encoding='utf-8')
		# print(session_id, type(session_id))
		# print(secret, type(secret))
		return hmac.new(session_id, secret, hashlib.sha256).hexdigest()


class InvalidSessionException(Exception):
	pass

