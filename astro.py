#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import sys

class Astro:

	def __init__(self, country:str, city:str):
		# opens relevant pages
		self.page = urllib2.urlopen('https://www.timeanddate.com/astronomy/'+country+'/'+city)
		self.soup = BeautifulSoup(self.page, 'html.parser')
		self.moonpage = urllib2.urlopen('https://www.timeanddate.com/moon/phases/'+country+'/'+city)
		self.soup2 = BeautifulSoup(self.moonpage, 'html.parser')


	def moon_state(self):
		# finds current moon state (percentage lit, description)
		moon_per = self.soup.find(id="cur-moon-percent").text
		moon_info = self.soup.findAll(class_="three columns tc", id="qlook")
		for x in moon_info:
			moon_state = x.find("p").text
		return [moon_per, moon_state]


	def risesets(self):
		# extracts sun/moon presence
		sunmoon_info = self.soup.findAll("span", class_="three")
		sunrise = sunmoon_info[0].text
		sunset = sunmoon_info[1].text
		moonrise = sunmoon_info[2].text
		moonset = sunmoon_info[3].text
		return [sunrise, sunset, moonrise, moonset]

		
	def day_length(self):
		# fetches length of day (not to be confused with hours of sun)
		daylight_info = self.soup.findAll(class_="five columns", id="qfacts")
		for tags in daylight_info:
			spans = tags.findAll("span")

		day_length = spans[15].text
		return day_length


	def moon_phases(self):
		# grabs table of moon phases 
		data = []
		table = self.soup2.find("table", class_="fw hoz tb-hover")
		rows = table.findAll("tr")
		for row in rows:
			cols = row.findAll("td")
			for text in cols: # cols is everything delimited with td, text is month/day pairs
				# creates list of day elements, puts spaces back in
				text = str(text)
				text = text.replace(u'\xa0', u' ')
				text = re.split(">,", text)

				# cleans
				for entry in text:
					entry = str(entry)
					if "<td>" in entry:
						entry = re.sub('<td>', '', entry)
					if "</td>" in entry:
						entry = re.sub('</td>', '', entry)
					if "moon1" in entry:
						entry = re.sub('(<img.*(moon1)?)', '🌑', entry)
					if "moon2" in entry:
						entry = re.sub('(<img.*(moon2)?)', '🌓', entry)
					if "moon3" in entry:
						entry = re.sub('(<img.*(moon3)?)', '🌕', entry)
					if "moon4" in entry:
						entry = re.sub('(<img.*(moon4)?)', '🌗', entry)
					entry = entry.replace(" ", "")
					data.append(entry)
		return data
		

	def moon_events(self):
		# parses table of moon events
		moon_info = self.soup2.findAll("h3", class_="mgt0")[1].next_sibling
		points = moon_info.findAll("li")

		data = []
		for bullet in points:
			if bullet.a:
				if len(bullet.contents) is 2:
					entry = str(bullet.a.contents[0]) + str(bullet.contents[1])
				else:
					entry = str(bullet.a.contents[0])
			else:
				entry = str(bullet.contents[0])
			data.append(entry)
		return data


	def moon_to_unicode(self, state: str):
		# reversed unicode descriptions since most terminals are white on black
		symbol = ""
		if state == "New Moon":
			symbol = "🌕"
		elif state == "Waxing Crescent":
			symbol = "🌖"
		elif state == "First Quarter":
			symbol = "🌗" 
		elif state == "Waxing Gibbous":
			symbol = "🌘"
		elif state == "Full Moon":
			symbol = "🌑"
		elif state == "Waning Gibbous":
			symbol = "🌒"
		elif state == "Last Quarter":
			symbol = "🌓"
		elif state == "Waning Crescent":
			symbol = "🌔"
		return symbol

	def calculate_iss_pos(self):
		return ""


def printdisplay(country: str, city: str):
	# make magic, pipe output to lolcat (https://github.com/busyloop/lolcat) for better effects
	# terminal should be at least 107x34
	a = Astro(country, city)
	p = a.moon_phases()
	print("\t\t\t\t\t\t\t|")
	print("             ___---___         			        |\t2018 Moon Phases Calendar")
	print("          .--         --.      			        |\t" + p[0] + "\t" + p[1] + "  " + p[2] + "  " + p[3] + "  " + p[4] + "  " + p[5])
	print("        ./   ()      .-. \.    			        |\t" + p[6] + "\t" + p[7] + "  " + p[8] + "  " + p[9])
	print("       /   o    .   (   )  \   			        |\t" + p[10] + "\t" + p[11] + "  " + p[12] + "  " + p[13] + "  " + p[14] + "  " + p[15])
	print("      / .            '-'    \  			        |\t" + p[16] + "\t" + p[17] + "  " + p[18] + "  " + p[19] + "  " + p[20])
	print("     | ()    .  O         .  | 			        |\t" + p[21] + "\t" + p[22] + "  " + p[23] + "  " + p[24] + "  " + p[25])
	print("    |                         |			        |\t" + p[26] + "\t" + p[27] + "  " + p[28] + "  " + p[29] + "  " + p[30])
	print("    |    o           ()       |			        |\t" + p[31] + "\t" + p[32] + "  " + p[33] + "  " + p[34] + "  " + p[35])
	print("    |       .--.          O   |			        |\t" + p[36] + "\t" + p[37] + "  " + p[38] + "  " + p[39] + "  " + p[40])
	print("     | .   |    |            | 			        |\t" + p[41] + "\t" + p[42] + "  " + p[43] + "  " + p[44] + "  " + p[45])
	print("      \    `.__.'    o   .  /  			        |\t" + p[46] + "\t" + p[47] + "  " + p[48] + "  " + p[49] + "  " + p[50] + "  " + p[51])
	print("       \                   / \t" + a.moon_state()[1] + " " + a.moon_to_unicode(a.moon_state()[1]) + "\t|\t" + p[52] + "\t" + p[53] + "  " + p[54] + "  " + p[55] + "  " + p[56])
	print("        `\  o    ()      /' \t\t" + a.moon_state()[0] + "\t\t|\t" + p[57] + "\t" + p[58] + "  " + p[59] + "  " + p[60] + "  " + p[61])
	print("          `--___   ___--'      			        |\t")
	print("                ---            			        |\t")
	print("    Sunrise: " + a.risesets()[0] + "\tMoonrise: " + a.risesets()[2] + "\t\t|\t")
	print("    Sunset: " + a.risesets()[1] + "\tMoonset: " + a.risesets()[3] + "\t\t|\t")
	print("    Length of Day: " + a.day_length() + "\t|\t")
	print("\t\t\t\t\t\t\t|")
	print("  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
	events_list = a.moon_events()
	for x in events_list:
		print("    " + x)
	print()


if __name__ == "__main__":
	if len(sys.argv) is not 3:
		print("Usage: ./astro.py country city")
		print("Note: needs to be recognized when you visit www.timeanddate.com/astronomy/<country>/<city> and www.timeanddate.com/moon/phases/<country>/<city>")
	if urllib2.urlopen("https://www.timeanddate.com/moon/phases/"+str(sys.argv[1])+"/"+str(sys.argv[2])).getcode() is 200:
		printdisplay(sys.argv[1], sys.argv[2])
	else:
		print("astro: unknown location"+sys.argv[1]+sys.argv[2])
