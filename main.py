from util.core.create_wav import *
from util.base.file import *

# id
id = 1

# 歌词
lyrics = ["グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー",
		  "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ", "グー", "グーあ",
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
wav_new_path = "output/audio/" + str(id) + "_syn.wav"
movefile(wav_origin_path, wav_new_path)
print(wav_origin_path, wav_new_path)
