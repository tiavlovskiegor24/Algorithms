def solution(S):
    '''
    function takes string 'S' and return 1 if S is properly nested, 0 otherwise
    solution_2 uses string implementation of a stack
    
    '''

    #look up mapping of opening characters to corresponding closing characters
    char_pairs = {
        "{" : "}",
        "(" : ")",
        "[" : "]"
    }

    #look up table for closing characters
    closing_chars = {
        "}",
        ")",
        "]"
    }

    # string that stores the sequence of expected closing characters
    # with the next expected character at the end (stack)
    expected_chars = " " # space character corresponds to bottom of the stack

    # initialise pointer to the next expected closing character in 'expected_chars'
    pointer = 0

    #valid S must be of even length
    if len(S) % 2 != 0:
        return 0
    
    # loop through the characters of input string
    for char in S:
        
        if char in char_pairs:
            #opening character encountered

            # remove all the checked closing characters
            # up to pointer 'position' in 'expected_chars'
            if pointer+1 < len(expected_chars):
                expected_chars = expected_chars[:pointer+1]
                

            #append the paired closing character to the end of expected_chars
            #and set pointer to it
            new_expected_char = char_pairs[char] 
            expected_chars += new_expected_char
            pointer += 1
            


        elif char in closing_chars:
            #closing character encountered

            #take the expected closing character from the stack
            #and check if it equals to the observed character
            expected_char = expected_chars[pointer]

            if char != expected_char:
                #'char' in 'S' does not equal to expected closing
                #character, hence S is not properly nested

                return 0

            else:
                #'char' is correct
                #move the pointer to the next expected closing character

                pointer -= 1
                  
        else:
            #invalid character encountered
            
            print "Invalid character: '{}'".format(char)

            return

    # when end of 'S' is reached check that stack is empty  
    if expected_chars[pointer] == " ":
        # stack is empty, hence 'S' is properly nested

        return 1

    else:
        # 'S' is missing some closing characters
        return 0


def test_solution(solution):
    '''
    function to test the solution() function on the samples of 
    valid and invalid strings
    '''
    valid_strings = ["[]","{[()()]}","","{{{{}}}}[]","()","[]"]
    invalid_strings = ["{","([)()]","]","(}"]
    

    for string in valid_strings:
        label = solution(string)
        assert label == 1,"valid string mislabeled: {},{}".format(label,string)

    for string in invalid_strings:
        label = solution(string)
        assert label == 0,"invalid string mislabeled: {},{}".format(label,string)

    

if __name__ == "__main__":
    import time
    
    #run standard test in case changes to solution() function where made
    test_solution(solution)

    #sample string
    S = "{[][]{([])}}({[{}([{}{[]}{}])][]})"
    print "\nSample string: {}".format(S)
    print "Label: {}\n\n".format(solution(S))

    # demos on large strings
    print "Some demo strings:"
    
    demos = ["200000 * '{'",
             "200001 * '{'",
             '100000 * "{" + 100000 * "}"',
             '100000 * "[]"',
             '50000 * "[()]"',
             '25000 * "{[(){}]}"',
             '12500 * "{[{([])}]}"']

    for string in demos:
        print "\nString = {}".format(string)
        exec('S = {}'.format(string))

        t0 = time.time()        
        print "Label: {}".format(solution(S))
        print "Time taken: {:.3f}s\n\n".format(time.time()-t0)

        
