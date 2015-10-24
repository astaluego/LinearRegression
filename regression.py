# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    regression.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderuell <aderuell@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/10/22 14:44:46 by aderuell          #+#    #+#              #
#    Updated: 2015/10/24 20:19:47 by aderuell         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
#!/nfs/zfs-student-5/users/2013/aderuell/.brew/bin/python3
# -*-codinf:tuf-8 -*

from sys import argv
import matplotlib.pyplot as plt
import csv

def estimatePrice(t0, t1, mileage):
	return t0 + (t1 * mileage)

class LinearRegression():
	t0 = 0.0
	t1 = 0.0
	learningRate = 0.1
	iterations = 10000
	precision = None
	dictionnaire = {}
	m = 0
	max_km = None
	max_price = None
	min_km = None
	min_price = None

	def __init__(self, fichier, precision):
		self.precision = precision
		for row in fichier:
			km = int(row['km'])
			price = int(row['price'])
			self.dictionnaire[km] = price
			if self.max_km is None:
				self.max_km = km
			else:
				if self.max_km < km:
					self.max_km = km
			if self.min_km is None:
				self.min_km = km
			else:
				if self.min_km > km:
					self.min_km = km
			if self.max_price is None:
				self.max_price = price
			else:
				if self.max_price < price:
					self.max_price = price
			if self.min_price is None:
				self.min_price = price
			else:
				if self.min_price > price:
					self.min_price = price
			self.m += 1

	def scaleKm(self, value):
		return ((value - self.min_km) / (self.max_km - self.min_km))

	def scalePrice(self, value):
		return ((value - self.min_price) / (self.max_price - self.min_price))

	def unscalePrice(self, value):
		return (value * (self.max_price - self.min_price) + self.min_price)

	def computeError(self):
		total = 0
		for km, price in self.dictionnaire.items():
			total += (price - (self.m * km + self.t0 )) ** 2
		return total / float(self.m)

	def gradientDescentRunner(self):
		for i in range(self.iterations):
			self.machineLearning()

	def machineLearning(self):
		sum_t0 = 0.0
		sum_t1 = 0.0
		tmp = self.learningRate * (1/self.m)
		for km, price in self.dictionnaire.items():
			km = self.scaleKm(km)
			price = self.scalePrice(price)
			sum_t0 += estimatePrice(self.t0, self.t1, km) - price
			tmp_t0 = tmp * sum_t0;
			sum_t1 += (estimatePrice(self.t0, self.t1, km) - price) * km
			tmp_t1 = tmp * sum_t1;
			self.t0 = self.t0 - (self.learningRate * tmp_t0)
			self.t1 = self.t1 - (self.learningRate * tmp_t1)

	def showGraph(self):
		x = list(self.dictionnaire.keys())
		y = list(self.dictionnaire.values())
		plt.xlabel('Km')
		plt.ylabel('Price')
		plt.plot(x, y, 'ro')
		plt.plot([self.unscalePrice(estimatePrice(self.t0, self.t1, self.scaleKm(x))) for x in range(self.min_km, self.max_km)])
		plt.show()

#Main
del argv[0]
if len(argv) < 1 or len(argv) >= 3:
	print('Not enough arguments')
	print('Usage : python3 regression.py <data.csv> [<precision>]')
else:
	#Open csv
	try:
		fichier = csv.DictReader(open(argv[0],'r'))
	except IOError:
		print('Cannot open', argv[0])
		exit()

	#Keep precision
	if len(argv) >= 2:
		try:
			precision = float(argv[1])
		except ValueError:
			print('Bad precision')
			exit()
	else:
		precision = 0

	lr = LinearRegression(fichier, precision)
	lr.gradientDescentRunner()
	#print(lr.t0)
	#print(lr.t1)
	#for km, price in lr.dictionnaire.items():
	#	tmp_km = lr.scaleKm(km)
	#	tmp_price = lr.unscalePrice(estimatePrice(lr.t0, lr.t1, tmp_km))
	#	print('km :', km, ' price:', price, ' => ', tmp_price)
	lr.showGraph()
