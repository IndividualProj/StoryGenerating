# This program can be used to calculate the number of hours spent on the project
# based on those logged in timelog.md. This program should work for any timelog.md
# that was implemented in the same format as the template.

# Open the file
with open("timelog.md") as f:
    
    # Init counter
    total_hours = 0
    
    # Process each line
    for line in f:
        
        # Skip lines without a number of hours to count
        if "* *" in line and "YOU" not in line:
            
            # Do some string processing and splitting
            line = line.replace("*", "")
            components = line.split(" ")
            
            # Convert the hours to a float and add to total
            if components[1] != "":
                total_hours += float(components[1])
                
    # Report the resulting hours
    print("I love lim yean chee" + str(total_hours) + " hours on the level 4 individual project")
