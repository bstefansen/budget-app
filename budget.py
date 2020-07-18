class Category:

  def __init__(self, category):
    self.category = category
    self.totalDeposit = 0
    self.totalWithdraw = 0
    self.ledger = []

  def category(self):
    return self.category

  def deposit(self, amount, *description):
    self.totalDeposit += amount
    self.ledger.append({
      "amount": amount, 
      "description": str(description[0]) if description else ""
    })

  def withdraw(self, amount, *description):
    if amount < self.totalDeposit:
      self.totalWithdraw += amount
      self.ledger.append({
        "amount": -amount, 
        "description": str(description[0]) if description else ""
      })
      return True
    else:
      return False

  def transfer(self, amount, object):
    if amount < self.totalDeposit:
      self.totalWithdraw += amount
      self.ledger.append({
        "amount": -amount, 
        "description": "Transfer to " + str(object.category).capitalize()
      })
      object.deposit(amount, "Transfer from " + str(self.category).capitalize())
      return True
    else:
      return False

  def check_funds(self, amount):
    return (False if amount > self.totalDeposit else True)

  def get_balance(self):
    return self.totalDeposit - self.totalWithdraw

  def __repr__(self):

    # defined variables
    leftStars = int(15 - round(len(self.category) / 2, 0))
    rightStars = 30 - leftStars - ((15 - leftStars) * 2)
    firstString = '*'  * leftStars + self.category + '*' * rightStars + '\n'
    ledgerStringList = []
    ledgerAmountList = []
    ledgerString = ''
    totalString = 'Total: ' + str(self.totalDeposit - self.totalWithdraw)

    # format ledgerString
    for obj in self.ledger:
      for key, value in obj.items():
        if key == 'description':
          ledgerStringList.append(str(value))
        else:
          ledgerAmountList.append(str(value))

    for x, y in zip(ledgerAmountList, ledgerStringList):
      newX = ''
      newY = ''

      if '.' not in x:
        newX += x + '.00'
      else:
        newX = x

      if len(y) + len(newX) > 29:
        removeCount = len(y) + len(newX) - 30 + 1
        newY = y[:-removeCount]
      else:
        newY = y

      ledgerString += newY + ' ' * (30 - (len(newX) + len(newY))) + newX + '\n'

    # return formatted ledger
    return ( 
      firstString + ledgerString + totalString
    )

def create_spend_chart(categories):
  categoryList = []
  withdrawList = []
  totalSpent = 0
  chartString = 'Percentage spent by category\n'

  # append category names and withdraws to list
  # count total withdrawls
  for x in categories:
    categoryList.append(x.category)
    withdrawList.append(x.totalWithdraw)
    totalSpent += x.totalWithdraw

  dashLength = (len(categoryList) * 3) + 1

  # returns chart numbers to chartString
  chartNum = 100
  check0 = ((withdrawList[0] / totalSpent) * 100)
  check1 = ((withdrawList[1] / totalSpent) * 100)
  check2 = ((withdrawList[2] / totalSpent) * 100)
  
  while chartNum >= 0:
    numberString = ''
    checkString = ''

    # check length of numbers on y axis
    if len(str(chartNum)) > 2:
      numberString += str(chartNum)
    else:
      numberString += ' ' * (3 - len(str(chartNum))) + str(chartNum)

    # check to add 'o'
    if check0 >= chartNum:
      checkString += ' o'
    else:
      checkString += '  '

    if check1 >= chartNum:
      checkString += '  o'
    else:
      checkString += '   '

    if check2 >= chartNum:
      checkString += '  o  '
    else:
      checkString += '     '

    # add newString to chartString and lower chartNum count
    chartString += numberString + '|' + checkString + '\n'
    chartNum -= 10

  # add dash string to chartString
  chartString += ' ' * 4 + '-' * dashLength + '\n'

  # find max string length
  maxLength = max(len(categoryList[0]), len(categoryList[1]), len(categoryList[2]))
  newList = []

  # add correct amount of spaces to each variable
  for x in categoryList:
    if len(x) < maxLength:
      newList.append(x + ' ' * (maxLength - len(x)))
    else:
      newList.append(x)

  # add formatted categories to chartString
  var1, var2, var3 = newList
  for x, y, z in zip(var1, var2, var3):
    chartString += '     ' + x  + '  ' + y + '  ' + z + '  ' + '\n'

  return chartString[:-1]
  