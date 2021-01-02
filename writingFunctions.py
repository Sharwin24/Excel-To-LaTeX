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

# Main function
if __name__ == '__main__':

    # Save User Input to a String
    print("After pasting text, use [Ctrl+Z and ENTER] to finish output")
    print("Copy and paste text: ")
    # userInput variable will save each row in an element of an array with a \n at the
    userInput = sys.stdin.readlines()

    # Get the caption string from the user
    captionString = input("Enter a caption for the table: ")

    # Get a width from the user
    widthString = input("Enter in inches how wide you want the table\nLeave blank for a default of the page width: ")
    if widthString.isnumeric():
        widthString += "in" 
    else:
        widthString = "\\textwidth"

    # print(userInput)
    # ['Header\t\tTwo\t3\t4\n', 'row\tValue\temptySpace\t0.456\t321.45\n']

    # Create a 2D Array to store data
    numberOfRows = len(userInput)
    numberOfCols = userInput[0].count("\t") + 1

    data = []

    for x in range(numberOfRows):
        data.append(rowStringToList(userInput[x]))

    # Print the table text
    divider = "".center(75,"=")
    print("Here is the LaTeX code for your table:\n")
    print(divider)
    finalOutput = ""
    finalOutput += "\\begin{table}[H]\n\t\\centering\n\t\\resizebox{"+ widthString + "}{!}\n\t{%\n\t\t\\begin{tabular}{"

    # Add |c| markers for number of cols
    for columns in range(numberOfCols):
        finalOutput += "|c"
    finalOutput += "|}\n\t\t\t"

    # Start the table contents itself
    finalOutput += "\\hline\n\t\t\t"
    for index in range(len(data)):
        finalOutput += listParser(data[index])
        if index != (len(data) - 1):
            finalOutput += "\n\t\t\t"

    # Print the end of the table environment
    finalOutput += "\n\t\t\\end{tabular}%\n\t}\n\t\\caption{" + captionString + "}\n\t\\label{tab:my_label}\n\end{table}"

    print(finalOutput)
    print(divider)