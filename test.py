# -*- coding: utf-8 -*-
import os, time


pdir = "/run/media/liveuser/hard/xp"
fcsv = open("csv.csv", "w")	

#функции
def changepath(path):
	path_ch = path
	for i in range(len(path_ch)*2):
		if (path_ch[i-1] != "\\"):
			path_ch = path_ch[0:i] + "\\" + path_ch[i:len(path_ch) + 1]
	return path_ch

def permission(path):
	os.system("ls -l " + path + " > permission")
	f_permission = open("permission", "r")
	perm = f_permission.read(10)
	return perm

def md5hash(path):
	check_hash = permission(path)
	if (check_hash[1] != "p"):
		os.system("md5sum " + path + " > md5hash")
		f_md5 = open("md5hash", "r")
		return f_md5.read(32)
	else:
		return " "

def changenameneo4j(path):
	path_ch = path
	path = path.replace(" ", "_")
	path = path.replace("/", "_")
	path = path.replace("'", "")
	return path		
	
numofcolumns = 350
a = []
a.append([","] * numofcolumns)
a[0][0] = "number,"
a[0][1] = "path,"
a[0][2] = "name,"
a[0][3] = "permissions,"
a[0][4] = "hashmd5,"
a[0][5] = "fileext,"
a[0][6] = "typefile,"
a[0][7] = "creation date,"
a[0][8] = "time of last access,"
a[0][9] = "time of last change,"
a[0][10] = "size,"

#проход по файлам

i = 0
count = 0
for ij, dirs, files in os.walk(pdir):
	for f in files:
#		if (i != 50):
		fullpath = os.path.join(ij, f)
		c = changepath(fullpath)
		a.append([","]*numofcolumns)
	
		print i + 1
		filename = fullpath.split('/')[-1]
		filepath = fullpath[0:len(fullpath)-len(filename)]	
		fileext = fullpath.split('.')[-1]
		a[i+1][0] = str(i + 1) + ","
		a[i+1][1] = filepath + ","
		a[i+1][2] = filename + ","
		a[i+1][3] = permission(c) + ","
		a[i+1][4] = md5hash(c) + ","
		if (len(fileext) != len(fullpath)):
			a[i+1][5] = fileext + ","
		a[i+1][7] = str(time.ctime(os.path.getctime(fullpath))) + ","
		a[i+1][8] = str(time.ctime(os.path.getatime(fullpath))) + ","
		a[i+1][9] = str(time.ctime(os.path.getmtime(fullpath))) + ","
		a[i+1][10] = str(os.path.getsize(fullpath)) + ","
		os.system('hachoir-metadata ' + c + ' 2&> 123456')
		f123456 = open("123456", "r")
		strchar = f123456.readline()
		if (strchar[0] == '['):
			os.system('hachoir-metadata ' + c + ' 2&>> errorlog.txt')
			count = count + 1
			i = i + 1
		else:
			if (fileext == "7z"):
				a[i+1][6] = "Archive,"	
			elif (fileext == "a"):
				a[i+1][6] = "Archive,"
						
			elif (fileext == "ace"):
				a[i+1][6] = "Archive,"

			elif (fileext == "bz2"):
				a[i+1][6] = "Archive,"
		
			elif (fileext == "cab"):
				a[i+1][6] = "Archive,"
		
			elif (fileext == "gz"):
				a[i+1][6] = "Archive,"
		
			elif (fileext == "iso"):
				a[i+1][6] = "ISO,"

			elif (fileext == "jar"):
				a[i+1][6] = "Archive,"
		
			elif (fileext == "mar"):
				a[i+1][6] = "Archive,"

			elif (fileext == "rar"):
				a[i+1][6] = "Archive,"

			elif (fileext == "tar"):
				a[i+1][6] = "Archive,"
			elif (fileext == "zip"):
				a[i+1][6] = "Archive,"
			elif (fileext == "txt"):
				a[i+1][6] = "TXT,"
			else:
				res = 0
				os.system('hachoir-metadata '+ c + ' > 	123456')
				for g in open("123456", "r"):
					if (res == 0): #res == 0 poluchaem tip faila, res ! 0 poluchaem parametri
						filetype = g[0:len(g)-2]	
						a[i+1][6] = filetype + ","
						res = res + 1
					else: #name_par - zagolovki, file_param - ix znacenie					
						name_par = g.split(":")[0]
						name_par = name_par[2:len(name_par)]
						file_param = g[len(name_par)+4:len(g)-1]
						res_columns = 0
						res_col = 0
						for j in range(numofcolumns):
							if (str(a[0][j]) == str(name_par) + ","):									res_columns = j
							if (a[0][j] == ","):
								res_col = j
								break
						if (res_columns == 0): #esli 0, t.e. ne naiden takoi zagolovok, to dobavliem ego
							a[0][res_col] = name_par + ","
							a[i+1][res_col] = file_param + ","
						else:
							a[i+1][res_columns] = str(a[i+1][res_columns]).split(",")[0]  + "  "+ file_param + ","	
			i = i + 1
			count = count + 1
		#else:
		#	break
#	if (i == 50):
#		break

for g in range(i+1):
	for j in range(numofcolumns):
		if (j == numofcolumns-1):
			fcsv.write(str(a[g][j]) + "\n")
		else:
			fcsv.write(str(a[g][j]))
"""
fneo4j = open("neo4j", "w")
fneo4j.write("CREATE (HDD:Memory {title:'HDD'})" + "\n")
for g in range(i):
	strneo = str(a[g+1][2]).split(',')[0]
	fneo4j.write("CREATE (FILE" + str(g+1) + ":File {name:'" + str(strneo) + "'")


	fneo4j.write("," + a[0][1].split(",")[0] + ": '" + a[g+1][1].split(",")[0] + "'")
	fneo4j.write("," + a[0][2].split(",")[0] + ": '" + a[g+1][2].split(",")[0] + "'")
	fneo4j.write("," + a[0][3].split(",")[0] + ": '" + a[g+1][3].split(",")[0] + "'")
	fneo4j.write("," + a[0][4].split(",")[0] + ": '" + a[g+1][4].split(",")[0] + "'")
	fneo4j.write("," + a[0][5].split(",")[0] + ": '" + a[g+1][5].split(",")[0] + "'")
	fneo4j.write("," + a[0][6].split(",")[0] + ": '" + a[g+1][6].split(",")[0] + "'")
	fneo4j.write("})" + "\n")


fneo4j.close()
fneo4j = open("neo4j", "a")
fneo4j.write("\n" + "CREATE" + "\n")
for g in range(i):
	strneo = str(a[g+1][2]).split(',')[0]
	if (g+1 == i):
		fneo4j.write("(FILE" + str(g+1) + ")-[:file]->(HDD)"+"\n")
	else:
		fneo4j.write("(FILE" + str(g+1) + ")-[:file]->(HDD),"+"\n")

for g in range(i):
	for j in range(numofcolumns):#numofcolumns
		if (a[g+1][j] != ","):
			fneo4j.write("CREATE (PARAM" + str(g+1) + "_" + str(j) + ":Param {name:'" + changenameneo4j(str(a[g+1][j].split(',')[0])) + "'})" + "\n")
			fneo4j.write("CREATE" + "\n" + "(PARAM" + str(g+1) + "_" + str(j) + ")-[:" + changenameneo4j(str(a[0][j].split(",")[0])) +"]->(FILE" + str(g+1) + ")" + "\n")

fneo4j.write("\n" + "RETURN HDD,")
"""
