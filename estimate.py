# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    estimate.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderuell <aderuell@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/10/24 20:29:52 by aderuell          #+#    #+#              #
#    Updated: 2015/10/30 14:17:03 by aderuell         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
#!/.brew/bin/python3
# -*-codinf:tuf-8 -*

from sys import argv
from regression import LinearRegression

#Main
del argv[0]
if len(argv) < 1:
	print('Not enough arguments')
	print('Usage : python3 estimate.py <km> ...')
else:
	for km in argv:
		try:
			fichier = open('result.txt', 'r')
			t0 = float(fichier.readline())
			t1 = float(fichier.readline())
			min_km = int(fichier.readline())
			max_km = int(fichier.readline())
			min_price = int(fichier.readline())
			max_price = int(fichier.readline())
			lr = LinearRegression()
			lr.constructeurEstimate(t0, t1, max_km, min_km, max_price, min_price)
			scale_km = lr.scaleKm(int(km))
			price = lr.estimatePrice(scale_km)
			estimate_price = lr.unscalePrice(price)
			if int(estimate_price) < 0:
				estimate_price = 0
			print('Km =', km, '\t\tEstimate price =', int(estimate_price))
		except:
			print(0)
			exit()
