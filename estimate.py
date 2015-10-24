# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    estimate.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aderuell <aderuell@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/10/24 20:29:52 by aderuell          #+#    #+#              #
#    Updated: 2015/10/24 21:07:02 by aderuell         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
#!/nfs/zfs-student-5/users/2013/aderuell/.brew/bin/python3
# -*-codinf:tuf-8 -*

from sys import argv

def estimatePrice(t0, t1, mileage):
	return t0 + (t1 * float(mileage))

def scaleKm(km, min_km, max_km):
	return ((km - min_km) / (max_km - min_km))

def unscalePrice(price, min_price, max_price):
	return (price * (max_price - min_price) + min_price)

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
			scale_km = scaleKm(int(km), min_km, max_km)
			price = estimatePrice(t0, t1, scale_km)
			estimate_price = unscalePrice(price, min_price, max_price)
			print('km = ', km, '\t\testimate price = ', estimate_price)
		except:
			print(0)
			exit()
