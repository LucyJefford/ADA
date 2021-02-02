
import time

class Cipher: ##Abstract Base Class, ABC
    def __init__(self,):
        self.plaintext = ""
        self.ciphertext = ""
        self.__alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    def encode(self):
        pass
    def decode(self):
        pass

    @staticmethod
    def AsciiToLetter(ascval):
        return chr(ascval)

    @staticmethod
    def LetterToAscii(letter):
        return ord(letter)


class Caesar(Cipher):
    def __init__(self, plaintext = "", ciphertext = "", shift = 0):
        self.__plaintext = plaintext
        self.__ciphertext = ciphertext
        self.__shift = shift #Initialises the variables for the Caesar class

    def encode(self):
        self.__ciphertext = self.solve(self.__plaintext) #Uses the function solve to encode the caesar
        return self.__ciphertext
    
    def solve(self, text1): #Every letter that is in the alphabet is shifted, the rest are left untouched
        text2 = ""
        for letter in text1:
            if letter.isalpha():
                text2 += self.shiftLetter(letter)
            else:
                text2 += letter
        return text2
            
    
    def shiftLetter(self, letter):
        value = self.LetterToAscii(letter) + self.__shift
        if letter.isupper():
            value -= self.LetterToAscii("A") #Takes away ascii value
            value = value % 26 # Makes sure it wraps around the alphabet
            value += self.LetterToAscii("A") # Adds back on ascii value
        elif letter.islower():
            value -= self.LetterToAscii("a") ##Same but instead uses the lowercase ascii values
            value = value % 26
            value += self.LetterToAscii("a")
        
        newLetter = self.AsciiToLetter(value) #Converts the new value back into a letter
        return newLetter

    def decode(self): 
        self.__shift *= -1 #Turns the shift negative, therefore it shifts the other way.
        self.__plaintext = self.solve(self.__ciphertext) #Puts the ciphertext into solve
        return self.__plaintext
    
    def autoSolve(self):
        texts = []
        for x in range(0,26):
            self.__shift = x
            self.decode()
            texts.append(self.__plaintext)
        return texts

class Substitution(Cipher):
    ## Use translate and make trans -> easy way to substitute the alphabet once you have it correct
    #e.g hello = string.maketrans(start,end)
    #  string.translate(hello)
    #OR -> string.translate(string.maketrans(start,end))

    def __init__(self, ciphertext = "", cipherbet = "", plaintext = ""):
        self.__plaintext = plaintext #Initialises the variables for the Substitution class
        self.__ciphertext = ciphertext
        self.__plainbet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" #In order to make sure the alphabet works with the maketrans, needs both upper and lower case.
        self.__cipherbet = cipherbet
        
        
    def encode(self):
        self.__ciphertext = self.__plaintext.translate(self.__plaintext.maketrans(self.__plainbet,self.__cipherbet))
        #Using the inbuilt maketrans and translate functions, the first is substitutued for the second 
        # (so plainbet 'a' is substituted for whatever the first letter in the cipherbet is)
        return self.__ciphertext
    
    def decode(self):
        self.__plaintext = self.__ciphertext.translate(self.__ciphertext.maketrans(self.__cipherbet,self.__plainbet))
        # The first letter in the cipherbet is substituted for 'a' from the plainbet
        return self.__plaintext
    
    def SuggestReplacements(self):
        self.__analyse = Analysis(text = self.__ciphertext) #Creates an Analysis object
        #self.__cipherFreq = self.__analyse.GetCipherFrequencies
        #self.__cipherPerc = self.__analyse.GetCipherPercents
        suggestedList = self.__analyse.PairUpValues() #Uses a function in the analysis class to pair up the values in the text.
        return suggestedList

class Vigenere(Cipher):
    
    def __init__(self, plaintext = "", ciphertext = "", key = ""):
        self.__ciphertext = ciphertext
        self.__plaintext = plaintext #Initialises thhe variables for the Vigenere Class
        self.__key = key

    def encode(self):
        self.__ciphertext = "" # Resets the ciphertext
        x = 0
        for letter in self.__plaintext:
            if letter.isalpha(): #If it's a letter
                newLetter = self.shiftLetterUp(letter, self.__key[x]) #Shifts the letter
                try:
                    self.__key[x+1] #cycles through the key, checking if it's gone over the edge of it
                    x += 1
                except:
                    x = 0 #goes back to the start of the key
                self.__ciphertext = self.__ciphertext + newLetter #Adds it onto the text
            else:
                self.__ciphertext = self.__ciphertext + letter
        return self.__ciphertext

    def shiftLetterUp(self, letter, keyChar):
        if letter.islower():
            #Adds on the key value to the letter, then loops around the alphabet, and turns it back into a letter
            shifted = self.AsciiToLetter((((self.LetterToAscii(letter)-97) + (self.LetterToAscii(keyChar.lower())-97)) %26) + 97) 
        elif letter.isupper(): # Same but using the uppercase values 
            shifted = self.AsciiToLetter((((self.LetterToAscii(letter)-65) + (self.LetterToAscii(keyChar.upper())-65)) %26) + 65)  
        return shifted

    def shiftLetterDown(self, letter, keyChar):
        if letter.islower(): #Similar to ShiftLetterUp but instead takes away the key value
            shifted = self.AsciiToLetter((((self.LetterToAscii(letter)-97) - (self.LetterToAscii(keyChar.lower())-97)) %26) + 97)
        elif letter.isupper():
            shifted = self.AsciiToLetter((((self.LetterToAscii(letter)-65) - (self.LetterToAscii(keyChar.upper())-65)) %26) + 65)  
        return shifted

    def decode(self):
        self.__plaintext = "" # Resets the plaintext
        x = 0
        for letter in self.__ciphertext: #Instance of using a STRING like an ARRAY
            if letter.isalpha(): #If it's a letter
                newLetter = self.shiftLetterDown(letter, self.__key[x])
                try:
                    self.__key[x+1] #Cycles through the key, checking if you've gone over
                    x += 1
                except:
                    x = 0
                self.__plaintext = self.__plaintext + newLetter
            else: #If it's not a letter ignore and add to text
                self.__plaintext = self.__plaintext + letter
        return self.__plaintext

    @staticmethod
    def ClosestToEnglish(listOfOptions):
        BestGuess = 10000 ##A large number to start off with, as if 0, then it'll never change
        BestText = ""
        englishValue = 1.73 #The value of a normal english text on average
        for option in listOfOptions:
            analyse = Analysis(text= option) #Creates an Analysis Object
            ioc = analyse.GetIoCValue() #Calculate IOC values
            ###DUE TO IOC IT WORKS BEST ON LONG TEXTS###
            close = englishValue - ioc
            if close < 0:
                close = close*-1 ###want a scalar value, no plus/minus
            if BestGuess > close: # If close is smaller, then it must be "better"/more like English
                BestGuess = close
                BestText = option #set this closest text as the best text
        return BestText

class Transposition(Cipher): 
    
    def __init__(self, ciphertext="", plaintext="", columns=0, order = [], reverseOrder = []):
        self.__ciphertext = ciphertext
        self.__plaintext = plaintext #Initialises variables for the Transposition class
        self.__columns = columns
        self.__columnOrder = order #In style [0,1,2,3,4,5]
        if columns != 0: #Columns may not have been set
            if reverseOrder == []:
                self.reversePermutation() #If it hasn't been set already, set the reverse order
            else:
                self.__reverseOrder = reverseOrder

    def encode(self):
        words = ""
        for index in self.__columnOrder:
            #Uses the normal order
            for x in range(0, len(self.__plaintext), self.__columns):
                #from the beginning of the plaintext, skipping by the columns
                try:
                    words += self.__plaintext[x+index]
                    #adds the letter onto the text tally
                except:
                    break
        return words
    
    def decode(self):
        words=""
        #Calculates the number of rows in the text
        rows = len(self.__ciphertext)//(self.__columns)
        #print(self.__columns)

        for x in range(0, rows): 
            #for every row
            for index in self.__reverseOrder:
                #pick from the index of your reverse combo
                try:
                    #you want to skip by index*rows each time
                    words += self.__ciphertext[index*rows + x]
                except:
                    #print(x)
                    pass
        return words
    
    def FindPossibleColumns(self):
        factors = []
        for i in range(1, (len(self.__ciphertext)) + 1):
            #finding the factors in the length of the text
            if (len(self.__ciphertext)) % i == 0:
                factors.append(i)
        return factors

    def reversePermutation(self):
        index = []
        for item in self.__columnOrder: #Creates a list of the column order and it's index (TUPLES)
            position = self.__columnOrder.index(item)
            index.append((item,position)) #Instance of a TUPLE
        reverse = []
        for i in index: #Creates a list filled with 0s, in order to avoid errors
            reverse.append(0)
        for elem in index: #The number of the order now becames the position
            reverse[elem[0]] = elem[1]
        #print(reverse)
        self.__reverseOrder = reverse #Sets as the variable
        return self.__reverseOrder

    def takeSecond(self, elem):
        return elem[1] #returns the second element

class RailFence(Cipher):
    ## characters = (c+1) + (r-2)(2c) + c
    # c = cycles, r = rails 
    def __init__(self, ciphertext = "", plaintext= "",railNo = 0):
        self.__ciphertext = ciphertext
        self.__plaintext = plaintext #Initialises the variable for use in the railfence class
        self.__railNo = railNo
        self.__railorder = []
        for x in range(0, railNo): #Creates an array with the values of the railfence (cycles)
            self.__railorder.append(x) #Will look like [0,1,2,3,2,1]
        for x in range(railNo-2, 0,-1): #Goes back up the rails
            self.__railorder.append(x)
        #print(self.__railorder)
        #the characters -1 divided by 2r-1 = cycles
        # OR characters divided by len(railorder)
        if self.__ciphertext == "":
            self.__cycles = len(self.__plaintext)/len(self.__railorder)
        else:
            self.__cycles = len(self.__ciphertext)/len(self.__railorder)
        self.__maxCycle = (2*self.__railNo) -2 #Max number of letters in a 'cycle'

        pass
    
    def encode(self):
        currentrail = 0
        self.__ciphertext = "" #resets ciphertext
        self.FirstRail() #encodes the first rail (special case)
        currentrail+=1 #moves onto the next rail
        while currentrail != (self.__railNo-1): #While it's not the last rail
            self.MiddleRail(currentrail, self.__maxCycle-currentrail) #Encodes the middle rail (general case)
            #puts into middlerail the two opposite numbers (so 2,4 if rail=5)
            currentrail+=1 #moves onto the next rail
        self.FinalRail() #encodes the last rail (special case)
        #print(self.__ciphertext)
        return self.__ciphertext

    def FinalRail(self):
        words = ""
        for x in range(0,len(self.__plaintext), int(self.__maxCycle)): #loops through the plaintext, skipping by the maxcycle
            try:
                words += self.__plaintext[x + (self.__railNo-1)] #Takes every value but increased by railno -1
            except:
                break
        #print(words)
        self.__ciphertext += words

    def MiddleRail(self, first, second):
        words = ""
        
        for x in range(0,len(self.__plaintext), int(self.__maxCycle)): #loops through the plaintext skipping by maxCycle
            try:
                words += self.__plaintext[x+first] #The first (down) letter
                words += self.__plaintext[x+ second] # the second (up) letter
            except:
                break
        #print(words)
        self.__ciphertext += words
                
    def FirstRail(self):
        words = ""
        for x in range(0,int(self.__cycles)+1): #Loops through values for total number of cycles plus one
            try:
                words += self.__plaintext[x * (((2*self.__railNo)-1)-1)] #Using algebra previously worked out, picks the next top line letter each time
            except:
                break
        #print(words)
        self.__ciphertext += words
        
    def decode(self):
        rails = self.SplitIntoRows() #Chunks it into rails

        #Take one from each going down then back up
        text = self.PickingValues(rails)

        #returns and adds the plaintext as the ciphertext.
        self.__plaintext = text
        return self.__plaintext
        
    def SplitIntoRows(self):
        toprail = ""
        bottomrail = "" #Initialises Varaible 
        rails = [] #an ARRAY to store the rails.
        counter = -1 #set to -1 as we add to counter inside loop and need 0 to begin with
        n = (len(self.__ciphertext)-1)//((2*self.__railNo)-2) #n is number of characters per row (used as part of the algebra)
        #print(n)
        #chunk into rails, bottom is n, top is n+1, middles are 2n
        try:
            for x in range(0, n+1):
                counter +=1
                toprail += self.__ciphertext[counter] #the top rail is n+1 characters
            rails.append(toprail)
            for i in range(0, self.__railNo-2):
                temp = ""
                for x in range(0, n *2 ): #middle rail is2n characters as up & down
                    counter +=1
                    temp+= self.__ciphertext[counter]
                rails.append(temp)
            for x in range(0, n): #bottom rail is only n characters
                counter +=1
                bottomrail += self.__ciphertext[counter]
            rails.append(bottomrail)
        except:
            pass
        #print(rails)
        return rails
    
    def PickingValues(self, rails):
        current = 0
        up = True
        text = ""
        while rails[0] != "": #whilst the toprail is not empty
            listOfChars = rails[current] #take the currrent row
            #print("Left:", listOfChars)
            first = listOfChars[0] # Using a functional programming "head" style function
            fixed = listOfChars[1:] # Using a functional programming "tails" style function
            rails[current] = fixed #returns the list back into the array
            #print(current)
            #print(first)
            text+= first #adds onto the running text tally
            if up == True: #takes the next rail, depending on if going up or down
                current+=1
            else:
                current-=1
            if current>= len(rails): #if it's larger than the rail length (gone over the bottom)
                current -=2 #goes back up to the right row
                up = False #Realises it's now reached the bottom so time to go up
            elif current <0: #If it's now gone over the top,
                current+=2 #goes back down to the right row 
                up = True #Realises that its time to start going down as it's reached the top
        #print("finished")
        #print
        return text
    
    def GuessRails(self, topGuess):
        potentials = []
        for x in range(2,1+topGuess): #between the two values, 2 and your top guess, check if the text can be a complete railfence
            #print(x, len(self.__ciphertext) % ( (2*x) -2))
            if (len(self.__ciphertext) % ( (2*x) -2)) == 1: #the modulus of the length of text by 2*rails -2 should be one if complete cycle
                potentials.append(x) #adds it onto a running rail length selection
        #print(potentials)
        return potentials

class Tutorial:
    def __init__(self):
        ##Caesar Section
        self.__CaesarPlaintext = "HARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNGLASSES"
        self.__CaesarCiphertext = "XQHHO XQI JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI"
        self.__CaesarShift = 16
        self.__CaesarQueue = ["You start by taking the first letter of the ciphertext. This then needs to be shifted back down the alphabet by the shift you used originally.",["So, we move the “X” back to an “H”.","HQHHO XQI JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI"], ["Once we’ve figured out that letter, we move onto the next. In this example, it’s the “Q”. This gets shifted back to an “A”. ","HAHHO XQI JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI"], ["The rest of this cipher is rather the same, just shifting a letter back through the text. Here is the mapping of the characters, so it’s easier to see: ","ABCDEFGHIJKLMNOPQRSTUVWXYZ (English) \nQRSTUVWXYZABCDEFGHIJKLMNOP (Ciphertext) "],["I’ll show you the rest of the cipher decryption now. ","HARHHO XQI JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRO XQI JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY XQI JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HQI JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAI JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS JXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS TXU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THU SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE SQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CQIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CAIU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASU VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE VYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FYBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FIBU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILU. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. CUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI "],["Almost there… ","HARRY HAS THE CASE FILE. MUUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEUJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEEJ QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI  \nHARRY HAS THE CASE FILE. MEET QJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AJ JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT JMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TMUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWUBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWEBLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELLU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVU JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE JXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE TXYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THYHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIHJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRJO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTO MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY MUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WUQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEQHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEAHYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARYDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARIDW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARINW IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING IKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SKDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUDWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNWBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNGBQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNGLQIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNGLAIIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNGLASIUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNGLASSUI \nHARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNGLASSEI "],["Ta-da!! Our decoded Caesar cipher. ","HARRY HAS THE CASE FILE. MEET AT TWELVE THIRTY WEARING SUNGLASSES"], "This cipher is the easiest cipher you’ll probably encounter, as it’s quite easy to decode. For this example, we know the shift, which is 16. If we didn’t know this, we could try 1 to 26 systematically, as this cipher is cyclical, meaning it has a finite number of options."]
        
        ##Vigenere Section
        self.__VigNoKeyQueue = ["Today we’ll be looking at how to decode a Vigenere Cipher if you do not know the key, but instead a small part of the text. We know “HARRY” is the first in the word in the text, but not what the key is, or how long it is. For context, this is a message from two spies in the world of George Orwell’s 1984, so we may be able to guess some key words.",["The way you decode without a key, is by putting the crib (what you call a piece of known text) in various positions through the text. Because we know that it is at the start of the text, we don’t need to keep shifting the crib around, as it’s the first word. We’ll start with just the crib like normal and see how that works.","OBRIE, HWQ BBLGEOK JW SXWMPVJW. AF KB VYPUEJ. SSQ"], ["That didn’t produce anything recognisable, however “HARRY” went to “OBRIE” Let’s try with the crib as “BIGBROTHER” (and without HARRY as we know what that is) to see if that’s in there.","NOB RIENOBR PO DNDFWFWD. GX VR CRWERQ. YKB"],["Can you see that repeating pattern? “NOBRIENOBR”, and when combined with the part from before, we can see that the start of the text is “OBRIE, NOB RIENOBR”. From this we can suggest the key is OBRIEN, which makes sense as he’s an influential character from the book. Next,  try your guessed key on the text to see the result.","HARRY, BIG BROTHER IS WATCHING. GO TO GROUND. MEG"], "And perfect! You’ve decoded this without using a key, and now you’ve cracked the code. The Vigenère is a lot harder than the Caesar cipher, however if you know a small section of the text, you can potentially find the key, then crack the whole thing. This may feel like cheating, but this is a valid way of decoding real world encryptions. In World War 2, the code-breakers at Bletchley Park used a crib when deciphering the Enigma codes, because the Germans started every morning’s cipher with “The weather is…”, so they knew what the code would start with, and therefore easier to crack!"]
        self.__VigNoKeyPlaintext = "HARRY, BIG BROTHER IS WATCHING. GO TO GROUND. MEG"
        self.__VigNoKeyCiphertext = "VBIZC, OWH SZSGVFI QW JOUTPMAU. HF BS TFPLVH. ZSH"
        #self.__VigNoKeyCrib = "OBRIEN"
        self.__VigNoKeyKey = "OBRIEN"

        ##Rail Fence Section
        self.__RailFenceQueue = ["This cipher is one of the most difficult to solve, as it looks on paper to be a transposition, however the way you unravel it is vastly different.  ",["Due to the length of the text, we can guess that this is a 4-rail Railfence, as to calculate the probable rails, you want a modulus of (2*rails -2) that equals 1, as the number of letters in the cycle = ((2*rails -2) * cycles + 1).   ","1 = 25 MOD (2*4 -2). Therefore it must be a 4-rail.  "], ["In order to decode a railfence, the main thing is that you have to keep track of which rail you’re on, and then whether you are going up or down them. That is our first point of call, break the text into 4 different “rails”: first (top) has n+1 characters, the middle lines have 2n characters, and the last (bottom) has n characters. This only works is the Railfence has a complete cycle, meaning it goes all the way down, all the way up, and ends on the top rail. ","'HUAEG', 'ETCLIEME', 'LSKNRREM', 'PIF!'"], ["Next we begin by taking values down the rows, and then back up them, by keeping track of whether we have reached the end of a cycle. Remember, a cycle goes through the top line, once, the middle lines twice, and the bottom once. I’ll show you the first cycle now: ","HELPST "],["Once you’ve got all your cycles you then concatenate all your cycles together (plus one extra character for the last element of the top row). ","HELPST, UCKINL, AIRFRE, ME!ME, G "],["And here we are – the final result. ","HELPSTUCKINLAIRFREEME!MEG "], "A Rail fence cipher may look complicated to decode, but as soon as you know what you need to do to decode it, it’s as easy as a simple transposition cipher."]
        self.__RailFencePlaintext = "HELPSTUCKINLAIRFREEME!MEG"
        self.__RailFenceCiphertext = "HUAEGETCLIEMELSKNRREMPIF!"
        
        #Unknown Section
        self.__UnknownCipherQueue = ["For this tutorial, we know somethings and not others. We have no idea which cipher this is, and therefore no idea on how to decode – yet. By looking at the known parts of the text, we can make inferences and find potential ciphers. The three categories that we will deal with are: Monoalphabetic, Polyalphabetic and Transposition. The first of these, Monoalphabetic, will be very obvious, as it has a frequency analysis and IOC similar to English, but the percentages of letter are in the wrong place. The second, Polyalphabetic, will have a “flat” frequency analysis (all values same or similar), and a completely different IOC value to English. The last, Transposition, will have a similar IOC to English, and the percentages will be the same, but the text will look nothing like English.",["We are going to start by looking at the frequency analysis and the Index of Coincidence. You can see that we have an IOC remarkably similar to the base English value (1.75) which suggests it’s not a Polyalphabetic cipher. Our Frequency Analysis has shown that ‘e’ is the most common letter, closely followed by ‘t’. This suggests it is not a monoalphabetic cipher either, as the letter frequencies are approximately on the right letters.  ","Percentages: {'a': 6.1, 'b': 2.07, 'c': 2.397, 'd': 4.575, 'e': 13.181, 'f': 2.07, 'g': 3.05, 'h': 7.625, 'i': 7.19, 'j': 0.109, 'k': 0.109, 'l': 3.595, 'm': 1.961, 'n': 6.1, 'o': 8.279, 'p': 2.07, 'q': 0.0, 'r': 6.645, 's': 3.922, 't': 10.458, 'u': 2.614, 'v': 1.089, 'w': 3.813, 'x': 0.0, 'y': 0.98, 'z': 0.0} \n IOC: 1.75 (3 s.f.)"], ["Now we know that it’s a Transposition, we can guess what type of Transposition it is. Normally if you’re working with the Cipher Challenge, there are very few Rail Fence ciphers so let’s assume it’s a normal (Columnar) Transposition until we find our otherwise. Let’s take a look at the length of the text next. This can help tell you what columns you’ll be using, as often they fill a complete grid, so their column number is a factor of the length.","Length: 1,160 \nFactors: [1, 2, 4, 5, 8, 10, 20, 29, 40, 58, 116, 145, 232, 290, 580, 1160]"],["Wow, that’s a long list.  Now we can look at the text to see if there are any clues to which of these to pick… Do you see that repeating section of Uppercase letters? This happens five times, at various points in the text. Let’s attempt using 5 columns now, and see if that observation has helped us.","pailo  shern eti WTGTDWBRRNH HOIIO   BEedriigfaHuole ionIsus wn etarategsn ic ihabomtwedtoho s dhtilt itsorc nht eWe eNH Hoe enrrg  ie hetwti hrdo itd eeeuPelt  s ame dlvmevfhese rtsirtciat t.ur  e.urwot  dcafvYid elow,n stnreeruo .Hedduuotm rigl  t-NH HOIIO   BEWTGTDWBRRr  nl  geltplanfit ritrgt irds  e  iatoneruro am eueip aoeesthHd ow,ahea ushrw   BErthfeoi mnfnWe  ihaoe itot,edr. go d jtaHdmdw lemde avenp hsaihonlhis gitcd giathtc oloeogosslrh  y, e ryen y hlouyr tppingapsOIIO   BEWTGTDWBRRNH Hvneafnlp oneegw a as e ifsrlowornuaetafnti f n te  tpdedntnrae.do heeektisl hetWTGT hrrifwn,edr.thn  d,we nowiaofcho cuemt .hot-liaotei n poe etc  a osifoc,yltoc n gtl e e m ecuf eerruootheott.in  psvhop,n anca   BEWTGTDWBRRNH HOIIO  oa,lhae d  i g c adnhi hpc s mdrttnl pg yt mhsptat laabn reoee d,e uewtwsse rDWBRR herdmtiaofchrwoterrthd nh  ie Thlw huhme i os  i,nhdet a-eelmaneleneThmha Thms ihobnerruhdusy iefe srl   dgos svtleeoa tirealDWBRRNH HOIIO   BEWTGToavg ia .c hfntep.wb,cetooauw noaohhi oe d, aee tor segna ep gr no vbs   ae.thoOIIO,we a  itd eee enh y he g  mnfnThtiogisee ct-uthct  e r tp- n ettd r lhteelihte anauecd . tgcf alvoabo atwb eu "],["So, recap. We know it’s a Transposition, it’s got 5 columns, now we need to figure out the order of those columns (if they’re even jumbled up). Here’s the text, once it’s been put through without changing the column order.  ","pH isaehn idl sldo vouupt uysl orvest hehmtooe pparrp, niint gn ielgart anei pca tsalW-O DTNI WGHI BT OBRDH ERWO WNBI THRIBG ROETHN WDOH TWI  GBIHBTROOEDR IWWN ITBH OGR B TRHE DNOW WHITBB IGERHOTeRv odrn ar eovi aaginf, glnlif lhaa pa Hg e.ueo colnd lte hepe f lginiaw ton genfa pIi c.sta wu sabsr d, iencwt henriit gf oetshot rpaailcurro wadws tso ne rmog ndaseuron ath  ethiitnicaal  tf oionpehntg aei dbr y,ouft mr  atonmew  heeats dmeptt  tooe arhutt oep s idlespeag  dandanbahotn ten eierrplsae tteog h.eriHde tdo ns  doooh, rweevc,e b aeusnhke hetw tait   swaeulseWs s.ehhet re hewtroN WDOH TWI  GBIHBTROoE R,erh w trheehre nfirarefd rowm ginti  ,it meadindo efrfe n.cehWtheeehr t nwew  onti thihde  a,ryhowr reethd  heoind  to giown ttih d,a m eo nedfifercene.h Tu oThPg hteoclil uwotde g  mhi jtusst he a.meaHhe mdo cemtit d- -dwloul istvla hmeo cemtitvde, fein h  heeand sv ereept  no trpeapt  --shee istenracl ti mech atioantan edtlol  hsertiin .sfelu oThrgcht i,me tyheeclal.dt iu oThrgchtwi meoans tt  a hgin tthadclouc  beaoencfl edvoer Ye r.iomu dg ht oedgescuclsusfolfy wr  a,heiln eev  rfosyreat,u bn osoreor e tlaerh trye wueo bontd   tge.y.ou "],["Hmm, looks a lot like gobble-de-gook. Let’s try a different one, but before we do that. Take a closer look at the start of the half-decoded text. Do you see “pH isaehn idl sldo vouupt”? It seems like ‘H’ is meant to be the start of the word, let’s move things around then to get that. ","H ispehn adl sido vluuptouysl orve t hesmtooh ppaerp, riintngn i lgare anet pcaitsal -O DWNI WTHI BG OBRTH ERDO WNWI THBIBG ROETHR WDON TWIH GBI BTROHEDR OWWN ITBH IGR BOTRHE DNOW WHIT B IGBRHOTERv oern ad eovr aaginf, ilnlig lhaf pa ag e.Heo culnd ote hlpe felgin aw tin geofa pni c.Ita ws sabur d,sienc t hewriitngf o tshoe rpatilcuaro wrdws aso nt rmoe ndageuros athn eth itniiaal ctf o onpeintg hei dar y,buft or  amonmet  hewats emeptd  tote aroutt hep soidle peags dan anbadotn hen eterrpisae lteogth.er Hde ido nt  dosoh, oweevr,e bcaeus hke netw hait t swa ulsees s.Whhetere h wtroe WDON TWIH GBI BTROHE R,orh wetrhe hre efiranefd rowm rintig ,it mead ndo ifrfeen.ce Wthehehr e nwet  onwi ththde ia,ry owr heethr  hedind oto g own itih t,a mdeo n dfifercene.h Te oThug htPoclie uwolde gt mhi jtus t hesa.me Hhe ado cmmtited- - wloud istlla hveo cmmtitede, vein f  hehand ev ersept eno t peapr  --thee ssteniacl ri meth atcoantin edalol thser iin tsfel. oThugchtri,me tyhe claledt i. oThugchtri mewans ot  athgin ttha cloud  becoencal edfoer ve r.Yomu ig htdoedg scucesusfllfy or  awheil, eevn rfo yreas,u bt osoneor r tlaerh teye wreo buntd o tge y.ou. "],["Now that’s starting to look like English. You can see “y.ou.” at the bottom, and “scucesusfllfy”; you and successfully respectively. Let’s twiddle a little more and see what it ends up like. I’ll try a column order of 1, 3, 4, 2, 0 next. ","Hi spenh ad lsid ovluputousyl ovre th esmotoh ppaer,p rinitng ni lagre naet cpaitasl - ODWN IWTH IBG BORTHE RDOW NWIT HBIGB ROTEHR DWON WTIH BGI BRTOHERD OWNW ITHB IG RBOTHRE DONW WIHT BI GBROHTER voer nad oevr aagin,f illnig hlaf ap age .He oculdn ot ehlp efelign a wting eof apnic .It aws asburd ,sinec th ewriitng fo thsoe praticluar owrdsw as ont mroe dnageruos tahn teh intiiala ct fo opneingt he idary ,butf or  amomnet h ewast empetd t otea routt he psoilde paegs adn abnadont he neterrpisea ltoegthe.r Hed id ont d oso,h oweevr, ebcaues hek newt hati t wsa usleess .Whehter eh wrtoe DWON WTIH BGI BRTOHER ,or hwethre her efrianedf romw ritnig i,t maed nod iffreenc.e Whteherh e wnet o nwit hthed iar,y orw hetehr h edidn ot og onw ithi t, amde on differecne. hTe Tohugh tPolcie wuold egt hmi juts th esam.e Heh ad ocmmitted -- wolud sitll ahve ocmmitted,e veni f h ehadn eve rsetp en ot paepr - -thee ssetnialc rim etha tconatine dallo thesr ini tsefl. Tohughctrim,e thye called ti. Tohughctrim ewasn ot  athign thta colud b econecale dfore ver .Youm igh tdodeg successufllyf or  awhiel, eevn fro yeras, ubt soonero r ltaer htey ewre obundt o gte yo.u. "],["Yes! This is the right order to decrypt it. Here’s your completed text: ","His pen had slid voluptuously over the smooth paper, printing in large neat capitals - DOWN WITH BIG BROTHER DOWN WITH BIG BROTHER DOWN WITH BIG BROTHER DOWN WITH BIG BROTHER DOWN WITH BIG BROTHER over and over again, filling half a page. He could not help feeling a twinge of panic. It was absurd, since the writing of those particular words was not more dangerous than the initial act of opening the diary, but for a moment he was tempted to tear out the spoiled pages and abandon the enterprise altogether. He did not do so, however, because he knew that it was useless. Whether he wrote DOWN WITH BIG BROTHER, or whether he refrained from writing it, made no difference. Whether he went on with the diary, or whether he did not go on with it, made no difference. The Thought Police would get him just the same. He had committed -- would still have committed, even if he had never set pen to paper -- the essential crime that contained all others in itself. Thoughtcrime, they called it. Thoughtcrime was not a thing that could be concealed for ever. You might dodge successfully for a while, even for years, but sooner or later they were bound to get you.. "], "Congratulations, you’ve cracked a cipher from start to finish! This is often a challenege for even the best code-breakers, as you have to make so many logical leaps and guesses. Keep on breaking! "]
        self.__UnknownCipherCipherText = "pailo  shern eti WTGTDWBRRNH HOIIO   BEedriigfaHuole ionIsus wn etarategsn ic ihabomtwedtoho s dhtilt itsorc nht eWe eNH Hoe enrrg  ie hetwti hrdo itd eeeuPelt  s ame dlvmevfhese rtsirtciat t.ur  e.urwot  dcafvYid elow,n stnreeruo .Hedduuotm rigl  t-NH HOIIO   BEWTGTDWBRRr  nl  geltplanfit ritrgt irds  e  iatoneruro am eueip aoeesthHd ow,ahea ushrw   BErthfeoi mnfnWe  ihaoe itot,edr. go d jtaHdmdw lemde avenp hsaihonlhis gitcd giathtc oloeogosslrh  y, e ryen y hlouyr tppingapsOIIO   BEWTGTDWBRRNH Hvneafnlp oneegw a as e ifsrlowornuaetafnti f n te  tpdedntnrae.do heeektisl hetWTGT hrrifwn,edr.thn  d,we nowiaofcho cuemt .hot-liaotei n poe etc  a osifoc,yltoc n gtl e e m ecuf eerruootheott.in  psvhop,n anca   BEWTGTDWBRRNH HOIIO  oa,lhae d  i g c adnhi hpc s mdrttnl pg yt mhsptat laabn reoee d,e uewtwsse rDWBRR herdmtiaofchrwoterrthd nh  ie Thlw huhme i os  i,nhdet a-eelmaneleneThmha Thms ihobnerruhdusy iefe srl   dgos svtleeoa tirealDWBRRNH HOIIO   BEWTGToavg ia .c hfntep.wb,cetooauw noaohhi oe d, aee tor segna ep gr no vbs   ae.thoOIIO,we a  itd eee enh y he g  mnfnThtiogisee ct-uthct  e r tp- n ettd r lhteelihte anauecd . tgcf alvoabo atwb eu"
        self.__UnknownCipherPlainText = "His pen had slid voluptuously over the smooth paper, printing in large neat capitals - DOWN WITH BIG BROTHER DOWN WITH BIG BROTHER DOWN WITH BIG BROTHER DOWN WITH BIG BROTHER DOWN WITH BIG BROTHER over and over again, filling half a page. He could not help feeling a twinge of panic. It was absurd, since the writing of those particular words was not more dangerous than the initial act of opening the diary, but for a moment he was tempted to tear out the spoiled pages and abandon the enterprise altogether. He did not do so, however, because he knew that it was useless. Whether he wrote DOWN WITH BIG BROTHER, or whether he refrained from writing it, made no difference. Whether he went on with the diary, or whether he did not go on with it, made no difference. The Thought Police would get him just the same. He had committed -- would still have committed, even if he had never set pen to paper -- the essential crime that contained all others in itself. Thoughtcrime, they called it. Thoughtcrime was not a thing that could be concealed for ever. You might dodge successfully for a while, even for years, but sooner or later they were bound to get you.."
        self.__UnknownCipherColumns = 5
        self.__UnknownCipherColumnOrder =  [4,0,3,1,2]
        self.__UnknownCipherReverseOrder =  [1, 3, 4, 2, 0]
        pass

    ##Order: Queue, Plaintext, Ciphertext, (extra stuff)
    def getCaesarInfo(self):
        return self.__CaesarQueue,  self.__CaesarPlaintext, self.__CaesarCiphertext, 
        #self.__CaesarShift

    def getVigNoKeyInfo(self):
        return self.__VigNoKeyQueue, self.__VigNoKeyPlaintext, self.__VigNoKeyCiphertext, 
        #self.__VigNoKeyKey

    def getRailFenceInfo(self):
        return self.__RailFenceQueue, self.__RailFencePlaintext, self.__RailFenceCiphertext
    def getUnknownInfo(self):
        return self.__UnknownCipherQueue, self.__UnknownCipherCipherText, self.__UnknownCipherPlainText, 
        #self.__UnknownCipherColumns, self.__UnknownCipherColumnOrder, self.__UnknownCipherReverseOrder

class Menu:
    #A.D.A.
     #Imports time (potentially for all functions but apparently have to import individually)

    def __init__(self):
        
        print("***** Cryptography Companion *****\n")
        print("ADA: Hi There! My name's ADA, and I'm here to help you encode, decode and crack your ciphers.")
        time.sleep(1)
        print("ADA: We can do many things here, focusing on a few ciphers in particular, with some help for any beginners out there.")
        time.sleep(1)
        tutorialChoice = input("ADA: Would you like to take a look at a Code-Breaking tutorial? \nYou: ")
        
        while tutorialChoice == "":
            tutorialChoice = input("ADA: I'm sorry I didn't get that. Can you try again? \nYou: ")
        if self.PositiveResponse(tutorialChoice):
            print("ADA: Coming right up!")
            time.sleep(1)
            self.tutorialMenu()
            quitChoice = input("ADA: Are you all finished up? There's plenty more I can do. \nYou: ")
            if self.PositiveResponse(quitChoice):
                print("ADA: Thanks for being here! See you next time!")
                time.sleep(3)
                quit()

        self.listOfChoices()

    def listOfChoices(self):
        import time
        toQuit = False
        while toQuit == False:   
            print("ADA: What cipher would you like to work with?")    
            time.sleep(1)
            print("ADA: Our options are Caesar, Rail Fence, Substitution, Transposition, Vigenere.")
            time.sleep(1)
            print("ADA: We can also help analyse your text, or there's a Tutorial for beginners!")
            time.sleep(1)
            print("ADA: Or if you're ready to quit, just say!")
            time.sleep(1)
            cipherChoice = input("You: ")
            decision = self.whichCipher(cipherChoice)
            if decision == "ERROR":
                print("ADA: Sorry I didn't get that.. Perhaps you spelt it wrong? Try again!")
            if decision == "Q":
                print("ADA: Goodbye!")
                time.sleep(2)
                quit()
            if decision == "C":
                self.CaesarMenu()
            if decision == "S":
                self.SubstitutionMenu()
            if decision == "RF":
                self.RailFenceMenu()
            if decision == "TR":
                self.TranspositionMenu()
            if decision == "A":
                self.AnalysisMenu()
            if decision == "V":
                self.VigenereMenu()
            if decision == "TU":
                self.tutorialMenu()

    def PositiveResponse(self, text):
        correctedtext = self.CorrectText(text)
        #print("Positive Test")
        positives = ["YES", "Y", "OFCOURSE", "YUP", "YEAH", "YAH", "YH", "DONE"] ##Add MORE
        if correctedtext in positives:
            return True

    def whichCipher(self, text):
        caesaroptions = ["CAESAR", "CAESARCIPHER"]
        railfenceOptions = ["RAIL", "RF", "RAILFENCE"]
        substitutionOptions = ["SUBSTITUTION", "SUB", "ALPHABETICSUBSTITUTION", "AS"]
        transpositionOptions = ["TRANS", "COLUMNARTRANPOSITION", "TRANSPOSITION", "CT"]
        analysisOptions = ["ANALYSIS", "ANALYSE", "CALCULATE", "FREQUENCYANALYSIS", "A", "HELPANALYSE"]
        vigenereOptions = ["VIG", "VIGENERE", "VIGENERECIPHER", "V"]
        tutorialOptions = ["TUTORIAL", "HELP"]
        unknownOptions = ["UNKNOWN", "COLDCIPHER", "UNKNOWNCIPHER", "CRYPTOGRAPHY", "DECRYPT"]
        quitOptions = ["DONE", "FINISHED", "STOP", "END", "EXIT", "QUIT"]
        correctedtext = self.CorrectText(text)
        if correctedtext in caesaroptions:
            return "C"
        elif correctedtext in substitutionOptions:
            return "S"
        elif correctedtext in railfenceOptions:
            return "RF"
        elif correctedtext in transpositionOptions:
            return "TR"
        elif correctedtext in analysisOptions:
            return "A"
        elif correctedtext in vigenereOptions:
            return "V"
        elif correctedtext in tutorialOptions:
            return "TU"
        elif correctedtext in quitOptions:
            return "Q"
        elif correctedtext in unknownOptions:
            return "U"
        else:
            return "ERROR"

    def GetText(self, remove=False):
        text = ""
        while text == "":
            choice = input("ADA: Now I need your text. Would you like to enter in a file name to get the text from? \nYou: ")
            
            if self.PositiveResponse(choice):
                filename = input("ADA: Then I need a file name. Please include the relevant extension (e.g. textfile.txt). Do you mind entering it below? \nYou: ")
                try:
                    textFile = open(filename, "r")
                    text = textFile.read()
                    #print(text)
                    textFile.close()
                except:
                    print("ADA: That file didn't open correctly, please try again!")
            else:
                text = input("ADA: Oh, then I need you to type in your text. Do you mind entering it below? \nYou: ")
            correctedText = self.CorrectText(text)
            letterText = len(list(filter(lambda x: x.isalpha(), text)))
            #print(correctedText, letterText)
            if correctedText.isalnum() and letterText > 0:
                if remove:
                    text = correctedText
                #print(text)
            else:
                text = ""
                print("ADA: Sorry I don't think that was a valid input. Please try that again!")
        return text

    @staticmethod
    def CorrectText(text):
        import string
        #Remove spaces
        newtext = (text.upper()).replace(" ", "")
        #Remove all punctuation too...
        newtext = newtext.translate(str.maketrans('', '', string.punctuation))
        return newtext

    def ModeChoice(self, text, encode = False, decode = False, solve = False, column = False, rails = False, Frequency=False, Index=False, compare=False, every= False, replace= False):
        decodeOptions = ["DECIPHER", "DECODE", "DECODING"]
        encodeOptions = ["ENCODE", "ENCIPHER",]
        solveOptions = ["AUTOSOLVE", "DOITFORME", "SOLVE"]
        quitOptions = ["DONE", "FINISHED", "STOP", "END", "EXIT", "QUIT"]
        columnOptions = ["SUGGESTCOLUMNS", "COLUMN", "COLUMNS"]
        railOptions = ["RAILS", "PICKRAILS"]
        FreqOptions = ["FREQUENCY", "FREQUENCYANALYSIS", "ANALYSE"]
        IndexOptions = ["IOC", "INDEXOFCOINCIDENCE", "INDEX"]
        compareOptions = ["COMPARISON", "COMPARE", "VALUES"]
        everyOptions = ["EVERY", "COMBOS", "COMBINATIONS"]
        replaceOptions = ["REPLACE", "SUGGEST", "SUGGESTREPLACEMENTS"]


        correctedtext = self.CorrectText(text)
        if correctedtext in decodeOptions:
            if decode:
                return "DECODE"
        elif correctedtext in encodeOptions:
            if encode:
                return "ENCODE"
        elif correctedtext in solveOptions:
            if solve:
                return "SOLVE"
        elif correctedtext in columnOptions:
            if column:
                return "COLUMN"
        elif correctedtext in railOptions:
            if rails:
                return "RAILS"
        elif correctedtext in FreqOptions:
            if Frequency:
                return "FREQ"
        elif correctedtext in IndexOptions:
            if Index:
                return "IOC"
        elif correctedtext in compareOptions:
            if compare:
                return "COMPARE"   
        elif correctedtext in everyOptions:
            if every:
                return "EVERY"  
        elif correctedtext in replaceOptions:
            if replace:
                return "REPLACE"   
        elif correctedtext in quitOptions:
            return "QUIT"
        else:
            return "ERROR"
        return "ERROR"

    def tutorialMenu(self): ##Done
        #print("Tutorial Menu Test Running")
        print("ADA: Welcome to the Tutorial!")
        ##Choose either caesar/vig/unknown/railfence USING WHICHCIPHER
        selectionCorrect = False
        while selectionCorrect == False:
            print("ADA: In total we have 4 tutorials: Caesar, Vigenere, a RailFence and an Unknown cipher.\nADA: For very beginners, I reccommend our Caesar or RailFence tutorials. \nFor more advanced codebreakers, the best place to start would be the Vigenere (which uses a crib) and the Unknown Cipher.")
            tutorialchoice = input("ADA: Which cipher would you like to see a tutorial of? \nYou: ")
            cipherChosen = self.whichCipher(tutorialchoice)
            if cipherChosen == "C":
                queue,  plaintext, ciphertext = Tutorial().getCaesarInfo()
                selectionCorrect = True
            elif cipherChosen == "RF":
                queue,  plaintext, ciphertext = Tutorial().getRailFenceInfo()
                selectionCorrect = True
            elif cipherChosen == "U":
                queue,  plaintext, ciphertext = Tutorial().getUnknownInfo()
                selectionCorrect = True
            elif cipherChosen == "V":
                queue,  plaintext, ciphertext = Tutorial().getVigNoKeyInfo()
                selectionCorrect = True
            else:
                print("ADA: That doesn't appear to be a cipher in my databanks. Could you try another?")
            pass

        #
        print("ADA: Now, onto the tutorial!")
        #print("ADA: I'll be showing you the tutorial in the format of rubric then ciphertext/etc")
        time.sleep(3)
        #Intro
        Intro = queue.pop(0)
        print("ADA: " + str(Intro))
        time.sleep(3)
        #Main Body
        for x in range(0,len(queue)-1):
            pairOfInfo = queue[x]
            print("ADA: " + str(pairOfInfo[0]))
            time.sleep(3)
            print("ADA: " + str(pairOfInfo[1]))
            time.sleep(3)

        #Outro
        Outro = queue[len(queue)-1]
        print("ADA: " + str(Outro))
        time.sleep(3)

        print("ADA: Hopefully that helped clear things up! Have a nice day! Heading back to the menu now...")
        time.sleep(2)

    def CaesarMenu(self): ##Done
        import time
        #print("Caesar Menu Test Running")
        print("ADA: We're now in the world of the Caesar Cipher. Here we can encode, decode and autosolve it!")
        time.sleep(1)
        toQuit = False
        while toQuit == False:
            chooseMode = input("ADA: What would you like to do today?  \nYou: ")
            mode = self.ModeChoice(chooseMode, encode=True, decode=True, solve=True)
            if mode == "ERROR":
                print("ADA: Sorry I didn't get that.. Perhaps you spelt it wrong? Try again!")
            elif mode == "QUIT":
                print("ADA: Goodbye!")
                time.sleep(2)
                toQuit =True
            elif mode == "ENCODE":
                self.C_DecodeEncode(encode=True)
                print("ADA: We're now back in the Caesar Cipher menu. Here we can encode, decode and autosolve it!")
            elif mode == "DECODE":
                self.C_DecodeEncode(encode=False)
                print("ADA: We're now back in the Caesar Cipher menu. Here we can encode, decode and autosolve it!")
            elif mode == "SOLVE":
                self.C_AutoSolve()
                print("ADA: We're now back in the Caesar Cipher menu. Here we can encode, decode and autosolve it!")
            else:
                pass

    def C_DecodeEncode(self, encode = True):
        print("ADA: Great choice! Just let my cogs whir...")
        time.sleep(1)
        text = self.GetText()
        shiftCorrect = False
        while shiftCorrect == False:
            try:
                if encode:
                    shiftChosen = int(input("ADA: What shift would you like to encode it by?  \nYou: "))
                else:
                    shiftChosen = int(input("ADA: What shift would you like to decode it by?  \nYou: "))
                shiftCorrect= True
                if shiftChosen > 26 or shiftChosen < 0:
                    shiftCorrect= False
            except:
                print("ADA: Sorry that shift is not valid. Please try another!")
                shiftCorrect= False
        if encode:
            caesarEncode = Caesar(plaintext=text, shift=shiftChosen)
            caesarEncoded = caesarEncode.encode()
            print("ADA: And here is your encoded Caesar Cipher: ", caesarEncoded, "\nADA: Back to the Caesar Menu!")
        else:
            caesarDecode = Caesar(ciphertext=text, shift=shiftChosen)
            caesarDecoded = caesarDecode.decode()
            print("ADA: And here is your decoded Caesar Cipher: ", caesarDecoded, "\nADA: Back to the menu!")


    def C_AutoSolve(self): ##Done
        import time
        print("ADA: Great choice! Just let my cogs whir...")
        time.sleep(1)
        text = self.GetText()
        caesarSolve = Caesar(ciphertext=text)
        caesarSolved = caesarSolve.autoSolve()
        print("ADA: And here are your potential Caesar Cipher solutions: ")
        for x in caesarSolved:
            print("ADA:", x)
            time.sleep(0.75)
        print("ADA: Hope this was useful. Now, back to the menu!\n")

    def TranspositionMenu(self): ##Done
        #print("Transposition Menu Test Running")
        import time
        print("ADA: We're now in the world of the Transposition Cipher. Here we can encode, decode and suggest column numbers!")
        time.sleep(1)
        quit = False
        while quit == False:
            chooseMode = input("ADA: What would you like to do today?  \nYou: ")
            mode = self.ModeChoice(chooseMode, encode=True, decode=True, column=True)
            if mode == "ERROR":
                print("ADA: Sorry I didn't get that.. Perhaps you spelt it wrong? Try again!")
            elif mode == "QUIT":
                print("ADA: Goodbye!")
                time.sleep(2)
                quit = True
            elif mode == "ENCODE":
                self.TR_EncodeDecode(encode=True)
                print("ADA: We're now back in the Transposition Cipher menu. Here we can encode, decode and suggest column numbers!")
            elif mode == "DECODE":
                self.TR_EncodeDecode(encode=False)
                print("ADA: We're now back in the Transposition Cipher menu. Here we can encode, decode and suggest column numbers!")
            elif mode == "COLUMN":
                self.TR_Column()
                print("ADA: We're now back in the Transposition Cipher menu. Here we can encode, decode and suggest column numbers!")
            else:
                pass

    def TR_EncodeDecode(self, encode= True):
        print("ADA: Great choice! Just let my cogs whir...")
        time.sleep(1)
        text = self.GetText(remove=True)
        columnCorrect = False
        transpositionColumnSuggestion = Transposition(ciphertext=text)
        ##here use SuggestColumns to suggest possible columns. 
        decision = input("ADA: Would you like me to suggest a potential number of columns? \nYou: ")
        if self.PositiveResponse(decision):
            columnIdeas = transpositionColumnSuggestion.FindPossibleColumns()
            print("ADA: Here are the factors of the text length. They're the best numbers to use for a good Transposition Encryption.")
            tempText = ""
            for x in columnIdeas:
                tempText += str(x)
                tempText += ","
            print("ADA: You could try", tempText, "perhaps?")
        while columnCorrect == False:
            try:
                if encode:
                    ColumnChoice = int(input("ADA: How many columns do you want to encode with?  \nYou: "))
                else:
                    ColumnChoice = int(input("ADA: How many columns do you want to decode with?  \nYou: "))
                columnCorrect= True
                if len(text) % ColumnChoice != 0:
                    if encode:
                        confirmBadColumn = input("ADA: Are you sure you want this number of columns? It could result in a bad encryption. I recommend that you use a multiple of the key length. \nYou: ")
                    else:
                        confirmBadColumn = input("ADA: Are you sure you want this number of columns? It could result in a bad decryption. I recommend that you use a multiple of the key length. \nYou: ")
                    if self.PositiveResponse(confirmBadColumn):
                        columnCorrect = True
                        pass #Confirms that the user knows this may end badly
                    else:
                        columnCorrect= False
                else:
                    columnCorrect= True
            except:
                print("ADA: Sorry that number of columns is not valid. Please try another!")
                columnCorrect= False
        ## Input the correct order, in a right way
        OrderOfColumns = []
        tempColumn = 0
        CorrectOrder = False
    
        print("ADA: I'm going to ask you the order of the columns now, one by one. The first number you enter will be the first column (and vice versa).")
        while CorrectOrder == False:
            #print("Start loop")
            try:
                for x in range(0, ColumnChoice):
                    tempColumn = int(input("ADA: Position " + str(x) + " will be? \nYou: "))
                    OrderOfColumns.append(tempColumn)
                    #print(OrderOfColumns, "Current Order")
                CorrectOrder = True
                
            except:
                print("ADA: Sorry that order of columns is not valid. Please try again!")
                tempColumn = 0
                OrderOfColumns = []
            for x in range(0,ColumnChoice):
                if x not in OrderOfColumns:
                    CorrectOrder = False
            if CorrectOrder == False:
                print("ADA: You didn't include all the column positions in your answer... Please try again!")
                tempColumn = 0
                OrderOfColumns = []
            
        if encode:
            transpositionEncode = Transposition(plaintext=text, columns=ColumnChoice, order=OrderOfColumns)
            transpositionEncoded = transpositionEncode.encode()
            print("ADA: And here is your encoded Transposition Cipher: ", transpositionEncoded, "\nADA: Back to the menu!")
        else:
            transpositionDecode = Transposition(ciphertext=text, columns=ColumnChoice, order=OrderOfColumns)
            transpositionDecoded = transpositionDecode.decode()
            print("ADA: And here is your decoded Transposition Cipher: ", transpositionDecoded, "\nADA: Back to the menu!")
        
    
    def TR_Column(self): ##Done
        #print("DEV WARNING: UNFINISHED - PROCEED AT OWN RISK")
        import time
        print("ADA: Great choice! Just let my cogs whir...")
        time.sleep(1)
        text = self.GetText()
        transpositionColumnSuggestion = Transposition(ciphertext=text)
        ##here use SuggestColumns to suggest possible columns. 
        columnIdeas = transpositionColumnSuggestion.FindPossibleColumns()
        print("ADA: Here are the factors of the text length. They're the best numbers to use for a good Transposition Encryption.")
        tempText = ""
        for x in columnIdeas:
            tempText += str(x)
            tempText += ", "
        print("ADA: You could try", tempText, "perhaps?")
        time.sleep(1)
        print("ADA: That's all for this... See you back in the Menu!")
        time.sleep(1)

    def VigenereMenu(self): ##Done
        #print("Vigenere Menu Test Running")
        import time
        print("ADA: We're now in the world of the Vigenere Cipher. Here we can encode, decode!")
        time.sleep(1)
        quit = False
        while quit == False:
            chooseMode = input("ADA: What would you like to do today?  \nYou: ")
            mode = self.ModeChoice(chooseMode, encode=True, decode=True)
            if mode == "ERROR":
                print("ADA: Sorry I didn't get that.. Perhaps you spelt it wrong? Try again!")
            elif mode == "QUIT":
                print("ADA: Goodbye!")
                time.sleep(2)
                quit = True
            elif mode == "ENCODE":
                self.V_EncodeDecode(encode=True)
                print("ADA: You're back in the Vigenere menu. Pick something else to do!")
            elif mode == "DECODE":
                self.V_EncodeDecode(encode=False)
                print("ADA: You're back in the Vigenere menu. Why don't you try something new?")
            else:
                pass
        pass

    def V_EncodeDecode(self, encode=True):
        print("ADA: Great choice! Just let my cogs whir...")
        time.sleep(1)
        text = self.GetText()
        keyCorrect = False
        while keyCorrect == False:
            try:
                if encode:
                    keyChosen = input("ADA: What Key would you like to encode it by?  \nYou: ")
                else:
                    keyChosen = input("ADA: What Key would you like to decode it by?  \nYou: ")
                keyCorrect= True
                if keyChosen.isalpha():
                    keyCorrect= True
                else:
                    print("ADA: The Key must be only made of characters in the Alphabet. I bet you know which those are!")
                    keyCorrect= False
                if len(keyChosen) > len(text):
                    print("ADA: Sorry that key is too long. Please try a shorter one! It should be shorter than the text.")
                    keyCorrect= False

            except:
                print("ADA: Sorry that key is not valid. Please try another!")
                keyCorrect= False
        if encode:
            vigEncode = Vigenere(plaintext=text, key=keyChosen)
            vigEncoded = vigEncode.encode()
            print("ADA: And here is your encoded Vigenere Cipher: ", vigEncoded, "\nADA: Back to the menu!")
        else:
            vigDecode = Vigenere(ciphertext=text, key=keyChosen)
            vigDecoded = vigDecode.decode()
            print("ADA: And here is your decoded Vigenere Cipher: ", vigDecoded, "\nADA: Back to the menu!")
        

    def SubstitutionMenu(self): ##Done
        #print("Substitution Menu Test Running")
        import time
        print("ADA: We're now in the world of the Substitution Cipher. Here we can encode, decode and suggest replacements!")
        time.sleep(1)
        quit = False
        while quit == False:
            chooseMode = input("ADA: What would you like to do today?  \nYou: ")
            mode = self.ModeChoice(chooseMode, encode=True, decode=True, replace=True)
            if mode == "ERROR":
                print("ADA: Sorry I didn't get that.. Perhaps you spelt it wrong? Try again!")
            elif mode == "QUIT":
                print("ADA: Goodbye!")
                time.sleep(2)
                quit = True
            elif mode == "ENCODE":
                self.S_EncodeDecode(encode=True)
                print("ADA: You've returned to the Substitution menu. You can encode, decode or suggest replacements.")
            elif mode == "DECODE":
                self.S_EncodeDecode(encode=False)
            elif mode == "REPLACE":
                self.S_Replace()
            else:
                pass
        pass

    def S_EncodeDecode(self, encode=True):
        #Need the respective letters, must be 26
        text = self.GetText()
        alphabetTemplate = Analysis().alphabet
        alphabet = ""
        SubCorrect = False
        while SubCorrect == False:
            alphabet = ""
            for letter in alphabetTemplate:
                LetterCorrect = False
                while LetterCorrect == False:
                    letterTemp = input(("ADA: What letter would you like to replace '" + letter + "'? \nYou: "))
                    if letterTemp.isalpha():
                        if len(letterTemp) ==1 and letterTemp != " ":
                            alphabet += letterTemp.lower()
                            LetterCorrect = True
                    else:
                        print("ADA: That doesn't appear to be a single letter, could you try something different?")
            SubCorrect = True
            for x in alphabetTemplate:
                if x not in alphabet:
                    SubCorrect = False
            if SubCorrect == False:
                print("ADA: You appear to have some duplicates in here. Can you try that all again?")
        CompleteAlphabet = alphabet + alphabet.upper()
        if encode:
            substitute = Substitution(plaintext=text, cipherbet=CompleteAlphabet)
            subEncoded = substitute.encode()
            print("ADA: Here is your encoded Substitution Cipher: ", subEncoded)
            time.sleep(2)
        else:
            substitute = Substitution(ciphertext=text, cipherbet=CompleteAlphabet)
            subDecoded = substitute.decode()
            print("ADA: Here is your decoded Substitution Cipher: ", subDecoded)
            time.sleep(2)
        print("ADA: All done now. Heading back to the Substitution Menu...")
        time.sleep(2)
    
    def S_Replace(self): ##Done
        #Suggest the replacements from the ciphertext
        #print("DEV WARNING: UNFINISHED - PROCEED AT OWN RISK")
        import time
        print("ADA: Great choice! Just let my cogs whir...")
        time.sleep(1)
        text = self.GetText()
        replace = Substitution(ciphertext=text)
        replacesuggests = replace.SuggestReplacements()
        print("ADA: Here are the suggested replacements of the text. They're likely to be slightly inaccurate but will give you a good place to start!")
        for x in replacesuggests:
            print("ADA: You could try " + str(x[0]) + " (English) to go to " + str(x[1]) + " (text), perhaps?")
        
        time.sleep(1)
        print("ADA: That's all for this... See you back in the Menu!")
        time.sleep(1)


    def RailFenceMenu(self): #Done
       # print("Rail Fence Menu Test Running")
        import time
        print("ADA: We're now in the world of the Rail Fence Cipher. Here we can encode, decode and suggest the number of rails!")
        time.sleep(1)
        quit = False
        while quit == False:
            chooseMode = input("ADA: What would you like to do today?  \nYou: ")
            mode = self.ModeChoice(chooseMode, encode=True, decode=True, rails=True)
            if mode == "ERROR":
                print("ADA: Sorry I didn't get that.. Perhaps you spelt it wrong? Try again!")
            elif mode == "QUIT":
                print("ADA: Goodbye!")
                time.sleep(2)
                quit = True
            elif mode == "ENCODE":
                self.RF_EncodeDecode(encode=True)
                print("ADA: You're back in the RailFence menu, please stay awhile. Here you can encode, decode and suggest the number of rails!")
            elif mode == "DECODE":
                self.RF_EncodeDecode(encode=False)
                print("ADA: You're back in the RailFence menu, please stay awhile. Here you can encode, decode and suggest the number of rails!")
            elif mode == "RAILS":
                self.RF_Rails()
                print("ADA: You're back in the RailFence menu, please stay awhile. Here you can encode, decode and suggest the number of rails!")
            else:
                pass
        pass
    
    def RF_EncodeDecode(self, encode=True):
        if encode:
            print("ADA: The Rail Fence cipher is complicated to encode, but it's simple with a couple of key pieces of information.")
        else:
            print("ADA: The Rail Fence cipher is complicated to decode, but it's simple with a couple of key pieces of information.")
        print("ADA: One of these is the number of rails, the other is your text! ")
        ##Get text
        text = self.GetText(remove=True)
        railCorrect = False
        while railCorrect == False:
            try:
                ##Get rail number (2 or higher) (this is covered by the "in rf potentials") 
                if encode:
                    railNum = int(input("ADA: How many rails do you want to use to encode this with? \nYou: "))
                else:
                    railNum = int(input("ADA: How many rails do you want to use to decode this with? \nYou: "))
                ##If rail number in the array returned by GuessRails
                rfRails = RailFence(ciphertext=text, railNo=railNum)
                guess = len(text) #Check all potential rails in case it doesn't exist then
                rfPotentials = rfRails.GuessRails(guess)
                if railNum in rfPotentials:
                    railCorrect = True
                elif rfPotentials == []:
                    if encode:
                        print("ADA: I'm so sorry but the text you are trying to encode has no suitable rail numbers to encode with. I'm going to have to ask for your text again.")
                    else:
                        print("ADA: I'm so sorry but the text you are trying to decode has no suitable rail numbers to encode with. I'm going to have to ask for your text again.")

                    #### Loops through this until RFPotentials actaully has something that works. Lets the user know how many extra characters they had to add
                    addChoice = input("ADA: Would you like me to instead add on characters ('X') to your text (you have just picked) until there is at least one valid number of rails? \nYou: ")
                    if self.PositiveResponse(addChoice):
                        correctRails = False
                        counter = 0
                        while correctRails == False:
                            counter +=1
                            text += "X"
                            rfRails = RailFence(ciphertext=text, railNo=railNum)
                            rfPotentials = rfRails.GuessRails(len(text))
                            if len(rfPotentials) >= 3:
                                correctRails = True
                        if encode:
                            print("ADA: I have added", counter, "letters to your text. You can now encode it with", rfPotentials)
                        else:
                            print("ADA: I have added", counter, "letters to your text. You can now decode it with", rfPotentials)
                    else:
                        print("ADA: Okay, then you'll have to enter in a different piece of text, as that wasn't valid.")
                        text = self.GetText(remove=True)
                else:
                    if encode:
                        
                        print("ADA: In order to properly encode the Rail Fence cipher, you need a rail number that, when you do the modulus of the length of text by ((2*rails) -2), it should be 1. \nADA: Please try a different number, as this wasn't acceptable.")
                        print("ADA: How about using ", str(rfPotentials), "to encode your text with?")
                    else:
                        print("ADA: In order to properly decode the Rail Fence cipher, you need a rail number that, when you do the modulus of the length of text by ((2*rails) -2), it should be 1. \nADA: Please try a different number, as this wasn't acceptable.")
                        print("ADA: How about using ", str(rfPotentials), "to decode your text with?")
            except:
                print("ADA: That doesn't seem right. Could you try something different perhaps?")
        if encode:
            print("ADA: Now I'm going to encode it for you.")
            #print(text)
            railEnc = RailFence(railNo=railNum, plaintext=text)
            railEncoded = railEnc.encode()
            print("ADA: Here is your encoded Rail Fence:", railEncoded)
        else:
            print("ADA: Now I'm going to decode it for you.")
            railDec = RailFence(railNo=railNum, ciphertext=text)
            railDecoded = railDec.decode()
            print("ADA: Here is your decoded Rail Fence:", railDecoded)
        time.sleep(3)
        print("ADA: Heading back to the Rail Fence menu now!")
        time.sleep(1.5)

    def RF_Rails(self): ##Done
        #print("NOT STARTED DON'T CONTINUE.")
        import time
        print("ADA: Great choice! Just let my cogs whir...")
        time.sleep(1)
        text = self.GetText(remove=True)
        print("ADA: I now need for you to input the maximum rails that you want me to check up to.")
        time.sleep(1)
        print("ADA: I'd recommend 10 but it's your choice.")
        time.sleep(1)
        guessCorrect = False
        guess = 0
        while guessCorrect == False:
            try:
                guess = int(input("ADA: What would you like it to be then?  \nYou: "))
                if guess >2:
                    guessCorrect = True
            except:
                print("ADA: I don't think that was a valid number... Could you try something different? Thanks!")
        rfRails = RailFence(ciphertext=text, railNo=5)
        rfPotentials = rfRails.GuessRails(guess)
        tempText = ""
        for x in rfPotentials:
            tempText += str(x)
            tempText += ", "
        print("ADA: And here are your the number of rails you could encode by:", tempText, "\nADA: Back to the menu!")

    
    def AnalysisMenu(self): #Done
        #print("Analysis Menu Test Running")
        import time
        print("ADA: We're now in the world of Text Analysis. Here we can display a frequency analysis, an Index of Coincidence, compare to the normal English text values, or find combinations of letters!")
        time.sleep(1)
        quit = False
        while quit == False:
            chooseMode = input("ADA: What would you like to do today?  \nYou: ")
            mode = self.ModeChoice(chooseMode, Frequency=True, Index=True, compare=True, every=True)
            if mode == "ERROR":
                print("ADA: Sorry I didn't get that.. Perhaps you spelt it wrong? Try again!")
            elif mode == "QUIT":
                print("ADA: Goodbye!")
                time.sleep(2)
                quit = True
            
            elif mode == "FREQ":
                self.FrequencyAnalysis()
                print("ADA: You're back in the Analysis menu, what shall you like to do next? Here we can display a frequency analysis, an Index of Coincidence, compare to the normal English text values, or find combinations of letters!")
            
            elif mode == "IOC":
                self.IndexOfCoincidence()
                print("ADA: You're back in the Analysis menu, what shall you like to do next? Here we can display a frequency analysis, an Index of Coincidence, compare to the normal English text values, or find combinations of letters!")
 
            elif mode == "COMPARE":
                self.Compare()
                print("ADA: You're back in the Analysis menu, what shall you like to do next? Here we can display a frequency analysis, an Index of Coincidence, compare to the normal English text values, or find combinations of letters!")
 
            elif mode == "EVERY":
                self.EveryX()
                print("ADA: You're back in the Analysis menu, what shall you like to do next? Here we can display a frequency analysis, an Index of Coincidence, compare to the normal English text values, or find combinations of letters!")
 
            else:
                pass
        pass

    def FrequencyAnalysis(self): ##Done
        #print("NOT STARTED DON'T CONTINUE.")

        print("ADA: Okay, time to do some Frequency Analysis!")
        time.sleep(1)
        print("ADA: But first...")
        Freqtext = self.GetText()
        print("ADA: Now, using your text, I'll show you the individual frequencies for each letter.")
        freq = Analysis(text=Freqtext)
        freqAnalysis = freq.GetCipherFrequencies()
        print("ADA: It'll be 'letter' : value. For example, 'a' : 17.")
        print("ADA: Here we go...")
        for key in freqAnalysis:
            print("ADA: '" + key + "' : ", str(freqAnalysis[key]))
            time.sleep(0.25)

        print("ADA: Maybe that helped with your code-breaking! Back to the Analysis menu...")

    def IndexOfCoincidence(self): ##Done
        #print("NOT STARTED DON'T CONTINUE.")

        print("ADA: So... You have chosen to calculate the Index of Coincidence of your text.\nThis value tells you how likely it is to get the same letter next in the piece of text. ")
        time.sleep(1)
        print("ADA: For English, the value is close to 1.73, however for a completely random text, it's close to 1.00.")
        time.sleep(1)
        print("ADA: But before I can do this...")
        time.sleep(0.5)
        ioctext = self.GetText()
        if len(ioctext) < 100:
            print("ADA: WARNING - a short piece of text will have a very inaccurate Index Of Coincidence, meaning you might not be able to trust it.")
        time.sleep(1)
        IoC = Analysis(text=ioctext)
        IOCValue = IoC.GetIoCValue()
        IOCValue = round(IOCValue, ndigits= 2)
        print("ADA: The Index Of Coincidence value for this piece of text is:", str(IOCValue))
        time.sleep(2)
        print("ADA: Thanks for your time! Back to the Analysis Menu...")
        time.sleep(1)

    def Compare(self): ##Done
        #print("NOT STARTED DON'T CONTINUE.")

        print("ADA: Here, I'm going to show you some comparisons between the text you 'll enter and the values for a normal English piece of text.")
        time.sleep(1)
        print("ADA: But, before I continue...")
        time.sleep(0.5)
        Perctext = self.GetText()
        print("ADA: I'm going to use the percentages for each letter in the text, as this is easier to visually compare.")
        perc = Analysis(text=Perctext)
        percAnalysis = perc.GetCipherPercents()
        engPerc = perc.GetEnglishPercents()
        print('''ADA: This'll be in the system:
Letter | English | Ciphertext 
-----------------------------''')
        for letter in engPerc:
            print( "     " + letter + " |  " + str(engPerc[letter]) + "   | " + str(percAnalysis[letter]))

        print("ADA: Hopefully this was useful for you! Heading back to the Analysis Menu now...")
        time.sleep(2)

    def EveryX(self): ##Done
        
        #print("NOT STARTED DON'T CONTINUE.")

        print("ADA: This section can help find common groupings of letters, with the number of letters chosen by you! ")
        print("ADA: To explain, if you enter 'abcdefggababcdgf' with 2, it'll calculate the combinations in the text, i.e. 'ab' : 3, 'cd' : 2.")
        print("ADA: But before I can do this...")
        time.sleep(0.5)
        EveryXtext = self.GetText()
        combo = Analysis(text=EveryXtext)
        print("ADA: The next thing I need is the number of letters per combination. I usually reccommend 2, but anything above 10 seems excessive.")
        xCorrect = False
        while xCorrect == False:
            try:
                x = int(input("ADA: What value would you like to use? \nYou: "))
                xCorrect = True
                if x > 10:
                    print("ADA: I said that above 10 seems excessive. Please try a lower value.")
                    xCorrect = False
                elif x < 0:
                    print("ADA: You cannot have a combination of less than 0 letters. Please try again!")
                    xCorrect = False
            except:
                print("ADA: Hmm that doesn't appear to be an integer. Could you try something different?")
        sortedCombo = combo.MostCommonXLetters(LetterNum=x)
        print("ADA: Now that I've calculated this, how many results would you like? (E.G. Top 10, top 5...)")
        valueCorrect = False
        value = 0
        while valueCorrect == False:
            try:
                value = int(input("ADA: How many would you like to see? \nYou: "))
                valueCorrect = True
                if value > 100:
                    print("ADA: I think that above 100 seems excessive. Please try a lower value.")
                    valueCorrect = False
                elif value < 0:
                    print("ADA: You cannot have a Top X of less than 0 items. Please try again!")
                    valueCorrect = False
            except:
                print("ADA: Hmm that doesn't appear to be an integer. Could you try something different?")
        print("ADA: It'll be 'combo' : key. For example, 'abc' : 17.")
        print("ADA: Here we go...")
        for i in range(0, value):
            #print(i, "test")
            print("ADA: '" + str(sortedCombo[i][0]) + "' : ", str(sortedCombo[i][1]))
            time.sleep(0.25)

        print("ADA: That's all finished now! Back to the Analysis Menu...")
        time.sleep(2)


class Analysis:
    def __init__(self, text = ""):
        import string
        ##Removes spaces
        self.__text = (text.lower()).replace(" ", "")
        ###Removes all punctuation too...
        self.__text = self.__text.translate(str.maketrans('', '', string.punctuation))
        #print(x)
        #print(string.punctuation)
        #print(self.__text)

        #DICTIONAIRIES to store the values of the letters/percentages of each letter
        self.__EnglishPercents = { "a":  8.04, "b": 1.48, "c": 3.34,"d": 3.82,"e": 12.49,"f": 2.40,"g": 1.87,"h": 5.05,"i": 7.57,"j": 0.16,"k": 0.54,"l": 4.07,"m": 2.51,"n": 7.23,"o": 7.64,"p": 2.14,"q": 0.12,"r": 6.28,"s": 6.51,"t": 9.28,"u": 2.73,"v": 1.05,"w": 1.68,"x": 0.23,"y": 1.66,"z": 0.09}
        self.__CipherPercents = {"a": 0, "b": 0, "c": 0,"d": 0,"e": 0,"f": 0,"g": 0,"h": 0,"i": 0,"j": 0,"k": 0,"l": 0,"m": 0,"n": 0,"o": 0,"p": 0,"q": 0,"r": 0,"s": 0,"t": 0,"u": 0,"v": 0,"w": 0,"x": 0,"y": 0,"z": 0}
        self.__pairedUp = [] # an ARRAY to store the paired up english to ciphertext values (later to be a 2D array)
        self.__CipherFrequencies = {"a": 0, "b": 0, "c": 0,"d": 0,"e": 0,"f": 0,"g": 0,"h": 0,"i": 0,"j": 0,"k": 0,"l": 0,"m": 0,"n": 0,"o": 0,"p": 0,"q": 0,"r": 0,"s": 0,"t": 0,"u": 0,"v": 0,"w": 0,"x": 0,"y": 0,"z": 0} #Empty to put values into
        
        ##Unused alphabet array
        self.alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        self.__iocValue = 0 #a FLOAT 
        self.take2 = False

        #list of preordered english values and percents
        # Means reduces time sorting the dictionary each time you instantiate the class 
        self.__orderedEnglishList = [12.49, 9.28, 8.04, 7.64, 7.57, 7.23, 6.51, 6.28, 5.05, 4.07, 3.82, 3.34, 2.73, 2.51, 2.40, 2.14, 1.87, 1.68, 1.66, 1.48, 1.05, 0.54, 0.23, 0.16, 0.12, 0.09]
        self.__orderedEnglishLetterList = ["e","t","a","o","i","n", "s", "r", "h", "l", "d", "c", "u","m", "f", "p", "g", "w", "y", "b", "v", "k", "x", "j", "q", "z"]
        ## Values From http://www.norvig.com/mayzner.html
        # Testing  -> , result: 8.04
        #print(self.__EnglishPercents[8.04])
        
        #Calculates the values of each before moving on 
        #Prevents errors occuring from empty dictionairies or the objects from not actually computing values
        self.IndexOfCoincidence()
        self.CalculateCipherFrequencies()
        self.CalculateCipherPercents()

    def GetText(self): #Returns the text without punctuation and all lowercase
        return self.__text
    
    def GetCipherPercents(self): #returns the dictionary with the percentages
        return self.__CipherPercents

    def GetCipherFrequencies(self): #returns the dictionary with the frequencies
        return self.__CipherFrequencies

    def GetEnglishPercents(self):
        return self.__EnglishPercents

    def GetIoCValue(self): #returns the IOC
        return self.__iocValue

    def makeCipherList(self): # makes a list of all the values in cipherpercents
        cipherList = []
        for key in self.__CipherPercents:
            cipherList.append(self.__CipherPercents[key])
        newcipherList = self.SortIt(cipherList, reverse=True)
        return newcipherList

    def returnkeyfrompercvalue(self, search):
        for name, value in self.__CipherPercents.items(): #uses a LINEAR SEARCH to return the key from the value
            if value == search:
                return name

    def MostCommonXLetters(self, LetterNum=2): #a sliding count, creates bigrams but in a sliding way
        ## "abcdef" => "ab", "bc", "cd", "de", "ef"

        #Explanation:
        ## Uses a dictionary, for the combos and the occurences { "ab": 1, "bc":5, ....}
        ## sort by the occurences, using sorted(dictionary, key=dictioanry value) --> then reverses it.
        # later will print out combo, ":", value --> for each pairing. 
        bigselection = {}
        try:
            for x in range(0, len(self.__text)): #for every letter in the text
                combo = ""
                for digit in range(0, LetterNum): #creates a combo with length specified
                    combo += self.__text[x+digit]
                if combo in bigselection: #if it's already in the dictionary
                    bigselection[combo] +=1 #add one to the value
                else:
                    bigselection.update( {combo : 1} ) #instead, add to dictionary with occurrence one
        except:
            pass #If it fails, move on
        #print(bigselection)

        #Sorts the dictionary by value
        ###WRITE OWN SORT?? QUICKSORT??###

        #sortedDict = sorted(dictionary, key=dictionary.get, reverse = True)
        sortedDictionary = self.SortIt(bigselection, take2=True, reverse=True) #sorts the dictionary using a QUICKSORT and returns a list

        return sortedDictionary

        ##Objective: Will match up most common groups of 3 letters, i.e. if gji comes up a lot, could suggest its "the"

    def PairUpValues(self):
        # The idea here is to match the highest percents with similarly high percents 
        # in a 2D array#
        # e.g. A (plaintext) is matched with g (ciphertextt)
        #explanation: makes a list of the values, order them, then use indexes to match them in a 2d array
        cipherList = self.makeCipherList()
        for x in range(0, len(cipherList)):
            value = cipherList[x] #takes the next value from cipherList
            letter = self.returnkeyfrompercvalue(value) #uses that value to find the key in the dictionary
            self.__pairedUp.append([self.__orderedEnglishLetterList[x], letter]) #append to a 2D array
        return self.__pairedUp

    def CalculateCipherFrequencies(self):
        for key in self.__CipherFrequencies: #for the length of the frequency dictionary
            self.__currentletter = key #sets the variable to the current letter            
            #Haskell Style!
            number = len(list(filter(lambda x: x==key, self.__text))) #returns the length of the list of the filter object of the text
            # Reason for use: not using elsewhere
            #                (& streamlines the code) 
            self.__CipherFrequencies[key] = number #the length is the number of occurences in the text
        #print(self.__CipherFrequencies)

    def CalculateCipherPercents(self): #Very similar to CalculateCipherFrequencies
        total = len(self.__text) #the maximum letters it can be
        for key in self.__CipherPercents:
            number = self.__CipherFrequencies[key]
            try:
                percent = round((number / total)*100, 3) #round the percentage to 3 decimal places
            except:
                percent = 0
            #print(percent)
            self.__CipherPercents[key] = percent #adds into the dictionary
        #print(self.__CipherPercents)
    
    def IndexOfCoincidence(self):
        ## WARNING LESS THAN 50 LETTERS, UNRELIABLE
        #Method from: https://www.thonky.com/kryptos/index-of-coincidence 

        ##PhiO
        self.CalculateCipherFrequencies() #calculates frequencies (f)
        F = 0
        phiO = 0
        for key in self.__CipherFrequencies:
            F = (self.__CipherFrequencies[key]) * (self.__CipherFrequencies[key] -1) #calculate frequencies * (frequencies-1) (F)
            phiO += F # add up all F (phiO)
        #print(phiO)
        
        ##PHIR
        N = len(self.__text)#count total letters (excluding spaces) (N)
        #print(N)
        phiR = N * (N-1) * 0.0385 # N * (N-1) * 0.0385 (this is the random prob) (phiR)
        #print(phiR)

        if phiR > 0:
            ioc = phiO / phiR #Divide phiO by phiR
        else:
            ioc = None #if the length of the text is one, you can't have a valid ioc 
        #print(ioc)
        self.__iocValue = ioc
        return ioc

        #ioc close to 1.00 -> possibly vigenere
        #ioc close to 1.73 -> english (pick closest to ioc 1.73?)

    def SortIt(self, toBeSorted, take2 = False, reverse=False):
        
        if take2 == False:
            self.take2 = False
        else:
            self.take2 = True
        listOfItems = []
        if type(toBeSorted) is list:
            listOfItems = toBeSorted
        elif type(toBeSorted) is dict:
            for key in toBeSorted:
                listOfItems.append((key,toBeSorted[key])) # Using a TUPLE here
        newList = self.QuickSort(listOfItems)
        if reverse == True:
            newList.reverse()

        return newList

    def QuickSort(self, items):

        #This is a quick sort
        #Using Algorithm from "Edexcel AS and A Level Modular Mathematics D1" 
        #By Susie G Jameson (Page 12)

        if len(items) == 1:
            return items
        elif items == []:
            return []
        else:
            LessList = []
            MoreList = []
            #Take an element as the pivot
            #For this we are using the first element
            pivot = items.pop(0)
            #Loop through the remaining items
            for element in items:
                if self.take2: #Because this work with tuples and arrays, must have this
                    if element[1] < pivot[1]:
                        LessList.append(element)
            #If the item is less than the pivot, add to a LessList
                    else:
                        MoreList.append(element)
            #If the item is greater than the pivot, add to MoreList
                else:
                    if element < pivot:
                        LessList.append(element)
            #If the item is less than the pivot, add to a LessList
                    else:
                        MoreList.append(element)

            #quicksort on each of these lists
            newLess = self.QuickSort(LessList)
            #print(newLess)
            newMore = self.QuickSort(MoreList)
            #print(newMore)
            #join the results togther
            #import itertools
            newList = newLess + [pivot] + newMore
            #print("Sorted", newList)
            #Return!
            return newList

##Menu!!
menu = Menu()