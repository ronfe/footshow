homeP, drawP, awayP = 0.3427, 0.2769, 0.3804
X1O, X2O = 1.36, 1.57

price = 0.0
result = []
while price <= 10.0:
    homeV = X1O * price
    awayV = X2O * (10- price)
    togetherV = homeP * homeV + drawP * (homeV + awayV) + awayP * awayV
    reduceV = homeP * (10-price) + awayP * price
    result.append(togetherV / reduceV)
    price += 0.01

print (result.index(max(result)))