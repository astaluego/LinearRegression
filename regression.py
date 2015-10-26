# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    regression.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderuell <aderuell@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/10/22 14:44:46 by aderuell          #+#    #+#              #
#    Updated: 2015/10/26 16:10:37 by aderuell         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
#!/.brew/bin/python3
# -*-codinf:tuf-8 -*

from sys import argv
import matplotlib.pyplot as plt
import csv

class LinearRegression():
	t0 = 0.0
	t1 = 0.0
	learningRate = 0.1
	iterations = 10000
	dictionnaire = {}
	m = 0
	max_km = None
	max_price = None
	min_km = None
	min_price = None

	def __init__(self):
		pass

	def constructeurRegression(self, fichier):
		for row in fichier:
			km = int(row['km'])
			price = int(row['price'])
			self.dictionnaire[km] = price
			self.m += 1
		self.max_km = max(self.dictionnaire.keys())
		self.min_km = min(self.dictionnaire.keys())
		self.max_price = max(self.dictionnaire.values())
		self.min_price = min(self.dictionnaire.values())
	
	def constructeurEstimate(self, t0, t1, max_km, min_km, max_price, min_price):
		self.t0 = t0
		self.t1 = t1
		self.max_km = max_km
		self.min_km = min_km
		self.max_price = max_price
		self.min_price = min_price

	def scaleKm(self, value):
		return ((value - self.min_km) / (self.max_km - self.min_km))

	def scalePrice(self, value):
		return ((value - self.min_price) / (self.max_price - self.min_price))

	def unscalePrice(self, value):
		return (value * (self.max_price - self.min_price) + self.min_price)

	def gradientDescent(self):
		for i in range(self.iterations):
			self.machineLearning()

	def machineLearning(self):
		sum_t0 = 0.0
		sum_t1 = 0.0
		tmp = self.learningRate * (1/self.m)
		for km, price in self.dictionnaire.items():
			km = self.scaleKm(km)
			price = self.scalePrice(price)
			sum_t0 += self.estimatePrice(km) - price
			tmp_t0 = tmp * sum_t0;
			sum_t1 += (self.estimatePrice(km) - price) * km
			tmp_t1 = tmp * sum_t1;
			self.t0 = self.t0 - (self.learningRate * tmp_t0)
			self.t1 = self.t1 - (self.learningRate * tmp_t1)

	def showGraph(self):
		x = list(self.dictionnaire.keys())
		y = list(self.dictionnaire.values())
		plt.xlabel('Km')
		plt.ylabel('Price')
		plt.plot(x, y, 'ro')
		plt.plot([self.unscalePrice(self.estimatePrice(self.scaleKm(x))) for x in range(self.min_km, self.max_km)])
		plt.show()

	def putResultsInFile(self):
		fichier = open('result.txt', 'w')
		lst = (self.t0, self.t1, self.min_km, self.max_km, self.min_price, self.max_price)
		string = '\n'.join(map(str, lst)) + '\n'
		fichier.write(string)
		fichier.close()

	def estimatePrice(self, mileage):
		return self.t0 + (self.t1 * float(mileage))

#Main
if __name__ == '__main__':
	del argv[0]
	if len(argv) < 1 or len(argv) >= 2:
		print('Bad arguments')
		print('Usage : python3 regression.py <data.csv>')
		exit()
	else:
		#Open csv
		try:
			fichier = csv.DictReader(open(argv[0],'r'))
		except IOError:
			print('Cannot open', argv[0])
			exit()
		lr = LinearRegression()
		lr.constructeurRegression(fichier)
		lr.gradientDescent()
		lr.putResultsInFile()
		lr.showGraph()
