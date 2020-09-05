def smarty(path: str, names, contents):
	with open(path, "rb") as file:
		xml = bytes.decode(file.read())
		file.close()

	for i in range(len(names)):
		xml = xml.replace("$" + names[i] + "$", str(contents[i]))

	return xml
