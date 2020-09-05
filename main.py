import os
from util.play import *
from util.generate import *
from util.xml.musicxml import *
from util.config import configuration

lyrics = ["グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー",
		  "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ",
		  "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー",
		  "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ",
		  "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー",
		  "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", ]

# 全曲参数
framerate = 44100
sample_width = 2
volume = 1000
bpm = 140
divisions = 4  # 用4代表一个四分音符的长度
path = configuration.path
# 拍数
time_num = 4
time_divide = 4
# 小节数
bar_num = 2

# 计算十六分音符数量
semiquaver_num = bar_num * 16 * time_num / time_divide
note_array_length = generate_note_array_length(configuration.length, int(semiquaver_num))
print("\nnote lengths : \n", note_array_length)

# 根据前一个音产生后一个音高
note_array_pitch = generate_note_all_pitch(len(note_array_length), configuration.note_weigh, configuration.note_next)
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

'''
# 生成音符时长-音频列表
audio_array = []
filename = configuration.filename + ".wav"

for i in range(len(note_array_length)):
	# 时长
	one_duration = 15.0 / bpm
	duration = one_duration * note_array_length[i]
	# 音高
	id = note_array_pitch[i][0]
	pitch = configuration.note_pitch[id]
	octive = note_array_pitch[i][1]
	frequency = pitch * (2 ** (octive - 5))

	# 将波形数据转换成数组
	new_audio_array = generate_audio_array(duration, framerate, frequency, volume)
	audio_array.extend(new_audio_array)

# 生成wave
generate_audio_file(path + filename, framerate, sample_width, audio_array)

# 播放音频
play_audio(path + filename)
'''

# 运行NEU
print("D: ; cd " + path + " ; " + "Run.bat")
cmd = '''D: & \
	cd %s & \
	Run.bat & \
	''' % (path)

os.system(cmd)

play_audio(path + configuration.path_wav + configuration.filename + "_syn.wav")
