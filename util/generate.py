import numpy as np
import wave
import struct
import random
from util.config import configuration


# 产生音符列的长度（以十六分音符计算）
def generate_note_array_length(p_length, semiquaver_num: int):
	# 产生累加概率
	p_accumulate = p_accumlate_array(p_length)

	# 随机产生音符长度
	all_note_length = 0
	all_note = []
	while all_note_length < semiquaver_num:
		# 生成一个随机长度
		note_length = generate_note_one_length(p_accumulate)
		# 没有超过长度限制
		if all_note_length + note_length <= semiquaver_num:
			all_note_length += note_length
			all_note.append(note_length)
		# 超过总长度限制
		else:
			note_length = semiquaver_num - all_note_length
			all_note_length += note_length
			all_note.append(note_length)

	return all_note


# 产生一个音符的长度（以十六分音符计算）
def generate_note_one_length(p_accumulate):
	# 随机数（概率盘）
	p = random.uniform(0, 1)
	note_len = 0
	for i in range(len(p_accumulate)):
		if p < p_accumulate[i]:
			note_len = i + 1
			break

	if note_len == 0:
		return len(p_accumulate) + 1
	else:
		return note_len


# 产生音高序列
def generate_note_all_pitch(note_num: int, note_weigh, note_next):
	# 产生第一个音符
	note_weigh_accumlate = p_accumlate_array(note_weigh)
	p = random.uniform(0, note_weigh_accumlate[len(note_weigh_accumlate) - 1])
	first_note_pitch_id = 0
	for i in range(len(note_weigh_accumlate)):
		if p < note_weigh_accumlate[i]:
			first_note_pitch_id = i
			break

	# 产生音符串
	note_array_pitch = [[first_note_pitch_id, 5 if first_note_pitch_id <= 4 else 4]]
	before_note_pitch_id = first_note_pitch_id
	before_note_octive = 4
	while len(note_array_pitch) < note_num:
		next_note = generate_note_one_pitch(before_note_pitch_id, before_note_octive, note_weigh, note_next)
		note_array_pitch.append(next_note)
		before_note_pitch_id = next_note[0]
		before_note_octive = next_note[1]

	return note_array_pitch


# 根据前一个音高产生后一个
def generate_note_one_pitch(pitch_id: int, octive: int, note_weigh, note_next):
	# 产生上下五度内的概率（以半音为单位，-7到7）
	p_list = []
	for i in range(len(note_next)):
		id = (pitch_id + 5 + i) % 12
		p = note_weigh[id] * note_next[i]
		p_list.append(p)

	# 根据概率生成随机音高
	p_accumlate = p_accumlate_array(p_list)
	p = random.uniform(0, p_accumlate[-1])
	id = 0
	for i in range(len(p_accumlate)):
		if p < p_accumlate[i]:
			id = i
			break

	# 判断后一个音的位置
	if pitch_id - 7 + id < 0:
		octive -= 1
	elif pitch_id - 7 + id >= 12:
		octive += 1

	return [(pitch_id + 5 + id) % 12, octive]


# 产生累加概率
def p_accumlate_array(p_array):
	p_accumulate = []
	p_flag = 0
	for p in p_array:
		p_flag += p
		p_accumulate.append(p_flag)
	return p_accumulate


# 产生音频波形数列
def generate_audio_array(duration: float, framerate: int, frequency: float, volume: int):
	x = np.linspace(0, duration, num=int(duration * framerate))
	y = np.sin(2 * np.pi * frequency * x) * volume
	return y


# 产生波形文件
def generate_audio_file(filename: str, framerate: int, sample_width: int, audio_array):
	# save wav file
	wf = wave.open(filename, 'wb')
	wf.setnchannels(1)
	wf.setframerate(framerate)
	wf.setsampwidth(sample_width)
	for i in audio_array:
		data = struct.pack('<h', int(i))
		wf.writeframesraw(data)
	wf.close()
