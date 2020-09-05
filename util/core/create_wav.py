import os
from util.core.generate import *
from util.xml.musicxml import *
from util.config import configuration

path = configuration.path


def create_wav(bpm: int, divisions: int, time_num: int, time_divide: int, bar_num: int, lyrics: [str]):
	# 计算十六分音符数量
	semiquaver_num = bar_num * 16 * time_num / time_divide
	note_array_length = generate_note_array_length(configuration.length, int(semiquaver_num))
	print("\nnote lengths : \n", note_array_length)

	# 根据前一个音产生后一个音高
	note_array_pitch = generate_note_all_pitch(len(note_array_length), configuration.note_weigh,
											   configuration.note_next)
	print("\nnote pitch : \n", note_array_pitch)

	# 组合成一个四元组数组：（pitch, octive, duration, lyric）
	note_array = note_array_pitch[:]
	for i in range(len(note_array_length)):
		note_array[i].append(note_array_length[i])
		note_array[i].append(lyrics[i])

	empty_measure = [-1, -1, divisions * 4, ""]
	note_array.insert(0, empty_measure)
	note_array.append(empty_measure[:])
	print("\nnote : \n", note_array)

	# 生成xml文件
	musicxml(divisions, bpm, time_num, time_divide, bar_num + 2, note_array, configuration.filename + ".musicxml")

	# 运行NEUTRINO
	commands_filter = "res/commands/"
	commands_file = "run"
	commands_path = ""
	if configuration.system == "linux":
		commands_path = commands_filter + "linux_bash/" + commands_file
	elif configuration.system == "windows":
		commands_path = commands_filter + "windows_dos/" + commands_file
	with open(commands_path, "rb") as file:
		commands = bytes.decode(file.read())
		file.close()

	cmd = commands % path

	print(cmd)
	os.system(cmd)
