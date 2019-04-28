import os
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["TweetAttuali"]
mycol = mydb["tweets"]
mydb2 = myclient["AnalisiTweebo"]
mycol2 = mydb2["tweets"]

#mycol2.delete_many({});


for document in mycol.find({}):

	obj = document['user']

	print(obj['id'])

	try:

		inputTweet = document['text'].encode('utf-8').strip().replace("\n", " ")

		f = open("input.txt", "w")
		f.write(inputTweet)
		f.close()

		#print("1: FILE SCRITTO")

		myCmd = './runTagger.sh input.txt > out.txt'
		os.system(myCmd)

		file = open("out.txt", "r") 
		output = str(file.read())

		#print("2: FILE LETTO")

		#print(v)
		#stringa = str(v)
		indice = output.index("0,")
		#print(indice)
		dato = output.replace(output[indice:],"").split()
		#print(dato)

		lunghezza = len(dato)
		#print(lunghezza)

		lun = lunghezza / 2

		#print (lun)

		sostantivi = []
		entita = []
		parole_nonNecessarie = []

		if lun == 0:
			print("ERRORE -- tweet nullo")
		else:
			for i in range(lun,lunghezza,1):
				#print(i)
				if dato[i] == "N":
					sostantivi.append(i)
				elif dato[i] == "^":
					entita.append(i)
				elif dato[i] == "~" or dato[i] == "@" or dato[i] == "U" or dato[i] == "#":
					parole_nonNecessarie.append(i)

		#s = []
		#e = []

		stringa_s = ""
		stringa_e = ""


		for x in sostantivi:
			#s.append(dato[x-lun])
			stringa_s += dato[x-lun] + ";"


		for y in entita:
			#e.append(dato[y-lun])
			stringa_e += dato[y-lun] + ";"

		#print("#######")
		#print(stringa_s)
		#print("#######")
		#print(stringa_e)


		tweetToken = ""
		tweetPulito = ""

		for z in range(0,lun,1):
			tweetToken += dato[z] + " "

		for z in range(0,lun,1):
			if z+lun not in parole_nonNecessarie:
				tweetPulito += dato[z] + " "

		#print(tweetToken)
		#print(tweetPulito)
		#print(parole_nonNecessarie)


		mycol2.insert_one({ "user_id": obj['id'], "TweetTokenizzato": tweetToken, "TweetPulitoTokenizzato": tweetPulito, "sostantivi": stringa_s, "entita": stringa_e })

		#print(document['text'])
		#print(tweetToken)
		#print(tweetPulito)
		#print(stringa_s)
		#print(stringa_e)

		print("3: FILE INSERITO")


	except Exception as e:
		print(e)




