# Sharwin Patil
# Excel Sheets to LaTeX converter with python script
import sys

# Takes in a string with \t and \n markers and returns a list of strings
# with each element being the substrings in between the \t markers
def rowStringToList(rowString):
    rowList = []

    # Loop ends once the string only contains the newline
    while (rowString != "\n"):
        indexOfTab = rowString.find("\t")  # find the index of the first \t
        if indexOfTab == -1:  # If there is none left, break from loop
            break
        # Else, continue to append to rowList
        rowList.append(rowString[0:indexOfTab])  # Add the string until the \t
        # Delete everything before the \t
        rowString = rowString[(indexOfTab+1):]
        # print(rowList)
        # print(rowString)
    # Return the list of strings

    # Add the last element before the '\n'
    rowList.append(rowString[0:(len(rowString) - 1)])

    return rowList

# Function to parse through a list of strings that represents a row
# list of strings contains cells of the table
# Returns a string with the LaTeX code for that row
def listParser(listOfStrings):
    thisRowString = ""

    specialChars = [ "$", "&" , "#" , "%" ]
    # Check for special characters and modify string to include '\'
    for stringToCheckIndex in range(len(listOfStrings)):
        for index in range(len(specialChars)):
            indexOfChar = listOfStrings[stringToCheckIndex].find(specialChars[index])
            if indexOfChar != -1:
                listOfStrings[stringToCheckIndex] = listOfStrings[stringToCheckIndex][:indexOfChar] + "\\" + listOfStrings[stringToCheckIndex][indexOfChar:]

    # If there is no multilines
    if listOfStrings.count('') == 0 :
        for element in listOfStrings :
            # Add the element itself to the string
            thisRowString += element
            if listOfStrings.index(element) != (len(listOfStrings) - 1) :
                thisRowString += " & "
    else : # There are multilines
        for elementIndex in range(0, len(listOfStrings) - 1) :
            # Check for trailing '' after element
            if listOfStrings[elementIndex] != "" and listOfStrings[elementIndex + 1] == "":
                multiLineString = listOfStrings[elementIndex]
                # Continue until '' characters end to find the size of multicolumn
                multiLineCount = countEmptyStrings(listOfStrings[(elementIndex + 1):])
                thisRowString += "\\multicolumn{" + str(multiLineCount) + "}{|c|}{" + multiLineString + "} & "
            elif listOfStrings[elementIndex] != "" and listOfStrings[elementIndex + 1] != "" :
                thisRowString += listOfStrings[elementIndex] + " & "
        # Add last element
        thisRowString += listOfStrings[-1]

    # Add the necessary LaTeX syntax to the end of the row
    thisRowString += " \\\\ \hline"

    return thisRowString
    
# Counts the total number of '' in the given list
# A list is only sent to this method if it contains at least one '' character
def countEmptyStrings(listOfStrings):
    num = 1

    # Count the number of "" characters in this list until the first non-empty character
    for i in range(len(listOfStrings)):
        if listOfStrings[i] == "":
            num += 1
        else:
            return num
    # If the rest of the strings are empty, then return the final num
    return num
    