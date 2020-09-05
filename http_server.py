# -*- coding: utf-8 -*-
from flask import Flask, request, Response
from util.core.create_wav import *
from util.base.file import *
from util.config import configuration

app = Flask(__name__)


@app.route('/')
def hello_world():
	return 'hello world'


@app.route('/create', methods=['GET'])
def create_wav_file():
	get_data = request.args

	# id
	if "id" in get_data:
		id = get_data["id"]
	else:
		id = 0

	print(id)

	# TODO:get from GET_DATA
	# 歌词
	lyrics = ["グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ",
			  "グー",
			  "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー",
			  "グーあ",
			  "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー"]

	# 全曲参数
	bpm = 140
	divisions = 4  # 用4代表一个四分音符的长度
	# 拍数
	time_num = 4
	time_divide = 4
	# 小节数
	bar_num = 2

	# 在规定目录生成文件
	create_wav(bpm, divisions, time_num, time_divide, bar_num, lyrics)

	# 将xml文件，wav文件copy至output下
	print("\nMove files Start:\n")
	xml_origin_path = configuration.path + configuration.path_xml + configuration.filename + ".musicxml"
	xml_new_path = "output/musicxml/" + str(id) + ".musicxml"
	print(xml_origin_path, xml_new_path)
	movefile(xml_origin_path, xml_new_path)

	wav_origin_path = configuration.path + configuration.path_wav + configuration.filename + "_syn.wav"
	wav_new_path = "output/audio/" + str(id) + ".wav"
	movefile(wav_origin_path, wav_new_path)
	print(wav_origin_path, wav_new_path)

	return "ok, id:" + str(id)


@app.route('/wav', methods=['GET'])
def return_wav_file():
	get_data = request.args

	# id
	if "id" in get_data:
		id = get_data["id"]
	else:
		id = 0

	# wav文件位置
	wav_path = "output/audio/" + str(id) + ".wav"

	return Response(generate(wav_path), mimetype="audio/x-wav")


@app.route('/direct', methods=['GET'])
def direct_wav_file():
	get_data = request.args

	# id
	if "id" in get_data:
		id = get_data["id"]
	else:
		id = 0

	print(id)

	# TODO:get from GET_DATA
	# 歌词
	lyrics = ["グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ",
			  "グー",
			  "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー",
			  "グーあ",
			  "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー"]

	# 全曲参数
	bpm = 140
	divisions = 4  # 用4代表一个四分音符的长度
	# 拍数
	time_num = 4
	time_divide = 4
	# 小节数
	bar_num = 2

	# 在规定目录生成文件
	create_wav(bpm, divisions, time_num, time_divide, bar_num, lyrics)

	# 将xml文件，wav文件copy至output下
	print("\nMove files Start:\n")
	xml_origin_path = configuration.path + configuration.path_xml + configuration.filename + ".musicxml"
	xml_new_path = "output/musicxml/" + str(id) + ".musicxml"
	print(xml_origin_path, xml_new_path)
	movefile(xml_origin_path, xml_new_path)

	wav_origin_path = configuration.path + configuration.path_wav + configuration.filename + "_syn.wav"
	wav_new_path = "output/audio/" + str(id) + ".wav"
	movefile(wav_origin_path, wav_new_path)
	print(wav_origin_path, wav_new_path)

	# wav文件位置
	wav_path = "output/audio/" + str(id) + ".wav"

	return Response(generate(wav_path), mimetype="audio/x-wav")


# 支持返回音频流
def generate(wav_path):
	with open(wav_path, 'rb') as wav:
		data = wav.read(1024)
		while data:
			yield data
			data = wav.read(1024)


'''
@app.route('/commandslist', methods=['POST'])
def http_commandslist():
	get_data = request.args
	post_data = request.form
	auth_result = auth(post_data)
	if auth_result == 0:
		if "page" not in get_data or "page_size" not in get_data:
			return {"result": False, "content": "命令错误：参数错误"}

		page = int(get_data["page"])
		page_size = int(get_data["page_size"])
		list = commandsList()
		start = (page - 1) * page_size
		end = min(page * page_size, len(list))

		return {"result": True, "content": list[start:end]}
	else:
		return {"result": False, "content": auth_result}


@app.route('/avatar', methods=['GET'])
def http_avatar():
	get_data = request.args
	if "user" in get_data:
		url = ""
		with open("res/json/admin_avatar_url.json", 'r') as load_file:
			avatar_list = json.load(load_file)
		for bot in avatar_list:
			if bot["account"] == get_data["user"]:
				url = bot["avatar_url"]

		# 直接返回图片
		if url == "":
			return
		else:
			with open("res/image/" + url, 'rb') as f:
				image = f.read()
			resp = Response(image, mimetype="image/jpeg")
			return resp
	else:
		return
'''
# 端口设置
app.run(host='127.0.0.1', port=configuration.port)
