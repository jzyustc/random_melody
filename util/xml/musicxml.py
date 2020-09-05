import numpy as np
import wave
import struct
import random
from util.config import configuration
from util.xml.smarty import *

xml_path = configuration.path + configuration.path_xml


def musicxml(divisions: int, bpm: int, time_num: int, time_divide: int, bar_num: int, note_array_pitch,
			 xml_file_name: str):
	# 获取xml头
	with open("res/musicxml/begin.musicxml", "rb") as file:
		begin = file.read()
		file.close()

	# 获取xml尾
	with open("res/musicxml/end.musicxml", "rb") as file:
		end = file.read()
		file.close()

	# 组织中间段落
	middle = musicxml_middle(divisions, bpm, time_num, time_divide, bar_num, note_array_pitch)

	# 打开文件
	with open(xml_path + xml_file_name, "wb") as file:
		file.write(begin)
		file.write(bytes(middle, encoding="utf8"))
		file.write(end)
		file.close()


# 生成中间变化的段落
def musicxml_middle(divisions: int, bpm: int, time_num: int, time_divide: int, bar_num: int, note_array):
	middle = ""

	# 运行到数组的记号
	flag = -1

	# 累计长度
	length_accum = 0

	# 对每个小节遍历
	for i in range(bar_num):
		print("\nmeasure " + str(i) + " begin")

		# 小节内实际音符
		note_array_measure = []

		# 第一个音符是否为上一小节延音
		if length_accum < 16 * i:
			tied = True
			# 添加延音元素
			note_tied = note_array[flag][:]
			note_tied.append([False, True])  # tie:stop
			note_tied[2] -= 16 * i - length_accum
			note_array_measure.append(note_tied)
			length_accum += note_array[flag][2]
		else:
			tied = False

		# 计算,组合成一个五元组数组：（pitch, octave, duration, lyric, tie: [bool(start), bool(stop)]）
		for j in range(flag + 1, len(note_array)):

			# 到达下一个小节
			if length_accum + note_array[j][2] > 16 * (i + 1):
				flag = j - 1
				# 最后一个是延音
				if length_accum < 16 * (i + 1):
					flag += 1
					note_last = note_array[j][:]
					note_last.append([True, False])  # tie:start
					note_last[2] = 16 * (i + 1) - length_accum
					note_array_measure.append(note_last)
				break

			length_accum += note_array[j][2]
			note_array[j].append([False, False])  # tie: None
			note_array_measure.append(note_array[j])

		# 按照延音切割音符
		note_array_measure = split_note_by_tie(note_array_measure, divisions)

		# 每个小节的xml
		middle += musicxml_middle_measure(divisions, bpm, time_num, time_divide, i, note_array_measure)

		print("measure " + str(i) + " ok!\n")

	return middle


# 按照延音切割音符为 (1/2)^n 音符长
def split_note_by_tie(note_array_measure, divisions):
	new_array = []
	for note in note_array_measure:

		# 拆分音符
		flag = False
		duration = note[2]
		split_division = 4 * divisions
		while duration != 0:
			if duration >= split_division:

				# 如果拆分成了两个以上音符，前一个音符添加start
				if flag:
					new_array[-1][4] = [True, new_array[-1][4][1]]

				new_note = note[:]
				new_note[2] = split_division

				# 如果拆分成了两个以上音符，后一个音符添加stop
				if flag:
					new_note[4] = [new_note[4][0], True]

				new_array.append(new_note)
				duration -= split_division
				flag = True  # 从第二个音符开始，前一个音符start，后一个音符stop

			split_division = int(split_division / 2)

	return new_array


base_path = "res/musicxml/"


# 生成一个小节
def musicxml_middle_measure(divisions: int, bpm: int, time_num: int, time_divide: int, bar_id: int, note_array):
	# 五元组数组：（pitch, octave, duration, lyric, tie: [bool(start), bool(stop)]）
	print(note_array)
	xml = ""

	# attr$dire
	ad = smarty(base_path + "attr&dire.musicxml", ["divisions", "time_num", "time_divide", "bpm"],
				[divisions, time_num, time_divide, bpm]) if bar_id == 0 else ""

	# note
	notes = ""
	for note_attr in note_array:
		notes += musicxml_note(note_attr)

	xml += smarty(base_path + "measure.musicxml", ["measure_no", "attr&dire", "notes"], [bar_id + 1, ad, notes])

	return xml


# 生成一个note
def musicxml_note(note_attr):
	step = configuration.note[note_attr[0]][0]

	alter = smarty(base_path + "note/contents/alter.musicxml", ["alter"], [1]) if len(
		configuration.note[note_attr[0]]) == 2 else ""

	if note_attr[0] == -1:
		# rest
		contents = smarty(base_path + "note/contents/rest.musicxml", [], [])
		lyric = ""
		notations = ""
		tie = ""
	else:
		# pitch
		contents = smarty(base_path + "note/contents/pitch.musicxml", ["step", "alter", "octave"],
						  [step, alter, note_attr[1]])
		lyric = smarty(base_path + "note/lyric.musicxml", ["lyric", "lyric_num"],
					   [note_attr[3], len(note_attr[3])]) if not note_attr[4][1] else ""
		tie = smarty(base_path + "note/tie.musicxml", ["tie"], ["stop"]) if note_attr[4][1] else ""
		tie += smarty(base_path + "note/tie.musicxml", ["tie"], ["start"]) if note_attr[4][0] else ""
		notations = smarty(base_path + "note/notations.musicxml", ["tie"], [tie]).replace("tie",
																						  "tied") if tie != "" else ""

	type_id = len(configuration.note_type) - int(np.log2(note_attr[2])) - 1
	type = configuration.note_type[type_id]

	xml = smarty(base_path + "notes.musicxml", ["contents", "duration", "lyric", "notations", "tie", "type"],
				 [contents, note_attr[2], lyric, notations, tie, type])

	return xml
